"""
Database Service for AI LAM

Enhanced database service following Suna's patterns for connection management and operations.
"""

import asyncio
import logging
from typing import Optional, Dict, Any, List
from contextlib import asynccontextmanager
from supabase import create_client, Client
from utils.config import get_config

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Base exception for database-related errors."""
    pass

class DatabaseConnectionError(DatabaseError):
    """Exception raised when database connection fails."""
    pass

class DatabaseService:
    """Enhanced database service with connection management."""
    
    def __init__(self):
        self.config = get_config()
        self._client: Optional[Client] = None
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the database connection."""
        if self._initialized:
            return
        
        try:
            if not self.config.SUPABASE_URL or not self.config.SUPABASE_KEY:
                raise DatabaseConnectionError("Supabase URL and key are required")
            
            self._client = create_client(
                self.config.SUPABASE_URL,
                self.config.SUPABASE_KEY
            )
            
            # Test connection
            await self._test_connection()
            
            self._initialized = True
            logger.info("Database service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database service: {e}")
            raise DatabaseConnectionError(f"Database initialization failed: {str(e)}")
    
    async def _test_connection(self) -> bool:
        """Test the database connection."""
        try:
            # Simple test query
            result = self._client.table('users').select('id').limit(1).execute()
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    @property
    def client(self) -> Client:
        """Get the database client."""
        if not self._initialized or not self._client:
            raise DatabaseError("Database service not initialized")
        return self._client
    
    async def disconnect(self) -> None:
        """Disconnect from the database."""
        if self._client:
            # Supabase client doesn't need explicit disconnection
            self._client = None
            self._initialized = False
            logger.info("Database service disconnected")
    
    @asynccontextmanager
    async def transaction(self):
        """Context manager for database transactions."""
        # Note: Supabase doesn't support explicit transactions in the Python client
        # This is a placeholder for future transaction support
        try:
            yield self.client
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            raise
    
    # User operations
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get a user by ID."""
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise DatabaseError(f"Failed to get user: {str(e)}")
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get a user by email."""
        try:
            result = self.client.table('users').select('*').eq('email', email).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            raise DatabaseError(f"Failed to get user by email: {str(e)}")
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user."""
        try:
            result = self.client.table('users').insert(user_data).execute()
            logger.info(f"Created user: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise DatabaseError(f"Failed to create user: {str(e)}")
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update a user."""
        try:
            result = self.client.table('users').update(updates).eq('id', user_id).execute()
            if not result.data:
                raise DatabaseError(f"User {user_id} not found")
            logger.info(f"Updated user: {user_id}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise DatabaseError(f"Failed to update user: {str(e)}")
    
    # Application operations
    async def create_application(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new application."""
        try:
            result = self.client.table('applications').insert(application_data).execute()
            logger.info(f"Created application: {result.data[0]['id']}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error creating application: {e}")
            raise DatabaseError(f"Failed to create application: {str(e)}")
    
    async def get_applications_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Get applications for a user."""
        try:
            result = self.client.table('applications').select('*').eq('user_id', user_id).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error getting applications for user {user_id}: {e}")
            raise DatabaseError(f"Failed to get applications: {str(e)}")
    
    async def update_application_status(
        self, 
        application_id: str, 
        status: str, 
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update application status."""
        try:
            updates = {'status': status}
            if notes:
                updates['notes'] = notes
            
            result = self.client.table('applications').update(updates).eq('id', application_id).execute()
            if not result.data:
                raise DatabaseError(f"Application {application_id} not found")
            
            logger.info(f"Updated application {application_id} status to {status}")
            return result.data[0]
        except Exception as e:
            logger.error(f"Error updating application {application_id}: {e}")
            raise DatabaseError(f"Failed to update application status: {str(e)}")
    
    # Automation operations
    async def log_automation_run(self, automation_data: Dict[str, Any]) -> Dict[str, Any]:
        """Log an automation run."""
        try:
            result = self.client.table('automation_logs').insert(automation_data).execute()
            return result.data[0]
        except Exception as e:
            logger.error(f"Error logging automation run: {e}")
            raise DatabaseError(f"Failed to log automation run: {str(e)}")
    
    async def get_automation_history(
        self, 
        user_id: str, 
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get automation history for a user."""
        try:
            result = (self.client.table('automation_logs')
                     .select('*')
                     .eq('user_id', user_id)
                     .order('created_at', desc=True)
                     .limit(limit)
                     .execute())
            return result.data
        except Exception as e:
            logger.error(f"Error getting automation history for user {user_id}: {e}")
            raise DatabaseError(f"Failed to get automation history: {str(e)}")

# Global instance
_database_service = None

def get_database_service() -> DatabaseService:
    """Get or create the global database service instance."""
    global _database_service
    if _database_service is None:
        _database_service = DatabaseService()
    return _database_service 