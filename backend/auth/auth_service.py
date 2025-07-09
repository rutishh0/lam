"""
Authentication and authorization service for the SaaS application
"""

import os
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from passlib.context import CryptContext
from passlib.hash import bcrypt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
import logging

logger = logging.getLogger(__name__)

# JWT Configuration
SECRET_KEY = os.environ.get("JWT_SECRET", "your-secret-key-change-this-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

class UserCreate(BaseModel):
    name: str
    full_name: Optional[str] = None  # Add alias for backwards compatibility
    email: EmailStr
    password: str
    plan: str = "starter"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    subscription_status: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class AuthService:
    """Handle authentication operations"""
    
    def __init__(self, supabase_client):
        self.supabase = supabase_client
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode a JWT token"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Check if user already exists
            existing_user = await self.supabase.get_user_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="User with this email already exists"
                )
            
            # Hash password
            hashed_password = self.hash_password(user_data.password)
            
            # Create user record
            user_record = {
                "id": str(uuid.uuid4()),
                "name": user_data.name,
                "email": user_data.email,
                "password_hash": hashed_password,
                "role": "customer",
                "is_active": True,
                "email_verified": False,
                "created_at": datetime.utcnow().isoformat()
            }
            
            # Insert user into database
            user = await self.supabase.create_user(user_record)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user account"
                )
            
            # Create subscription based on selected plan
            await self.create_trial_subscription(user["id"], user_data.plan)
            
            # Generate tokens
            token_data = {"sub": user["id"], "email": user["email"], "role": user["role"]}
            access_token = self.create_access_token(token_data)
            refresh_token = self.create_refresh_token(token_data)
            
            # Update last login
            await self.supabase.update_user_last_login(user["id"])
            
            return {
                "token": access_token,
                "refresh_token": refresh_token,
                "user": UserResponse(
                    id=user["id"],
                    name=user["name"],
                    email=user["email"],
                    role=user["role"],
                    is_active=user["is_active"],
                    email_verified=user["email_verified"],
                    created_at=user["created_at"],
                    subscription_status="trialing"
                )
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Registration error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed"
            )
    
    async def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Authenticate and login a user"""
        try:
            # Get user by email
            user = await self.supabase.get_user_by_email(login_data.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Verify password
            if not self.verify_password(login_data.password, user["password_hash"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password"
                )
            
            # Check if user is active
            if not user["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Account is deactivated"
                )
            
            # Get subscription status
            subscription = await self.supabase.get_user_subscription(user["id"])
            subscription_status = subscription["status"] if subscription else None
            
            # Generate tokens
            token_data = {"sub": user["id"], "email": user["email"], "role": user["role"]}
            access_token = self.create_access_token(token_data)
            refresh_token = self.create_refresh_token(token_data)
            
            # Update last login
            await self.supabase.update_user_last_login(user["id"])
            
            return {
                "token": access_token,
                "refresh_token": refresh_token,
                "user": UserResponse(
                    id=user["id"],
                    name=user["name"],
                    email=user["email"],
                    role=user["role"],
                    is_active=user["is_active"],
                    email_verified=user["email_verified"],
                    created_at=user["created_at"],
                    subscription_status=subscription_status
                )
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed"
            )
    
    async def create_trial_subscription(self, user_id: str, plan_slug: str) -> Dict[str, Any]:
        """Create a trial subscription for new user"""
        try:
            # Get plan details
            plan = await self.supabase.get_subscription_plan_by_slug(plan_slug)
            if not plan:
                plan = await self.supabase.get_subscription_plan_by_slug("starter")  # Default
            
            # Create trial subscription
            trial_start = datetime.utcnow()
            trial_end = trial_start + timedelta(days=14)  # 14-day trial
            
            subscription_data = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "plan_id": plan["id"],
                "status": "trialing",
                "trial_start": trial_start.isoformat(),
                "trial_end": trial_end.isoformat(),
                "current_period_start": trial_start.isoformat(),
                "current_period_end": trial_end.isoformat(),
                "created_at": trial_start.isoformat()
            }
            
            return await self.supabase.create_subscription(subscription_data)
            
        except Exception as e:
            logger.error(f"Failed to create trial subscription: {str(e)}")
            return None
    
    async def refresh_access_token(self, refresh_token: str) -> Dict[str, Any]:
        """Refresh an access token using a refresh token"""
        try:
            payload = self.verify_token(refresh_token)
            
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            
            user_id = payload.get("sub")
            user = await self.supabase.get_user_by_id(user_id)
            
            if not user or not user["is_active"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )
            
            # Generate new access token
            token_data = {"sub": user["id"], "email": user["email"], "role": user["role"]}
            access_token = self.create_access_token(token_data)
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Token refresh error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

# Dependency to get current user
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase_client = None
) -> Dict[str, Any]:
    """Get current authenticated user"""
    if not supabase_client:
        from database.supabase_client import get_supabase_client
        supabase_client = get_supabase_client()
    
    auth_service = AuthService(supabase_client)
    
    try:
        payload = auth_service.verify_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        
        user = await supabase_client.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        if not user["is_active"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is deactivated"
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"User authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )

# Dependency to require admin role
async def require_admin(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require admin role for access"""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user

# Dependency to check subscription limits
async def check_usage_limits(
    current_user: Dict[str, Any] = Depends(get_current_user),
    resource_type: str = "application",
    supabase_client = None
) -> Dict[str, Any]:
    """Check if user has exceeded their subscription limits"""
    if not supabase_client:
        from database.supabase_client import get_supabase_client
        supabase_client = get_supabase_client()
    
    try:
        # Get user's current subscription
        subscription = await supabase_client.get_user_subscription(current_user["id"])
        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="No active subscription found"
            )
        
        # Get plan limits
        plan = await supabase_client.get_subscription_plan_by_id(subscription["plan_id"])
        if not plan:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Subscription plan not found"
            )
        
        limits = plan.get("limits", {})
        max_resource = limits.get(f"max_{resource_type}s", 0)
        
        # Check if unlimited (value of -1)
        if max_resource == -1:
            return current_user
        
        # Count current usage
        current_usage = await supabase_client.count_user_resource_usage(
            current_user["id"], 
            resource_type
        )
        
        if current_usage >= max_resource:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Usage limit exceeded for {resource_type}s. Upgrade your plan to continue."
            )
        
        return current_user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Usage limit check error: {str(e)}")
        return current_user  # Allow by default on error 

# Standalone wrapper functions for backwards compatibility
from database.supabase_client import get_supabase_client

def create_user(email: str, password: str, full_name: str):
    """Create a new user - wrapper for AuthService.register_user"""
    import asyncio
    supabase_client = get_supabase_client()
    auth_service = AuthService(supabase_client)
    
    user_data = UserCreate(
        name=full_name,
        full_name=full_name,
        email=email,
        password=password
    )
    
    # Run async function synchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(auth_service.register_user(user_data))
        return result["user"]
    finally:
        loop.close()

def authenticate_user(email: str, password: str):
    """Authenticate user - wrapper for AuthService.login_user"""
    import asyncio
    supabase_client = get_supabase_client()
    auth_service = AuthService(supabase_client)
    
    login_data = UserLogin(email=email, password=password)
    
    # Run async function synchronously
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(auth_service.login_user(login_data))
        return result["user"]
    except:
        return None
    finally:
        loop.close()

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create access token - wrapper for AuthService.create_access_token"""
    supabase_client = get_supabase_client()
    auth_service = AuthService(supabase_client)
    return auth_service.create_access_token(data, expires_delta)

def create_refresh_token(data: Dict[str, Any]) -> str:
    """Create refresh token - wrapper for AuthService.create_refresh_token"""
    supabase_client = get_supabase_client()
    auth_service = AuthService(supabase_client)
    return auth_service.create_refresh_token(data)

# Additional wrapper functions that server.py expects
def get_current_active_user():
    """Wrapper to return the get_current_user dependency"""
    return get_current_user

def update_user_plan(user_id: str, plan: str):
    """Update user subscription plan"""
    # This would need to be implemented based on your requirements
    pass

def check_user_limits(user_id: str, limit_type: str):
    """Check if user has reached limits"""
    # Basic implementation - returns True for now
    return True, "OK"

# Export the User model and Token response for server.py
User = UserResponse
Token = TokenResponse 