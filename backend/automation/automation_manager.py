"""
Enhanced Automation Manager
Coordinates form automation tasks and manages browser sessions
"""

import asyncio
import uuid
import logging
import json
import base64
from datetime import datetime
from typing import Dict, Any, Optional, List

from .intelligent_automation import IntelligentFormAutomation
from .data_parser import DataParser
from database.supabase_client import get_supabase_client
from security.encryption import encrypt_data, decrypt_data

logger = logging.getLogger(__name__)

class AutomationManager:
    """Manages automation sessions and coordinates tasks"""
    
    def __init__(self):
        self.sessions: Dict[str, Any] = {}
        self.data_parser = DataParser()
        self.db_client = get_supabase_client()
    
    async def create_automation_session(self, 
                                      user_id: str,
                                      target_url: str,
                                      file_data: Optional[Dict[str, Any]] = None,
                                      user_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new automation session
        
        Args:
            user_id: ID of the user initiating the automation
            target_url: URL of the website to automate
            file_data: Uploaded file data (content, type, filename)
            user_data: Direct user data if no file provided
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        
        # Parse data from file if provided
        parsed_data = []
        if file_data:
            try:
                parsed_data = await self.data_parser.parse_file(
                    file_data['content'],
                    file_data['type'],
                    file_data.get('filename', '')
                )
            except Exception as e:
                logger.error(f"Failed to parse file: {str(e)}")
                raise
        elif user_data:
            parsed_data = [user_data]
        
        if not parsed_data:
            raise ValueError("No data provided for automation")
        
        # Create session
        session = {
            'id': session_id,
            'user_id': user_id,
            'target_url': target_url,
            'data': parsed_data,
            'status': 'initialized',
            'created_at': datetime.utcnow().isoformat(),
            'automation_engine': None,
            'results': [],
            'progress': 0
        }
        
        self.sessions[session_id] = session
        
        # Store session in database
        await self._store_session(session)
        
        return session_id

    async def start_automation(self, session_id: str, progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Start the automation process for a session
        
        Args:
            session_id: ID of the automation session
            progress_callback: Callback for progress updates
            
        Returns:
            Automation results
        """
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session['status'] != 'initialized':
            raise ValueError(f"Session {session_id} is not in initialized state")
        
        # Update status
        session['status'] = 'running'
        session['started_at'] = datetime.utcnow().isoformat()
        
        # Create automation engine
        automation_engine = IntelligentFormAutomation()
        session['automation_engine'] = automation_engine
        
        try:
            # Initialize browser
            await automation_engine.initialize_stealth_browser()
            
            # Process each data record
            results = []
            total_records = len(session['data'])
            
            for i, data_record in enumerate(session['data']):
                # Update progress
                base_progress = (i * 100) // total_records
                
                # Create a wrapped progress callback
                async def wrapped_progress(update):
                    record_progress = base_progress + (update['progress'] // total_records)
                    session['progress'] = record_progress
                    
                    if progress_callback:
                        await progress_callback({
                            'session_id': session_id,
                            'record': i + 1,
                            'total_records': total_records,
                            'progress': record_progress,
                            'status': update['status'],
                            'timestamp': update['timestamp']
                        })
                
                # Run automation for this record
                result = await automation_engine.automate_form_filling(
                    session['target_url'],
                    data_record,
                    session_id,
                    wrapped_progress
                )
                
                # Store result
                result['record_index'] = i
                result['data_used'] = data_record
                results.append(result)
                
                # Store result in database
                await self._store_automation_result(session_id, result)
                
                # Add delay between records to avoid rate limiting
                if i < total_records - 1:
                    await asyncio.sleep(2)
            
            # Update session
            session['status'] = 'completed'
            session['completed_at'] = datetime.utcnow().isoformat()
            session['results'] = results
            session['progress'] = 100
            
            # Calculate summary
            success_count = sum(1 for r in results if r['success'])
            session['summary'] = {
                'total_records': total_records,
                'successful': success_count,
                'failed': total_records - success_count,
                'fields_filled': sum(r.get('fields_filled', 0) for r in results)
            }
            
            # Update database
            await self._update_session_status(session)
            
            return {
                'session_id': session_id,
                'status': 'completed',
                'summary': session['summary'],
                'results': results
            }
            
        except Exception as e:
            logger.error(f"Automation error for session {session_id}: {str(e)}")
            session['status'] = 'failed'
            session['error'] = str(e)
            session['failed_at'] = datetime.utcnow().isoformat()
            
            await self._update_session_status(session)
            
            raise
            
        finally:
            # Clean up browser
            if automation_engine and automation_engine.browser:
                await automation_engine.cleanup()
            
            # Remove engine reference to free memory
            if 'automation_engine' in session:
                del session['automation_engine']
    
    async def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get the current status of an automation session"""
        session = self.sessions.get(session_id)
        if not session:
            # Try to load from database
            session = await self._load_session(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
        
        # Don't include the automation engine in the response
        status = {k: v for k, v in session.items() if k != 'automation_engine'}
        
        return status
    
    async def get_session_screenshots(self, session_id: str) -> List[Dict[str, Any]]:
        """Get all screenshots from a session"""
        session = await self.get_session_status(session_id)
        
        screenshots = []
        for result in session.get('results', []):
            screenshots.extend(result.get('screenshots', []))
        
        return screenshots
    
    async def cancel_session(self, session_id: str) -> bool:
        """Cancel a running automation session"""
        session = self.sessions.get(session_id)
        if not session:
            return False
        
        if session['status'] == 'running':
            session['status'] = 'cancelled'
            session['cancelled_at'] = datetime.utcnow().isoformat()
            
            # Clean up browser if running
            if 'automation_engine' in session and session['automation_engine']:
                await session['automation_engine'].cleanup()
            
            await self._update_session_status(session)
            return True
        
        return False
    
    async def cleanup_old_sessions(self, hours: int = 24):
        """Clean up sessions older than specified hours"""
        cutoff_time = datetime.utcnow().timestamp() - (hours * 3600)
        
        sessions_to_remove = []
        for session_id, session in self.sessions.items():
            created_at = datetime.fromisoformat(session['created_at'].replace('Z', '+00:00'))
            if created_at.timestamp() < cutoff_time:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            del self.sessions[session_id]
        
        logger.info(f"Cleaned up {len(sessions_to_remove)} old sessions")
    
    # Database operations
    
    async def _store_session(self, session: Dict[str, Any]):
        """Store session in database"""
        try:
            # Encrypt sensitive data
            encrypted_data = encrypt_data(json.dumps(session['data']))
            
            record = {
                'id': session['id'],
                'user_id': session['user_id'],
                'target_url': session['target_url'],
                'encrypted_data': encrypted_data,
                'status': session['status'],
                'created_at': session['created_at']
            }
            
            self.db_client.table('automation_sessions').insert(record).execute()
                
        except Exception as e:
            logger.error(f"Failed to store session: {str(e)}")
    
    async def _update_session_status(self, session: Dict[str, Any]):
        """Update session status in database"""
        try:
            update_data = {
                'status': session['status'],
                'progress': session.get('progress', 0)
            }
            
            if 'summary' in session:
                update_data['summary'] = json.dumps(session['summary'])
            
            if 'error' in session:
                update_data['error'] = session['error']
            
            if 'completed_at' in session:
                update_data['completed_at'] = session['completed_at']
            
            self.db_client.table('automation_sessions').update(
                update_data
            ).eq('id', session['id']).execute()
            
        except Exception as e:
            logger.error(f"Failed to update session status: {str(e)}")
    
    async def _store_automation_result(self, session_id: str, result: Dict[str, Any]):
        """Store automation result in database"""
        try:
            # Prepare result for storage
            stored_result = {
                'session_id': session_id,
                'record_index': result.get('record_index', 0),
                'success': result.get('success', False),
                'fields_filled': result.get('fields_filled', 0),
                'forms_detected': result.get('forms_detected', 0)
            }
            
            # Store screenshots separately
            if 'screenshots' in result:
                screenshot_ids = []
                for screenshot in result['screenshots']:
                    screenshot_record = {
                        'session_id': session_id,
                        'name': screenshot['name'],
                        'timestamp': screenshot['timestamp'],
                        'data': screenshot['data']
                    }
                    
                    response = self.db_client.table('automation_screenshots').insert(
                        screenshot_record
                    ).execute()
                    
                    if response.data:
                        screenshot_ids.append(response.data[0]['id'])
                
                stored_result['screenshot_ids'] = screenshot_ids
            
            # Store log
            if 'log' in result:
                stored_result['log'] = json.dumps(result['log'])
            
            # Store errors
            if 'errors' in result:
                stored_result['errors'] = json.dumps(result['errors'])
            
            self.db_client.table('automation_results').insert(stored_result).execute()
            
        except Exception as e:
            logger.error(f"Failed to store automation result: {str(e)}")
    
    async def _load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load session from database"""
        try:
            response = self.db_client.table('automation_sessions').select('*').eq(
                'id', session_id
            ).execute()
            
            if not response.data:
                return None
            
            record = response.data[0]
            
            # Decrypt data
            decrypted_data = json.loads(decrypt_data(record['encrypted_data']))
            
            session = {
                'id': record['id'],
                'user_id': record['user_id'],
                'target_url': record['target_url'],
                'data': decrypted_data,
                'status': record['status'],
                'created_at': record['created_at'],
                'progress': record.get('progress', 0)
            }
            
            if record.get('summary'):
                session['summary'] = json.loads(record['summary'])
            
            if record.get('error'):
                session['error'] = record['error']
            
            if record.get('completed_at'):
                session['completed_at'] = record['completed_at']
            
            # Load results
            results_response = self.db_client.table('automation_results').select('*').eq(
                'session_id', session_id
            ).order('record_index').execute()
            
            if results_response.data:
                session['results'] = []
                for result_record in results_response.data:
                    result = {
                        'record_index': result_record['record_index'],
                        'success': result_record['success'],
                        'fields_filled': result_record['fields_filled'],
                        'forms_detected': result_record['forms_detected']
                    }
                    
                    if result_record.get('log'):
                        result['log'] = json.loads(result_record['log'])
                    
                    if result_record.get('errors'):
                        result['errors'] = json.loads(result_record['errors'])
                    
                    session['results'].append(result)
            
            # Cache in memory
            self.sessions[session_id] = session
            
            return session
            
        except Exception as e:
            logger.error(f"Failed to load session: {str(e)}")
            return None 