"""
Authentication services for university application agent
"""
import logging
import os
import json
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, EmailStr, Field
from fastapi import HTTPException, Depends, Header

logger = logging.getLogger(__name__)

# JWT Configuration
JWT_SECRET = os.environ.get("JWT_SECRET", "mock-jwt-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 60 * 60  # 1 hour
REFRESH_EXPIRATION = 60 * 60 * 24 * 7  # 7 days

# Models
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str
    is_active: bool
    email_verified: bool
    created_at: str
    subscription_status: Optional[str] = None

class TokenResponse(BaseModel):
    token: str
    refresh_token: str
    expires_at: str

class AuthService:
    """Authentication service"""
    
    def __init__(self, supabase_client):
        self.supabase_client = supabase_client
        
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Check if email already exists
            existing_user = await self.supabase_client.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            # Create user data for Supabase (don't include uuid - let database generate it)
            new_user = {
                "name": user_data.name,
                "email": user_data.email,
                "password_hash": user_data.password,  # Use 'password_hash' to match your schema
                "role": "student",  # Use 'student' instead of 'user' to match your database constraint
                "is_active": True,
                "email_verified": False
                # created_at will be set by the database function
            }
            
            # Create user in Supabase
            result = await self.supabase_client.create_user(new_user)
            
            if "error" in result:
                raise HTTPException(status_code=500, detail=f"Failed to create user: {result['error']}")
            
            # Get the created user data
            created_user = result.get("user", {})
            
            # Generate tokens using the created user data
            token_data = self._generate_tokens(created_user)
            
            # Return user data without password
            user_response = {**created_user}
            user_response.pop("password_hash", None)
            user_response["id"] = user_response.get("uuid")  # Return 'id' for frontend compatibility
            
            return {
                "user": user_response,
                **token_data
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            raise HTTPException(status_code=500, detail="Registration failed")
    
    async def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Authenticate user and return tokens"""
        try:
            # Find user by email
            user = await self.supabase_client.get_user_by_email(login_data.email)
            
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # In real app, would verify password hash
            if user.get("password_hash") != login_data.password:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            if not user.get("is_active", False):
                raise HTTPException(status_code=401, detail="User account is inactive")
            
            # Generate tokens
            token_data = self._generate_tokens(user)
            
            # Return user data without password
            user_response = {**user}
            user_response.pop("password_hash", None)
            # Add 'id' field for frontend compatibility 
            if "uuid" in user_response:
                user_response["id"] = user_response["uuid"]
            
            return {
                "user": user_response,
                **token_data
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise HTTPException(status_code=500, detail="Login failed")
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh access token"""
        try:
            # Verify refresh token
            try:
                payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
                user_id = payload.get("sub")
                token_type = payload.get("type")
                
                if not user_id or token_type != "refresh":
                    raise HTTPException(status_code=401, detail="Invalid refresh token")
                
            except jwt.PyJWTError:
                raise HTTPException(status_code=401, detail="Invalid refresh token")
            
            # Get user
            user = await self.supabase_client.get_user_by_id(user_id)
            
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            
            if not user.get("is_active", False):
                raise HTTPException(status_code=401, detail="User account is inactive")
            
            # Generate new access token
            access_token = self._create_access_token(user)
            
            return {
                "token": access_token,
                "refresh_token": refresh_token,  # Keep the same refresh token
                "expires_at": (datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)).isoformat()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            raise HTTPException(status_code=401, detail="Token refresh failed")
    
    def _generate_tokens(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Generate access and refresh tokens"""
        access_token = self._create_access_token(user)
        refresh_token = self._create_refresh_token(user)
        
        return {
            "token": access_token,
            "refresh_token": refresh_token,
            "expires_at": (datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)).isoformat()
        }
    
    def _create_access_token(self, user: Dict[str, Any]) -> str:
        """Create JWT access token"""
        expires = datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)
        
        # Handle both 'id' and 'uuid' field names
        user_id = user.get("id") or user.get("uuid")
        
        payload = {
            "sub": user_id,
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "type": "access",
            "exp": expires
        }
        
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    def _create_refresh_token(self, user: Dict[str, Any]) -> str:
        """Create JWT refresh token"""
        expires = datetime.utcnow() + timedelta(seconds=REFRESH_EXPIRATION)
        
        # Handle both 'id' and 'uuid' field names
        user_id = user.get("id") or user.get("uuid")
        
        payload = {
            "sub": user_id,
            "type": "refresh",
            "exp": expires
        }
        
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

async def get_current_user(authorization: str = Header(None)):
    """Dependency to get current authenticated user"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Extract token from Authorization header
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
        
        # Verify token
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            user_id = payload.get("sub")
            token_type = payload.get("type")
            
            if not user_id or token_type != "access":
                raise HTTPException(status_code=401, detail="Invalid token")
            
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Get user from database
        supabase_client = get_supabase_client()
        user = await supabase_client.get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        if not user.get("is_active", False):
            raise HTTPException(status_code=401, detail="User account is inactive")
        
        # Return user data without password
        user_response = {**user}
        user_response.pop("password", None)
        
        return user_response
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(status_code=401, detail="Authentication failed")

async def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency to require admin role"""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    
    return current_user

async def check_usage_limits(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency to check usage limits based on subscription"""
    try:
        supabase_client = get_supabase_client()
        
        # Get user subscription
        subscription = await supabase_client.get_user_subscription(current_user["id"])
        
        if not subscription or subscription.get("status") != "active":
            raise HTTPException(status_code=402, detail="Active subscription required")
        
        # Get subscription plan
        plan = await supabase_client.get_subscription_plan_by_id(subscription["plan_id"])
        
        if not plan:
            raise HTTPException(status_code=500, detail="Subscription plan not found")
        
        # Check limits
        limits = plan.get("limits", {})
        
        # Get current usage
        client_count = len(await supabase_client.get_user_clients(current_user["id"]))
        
        # Check client limit
        max_clients = limits.get("max_clients", 0)
        if max_clients >= 0 and client_count >= max_clients:
            raise HTTPException(status_code=402, detail="Client limit reached for your subscription")
        
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error checking usage limits: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to check usage limits")

# Import at the end to avoid circular imports
from database.supabase_client import get_supabase_client