from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from auth.auth_service import AuthService, UserLogin

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="UniAgent API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://d7a0ac55-32a2-46e1-857b-d77484269258.preview.emergentagent.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase
try:
    from database.supabase_client import get_supabase_client
    supabase_client = get_supabase_client()
    auth_service = AuthService(supabase_client)
    logger.info("✅ Supabase client initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Supabase: {e}")
    supabase_client = None
    auth_service = None

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/auth/login")
async def login_user(login_data: UserLogin):
    """Authenticate user and return tokens"""
    try:
        if not auth_service:
            raise HTTPException(status_code=500, detail="Authentication service not available")
        
        result = await auth_service.login_user(login_data)
        return {
            "status": "success",
            "message": "Login successful",
            "token": result["token"],
            "refresh_token": result["refresh_token"],
            "user": result["user"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@app.get("/api/admin/stats")  
async def get_admin_stats():
    """Get basic admin stats"""
    try:
        if not supabase_client:
            # Return mock data if no database
            return {
                "total_users": 1,
                "active_applications": 0,
                "success_rate": 0,
                "uptime": "99.9%"
            }
        
        # Get real data
        users = await supabase_client.get_all_users()
        return {
            "total_users": len(users),
            "active_applications": 0,
            "success_rate": 0,
            "uptime": "99.9%"
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)