"""
Supabase Database Client
Handles all database operations for the Autonomous University Application Agent
"""
import os
import asyncio
from typing import List, Dict, Optional, Any, Union
from datetime import datetime, date, timedelta
import logging
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import json
import uuid

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Enhanced Supabase client with comprehensive database operations"""
    
    def __init__(self):
        """Initialize Supabase client with configuration"""
        self.url = os.environ.get('SUPABASE_URL')
        self.key = os.environ.get('SUPABASE_KEY')
        
        if not self.url or not self.key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")
        
        # Initialize Supabase client
        self.client: Client = create_client(self.url, self.key)
        logger.info("Supabase client initialized successfully")
    
    def _serialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Serialize data for Supabase insertion, handling dates and UUIDs"""
        serialized = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                serialized[key] = value.isoformat()
            elif isinstance(value, date):
                serialized[key] = value.isoformat()
            elif isinstance(value, uuid.UUID):
                serialized[key] = str(value)
            elif isinstance(value, (dict, list)):
                serialized[key] = value  # JSONB fields
            else:
                serialized[key] = value
        return serialized
    
    def _deserialize_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deserialize data from Supabase, converting date strings back to objects"""
        if not data:
            return data
            
        deserialized = data.copy()
        
        # Convert ISO date strings back to datetime objects for specific fields
        date_fields = ['created_at', 'updated_at', 'last_checked', 'submitted_at', 'changed_at', 'recorded_at']
        for field in date_fields:
            if field in deserialized and isinstance(deserialized[field], str):
                try:
                    deserialized[field] = datetime.fromisoformat(deserialized[field].replace('Z', '+00:00'))
                except ValueError:
                    pass  # Keep as string if parsing fails
        
        return deserialized

    # === CLIENT OPERATIONS ===
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client record"""
        try:
            # Ensure UUID is string if provided
            if 'id' in client_data:
                client_data['id'] = str(client_data['id'])
            
            serialized_data = self._serialize_data(client_data)
            
            result = self.client.table('clients').insert(serialized_data).execute()
            
            if result.data:
                logger.info(f"Client created successfully: {result.data[0]['id']}")
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            raise
    
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get a client by ID"""
        try:
            result = self.client.table('clients').select('*').eq('id', client_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error fetching client {client_id}: {str(e)}")
            raise
    
    async def get_all_clients(self) -> List[Dict[str, Any]]:
        """Get all clients"""
        try:
            result = self.client.table('clients').select('*').order('created_at', desc=True).execute()
            return [self._deserialize_data(client) for client in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching clients: {str(e)}")
            raise
    
    async def update_client(self, client_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a client record"""
        try:
            serialized_data = self._serialize_data(update_data)
            
            result = self.client.table('clients').update(serialized_data).eq('id', client_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from update operation")
                
        except Exception as e:
            logger.error(f"Error updating client {client_id}: {str(e)}")
            raise
    
    async def delete_client(self, client_id: str) -> bool:
        """Delete a client record"""
        try:
            result = self.client.table('clients').delete().eq('id', client_id).execute()
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error deleting client {client_id}: {str(e)}")
            raise

    # === USER MANAGEMENT OPERATIONS ===
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user account"""
        try:
            if 'id' in user_data:
                user_data['id'] = str(user_data['id'])
            
            serialized_data = self._serialize_data(user_data)
            
            result = self.client.table('users').insert(serialized_data).execute()
            
            if result.data:
                logger.info(f"User created successfully: {result.data[0]['id']}")
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email address"""
        try:
            result = self.client.table('users').select('*').eq('email', email).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            raise

    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            result = self.client.table('users').select('*').eq('id', user_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            raise

    async def update_user_last_login(self, user_id: str) -> bool:
        """Update user's last login timestamp"""
        try:
            result = self.client.table('users').update({
                'last_login': datetime.utcnow().isoformat()
            }).eq('id', user_id).execute()
            
            return len(result.data) > 0
                
        except Exception as e:
            logger.error(f"Error updating user last login: {str(e)}")
            return False

    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users (admin only)"""
        try:
            result = self.client.table('users').select('*').order('created_at', desc=True).execute()
            return [self._deserialize_data(user) for user in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching users: {str(e)}")
            raise

    # === SUBSCRIPTION MANAGEMENT OPERATIONS ===
    
    async def get_subscription_plan_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Get subscription plan by slug"""
        try:
            result = self.client.table('subscription_plans').select('*').eq('slug', slug).eq('is_active', True).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Error getting subscription plan by slug: {str(e)}")
            raise

    async def get_subscription_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription plan by ID"""
        try:
            result = self.client.table('subscription_plans').select('*').eq('id', plan_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Error getting subscription plan by ID: {str(e)}")
            raise

    async def get_all_subscription_plans(self) -> List[Dict[str, Any]]:
        """Get all active subscription plans"""
        try:
            result = self.client.table('subscription_plans').select('*').eq('is_active', True).order('sort_order').execute()
            return [self._deserialize_data(plan) for plan in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching subscription plans: {str(e)}")
            raise

    async def create_subscription(self, subscription_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user subscription"""
        try:
            if 'id' in subscription_data:
                subscription_data['id'] = str(subscription_data['id'])
            
            serialized_data = self._serialize_data(subscription_data)
            
            result = self.client.table('user_subscriptions').insert(serialized_data).execute()
            
            if result.data:
                logger.info(f"Subscription created successfully: {result.data[0]['id']}")
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}")
            raise

    async def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's active subscription"""
        try:
            result = self.client.table('user_subscriptions').select('*').eq('user_id', user_id).in_('status', ['active', 'trialing']).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
                
        except Exception as e:
            logger.error(f"Error getting user subscription: {str(e)}")
            raise

    async def update_subscription(self, subscription_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a subscription"""
        try:
            serialized_data = self._serialize_data(update_data)
            
            result = self.client.table('user_subscriptions').update(serialized_data).eq('id', subscription_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from update operation")
                
        except Exception as e:
            logger.error(f"Error updating subscription {subscription_id}: {str(e)}")
            raise

    # === USAGE TRACKING OPERATIONS ===
    
    async def count_user_resource_usage(self, user_id: str, resource_type: str) -> int:
        """Count user's resource usage"""
        try:
            if resource_type == "application":
                result = self.client.table('application_tasks').select('id', count='exact').eq('user_id', user_id).execute()
            elif resource_type == "client":
                result = self.client.table('clients').select('id', count='exact').eq('user_id', user_id).execute()
            else:
                return 0
            
            return result.count if result.count else 0
                
        except Exception as e:
            logger.error(f"Error counting user resource usage: {str(e)}")
            return 0

    async def track_usage(self, user_id: str, resource_type: str, resource_id: str = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Track user resource usage"""
        try:
            usage_data = {
                'user_id': user_id,
                'resource_type': resource_type,
                'resource_id': resource_id,
                'metadata': metadata or {},
                'usage_date': datetime.utcnow().date().isoformat()
            }
            
            # Use upsert to handle duplicate tracking
            result = self.client.table('usage_tracking').upsert(usage_data).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from upsert operation")
                
        except Exception as e:
            logger.error(f"Error tracking usage: {str(e)}")
            raise

    # === ENHANCED CLIENT OPERATIONS WITH USER CONTEXT ===
    
    async def get_user_clients(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all clients for a user"""
        try:
            result = self.client.table('clients').select('*').eq('user_id', user_id).eq('is_active', True).order('created_at', desc=True).execute()
            
            return [self._deserialize_data(client) for client in result.data]
                
        except Exception as e:
            logger.error(f"Error getting user clients: {str(e)}")
            raise

    async def get_user_applications(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all applications for a user"""
        try:
            result = self.client.table('application_tasks').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
            
            return [self._deserialize_data(task) for task in result.data]
                
        except Exception as e:
            logger.error(f"Error getting user applications: {str(e)}")
            raise

    # === BILLING OPERATIONS ===
    
    async def create_billing_record(self, billing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a billing history record"""
        try:
            if 'id' in billing_data:
                billing_data['id'] = str(billing_data['id'])
            
            serialized_data = self._serialize_data(billing_data)
            
            result = self.client.table('billing_history').insert(serialized_data).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error creating billing record: {str(e)}")
            raise

    async def get_user_billing_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Get billing history for a user"""
        try:
            result = self.client.table('billing_history').select('*').eq('user_id', user_id).order('billing_date', desc=True).execute()
            
            return [self._deserialize_data(record) for record in result.data]
                
        except Exception as e:
            logger.error(f"Error getting user billing history: {str(e)}")
            raise

    # === APPLICATION TASK OPERATIONS ===
    
    async def create_application_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new application task"""
        try:
            # Ensure UUID is string if provided
            if 'id' in task_data:
                task_data['id'] = str(task_data['id'])
            
            serialized_data = self._serialize_data(task_data)
            
            result = self.client.table('application_tasks').insert(serialized_data).execute()
            
            if result.data:
                logger.info(f"Application task created: {result.data[0]['id']}")
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error creating application task: {str(e)}")
            raise
    
    async def get_application_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get an application task by ID"""
        try:
            result = self.client.table('application_tasks').select('*').eq('id', task_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            return None
            
        except Exception as e:
            logger.error(f"Error fetching application task {task_id}: {str(e)}")
            raise
    
    async def get_client_application_tasks(self, client_id: str) -> List[Dict[str, Any]]:
        """Get all application tasks for a client"""
        try:
            result = (self.client.table('application_tasks')
                     .select('*')
                     .eq('client_id', client_id)
                     .order('created_at', desc=True)
                     .execute())
            
            return [self._deserialize_data(task) for task in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching application tasks for client {client_id}: {str(e)}")
            raise
    
    async def get_all_application_tasks(self) -> List[Dict[str, Any]]:
        """Get all application tasks"""
        try:
            result = (self.client.table('application_tasks')
                     .select('*')
                     .order('created_at', desc=True)
                     .execute())
            
            return [self._deserialize_data(task) for task in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching application tasks: {str(e)}")
            raise
    
    async def update_application_task(self, task_id: str, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an application task"""
        try:
            serialized_data = self._serialize_data(update_data)
            
            result = self.client.table('application_tasks').update(serialized_data).eq('id', task_id).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from update operation")
                
        except Exception as e:
            logger.error(f"Error updating application task {task_id}: {str(e)}")
            raise
    
    async def get_tasks_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get application tasks by status"""
        try:
            result = (self.client.table('application_tasks')
                     .select('*')
                     .eq('status', status)
                     .order('created_at', desc=True)
                     .execute())
            
            return [self._deserialize_data(task) for task in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching tasks by status {status}: {str(e)}")
            raise

    # === MOCK APPLICATION OPERATIONS ===
    
    async def create_mock_application(self, app_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a mock application for testing"""
        try:
            if 'id' in app_data:
                app_data['id'] = str(app_data['id'])
                
            serialized_data = self._serialize_data(app_data)
            
            result = self.client.table('mock_applications').insert(serialized_data).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error creating mock application: {str(e)}")
            raise
    
    async def get_mock_applications_by_university(self, university_code: str) -> List[Dict[str, Any]]:
        """Get mock applications for a university"""
        try:
            result = (self.client.table('mock_applications')
                     .select('*')
                     .eq('university_code', university_code)
                     .order('submitted_at', desc=True)
                     .execute())
            
            return [self._deserialize_data(app) for app in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching mock applications for {university_code}: {str(e)}")
            raise

    # === STATUS LOG OPERATIONS ===
    
    async def log_status_change(self, task_id: str, previous_status: str, new_status: str, notes: str = None) -> Dict[str, Any]:
        """Log a status change for an application task"""
        try:
            log_data = {
                'application_task_id': task_id,
                'previous_status': previous_status,
                'new_status': new_status,
                'notes': notes
            }
            
            result = self.client.table('application_status_log').insert(log_data).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error logging status change: {str(e)}")
            raise
    
    async def get_status_history(self, task_id: str) -> List[Dict[str, Any]]:
        """Get status change history for a task"""
        try:
            result = (self.client.table('application_status_log')
                     .select('*')
                     .eq('application_task_id', task_id)
                     .order('changed_at', desc=True)
                     .execute())
            
            return [self._deserialize_data(log) for log in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching status history for task {task_id}: {str(e)}")
            raise

    # === PERFORMANCE METRICS OPERATIONS ===
    
    async def record_metric(self, metric_type: str, metric_value: float, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Record a performance metric"""
        try:
            metric_data = {
                'metric_type': metric_type,
                'metric_value': metric_value,
                'metadata': metadata or {}
            }
            
            result = self.client.table('performance_metrics').insert(metric_data).execute()
            
            if result.data:
                return self._deserialize_data(result.data[0])
            else:
                raise Exception("No data returned from insert operation")
                
        except Exception as e:
            logger.error(f"Error recording metric: {str(e)}")
            raise
    
    async def get_metrics_by_type(self, metric_type: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get metrics by type for the last N days"""
        try:
            from_date = (datetime.now() - timedelta(days=days)).isoformat()
            
            result = (self.client.table('performance_metrics')
                     .select('*')
                     .eq('metric_type', metric_type)
                     .gte('recorded_at', from_date)
                     .order('recorded_at', desc=True)
                     .execute())
            
            return [self._deserialize_data(metric) for metric in result.data]
            
        except Exception as e:
            logger.error(f"Error fetching metrics for type {metric_type}: {str(e)}")
            raise

    # === ANALYTICS OPERATIONS ===
    
    async def get_client_analytics(self, client_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a client"""
        try:
            # Get client basic info
            client = await self.get_client(client_id)
            if not client:
                raise Exception(f"Client {client_id} not found")
            
            # Get application tasks
            tasks = await self.get_client_application_tasks(client_id)
            
            # Calculate analytics
            total_applications = len(tasks)
            status_counts = {}
            for task in tasks:
                status = task.get('status', 'unknown')
                status_counts[status] = status_counts.get(status, 0) + 1
            
            # Get status history for timeline
            timeline = []
            for task in tasks:
                history = await self.get_status_history(task['id'])
                timeline.extend(history)
            
            timeline.sort(key=lambda x: x['changed_at'], reverse=True)
            
            analytics = {
                'client': client,
                'total_applications': total_applications,
                'status_breakdown': status_counts,
                'applications': tasks,
                'timeline': timeline[:10],  # Last 10 status changes
                'success_rate': (status_counts.get('accepted', 0) / total_applications * 100) if total_applications > 0 else 0
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating client analytics: {str(e)}")
            raise

    # === UTILITY METHODS ===
    
    async def health_check(self) -> Dict[str, Any]:
        """Check database connection and basic functionality"""
        try:
            # Test basic query
            result = self.client.table('clients').select('id').limit(1).execute()
            
            return {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'tables_accessible': True
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {str(e)}")
            return {
                'status': 'unhealthy',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }
    
    async def execute_sql(self, sql: str) -> Any:
        """Execute raw SQL (use with caution)"""
        try:
            result = self.client.rpc('execute_sql', {'sql': sql}).execute()
            return result.data
        except Exception as e:
            logger.error(f"Error executing SQL: {str(e)}")
            raise

# Global instance
supabase_client = None

def get_supabase_client() -> SupabaseClient:
    """Get the global Supabase client instance"""
    global supabase_client
    if supabase_client is None:
        supabase_client = SupabaseClient()
    return supabase_client

# Async wrapper functions for compatibility
async def get_db_client() -> SupabaseClient:
    """Async wrapper to get database client"""
    return get_supabase_client() 