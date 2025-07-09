"""
Eko Automation API Routes

Provides endpoints for creating and managing AI-powered automation workflows
using the Eko framework for university application automation.
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import logging

from services.eko_automation_service import eko_service
from security.auth import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/eko", tags=["Eko Automation"])

# Pydantic models for request/response
class AutomationWorkflowRequest(BaseModel):
    task_description: str = Field(..., description="Natural language description of the automation task")
    client_data: Optional[Dict] = Field(None, description="Client information for form filling")
    university_data: Optional[Dict] = Field(None, description="University-specific requirements")
    documents: Optional[List[str]] = Field(None, description="List of document paths")

class UniversityApplicationRequest(BaseModel):
    university_name: str = Field(..., description="Name of the university")
    application_url: str = Field(..., description="URL of the application portal")
    client_profile: Dict = Field(..., description="Client's profile information")
    documents: List[str] = Field(..., description="List of required documents")

class ApplicationMonitoringRequest(BaseModel):
    applications: List[Dict] = Field(..., description="List of applications to monitor")

class DocumentPreparationRequest(BaseModel):
    required_documents: List[str] = Field(..., description="List of required document types")
    client_documents: Dict[str, str] = Field(..., description="Mapping of document types to file paths")

class AutomationResponse(BaseModel):
    success: bool
    workflow_id: Optional[str] = None
    result: Optional[str] = None
    steps_completed: List[str] = []
    execution_time: Optional[int] = None
    error: Optional[str] = None
    metadata: Dict = {}

@router.post("/initialize", response_model=Dict[str, Any])
async def initialize_eko_environment(current_user: dict = Depends(get_current_user)):
    """Initialize Eko automation environment"""
    try:
        success = await eko_service.initialize_eko_environment()
        
        if success:
            return {
                "success": True,
                "message": "Eko environment initialized successfully",
                "capabilities": [
                    "University application automation",
                    "Multi-step workflow creation",
                    "Document processing",
                    "Application status monitoring",
                    "Browser automation"
                ]
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to initialize Eko environment")
            
    except Exception as e:
        logger.error(f"Error initializing Eko environment: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Initialization error: {str(e)}")

@router.post("/workflow/create", response_model=AutomationResponse)
async def create_automation_workflow(
    request: AutomationWorkflowRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Create and execute a custom automation workflow using natural language"""
    try:
        logger.info(f"Creating automation workflow for user {current_user.get('email')}")
        
        result = await eko_service.create_automation_workflow(
            task_description=request.task_description,
            client_data=request.client_data,
            university_data=request.university_data,
            documents=request.documents
        )
        
        # Log workflow creation
        background_tasks.add_task(
            log_workflow_activity,
            user_id=current_user.get("id"),
            workflow_type="custom",
            task_description=request.task_description,
            result=result
        )
        
        return AutomationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error creating automation workflow: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Workflow creation error: {str(e)}")

@router.post("/university/apply", response_model=AutomationResponse)
async def automate_university_application(
    request: UniversityApplicationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Automate university application process using Eko"""
    try:
        logger.info(f"Starting university application automation for {request.university_name}")
        
        result = await eko_service.university_application_automation(
            university_name=request.university_name,
            application_url=request.application_url,
            client_profile=request.client_profile,
            documents=request.documents
        )
        
        # Log application automation
        background_tasks.add_task(
            log_workflow_activity,
            user_id=current_user.get("id"),
            workflow_type="university_application",
            task_description=f"University application: {request.university_name}",
            result=result
        )
        
        return AutomationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in university application automation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Application automation error: {str(e)}")

@router.post("/applications/monitor", response_model=AutomationResponse)
async def monitor_application_status(
    request: ApplicationMonitoringRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Monitor status of multiple university applications"""
    try:
        logger.info(f"Starting application status monitoring for {len(request.applications)} applications")
        
        result = await eko_service.monitor_application_status(
            applications=request.applications
        )
        
        # Log monitoring activity
        background_tasks.add_task(
            log_workflow_activity,
            user_id=current_user.get("id"),
            workflow_type="application_monitoring",
            task_description=f"Monitoring {len(request.applications)} applications",
            result=result
        )
        
        return AutomationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in application monitoring: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Monitoring error: {str(e)}")

@router.post("/documents/prepare", response_model=AutomationResponse)
async def prepare_documents(
    request: DocumentPreparationRequest,
    background_tasks: BackgroundTasks,
    current_user: dict = Depends(get_current_user)
):
    """Automate document preparation and formatting"""
    try:
        logger.info(f"Starting document preparation for {len(request.required_documents)} document types")
        
        result = await eko_service.document_preparation_workflow(
            required_documents=request.required_documents,
            client_documents=request.client_documents
        )
        
        # Log document preparation
        background_tasks.add_task(
            log_workflow_activity,
            user_id=current_user.get("id"),
            workflow_type="document_preparation",
            task_description=f"Document preparation: {', '.join(request.required_documents)}",
            result=result
        )
        
        return AutomationResponse(**result)
        
    except Exception as e:
        logger.error(f"Error in document preparation: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Document preparation error: {str(e)}")

@router.get("/capabilities", response_model=Dict[str, Any])
async def get_eko_capabilities(current_user: dict = Depends(get_current_user)):
    """Get available Eko automation capabilities"""
    return {
        "framework": "Eko v1.0",
        "agents": [
            {
                "name": "BrowserAgent",
                "description": "Web automation and form filling",
                "capabilities": [
                    "Navigate to websites",
                    "Fill forms automatically",
                    "Upload documents",
                    "Take screenshots",
                    "Extract page content"
                ]
            },
            {
                "name": "FileAgent",
                "description": "Document management and processing",
                "capabilities": [
                    "Read and write files",
                    "Document conversion",
                    "File organization",
                    "Backup creation"
                ]
            }
        ],
        "workflow_types": [
            {
                "type": "university_application",
                "description": "Complete university application automation",
                "estimated_time": "15-30 minutes per application"
            },
            {
                "type": "application_monitoring",
                "description": "Monitor multiple application statuses",
                "estimated_time": "5-10 minutes per check"
            },
            {
                "type": "document_preparation",
                "description": "Prepare and format documents",
                "estimated_time": "10-15 minutes"
            },
            {
                "type": "custom_workflow",
                "description": "Natural language to automation workflow",
                "estimated_time": "Variable based on complexity"
            }
        ],
        "supported_universities": [
            "Oxford University",
            "Cambridge University",
            "Imperial College London",
            "UCL",
            "King's College London",
            "Edinburgh University",
            "Manchester University",
            "And many more..."
        ]
    }

@router.get("/workflows/history", response_model=List[Dict[str, Any]])
async def get_workflow_history(
    limit: int = 50,
    offset: int = 0,
    current_user: dict = Depends(get_current_user)
):
    """Get user's workflow execution history"""
    try:
        # This would typically fetch from database
        # For now, return mock data
        return [
            {
                "id": "wf_001",
                "type": "university_application",
                "description": "Oxford University Computer Science Application",
                "status": "completed",
                "created_at": "2024-01-15T10:30:00Z",
                "execution_time": 1800,
                "result": "Application submitted successfully"
            },
            {
                "id": "wf_002", 
                "type": "application_monitoring",
                "description": "Monitor 5 university applications",
                "status": "completed",
                "created_at": "2024-01-14T16:45:00Z",
                "execution_time": 600,
                "result": "All applications checked, 2 updates found"
            }
        ]
        
    except Exception as e:
        logger.error(f"Error fetching workflow history: {str(e)}")
        raise HTTPException(status_code=500, detail=f"History fetch error: {str(e)}")

async def log_workflow_activity(
    user_id: str,
    workflow_type: str,
    task_description: str,
    result: Dict[str, Any]
):
    """Background task to log workflow activity"""
    try:
        # Implementation would log to database
        logger.info(f"Workflow logged - User: {user_id}, Type: {workflow_type}, Success: {result.get('success')}")
    except Exception as e:
        logger.error(f"Error logging workflow activity: {str(e)}") 