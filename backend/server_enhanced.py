"""
Enhanced AI LAM Server

FastAPI server following Suna's architectural patterns with proper service management,
lifecycle handling, and structured logging.
"""

import asyncio
import sys
import uuid
import time
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Services
from services import (
    get_database_service, 
    get_llm_service, 
    get_automation_service,
    get_notification_service,
    get_monitoring_service
)
from utils.config import get_config, validate_config
from auth.auth_service import get_current_user, User

# Configuration
config = get_config()

# Initialize instance ID
instance_id = str(uuid.uuid4())[:8]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager following Suna's pattern."""
    print(f"🚀 Starting AI LAM server with instance ID: {instance_id} in {config.ENV_MODE.value} mode")
    
    try:
        # Validate configuration
        validate_config()
        print("✅ Configuration validated")
        
        # Initialize services in order
        print("🔧 Initializing services...")
        
        db_service = get_database_service()
        await db_service.initialize()
        print("✅ Database service initialized")
        
        llm_service = get_llm_service()
        print("✅ LLM service initialized")
        
        automation_service = get_automation_service()
        await automation_service.initialize()
        print("✅ Automation service initialized")
        
        notification_service = get_notification_service()
        await notification_service.initialize()
        print("✅ Notification service initialized")
        
        monitoring_service = get_monitoring_service()
        await monitoring_service.initialize()
        print("✅ Monitoring service initialized")
        
        print(f"🎉 All services initialized successfully!")
        
        yield
        
        # Cleanup on shutdown
        print("🛑 Shutting down services...")
        
        await monitoring_service.shutdown()
        print("✅ Monitoring service shutdown")
        
        await db_service.disconnect()
        print("✅ Database service disconnected")
        
        print("🏁 Server shutdown complete")
        
    except Exception as e:
        print(f"❌ Error during application startup: {e}")
        raise

# Create FastAPI app with lifespan
app = FastAPI(
    title="AI LAM - Autonomous University Application Management",
    description="Enhanced AI-powered automation system for university applications",
    version="2.0.0",
    lifespan=lifespan
)

# Request tracking middleware
@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    """Track requests with enhanced logging following Suna's pattern."""
    request_id = str(uuid.uuid4())
    start_time = time.time()
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    path = request.url.path
    
    # Add request ID to request state
    request.state.request_id = request_id
    
    print(f"📥 Request {request_id}: {method} {path} from {client_ip}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        
        print(f"📤 Request {request_id}: {response.status_code} in {process_time:.2f}s")
        
        # Add custom headers
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}s"
        response.headers["X-Instance-ID"] = instance_id
        
        return response
        
    except Exception as e:
        process_time = time.time() - start_time
        print(f"❌ Request {request_id}: Failed in {process_time:.2f}s - {str(e)}")
        raise

# CORS Configuration
allowed_origins = config.ALLOWED_ORIGINS.copy()
if config.is_local:
    allowed_origins.extend(["http://localhost:3000", "http://127.0.0.1:3000"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)

# Enhanced Health Check
@app.get("/health")
async def enhanced_health_check():
    """Enhanced health check endpoint following Suna's pattern."""
    monitoring_service = get_monitoring_service()
    health_status = await monitoring_service.get_health_status()
    
    return {
        "status": health_status["status"],
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "instance_id": instance_id,
        "version": "2.0.0",
        "environment": config.ENV_MODE.value,
        "health_score": health_status["health_score"],
        "services": health_status["services"],
        "issues": health_status.get("issues", [])
    }

# System Status Endpoint
@app.get("/status")
async def system_status():
    """Get detailed system status."""
    monitoring_service = get_monitoring_service()
    metrics = monitoring_service.get_cached_metrics()
    
    return {
        "instance_id": instance_id,
        "uptime": time.time(),
        "environment": config.ENV_MODE.value,
        "metrics": metrics,
        "features": {
            "automation": config.ENABLE_AUTOMATION,
            "notifications": config.ENABLE_NOTIFICATIONS
        }
    }

# User Profile Endpoint (Example of service integration)
@app.get("/api/user/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile - example of service integration."""
    db_service = get_database_service()
    
    # Get user details
    user_data = await db_service.get_user_by_id(current_user.id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's recent automations
    automation_service = get_automation_service()
    recent_automations = await automation_service.get_automation_history(
        user_id=current_user.id, 
        limit=5
    )
    
    # Get user's recent notifications
    notification_service = get_notification_service()
    notifications = await notification_service.get_user_notifications(
        user_id=current_user.id,
        limit=10,
        unread_only=False
    )
    
    return {
        "user": {
            "id": user_data["id"],
            "email": user_data["email"],
            "full_name": user_data["full_name"],
            "role": user_data["role"],
            "subscription_plan": user_data["subscription_plan"],
            "created_at": user_data["created_at"]
        },
        "recent_automations": recent_automations,
        "notifications": notifications
    }

# Automation Endpoint
@app.post("/api/automation/execute")
async def execute_automation(
    task_type: str,
    task_data: dict,
    current_user: User = Depends(get_current_user)
):
    """Execute an automation task."""
    automation_service = get_automation_service()
    notification_service = get_notification_service()
    
    try:
        # Execute automation
        result = await automation_service.execute_automation_task(
            task_type=task_type,
            task_data=task_data,
            user_id=current_user.id
        )
        
        # Send completion notification
        await notification_service.send_automation_complete_notification(
            user_id=current_user.id,
            automation_type=task_type,
            automation_id=result["automation_id"],
            success=result["success"],
            details=result
        )
        
        return result
        
    except Exception as e:
        # Send failure notification
        await notification_service.send_automation_complete_notification(
            user_id=current_user.id,
            automation_type=task_type,
            automation_id="failed",
            success=False,
            details={"error": str(e)}
        )
        
        raise HTTPException(status_code=500, detail=f"Automation failed: {str(e)}")

# Performance Metrics Endpoint
@app.get("/api/admin/metrics")
async def get_performance_metrics(
    hours: int = 24,
    current_user: User = Depends(get_current_user)
):
    """Get performance metrics (admin only)."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    monitoring_service = get_monitoring_service()
    stats = await monitoring_service.get_performance_stats(hours=hours)
    
    return stats

# Error Handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Enhanced HTTP exception handler."""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """General exception handler."""
    request_id = getattr(request.state, 'request_id', 'unknown')
    
    print(f"❌ Unhandled exception in request {request_id}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "request_id": request_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    print(f"🌟 Starting AI LAM Enhanced Server")
    print(f"📍 Environment: {config.ENV_MODE.value}")
    print(f"🎯 Instance ID: {instance_id}")
    
    uvicorn.run(
        "server_enhanced:app",
        host=config.HOST,
        port=config.PORT,
        workers=1,  # Single worker for development
        reload=config.is_local,
        log_level=config.LOG_LEVEL.lower()
    ) 