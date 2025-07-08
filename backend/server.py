"""
Enhanced Backend Server with Real Automation
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, List

# Local imports
from auth.auth_service import (
    create_user, authenticate_user, create_access_token, create_refresh_token,
    get_current_user, get_current_active_user, User, Token, UserCreate,
    update_user_plan, check_user_limits
)
from database.supabase_client import get_supabase_client, test_connection
from automation.ai_enhanced_automation import AIEnhancedAutomation
from automation.enhanced_data_parser import EnhancedDataParser
from notifications.notification_service import NotificationService
from monitoring.status_monitor import SystemMonitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Service manager removed - using simplified architecture

# Global instances
automation_manager = AutomationManager()
notification_service = NotificationService()
system_monitor = SystemMonitor()
websocket_connections: Dict[str, WebSocket] = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("Starting AI LAM Backend Server...")
    
    # Test database connection
    if not test_connection():
        logger.error("Failed to connect to database")
        # Continue anyway for development
    
    # Start background tasks
    asyncio.create_task(system_monitor.start_monitoring())
    asyncio.create_task(cleanup_old_sessions())
    
    yield
    
    # Cleanup
    logger.info("Shutting down AI LAM Backend Server...")

# Create FastAPI app
app = FastAPI(
    title="AI LAM - Intelligent Form Automation API",
    description="Backend API for AI-powered form automation system",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if test_connection() else "disconnected"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "version": "2.0.0",
            "services": {
            "automation": "active",
            "notifications": "active",
            "monitoring": "active"
        }
    }

# Authentication endpoints
@app.post("/auth/register", response_model=dict)
async def register(user: UserCreate):
    """Register a new user"""
    try:
        new_user = create_user(
            email=user.email,
            password=user.password,
            full_name=user.full_name
        )
        
        # Send welcome email
        await notification_service.send_notification(
            user_id=new_user.id,
            type="email",
            subject="Welcome to AI LAM",
            content=f"Hello {new_user.full_name}, welcome to AI LAM!"
        )
        
        return {
            "message": "User created successfully",
            "user_id": new_user.id,
            "email": new_user.email
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/auth/login", response_model=Token)
async def login(email: str = Form(...), password: str = Form(...)):
    """Login user"""
    user = authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
        
        return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "subscription_plan": user.subscription_plan
        }
    }

@app.post("/auth/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    # Implement refresh token logic
    pass

@app.get("/auth/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    """Get current user info"""
    return current_user

# Automation endpoints
@app.post("/automation/create-session")
async def create_automation_session(
    target_url: str = Form(...),
    automation_type: str = Form("general"),  # signup, job_application, visa, appointment, general
    files: List[UploadFile] = File(None),
    user_data: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new universal automation session"""
    try:
        # Check user limits
        can_automate, message = check_user_limits(current_user.id, 'automation')
        if not can_automate:
            raise HTTPException(status_code=403, detail=message)
        
        # Process multiple files if uploaded
        file_data_list = []
        if files:
            for file in files:
                if file.filename:  # Skip empty file uploads
                    file_content = await file.read()
                    file_extension = file.filename.split('.')[-1].lower()
                    file_data_list.append({
                        'content': file_content,
                        'type': file_extension,
                        'filename': file.filename
                    })
        
        # Parse user data if provided as JSON
        parsed_user_data = None
        if user_data and not file_data_list:
            try:
                parsed_user_data = json.loads(user_data)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid user data format")
        
        # Create session with enhanced parser
        parser = EnhancedDataParser()
        
        # Parse all files
        if file_data_list:
            parsed_data = await parser.parse_multiple_files(file_data_list)
        elif parsed_user_data:
            parsed_data = [parsed_user_data]
        else:
            raise HTTPException(status_code=400, detail="No data provided")
        
        # Create automation session
        automation = AIEnhancedAutomation()
        session_id = await automation.create_session(
            user_id=current_user.id,
            target_url=target_url,
            automation_type=automation_type,
            parsed_data=parsed_data
        )
        
        return {
            "session_id": session_id,
            "automation_type": automation_type,
            "files_processed": len(file_data_list),
            "data_records": len(parsed_data),
            "status": "created",
            "message": "AI-enhanced automation session created successfully"
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error creating automation session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create automation session")

@app.post("/automation/start/{session_id}")
async def start_automation(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Start AI-enhanced automation for a session"""
    try:
        # Create AI-enhanced automation instance
        automation = AIEnhancedAutomation()
        
        # Start automation in background
        asyncio.create_task(run_ai_enhanced_automation(session_id, automation))
        
        return {
            "session_id": session_id,
            "ai_enabled": automation.ai_service.enabled,
            "status": "started",
            "message": "AI-enhanced automation started successfully"
        }
        
    except Exception as e:
        logger.error(f"Error starting AI automation: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start AI automation")

@app.get("/automation/status/{session_id}")
async def get_automation_status(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get automation session status"""
    try:
        session = await automation_manager.get_session_status(session_id)
        
        # Verify access
        if session['user_id'] != current_user.id and current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Access denied")
        
        return session
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/automation/screenshots/{session_id}")
async def get_automation_screenshots(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Get screenshots from automation session"""
    try:
        # Verify access
        session = await automation_manager.get_session_status(session_id)
        if session['user_id'] != current_user.id and current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Access denied")
        
        screenshots = await automation_manager.get_session_screenshots(session_id)
        return {"screenshots": screenshots}
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/automation/cancel/{session_id}")
async def cancel_automation(
    session_id: str,
    current_user: User = Depends(get_current_active_user)
):
    """Cancel a running automation session"""
    try:
        # Verify access
        session = await automation_manager.get_session_status(session_id)
        if session['user_id'] != current_user.id and current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Access denied")
        
        success = await automation_manager.cancel_session(session_id)
        
        if success:
            return {"message": "Automation cancelled successfully"}
        else:
            return {"message": "Automation not running or already completed"}
            
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/automation/history")
async def get_automation_history(
    current_user: User = Depends(get_current_active_user),
    limit: int = 10,
    offset: int = 0
):
    """Get user's automation history"""
    try:
        db_client = get_supabase_client()
        
        # Query user's automation sessions
        query = db_client.table('automation_sessions').select('*').eq(
            'user_id', current_user.id
        ).order('created_at', desc=True)
        
        if limit:
            query = query.limit(limit)
        if offset:
            query = query.offset(offset)
        
        response = query.execute()
        
        return {
            "sessions": response.data,
            "total": len(response.data),
            "limit": limit,
            "offset": offset
        }
        
    except Exception as e:
        logger.error(f"Error fetching automation history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch automation history")

# WebSocket endpoint for real-time updates
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time automation updates"""
    await websocket.accept()
    websocket_connections[session_id] = websocket
    
    try:
        while True:
            # Keep connection alive
            await asyncio.sleep(30)
            await websocket.send_json({"type": "ping"})
            
    except WebSocketDisconnect:
        del websocket_connections[session_id]
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        if session_id in websocket_connections:
            del websocket_connections[session_id]

# Admin endpoints
@app.get("/admin/stats", dependencies=[Depends(get_current_active_user)])
async def get_admin_stats(current_user: User = Depends(get_current_active_user)):
    """Get system statistics (admin only)"""
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    stats = await system_monitor.get_system_stats()
    return stats

@app.get("/admin/users", dependencies=[Depends(get_current_active_user)])
async def get_all_users(
    current_user: User = Depends(get_current_active_user),
    limit: int = 50,
    offset: int = 0
):
    """Get all users (admin only)"""
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db_client = get_supabase_client()
    response = db_client.table('users').select('*').limit(limit).offset(offset).execute()
    
    return {
        "users": response.data,
        "total": len(response.data),
        "limit": limit,
        "offset": offset
    }

@app.put("/admin/user/{user_id}/plan")
async def update_user_subscription(
    user_id: str,
    plan: str,
    current_user: User = Depends(get_current_active_user)
):
    """Update user subscription plan (admin only)"""
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        update_user_plan(user_id, plan)
        return {"message": f"User plan updated to {plan}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Add new endpoint for AI capabilities
@app.get("/automation/ai-status")
async def get_ai_status():
    """Get AI service status and capabilities"""
    from automation.ai_analysis_service import AIAnalysisService
    
    ai_service = AIAnalysisService()
    
    return {
        "ai_enabled": ai_service.enabled,
        "gemini_available": ai_service.api_key is not None,
        "model": ai_service.model_name if ai_service.enabled else None,
        "capabilities": [
            "Visual webpage analysis",
            "Intelligent field classification", 
            "Smart action suggestion",
            "Error recovery guidance",
            "Form structure understanding"
        ] if ai_service.enabled else []
    }

# Background tasks
async def run_ai_enhanced_automation(session_id: str, automation: AIEnhancedAutomation):
    """Run AI-enhanced automation with progress updates"""
    async def send_progress_update(update: Dict[str, Any]):
        if session_id in websocket_connections:
            try:
                await websocket_connections[session_id].send_json({
                    "type": "progress",
                    "data": update
                })
            except:
                pass
    
    try:
        # Get session data (this would come from your session storage)
        # For now, using placeholder data - in production, retrieve from database
        session_data = {
            'target_url': 'https://example.com',
            'automation_type': 'general',
            'user_data': {'email': 'test@example.com', 'name': 'Test User'}
        }
        
        # Run AI-enhanced automation
        result = await automation.intelligent_form_automation(
            url=session_data['target_url'],
            user_data=session_data['user_data'],
            session_id=session_id,
            automation_type=session_data['automation_type'],
            progress_callback=send_progress_update
        )
        
        # Send completion notification with AI insights
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_json({
                "type": "completed",
                "data": {
                    **result,
                    "ai_insights_count": len(result.get('ai_insights', [])),
                    "ai_confidence": result.get('ai_insights', [{}])[-1].get('confidence', 0) if result.get('ai_insights') else 0
                }
            })
    
    except Exception as e:
        logger.error(f"AI-enhanced automation failed: {str(e)}")
        if session_id in websocket_connections:
            await websocket_connections[session_id].send_json({
                "type": "error",
                "data": {"error": str(e), "ai_enabled": automation.ai_service.enabled}
            })

async def cleanup_old_sessions():
    """Periodically clean up old sessions"""
    while True:
        try:
            await asyncio.sleep(3600)  # Run every hour
            await automation_manager.cleanup_old_sessions(24)
    except Exception as e:
            logger.error(f"Error cleaning up sessions: {str(e)}")

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
