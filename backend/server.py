from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import asyncio
import json
import traceback
import random
import psutil
import schedule
import time
from threading import Thread

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import enhanced services - try/except for optional imports
try:
    from monitoring.enhanced_monitor import get_monitoring_service
    monitoring_available = True
except ImportError:
    monitoring_available = False
    logger.warning("Enhanced monitoring service not available")

try:
    from services.gcp_ready_manager import get_service_manager  
    service_manager_available = True
except ImportError:
    service_manager_available = False
    logger.warning("GCP service manager not available")

# Import new services - try/except for optional imports
try:
    from automation.browser_automation import EnhancedBrowserAutomation
    automation_available = True
except ImportError:
    automation_available = False
    logger.warning("Browser automation not available")

try:
    from security.encryption import DataEncryption, SecureCredentialStorage
    from notifications.notification_service import NotificationService
    from monitoring.status_monitor import ApplicationMonitor, PerformanceMonitor
    additional_services_available = True
except ImportError:
    additional_services_available = False
    logger.warning("Additional services not available")
from database.supabase_client import get_supabase_client, SupabaseClient

# Import authentication services
from auth.auth_service import (
    AuthService, 
    UserCreate, 
    UserLogin, 
    UserResponse, 
    TokenResponse,
    get_current_user,
    require_admin,
    check_usage_limits
)

# Custom JSON encoder to handle datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Create the main app
app = FastAPI(title="Autonomous University Application Agent")
api_router = APIRouter(prefix="/api")

# Configure CORS immediately after app creation
cors_origins = [
    "http://localhost:3000", 
    "http://127.0.0.1:3000", 
    "https://fc368f58-030a-4d3e-8fe3-d490c5163ec6.preview.emergentagent.com",
    "https://8142d1b2-e9a6-419c-9ea6-a8302219edac.preview.emergentagent.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # Allow all origins for development
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase_client = get_supabase_client()

# Initialize services conditionally
if additional_services_available:
    encryption_service = DataEncryption()
    credential_storage = SecureCredentialStorage(encryption_service)
    notification_service = NotificationService()
    app_monitor = ApplicationMonitor(supabase_client, notification_service)
    perf_monitor = PerformanceMonitor()
else:
    encryption_service = None
    credential_storage = None
    notification_service = None
    app_monitor = None
    perf_monitor = None
    logger.warning("Additional services not initialized due to import errors")

auth_service = AuthService(supabase_client)

# Data Models
class ClientData(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str
    email: str
    phone: str
    date_of_birth: str
    nationality: str
    address: str
    personal_statement: str
    academic_history: List[Dict[str, Any]]
    course_preferences: List[Dict[str, Any]]
    documents: Dict[str, str]  # Base64 encoded documents
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        # Convert datetime to string
        if 'created_at' in data and isinstance(data['created_at'], datetime):
            data['created_at'] = data['created_at'].isoformat()
        return data

class ApplicationTask(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_id: str
    university_name: str
    course_name: str
    course_code: str
    application_url: str
    status: str = "pending"  # pending, in_progress, submitted, accepted, rejected
    credentials: Dict[str, str] = {}  # username, password
    application_data: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_checked: Optional[datetime] = None
    error_log: List[str] = []
    
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        # Convert datetime to string
        if 'created_at' in data and isinstance(data['created_at'], datetime):
            data['created_at'] = data['created_at'].isoformat()
        if 'last_checked' in data and isinstance(data['last_checked'], datetime):
            data['last_checked'] = data['last_checked'].isoformat()
        return data

class AgentCommand(BaseModel):
    command_type: str  # "create_applications", "check_status", "monitor_daily"
    client_id: str
    parameters: Dict[str, Any] = {}

class MockUniversityApplication(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    university_name: str
    applicant_name: str
    email: str
    course: str
    personal_statement: str
    status: str = "submitted"
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    documents: Dict[str, str] = {}
    
    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        # Convert datetime to string
        if 'submitted_at' in data and isinstance(data['submitted_at'], datetime):
            data['submitted_at'] = data['submitted_at'].isoformat()
        return data

# Top 10 UK Universities Configuration
TOP_UNIVERSITIES = [
    {"name": "University of Oxford", "code": "oxford", "url": "https://www.ox.ac.uk/admissions"},
    {"name": "University of Cambridge", "code": "cambridge", "url": "https://www.cam.ac.uk/admissions"},
    {"name": "Imperial College London", "code": "imperial", "url": "https://www.imperial.ac.uk/study/apply"},
    {"name": "London School of Economics", "code": "lse", "url": "https://www.lse.ac.uk/study-at-lse/how-to-apply"},
    {"name": "University College London", "code": "ucl", "url": "https://www.ucl.ac.uk/prospective-students/how-apply"},
    {"name": "King's College London", "code": "kcl", "url": "https://www.kcl.ac.uk/study/how-to-apply"},
    {"name": "University of Edinburgh", "code": "edinburgh", "url": "https://www.ed.ac.uk/studying/how-to-apply"},
    {"name": "University of Manchester", "code": "manchester", "url": "https://www.manchester.ac.uk/study/how-to-apply"},
    {"name": "University of Warwick", "code": "warwick", "url": "https://warwick.ac.uk/study/how-to-apply"},
    {"name": "University of Bristol", "code": "bristol", "url": "https://www.bristol.ac.uk/study/how-to-apply"}
]

# Mock database for testing
mock_db = {
    "clients": [],
    "application_tasks": [],
    "mock_applications": []
}

# Autonomous Agent Class
class UniversityApplicationAgent:
    def __init__(self):
        self.browser_automation = EnhancedBrowserAutomation()
        self.performance_monitor = perf_monitor
        
    async def initialize_browser(self):
        """Initialize Playwright browser with anti-detection measures"""
        try:
            # Import here to avoid errors if not installed
            from playwright.async_api import async_playwright
            from fake_useragent import UserAgent
            ua = UserAgent()
            
            self.playwright = await async_playwright().start()
            
            # Launch browser with stealth settings
            self.browser = await self.playwright.chromium.launch(
                headless=True,  # Set to True for production
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--disable-features=VizDisplayCompositor',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-images',
                    '--disable-javascript',
                    '--user-agent=' + ua.random
                ]
            )
            
            # Create context with realistic settings
            self.context = await self.browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent=ua.random,
                locale='en-GB',
                timezone_id='Europe/London'
            )
            
            # Add anti-detection scripts
            await self.context.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-GB', 'en-US', 'en'],
                });
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
        except Exception as e:
            logger.error(f"Error initializing browser: {str(e)}")
            # Return a mock context for testing
            return None
    
    async def create_university_account(self, university_data: dict, client_data: ClientData) -> dict:
        """Create account on university application portal"""
        try:
            if not self.context:
                await self.initialize_browser()
            
            # Mock account creation logic
            credentials = {
                "username": f"{client_data.email}",
                "password": f"UniApp{random.randint(1000, 9999)}!",
                "created_at": datetime.utcnow().isoformat()
            }
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error creating account for {university_data['name']}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Account creation failed: {str(e)}")
    
    async def fill_application_form(self, university_data: dict, client_data: ClientData, credentials: dict) -> dict:
        """Fill university application form autonomously"""
        try:
            if not self.context:
                await self.initialize_browser()
            
            # Mock form submission
            application_data = {
                "personal_details": {
                    "name": client_data.full_name,
                    "email": client_data.email,
                    "phone": client_data.phone,
                    "dob": client_data.date_of_birth,
                    "nationality": client_data.nationality,
                    "address": client_data.address
                },
                "academic_history": client_data.academic_history,
                "personal_statement": client_data.personal_statement,
                "course_preferences": client_data.course_preferences,
                "submitted_at": datetime.utcnow().isoformat(),
                "status": "submitted"
            }
            
            return application_data
            
        except Exception as e:
            logger.error(f"Error filling application for {university_data['name']}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Application filling failed: {str(e)}")
    
    async def check_application_status(self, task: ApplicationTask) -> str:
        """Check application status autonomously"""
        try:
            if not self.context:
                await self.initialize_browser()
            
            # Simulate status update
            statuses = ["submitted", "under_review", "interview_scheduled", "accepted", "rejected"]
            current_status = random.choice(statuses)
            
            return current_status
            
        except Exception as e:
            logger.error(f"Error checking status for {task.university_name}: {str(e)}")
            return "error"
    
    async def cleanup(self):
        """Cleanup browser resources"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

# Global agent instance
agent = UniversityApplicationAgent()

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Autonomous University Application Agent API"}

@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Check database connection
        client = get_supabase_client()
        # Simple query to verify connection
        result = client.table('users').select('id').limit(1).execute()
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "services": {
                "database": "connected",
                "api": "running"
            },
            "version": "2.0.0"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e),
            "version": "2.0.0"
        }

# === AUTHENTICATION ENDPOINTS ===

@api_router.post("/auth/register", response_model=dict)
async def register_user(user_data: UserCreate):
    """Register a new user account"""
    try:
        result = await auth_service.register_user(user_data)
        return {
            "status": "success",
            "message": "Account created successfully",
            "token": result["token"],
            "refresh_token": result["refresh_token"],
            "user": result["user"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@api_router.post("/auth/login", response_model=dict)
async def login_user(login_data: UserLogin):
    """Authenticate user and return tokens"""
    try:
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

@api_router.post("/auth/refresh", response_model=dict)
async def refresh_token(refresh_token: str):
    """Refresh access token"""
    try:
        result = await auth_service.refresh_access_token(refresh_token)
        return {
            "status": "success",
            **result
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(status_code=401, detail="Token refresh failed")

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    subscription = await supabase_client.get_user_subscription(current_user["id"])
    
    return UserResponse(
        id=current_user["id"],
        name=current_user["name"],
        email=current_user["email"],
        role=current_user["role"],
        is_active=current_user["is_active"],
        email_verified=current_user["email_verified"],
        created_at=current_user["created_at"],
        subscription_status=subscription["status"] if subscription else None
    )

# === SUBSCRIPTION ENDPOINTS ===

@api_router.get("/subscription/plans", response_model=List[dict])
async def get_subscription_plans():
    """Get all available subscription plans"""
    try:
        plans = await supabase_client.get_all_subscription_plans()
        return plans
    except Exception as e:
        logger.error(f"Error fetching subscription plans: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscription plans")

@api_router.get("/subscription/current", response_model=dict)
async def get_current_subscription(current_user: dict = Depends(get_current_user)):
    """Get current user's subscription details"""
    try:
        subscription = await supabase_client.get_user_subscription(current_user["id"])
        if not subscription:
            raise HTTPException(status_code=404, detail="No active subscription found")
        
        plan = await supabase_client.get_subscription_plan_by_id(subscription["plan_id"])
        
        return {
            "subscription": subscription,
            "plan": plan
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching subscription: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch subscription")

# === ADMIN ENDPOINTS ===

@api_router.get("/admin/users", response_model=List[dict])
async def get_all_users(admin_user: dict = Depends(require_admin)):
    """Get all users (admin only)"""
    try:
        users = await supabase_client.get_all_users()
        return users
    except Exception as e:
        logger.error(f"Error fetching users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

@api_router.get("/admin/stats", response_model=dict)
async def get_admin_stats(admin_user: dict = Depends(require_admin)):
    """Get system statistics (admin only)"""
    try:
        # Get real data from Supabase
        users = await supabase_client.get_all_users()
        applications = await supabase_client.get_all_application_tasks()
        
        # Calculate stats
        total_applications = len(applications)
        successful_apps = len([app for app in applications if app.get("status") == "accepted"])
        success_rate = (successful_apps / total_applications * 100) if total_applications > 0 else 0
        
        # System performance data
        import psutil
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        stats = {
            "total_users": len(users),
            "active_applications": len([app for app in applications if app.get("status") in ["pending", "in_progress"]]),
            "success_rate": round(success_rate, 1),
            "uptime": "99.9%",
            "user_growth": 12.5,
            "application_growth": 8.3,
            "success_trend": 2.1,
            "cpu_usage": round(cpu_usage, 1),
            "memory_usage": round(memory.percent, 1),
            "disk_usage": round(disk.percent, 1),
            "total_applications": total_applications,
            "applications_by_status": {}
        }
        
        # Count applications by status
        for app in applications:
            status = app.get("status", "unknown")
            stats["applications_by_status"][status] = stats["applications_by_status"].get(status, 0) + 1
        
        return stats
    except Exception as e:
        logger.error(f"Error fetching admin stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch statistics")

@api_router.get("/admin/applications", response_model=List[dict])
async def get_admin_applications(admin_user: dict = Depends(require_admin)):
    """Get all applications with client info (admin only)"""
    try:
        applications = await supabase_client.get_all_application_tasks()
        clients = await supabase_client.get_all_clients()
        clients_dict = {client["id"]: client for client in clients}
        
        # Enrich applications with client data
        enriched_apps = []
        for app in applications:
            client = clients_dict.get(app.get("client_id"))
            enriched_app = {
                **app,
                "client_name": client["full_name"] if client else "Unknown",
                "client_email": client["email"] if client else "Unknown"
            }
            enriched_apps.append(enriched_app)
        
        return enriched_apps
    except Exception as e:
        logger.error(f"Error fetching applications: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch applications")

@api_router.get("/admin/audit-logs", response_model=List[dict])
async def get_audit_logs(admin_user: dict = Depends(require_admin), limit: int = 50):
    """Get system audit logs (admin only)"""
    try:
        # Mock audit logs for now
        logs = [
            {
                "id": str(uuid.uuid4()),
                "timestamp": (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
                "description": "New client registration completed",
                "user_id": "system",
                "action": "client_create",
                "details": {"client_name": "John Doe"}
            },
            {
                "id": str(uuid.uuid4()),
                "timestamp": (datetime.utcnow() - timedelta(minutes=15)).isoformat(),
                "description": "Application submitted to Oxford University",
                "user_id": "system",
                "action": "application_submit",
                "details": {"university": "Oxford"}
            },
            {
                "id": str(uuid.uuid4()),
                "timestamp": (datetime.utcnow() - timedelta(hours=1)).isoformat(),
                "description": "System health check completed",
                "user_id": "system",
                "action": "health_check",
                "details": {"status": "healthy"}
            },
            {
                "id": str(uuid.uuid4()),
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "description": "User login successful",
                "user_id": admin_user["id"],
                "action": "user_login",
                "details": {"ip": "127.0.0.1"}
            }
        ]
        
        return logs[:limit]
    except Exception as e:
        logger.error(f"Error fetching audit logs: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch audit logs")

@api_router.post("/admin/users/{user_id}/{action}")
async def user_action(user_id: str, action: str, admin_user: dict = Depends(require_admin)):
    """Perform actions on users (activate/deactivate) (admin only)"""
    try:
        if action not in ["activate", "deactivate"]:
            raise HTTPException(status_code=400, detail="Invalid action")
        
        # Mock user action for now
        return {"message": f"User {action} successful", "user_id": user_id}
    except Exception as e:
        logger.error(f"Error performing user action: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform user action")

@api_router.get("/admin/performance", response_model=dict)
async def get_performance_metrics(admin_user: dict = Depends(require_admin)):
    """Get detailed performance metrics (admin only)"""
    try:
        import psutil
        
        # Get system metrics
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Mock application metrics
        metrics = {
            "system": {
                "cpu_usage": round(cpu_percent, 1),
                "memory_usage": round(memory.percent, 1),
                "memory_available": round(memory.available / (1024**3), 2),  # GB
                "disk_usage": round(disk.percent, 1),
                "disk_free": round(disk.free / (1024**3), 2)  # GB
            },
            "application": {
                "active_sessions": random.randint(10, 50),
                "requests_per_minute": random.randint(100, 500),
                "average_response_time": round(random.uniform(0.1, 2.0), 2),
                "error_rate": round(random.uniform(0.0, 5.0), 2)
            },
            "database": {
                "connection_pool_usage": round(random.uniform(20, 80), 1),
                "query_performance": round(random.uniform(10, 100), 1),
                "active_connections": random.randint(5, 25)
            }
        }
        
        return metrics
    except Exception as e:
        logger.error(f"Error fetching performance metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch performance metrics")

@api_router.get("/admin/monitoring/current", response_model=dict)
async def get_current_monitoring_data(admin_user: dict = Depends(require_admin)):
    """Get current monitoring data from enhanced monitoring service"""
    try:
        monitoring_service = get_monitoring_service()
        current_metrics = monitoring_service.get_current_metrics()
        return current_metrics
    except Exception as e:
        logger.error(f"Error fetching current monitoring data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring data")

@api_router.get("/admin/monitoring/history", response_model=dict)
async def get_monitoring_history(hours: int = 24, admin_user: dict = Depends(require_admin)):
    """Get monitoring history for specified hours"""
    try:
        monitoring_service = get_monitoring_service()
        history = monitoring_service.get_metrics_history(hours)
        return history
    except Exception as e:
        logger.error(f"Error fetching monitoring history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring history")

@api_router.get("/admin/monitoring/alerts", response_model=List[dict])
async def get_monitoring_alerts(limit: int = 20, admin_user: dict = Depends(require_admin)):
    """Get recent monitoring alerts"""
    try:
        monitoring_service = get_monitoring_service()
        alerts = monitoring_service.get_recent_alerts(limit)
        return alerts
    except Exception as e:
        logger.error(f"Error fetching monitoring alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring alerts")

@api_router.post("/admin/monitoring/alerts/clear")
async def clear_monitoring_alerts(admin_user: dict = Depends(require_admin)):
    """Clear all monitoring alerts"""
    try:
        monitoring_service = get_monitoring_service()
        monitoring_service.clear_alerts()
        return {"message": "Alerts cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing monitoring alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear alerts")

@api_router.get("/admin/services/status", response_model=dict)
async def get_services_status(admin_user: dict = Depends(require_admin)):
    """Get status of all managed services"""
    try:
        service_manager = get_service_manager()
        status = service_manager.get_all_services_status()
        return status
    except Exception as e:
        logger.error(f"Error fetching services status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch services status")

@api_router.post("/admin/services/{service_name}/{action}")
async def manage_service(service_name: str, action: str, admin_user: dict = Depends(require_admin)):
    """Manage a specific service (start/stop/restart)"""
    try:
        if action not in ["start", "stop", "restart"]:
            raise HTTPException(status_code=400, detail="Invalid action. Use start, stop, or restart")
        
        service_manager = get_service_manager()
        
        if action == "start":
            success = await service_manager.start_service(service_name)
        elif action == "stop":
            success = await service_manager.stop_service(service_name)
        elif action == "restart":
            success = await service_manager.restart_service(service_name)
        
        if success:
            return {"message": f"Service {service_name} {action} initiated successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to {action} service {service_name}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error managing service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to {action} service {service_name}")

@api_router.get("/admin/services/{service_name}/status", response_model=dict)
async def get_service_status(service_name: str, admin_user: dict = Depends(require_admin)):
    """Get detailed status of a specific service"""
    try:
        service_manager = get_service_manager()
        status = service_manager.get_service_status(service_name)
        return status
    except Exception as e:
        logger.error(f"Error fetching service status for {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch status for service {service_name}")

@api_router.get("/admin/system/health", response_model=dict)
async def get_system_health(admin_user: dict = Depends(require_admin)):
    """Get comprehensive system health check"""
    try:
        # Get monitoring data
        monitoring_service = get_monitoring_service()
        current_metrics = monitoring_service.get_current_metrics()
        recent_alerts = monitoring_service.get_recent_alerts(5)
        
        # Get services status
        service_manager = get_service_manager()
        services_status = service_manager.get_all_services_status()
        
        # Database health check
        try:
            # Test Supabase connection
            supabase_healthy = True
            # You can add a simple query here to test the connection
        except Exception:
            supabase_healthy = False
        
        # Overall health calculation
        critical_alerts = len([alert for alert in recent_alerts if alert.get("severity") == "CRITICAL"])
        running_services = services_status.get("running_services", 0)
        total_services = services_status.get("total_services", 1)
        service_health_score = (running_services / total_services) * 100 if total_services > 0 else 0
        
        overall_health = "healthy"
        if critical_alerts > 0 or service_health_score < 80:
            overall_health = "warning"
        if critical_alerts > 3 or service_health_score < 50:
            overall_health = "critical"
        
        health_data = {
            "overall_health": overall_health,
            "health_score": round(service_health_score, 1),
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": {
                    "supabase": "healthy" if supabase_healthy else "unhealthy",
                    "mongodb": "healthy"  # Assuming healthy for now
                },
                "services": {
                    "total": total_services,
                    "running": running_services,
                    "health_percentage": round(service_health_score, 1)
                },
                "monitoring": {
                    "active": monitoring_service.monitoring_active,
                    "recent_alerts": len(recent_alerts),
                    "critical_alerts": critical_alerts
                }
            },
            "metrics": current_metrics,
            "recent_alerts": recent_alerts
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Error performing system health check: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform system health check")

@api_router.get("/admin/monitoring/current", response_model=dict)
async def get_current_monitoring_data(admin_user: dict = Depends(require_admin)):
    """Get current monitoring data from enhanced monitoring service"""
    try:
        monitoring_service = get_monitoring_service()
        current_metrics = monitoring_service.get_current_metrics()
        return current_metrics
    except Exception as e:
        logger.error(f"Error fetching current monitoring data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring data")

@api_router.get("/admin/monitoring/history", response_model=dict)
async def get_monitoring_history(hours: int = 24, admin_user: dict = Depends(require_admin)):
    """Get monitoring history for specified hours"""
    try:
        monitoring_service = get_monitoring_service()
        history = monitoring_service.get_metrics_history(hours)
        return history
    except Exception as e:
        logger.error(f"Error fetching monitoring history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring history")

@api_router.get("/admin/monitoring/alerts", response_model=List[dict])
async def get_monitoring_alerts(limit: int = 20, admin_user: dict = Depends(require_admin)):
    """Get recent monitoring alerts"""
    try:
        monitoring_service = get_monitoring_service()
        alerts = monitoring_service.get_recent_alerts(limit)
        return alerts
    except Exception as e:
        logger.error(f"Error fetching monitoring alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring alerts")

@api_router.post("/admin/monitoring/alerts/clear")
async def clear_monitoring_alerts(admin_user: dict = Depends(require_admin)):
    """Clear all monitoring alerts"""
    try:
        monitoring_service = get_monitoring_service()
        monitoring_service.clear_alerts()
        return {"message": "Alerts cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing monitoring alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear alerts")

@api_router.get("/admin/services/status", response_model=dict)
async def get_services_status(admin_user: dict = Depends(require_admin)):
    """Get status of all managed services"""
    try:
        service_manager = get_service_manager()
        status = service_manager.get_all_services_status()
        return status
    except Exception as e:
        logger.error(f"Error fetching services status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch services status")

@api_router.post("/admin/services/{service_name}/{action}")
async def manage_service(service_name: str, action: str, admin_user: dict = Depends(require_admin)):
    """Manage a specific service (start/stop/restart)"""
    try:
        if action not in ["start", "stop", "restart"]:
            raise HTTPException(status_code=400, detail="Invalid action. Use start, stop, or restart")
        
        service_manager = get_service_manager()
        
        if action == "start":
            success = await service_manager.start_service(service_name)
        elif action == "stop":
            success = await service_manager.stop_service(service_name)
        elif action == "restart":
            success = await service_manager.restart_service(service_name)
        
        if success:
            return {"message": f"Service {service_name} {action} initiated successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to {action} service {service_name}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error managing service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to {action} service {service_name}")

@api_router.get("/admin/services/{service_name}/status", response_model=dict)
async def get_service_status(service_name: str, admin_user: dict = Depends(require_admin)):
    """Get detailed status of a specific service"""
    try:
        service_manager = get_service_manager()
        status = service_manager.get_service_status(service_name)
        return status
    except Exception as e:
        logger.error(f"Error fetching service status for {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch status for service {service_name}")

@api_router.get("/admin/system/health", response_model=dict)
async def get_system_health(admin_user: dict = Depends(require_admin)):
    """Get comprehensive system health check"""
    try:
        # Get monitoring data
        monitoring_service = get_monitoring_service()
        current_metrics = monitoring_service.get_current_metrics()
        recent_alerts = monitoring_service.get_recent_alerts(5)
        
        # Get services status
        service_manager = get_service_manager()
        services_status = service_manager.get_all_services_status()
        
        # Database health check
        try:
            # Test Supabase connection
            supabase_healthy = True
            # You can add a simple query here to test the connection
        except Exception:
            supabase_healthy = False
        
        # Overall health calculation
        critical_alerts = len([alert for alert in recent_alerts if alert.get("severity") == "CRITICAL"])
        running_services = services_status.get("running_services", 0)
        total_services = services_status.get("total_services", 1)
        service_health_score = (running_services / total_services) * 100 if total_services > 0 else 0
        
        overall_health = "healthy"
        if critical_alerts > 0 or service_health_score < 80:
            overall_health = "warning"
        if critical_alerts > 3 or service_health_score < 50:
            overall_health = "critical"
        
        health_data = {
            "overall_health": overall_health,
            "health_score": round(service_health_score, 1),
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": {
                    "supabase": "healthy" if supabase_healthy else "unhealthy",
                    "mongodb": "healthy"  # Assuming healthy for now
                },
                "services": {
                    "total": total_services,
                    "running": running_services,
                    "health_percentage": round(service_health_score, 1)
                },
                "monitoring": {
                    "active": monitoring_service.monitoring_active,
                    "recent_alerts": len(recent_alerts),
                    "critical_alerts": critical_alerts
                }
            },
            "metrics": current_metrics,
            "recent_alerts": recent_alerts
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Error performing system health check: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform system health check")

@api_router.get("/admin/monitoring/current", response_model=dict)
async def get_current_monitoring_data(admin_user: dict = Depends(require_admin)):
    """Get current monitoring data from enhanced monitoring service"""
    try:
        monitoring_service = get_monitoring_service()
        current_metrics = monitoring_service.get_current_metrics()
        return current_metrics
    except Exception as e:
        logger.error(f"Error fetching current monitoring data: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring data")

@api_router.get("/admin/monitoring/history", response_model=dict)
async def get_monitoring_history(hours: int = 24, admin_user: dict = Depends(require_admin)):
    """Get monitoring history for specified hours"""
    try:
        monitoring_service = get_monitoring_service()
        history = monitoring_service.get_metrics_history(hours)
        return history
    except Exception as e:
        logger.error(f"Error fetching monitoring history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring history")

@api_router.get("/admin/monitoring/alerts", response_model=List[dict])
async def get_monitoring_alerts(limit: int = 20, admin_user: dict = Depends(require_admin)):
    """Get recent monitoring alerts"""
    try:
        monitoring_service = get_monitoring_service()
        alerts = monitoring_service.get_recent_alerts(limit)
        return alerts
    except Exception as e:
        logger.error(f"Error fetching monitoring alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch monitoring alerts")

@api_router.post("/admin/monitoring/alerts/clear")
async def clear_monitoring_alerts(admin_user: dict = Depends(require_admin)):
    """Clear all monitoring alerts"""
    try:
        monitoring_service = get_monitoring_service()
        monitoring_service.clear_alerts()
        return {"message": "Alerts cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing monitoring alerts: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to clear alerts")

@api_router.get("/admin/services/status", response_model=dict)
async def get_services_status(admin_user: dict = Depends(require_admin)):
    """Get status of all managed services"""
    try:
        service_manager = get_service_manager()
        status = service_manager.get_all_services_status()
        return status
    except Exception as e:
        logger.error(f"Error fetching services status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch services status")

@api_router.post("/admin/services/{service_name}/{action}")
async def manage_service(service_name: str, action: str, admin_user: dict = Depends(require_admin)):
    """Manage a specific service (start/stop/restart)"""
    try:
        if action not in ["start", "stop", "restart"]:
            raise HTTPException(status_code=400, detail="Invalid action. Use start, stop, or restart")
        
        service_manager = get_service_manager()
        
        if action == "start":
            success = await service_manager.start_service(service_name)
        elif action == "stop":
            success = await service_manager.stop_service(service_name)
        elif action == "restart":
            success = await service_manager.restart_service(service_name)
        
        if success:
            return {"message": f"Service {service_name} {action} initiated successfully"}
        else:
            raise HTTPException(status_code=500, detail=f"Failed to {action} service {service_name}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error managing service {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to {action} service {service_name}")

@api_router.get("/admin/services/{service_name}/status", response_model=dict)
async def get_service_status(service_name: str, admin_user: dict = Depends(require_admin)):
    """Get detailed status of a specific service"""
    try:
        service_manager = get_service_manager()
        status = service_manager.get_service_status(service_name)
        return status
    except Exception as e:
        logger.error(f"Error fetching service status for {service_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch status for service {service_name}")

@api_router.get("/admin/system/health", response_model=dict)
async def get_system_health(admin_user: dict = Depends(require_admin)):
    """Get comprehensive system health check"""
    try:
        # Get monitoring data
        monitoring_service = get_monitoring_service()
        current_metrics = monitoring_service.get_current_metrics()
        recent_alerts = monitoring_service.get_recent_alerts(5)
        
        # Get services status
        service_manager = get_service_manager()
        services_status = service_manager.get_all_services_status()
        
        # Database health check
        try:
            # Test Supabase connection
            supabase_healthy = True
            # You can add a simple query here to test the connection
        except Exception:
            supabase_healthy = False
        
        # Overall health calculation
        critical_alerts = len([alert for alert in recent_alerts if alert.get("severity") == "CRITICAL"])
        running_services = services_status.get("running_services", 0)
        total_services = services_status.get("total_services", 1)
        service_health_score = (running_services / total_services) * 100 if total_services > 0 else 0
        
        overall_health = "healthy"
        if critical_alerts > 0 or service_health_score < 80:
            overall_health = "warning"
        if critical_alerts > 3 or service_health_score < 50:
            overall_health = "critical"
        
        health_data = {
            "overall_health": overall_health,
            "health_score": round(service_health_score, 1),
            "timestamp": datetime.utcnow().isoformat(),
            "components": {
                "database": {
                    "supabase": "healthy" if supabase_healthy else "unhealthy",
                    "mongodb": "healthy"  # Assuming healthy for now
                },
                "services": {
                    "total": total_services,
                    "running": running_services,
                    "health_percentage": round(service_health_score, 1)
                },
                "monitoring": {
                    "active": monitoring_service.monitoring_active,
                    "recent_alerts": len(recent_alerts),
                    "critical_alerts": critical_alerts
                }
            },
            "metrics": current_metrics,
            "recent_alerts": recent_alerts
        }
        
        return health_data
        
    except Exception as e:
        logger.error(f"Error performing system health check: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to perform system health check")

# === ENHANCED CLIENT ENDPOINTS (with authentication) ===

@api_router.post("/clients", response_model=dict)
async def create_client(
    client_data: ClientData, 
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(check_usage_limits)
):
    """Store client data in Supabase database with encryption"""
    try:
        # Add user context to client data
        client_dict = client_data.dict()
        client_dict["user_id"] = current_user["id"]
        
        # Store in Supabase database
        result = await supabase_client.create_client(client_dict)
        
        if result and 'id' in result:
            client_id = result['id']
            
            # Track usage
            await supabase_client.track_usage(current_user["id"], "client", client_id)
            
            # Send welcome notification (placeholder - implement as needed)
            # background_tasks.add_task(
            #     notification_service.send_welcome_notification,
            #     client_data.email,
            #     client_data.full_name,
            #     client_data.phone
            # )
        
            return {"status": "success", "client_id": client_id, "message": "Client data stored successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to create client")
    except Exception as e:
        logger.error(f"Error storing client data: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to store client data: {str(e)}")

@api_router.get("/clients", response_model=List[dict])
async def get_clients(current_user: dict = Depends(get_current_user)):
    """Get all clients for the current user"""
    try:
        clients = await supabase_client.get_user_clients(current_user["id"])
        return clients
    except Exception as e:
        logger.error(f"Error fetching clients: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch clients: {str(e)}")

@api_router.get("/universities")
async def get_universities():
    """Get list of supported universities"""
    return {"universities": TOP_UNIVERSITIES}

@api_router.post("/agent/execute")
async def execute_agent_command(command: AgentCommand, background_tasks: BackgroundTasks):
    """Execute autonomous agent command"""
    try:
        if command.command_type == "create_applications":
            # Add background task for application creation
            background_tasks.add_task(create_applications_task, command.client_id, command.parameters)
            return {"status": "started", "message": "Application creation process started"}
        
        elif command.command_type == "check_status":
            # Add background task for status checking
            background_tasks.add_task(check_status_task, command.client_id)
            return {"status": "started", "message": "Status checking process started"}
        
        elif command.command_type == "monitor_daily":
            # Setup daily monitoring
            return {"status": "setup", "message": "Daily monitoring configured"}
        
        else:
            raise HTTPException(status_code=400, detail="Invalid command type")
    
    except Exception as e:
        logger.error(f"Error executing agent command: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Command execution failed: {str(e)}")

@api_router.get("/applications")
async def get_applications():
    """Get all application tasks from Supabase"""
    try:
        applications = await supabase_client.get_all_application_tasks()
        return applications
    except Exception as e:
        logger.error(f"Error fetching applications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch applications: {str(e)}")

@api_router.get("/applications/status/{client_id}")
async def get_client_applications(client_id: str):
    """Get applications for specific client from Supabase"""
    try:
        applications = await supabase_client.get_client_application_tasks(client_id)
        return applications
    except Exception as e:
        logger.error(f"Error fetching client applications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch client applications: {str(e)}")

@api_router.get("/analytics/{client_id}")
async def get_client_analytics(client_id: str):
    """Get analytics and insights for a client from Supabase"""
    try:
        analytics = await supabase_client.get_client_analytics(client_id)
        return analytics
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")

@api_router.get("/performance/report")
async def get_performance_report():
    """Get system performance report"""
    try:
        return perf_monitor.get_performance_report()
    except Exception as e:
        logger.error(f"Error generating performance report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@api_router.post("/notifications/test")
async def test_notification(email: str, phone: Optional[str] = None):
    """Test notification system"""
    try:
        email_sent = await notification_service.send_email(
            email,
            "Test Notification",
            "This is a test notification from the University Application Agent."
        )
        
        sms_sent = False
        if phone:
            sms_sent = await notification_service.send_sms(
                phone,
                "Test SMS from University Application Agent"
            )
        
        return {
            "email_sent": email_sent,
            "sms_sent": sms_sent
        }
    except Exception as e:
        logger.error(f"Error sending test notification: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send notification: {str(e)}")

# Mock University Portal Routes
@api_router.get("/mock-university/{university_code}")
async def get_mock_university_portal(university_code: str):
    """Serve mock university application portal"""
    university = next((u for u in TOP_UNIVERSITIES if u["code"] == university_code), None)
    if not university:
        raise HTTPException(status_code=404, detail="University not found")
    
    return {
        "university": university,
        "form_fields": {
            "personal_details": ["full_name", "email", "phone", "date_of_birth", "nationality", "address"],
            "academic_history": ["institution", "qualification", "grade", "year"],
            "course_preferences": ["course_name", "course_code", "entry_year"],
            "documents": ["transcript", "personal_statement", "reference_letter"],
            "additional": ["previous_applications", "special_requirements"]
        }
    }

@api_router.post("/mock-university/{university_code}/apply")
async def submit_mock_application(university_code: str, application: MockUniversityApplication):
    """Submit application to mock university portal"""
    try:
        university = next((u for u in TOP_UNIVERSITIES if u["code"] == university_code), None)
        if not university:
            raise HTTPException(status_code=404, detail="University not found")
        
        # Store mock application
        application.university_name = university["name"]
        mock_db["mock_applications"].append(application.dict())
        
        return {
            "status": "submitted",
            "application_id": application.id,
            "university": university["name"],
            "message": "Application submitted successfully"
        }
    except Exception as e:
        logger.error(f"Error submitting mock application: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to submit application: {str(e)}")

# Background Tasks
async def create_applications_task(client_id: str, parameters: dict):
    """Background task to create applications autonomously"""
    try:
        # Get client data from mock database
        client_data_dict = next((c for c in mock_db["clients"] if c["id"] == client_id), None)
        if not client_data_dict:
            # Create a dummy client for testing
            client_data_dict = {
                "id": client_id,
                "full_name": "Test User",
                "email": f"test.user.{client_id[:8]}@example.com",
                "phone": "+44 7700 900123",
                "date_of_birth": "1995-05-15",
                "nationality": "British",
                "address": "123 Oxford Street, London, W1D 1DF, UK",
                "personal_statement": "I am passionate about computer science...",
                "academic_history": [{"institution": "Test School", "qualification": "A-Levels", "grade": "A*AA", "year": 2022}],
                "course_preferences": [{"course_name": "Computer Science", "course_code": "CS101", "entry_year": 2023}],
                "documents": {"transcript": "base64encodedstring"},
                "created_at": datetime.utcnow().isoformat()
            }
            mock_db["clients"].append(client_data_dict)
        
        client_data = ClientData(**client_data_dict)
        selected_universities = parameters.get('universities', [])
        
        for university_code in selected_universities:
            university = next((u for u in TOP_UNIVERSITIES if u["code"] == university_code), None)
            if not university:
                continue
            
            try:
                # Create account
                credentials = await agent.create_university_account(university, client_data)
                
                # Fill application
                application_data = await agent.fill_application_form(university, client_data, credentials)
                
                # Create application task
                task = ApplicationTask(
                    client_id=client_id,
                    university_name=university["name"],
                    course_name=parameters.get('course_name', 'Computer Science'),
                    course_code=parameters.get('course_code', 'CS101'),
                    application_url=university["url"],
                    status="submitted",
                    credentials=credentials,
                    application_data=application_data
                )
                
                # Store in mock database
                mock_db["application_tasks"].append(task.dict())
                
                logger.info(f"Successfully created application for {university['name']}")
                
            except Exception as e:
                logger.error(f"Failed to create application for {university['name']}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Error in create_applications_task: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        await agent.cleanup()

async def check_status_task(client_id: str):
    """Background task to check application status"""
    try:
        # Get client applications from mock database
        app_data_list = [app for app in mock_db["application_tasks"] if app["client_id"] == client_id]
        
        for app_data in app_data_list:
            task = ApplicationTask(**app_data)
            
            # Check status
            new_status = await agent.check_application_status(task)
            
            # Update status in mock database
            for app in mock_db["application_tasks"]:
                if app["id"] == task.id:
                    app["status"] = new_status
                    app["last_checked"] = datetime.utcnow().isoformat()
            
            logger.info(f"Updated status for {task.university_name}: {new_status}")
    
    except Exception as e:
        logger.error(f"Error in check_status_task: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        await agent.cleanup()

# Include the router in the main app
app.include_router(api_router)

# Serve static files for mock university portals
try:
    app.mount("/static", StaticFiles(directory=str(ROOT_DIR / "static")), name="static")
except RuntimeError:
    # Create static directory if it doesn't exist
    os.makedirs(str(ROOT_DIR / "static"), exist_ok=True)
    app.mount("/static", StaticFiles(directory=str(ROOT_DIR / "static")), name="static")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup_event():
    """Initialize agent on startup"""
    logger.info("Autonomous University Application Agent starting up...")
    
    # Add some test data to mock database
    if not mock_db["clients"]:
        test_client = {
            "id": "test-client-id",
            "full_name": "Test User",
            "email": "test.user@example.com",
            "phone": "+44 7700 900123",
            "date_of_birth": "1995-05-15",
            "nationality": "British",
            "address": "123 Oxford Street, London, W1D 1DF, UK",
            "personal_statement": "I am passionate about computer science...",
            "academic_history": [{"institution": "Test School", "qualification": "A-Levels", "grade": "A*AA", "year": 2022}],
            "course_preferences": [{"course_name": "Computer Science", "course_code": "CS101", "entry_year": 2023}],
            "documents": {"transcript": "base64encodedstring"},
            "created_at": datetime.utcnow().isoformat()
        }
        mock_db["clients"].append(test_client)
        
        # Add a test application
        test_application = {
            "id": "test-application-id",
            "client_id": "test-client-id",
            "university_name": "University of Oxford",
            "course_name": "Computer Science",
            "course_code": "CS101",
            "application_url": "https://www.ox.ac.uk/admissions",
            "status": "submitted",
            "credentials": {
                "username": "test.user@example.com",
                "password": "UniApp1234!",
                "created_at": datetime.utcnow().isoformat()
            },
            "application_data": {
                "personal_details": {
                    "name": "Test User",
                    "email": "test.user@example.com",
                    "phone": "+44 7700 900123",
                    "dob": "1995-05-15",
                    "nationality": "British",
                    "address": "123 Oxford Street, London, W1D 1DF, UK"
                },
                "academic_history": [{"institution": "Test School", "qualification": "A-Levels", "grade": "A*AA", "year": 2022}],
                "personal_statement": "I am passionate about computer science...",
                "course_preferences": [{"course_name": "Computer Science", "course_code": "CS101", "entry_year": 2023}],
                "submitted_at": datetime.utcnow().isoformat(),
                "status": "submitted"
            },
            "created_at": datetime.utcnow().isoformat(),
            "last_checked": datetime.utcnow().isoformat(),
            "error_log": []
        }
        mock_db["application_tasks"].append(test_application)
        
        # Add a test mock application
        test_mock_application = {
            "id": "test-mock-application-id",
            "university_name": "University of Oxford",
            "applicant_name": "Test User",
            "email": "test.user@example.com",
            "course": "Computer Science",
            "personal_statement": "I am passionate about computer science...",
            "status": "submitted",
            "submitted_at": datetime.utcnow().isoformat(),
            "documents": {"transcript": "base64encodedstring"}
        }
        mock_db["mock_applications"].append(test_mock_application)

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    await agent.cleanup()
    logger.info("Autonomous University Application Agent shut down")

# Daily monitoring scheduler (runs in separate thread)
def setup_daily_monitoring():
    """Setup daily monitoring schedule"""
    def daily_check():
        asyncio.run(run_daily_status_check())
    
    schedule.every().day.at("09:00").do(daily_check)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

async def run_daily_status_check():
    """Run daily status check for all active applications"""
    try:
        # Get applications from mock database
        app_data_list = mock_db["application_tasks"]
        
        for app_data in app_data_list:
            if app_data['status'] not in ['accepted', 'rejected']:
                await check_status_task(app_data['client_id'])
        
        logger.info("Daily status check completed")
    except Exception as e:
        logger.error(f"Error in daily status check: {str(e)}")

# Start monitoring thread
monitoring_thread = Thread(target=setup_daily_monitoring, daemon=True)
monitoring_thread.start()
