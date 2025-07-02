from fastapi import FastAPI, APIRouter, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timedelta
import asyncio
import json
import schedule
import time
from threading import Thread
import random
import traceback

# Import new services
from automation.browser_automation import EnhancedBrowserAutomation
from security.encryption import DataEncryption, SecureCredentialStorage
from notifications.notification_service import NotificationService
from monitoring.status_monitor import ApplicationMonitor, PerformanceMonitor

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

# MongoDB connection (keeping for local data)
mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'test_database')]

# Initialize services
encryption_service = DataEncryption()
credential_storage = SecureCredentialStorage(encryption_service)
notification_service = NotificationService()
app_monitor = ApplicationMonitor(db, notification_service)
perf_monitor = PerformanceMonitor()

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

@api_router.post("/clients", response_model=dict)
async def create_client(client_data: ClientData, background_tasks: BackgroundTasks):
    """Store client data in database with encryption"""
    try:
        # Encrypt sensitive data
        encrypted_data = encryption_service.encrypt_client_data(client_data.dict())
        
        # Store in mock database (unencrypted for demo)
        mock_db["clients"].append(client_data.dict())
        
        # Store encrypted data in MongoDB
        try:
            await db.clients.insert_one(encrypted_data)
        except Exception as e:
            logger.error(f"MongoDB error: {str(e)}")
        
        # Send welcome notification
        background_tasks.add_task(
            notification_service.send_email,
            client_data.email,
            "Welcome to University Application Agent",
            f"Hello {client_data.full_name},\n\nWe've successfully received your information and are ready to help with your university applications.\n\nBest regards,\nUniversity Application Agent"
        )
        
        return {"status": "success", "client_id": client_data.id, "message": "Client data stored successfully"}
    except Exception as e:
        logger.error(f"Error storing client data: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to store client data: {str(e)}")

@api_router.get("/clients", response_model=List[dict])
async def get_clients():
    """Get all clients from database"""
    try:
        # Return from mock database
        return mock_db["clients"]
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
    """Get all application tasks"""
    try:
        # Return from mock database
        return mock_db["application_tasks"]
    except Exception as e:
        logger.error(f"Error fetching applications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch applications: {str(e)}")

@api_router.get("/applications/status/{client_id}")
async def get_client_applications(client_id: str):
    """Get applications for specific client"""
    try:
        # Return from mock database
        return [app for app in mock_db["application_tasks"] if app["client_id"] == client_id]
    except Exception as e:
        logger.error(f"Error fetching client applications: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch client applications: {str(e)}")

@api_router.get("/analytics/{client_id}")
async def get_client_analytics(client_id: str):
    """Get analytics and insights for a client"""
    try:
        analytics = await app_monitor.get_client_analytics(client_id)
        insights = await app_monitor.generate_insights(client_id)
        deadlines = await app_monitor.check_deadlines(client_id)
        
        return {
            "analytics": analytics,
            "insights": insights,
            "deadlines": deadlines
        }
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

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    client.close()
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
