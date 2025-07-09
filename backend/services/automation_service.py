"""
Automation Service for AI LAM

Enhanced automation service following Suna's patterns for browser automation and task execution.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from services.database_service import get_database_service
from services.llm_service import get_llm_service
from utils.config import get_config

logger = logging.getLogger(__name__)

class AutomationError(Exception):
    """Base exception for automation-related errors."""
    pass

class AutomationService:
    """Enhanced automation service with AI-powered capabilities."""
    
    def __init__(self):
        self.config = get_config()
        self.db_service = get_database_service()
        self.llm_service = get_llm_service()
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the automation service."""
        if self._initialized:
            return
        
        try:
            # Ensure dependencies are initialized
            await self.db_service.initialize()
            
            self._initialized = True
            logger.info("Automation service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize automation service: {e}")
            raise AutomationError(f"Automation service initialization failed: {str(e)}")
    
    async def execute_automation_task(
        self,
        task_type: str,
        task_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Execute an automation task.
        
        Args:
            task_type: Type of automation task
            task_data: Task configuration and data
            user_id: User executing the task
        
        Returns:
            Dict containing task execution results
        """
        if not self._initialized:
            await self.initialize()
        
        start_time = datetime.now(timezone.utc)
        
        try:
            logger.info(f"Starting automation task: {task_type} for user {user_id}")
            
            # Log automation start
            automation_log = await self.db_service.log_automation_run({
                'user_id': user_id,
                'task_type': task_type,
                'status': 'running',
                'started_at': start_time.isoformat(),
                'task_data': task_data
            })
            
            # Execute based on task type
            if task_type == 'application_filling':
                result = await self._execute_application_filling(task_data, user_id)
            elif task_type == 'document_processing':
                result = await self._execute_document_processing(task_data, user_id)
            elif task_type == 'form_automation':
                result = await self._execute_form_automation(task_data, user_id)
            else:
                raise AutomationError(f"Unknown task type: {task_type}")
            
            # Update automation log with success
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            await self.db_service.client.table('automation_logs').update({
                'status': 'completed',
                'completed_at': end_time.isoformat(),
                'duration': duration,
                'result': result
            }).eq('id', automation_log['id']).execute()
            
            logger.info(f"Automation task {task_type} completed successfully in {duration:.2f}s")
            
            return {
                'success': True,
                'task_type': task_type,
                'duration': duration,
                'result': result,
                'automation_id': automation_log['id']
            }
            
        except Exception as e:
            # Log automation failure
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            if 'automation_log' in locals():
                await self.db_service.client.table('automation_logs').update({
                    'status': 'failed',
                    'completed_at': end_time.isoformat(),
                    'duration': duration,
                    'error': str(e)
                }).eq('id', automation_log['id']).execute()
            
            logger.error(f"Automation task {task_type} failed: {e}")
            raise AutomationError(f"Task execution failed: {str(e)}")
    
    async def _execute_application_filling(
        self,
        task_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """Execute application filling automation."""
        try:
            application_url = task_data.get('url')
            user_data = task_data.get('user_data', {})
            
            if not application_url:
                raise AutomationError("Application URL is required")
            
            # Use AI to analyze the form and generate filling strategy
            form_analysis_prompt = f"""
            Analyze this application form URL and user data to create an automation strategy:
            
            URL: {application_url}
            User Data: {user_data}
            
            Provide a step-by-step automation plan including:
            1. Form field identification
            2. Data mapping strategy
            3. Validation requirements
            4. Submission process
            """
            
            analysis = await self.llm_service.generate_response(
                prompt=form_analysis_prompt,
                system_prompt="You are an expert automation engineer specializing in form filling."
            )
            
            # TODO: Implement actual browser automation
            # This would integrate with your existing browser automation modules
            
            return {
                'url': application_url,
                'analysis': analysis,
                'status': 'analyzed',
                'fields_identified': True,
                'ready_for_execution': True
            }
            
        except Exception as e:
            logger.error(f"Application filling failed: {e}")
            raise AutomationError(f"Application filling failed: {str(e)}")
    
    async def _execute_document_processing(
        self,
        task_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """Execute document processing automation."""
        try:
            document_path = task_data.get('document_path')
            processing_type = task_data.get('processing_type', 'extract')
            
            if not document_path:
                raise AutomationError("Document path is required")
            
            # Use AI to process document
            processing_prompt = f"""
            Process this document for automation purposes:
            
            Document: {document_path}
            Processing Type: {processing_type}
            
            Extract relevant information that can be used for form filling or data entry.
            """
            
            processing_result = await self.llm_service.generate_response(
                prompt=processing_prompt,
                system_prompt="You are an expert document processor and data extractor."
            )
            
            return {
                'document_path': document_path,
                'processing_type': processing_type,
                'extracted_data': processing_result,
                'status': 'processed'
            }
            
        except Exception as e:
            logger.error(f"Document processing failed: {e}")
            raise AutomationError(f"Document processing failed: {str(e)}")
    
    async def _execute_form_automation(
        self,
        task_data: Dict[str, Any],
        user_id: str
    ) -> Dict[str, Any]:
        """Execute form automation."""
        try:
            form_url = task_data.get('url')
            form_data = task_data.get('form_data', {})
            automation_config = task_data.get('config', {})
            
            if not form_url:
                raise AutomationError("Form URL is required")
            
            # Generate automation strategy
            strategy_prompt = f"""
            Create a form automation strategy:
            
            Form URL: {form_url}
            Form Data: {form_data}
            Config: {automation_config}
            
            Provide specific automation steps and error handling.
            """
            
            strategy = await self.llm_service.generate_response(
                prompt=strategy_prompt,
                system_prompt="You are an expert form automation specialist."
            )
            
            return {
                'form_url': form_url,
                'strategy': strategy,
                'data_mapped': True,
                'automation_ready': True,
                'status': 'strategy_generated'
            }
            
        except Exception as e:
            logger.error(f"Form automation failed: {e}")
            raise AutomationError(f"Form automation failed: {str(e)}")
    
    async def get_automation_history(
        self,
        user_id: str,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get automation history for a user."""
        try:
            return await self.db_service.get_automation_history(user_id, limit)
        except Exception as e:
            logger.error(f"Error getting automation history: {e}")
            raise AutomationError(f"Failed to get automation history: {str(e)}")
    
    async def cancel_automation(
        self,
        automation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Cancel a running automation."""
        try:
            # Update automation status
            result = await self.db_service.client.table('automation_logs').update({
                'status': 'cancelled',
                'completed_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', automation_id).eq('user_id', user_id).execute()
            
            if not result.data:
                raise AutomationError(f"Automation {automation_id} not found or access denied")
            
            logger.info(f"Cancelled automation {automation_id} for user {user_id}")
            
            return {
                'success': True,
                'automation_id': automation_id,
                'status': 'cancelled'
            }
            
        except Exception as e:
            logger.error(f"Error cancelling automation: {e}")
            raise AutomationError(f"Failed to cancel automation: {str(e)}")

# Global instance
_automation_service = None

def get_automation_service() -> AutomationService:
    """Get or create the global automation service instance."""
    global _automation_service
    if _automation_service is None:
        _automation_service = AutomationService()
    return _automation_service 