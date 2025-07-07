"""
Supabase client for university application agent
"""
import logging
import os
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from supabase import create_client, Client

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Real Supabase client implementation"""
    
    def __init__(self):
        self.api_url = os.environ.get("SUPABASE_URL")
        self.api_key = os.environ.get("SUPABASE_KEY")
        
        if not self.api_url or not self.api_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        # Initialize Supabase client
        self.client: Client = create_client(self.api_url, self.api_key)
        
        logger.info(f"Initialized Supabase client with URL: {self.api_url}")
        
        # Initialize default data
        self._initialize_default_data()
    
    def _initialize_default_data(self):
        """Initialize default subscription plans and admin user if they don't exist"""
        try:
            # Check if plans exist, if not create them
            existing_plans = self.client.table('subscription_plans').select('*').execute()
            if not existing_plans.data:
                default_plans = [
                    {
                        "id": "plan-basic",
                        "name": "Basic Plan",
                        "description": "Basic features for individual users",
                        "price": 9.99,
                        "features": ["5 applications", "Basic support", "Standard automation"],
                        "limits": {
                            "max_applications": 5,
                            "max_clients": 3
                        }
                    },
                    {
                        "id": "plan-premium",
                        "name": "Premium Plan",
                        "description": "Advanced features for power users",
                        "price": 29.99,
                        "features": ["Unlimited applications", "Priority support", "Advanced automation", "Analytics"],
                        "limits": {
                            "max_applications": -1,  # Unlimited
                            "max_clients": -1  # Unlimited
                        }
                    }
                ]
                for plan in default_plans:
                    self.client.table('subscription_plans').insert(plan).execute()
                logger.info("Initialized default subscription plans")
        except Exception as e:
            logger.warning(f"Could not initialize default data: {str(e)}")

    def table(self, table_name: str):
        """Get table reference"""
        return self.client.table(table_name)
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client"""
        try:
            # Ensure client has a UUID (your schema likely uses uuid too)
            if 'uuid' not in client_data and 'id' not in client_data:
                client_data['uuid'] = str(uuid.uuid4())
            
            # Set created_at if not present
            if 'created_at' not in client_data:
                client_data['created_at'] = datetime.utcnow().isoformat()
            
            # Insert into Supabase
            result = self.client.table('clients').insert(client_data).execute()
            
            if result.data:
                # Return the UUID from the database response
                record = result.data[0]
                client_id = record.get("uuid") or record.get("id")
                return {"id": client_id, "status": "success"}
            else:
                return {"error": "Failed to create client"}
                
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            return {"error": str(e)}
    
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        try:
            result = self.client.table('clients').select('*').eq('id', client_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting client: {str(e)}")
            return None
    
    async def get_user_clients(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all clients for a user"""
        try:
            result = self.client.table('clients').select('*').eq('user_id', user_id).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting user clients: {str(e)}")
            return []
    
    async def create_application(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new application"""
        try:
            # Ensure application has an ID
            if 'id' not in application_data:
                application_data['id'] = str(uuid.uuid4())
            
            # Set created_at if not present
            if 'created_at' not in application_data:
                application_data['created_at'] = datetime.utcnow().isoformat()
            
            # Insert into Supabase
            result = self.client.table('application_tasks').insert(application_data).execute()
            
            if result.data:
                return {"id": result.data[0]["id"], "status": "success"}
            else:
                return {"error": "Failed to create application"}
                
        except Exception as e:
            logger.error(f"Error creating application: {str(e)}")
            return {"error": str(e)}
    
    async def get_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get application by ID"""
        try:
            result = self.client.table('application_tasks').select('*').eq('id', application_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting application: {str(e)}")
            return None
    
    async def get_all_application_tasks(self) -> List[Dict[str, Any]]:
        """Get all application tasks"""
        try:
            result = self.client.table('application_tasks').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting all applications: {str(e)}")
            return []
    
    async def get_client_application_tasks(self, client_id: str) -> List[Dict[str, Any]]:
        """Get application tasks for a client"""
        try:
            result = self.client.table('application_tasks').select('*').eq('client_id', client_id).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting client applications: {str(e)}")
            return []
    
    async def update_application_status(self, application_id: str, status: str) -> bool:
        """Update application status"""
        try:
            result = self.client.table('application_tasks').update({
                "status": status,
                "last_checked": datetime.utcnow().isoformat()
            }).eq('id', application_id).execute()
            
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error updating application status: {str(e)}")
            return False
    
    async def get_client_analytics(self, client_id: str) -> Dict[str, Any]:
        """Get analytics for a client"""
        try:
            result = self.client.table('application_tasks').select('*').eq('client_id', client_id).execute()
            client_apps = result.data or []
            
            total_apps = len(client_apps)
            status_counts = {}
            for app in client_apps:
                status = app.get("status", "unknown")
                status_counts[status] = status_counts.get(status, 0) + 1
            
            return {
                "client_id": client_id,
                "total_applications": total_apps,
                "status_breakdown": status_counts,
                "success_rate": round((status_counts.get("accepted", 0) / total_apps * 100), 1) if total_apps > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error getting client analytics: {str(e)}")
            return {"error": str(e)}
    
    async def get_all_users(self) -> List[Dict[str, Any]]:
        """Get all users"""
        try:
            result = self.client.table('users').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []
    
    async def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new user"""
        try:
            # Ensure user has a UUID
            if 'uuid' not in user_data:
                user_data['uuid'] = str(uuid.uuid4())
            
            # Set created_at if not present
            if 'created_at' not in user_data:
                user_data['created_at'] = datetime.utcnow().isoformat()
            
            # Insert into Supabase
            result = self.client.table('users').insert(user_data).execute()
            
            if result.data:
                return {"id": result.data[0]["uuid"], "status": "success", "user": result.data[0]}
            else:
                return {"error": "Failed to create user"}
                
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return {"error": str(e)}
    
    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        try:
            result = self.client.table('users').select('*').eq('email', email).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {str(e)}")
            return None
    
    async def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user by ID"""
        try:
            result = self.client.table('users').select('*').eq('uuid', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID: {str(e)}")
            return None
    
    async def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription for a user"""
        try:
            result = self.client.table('user_subscriptions').select('*').eq('user_id', user_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user subscription: {str(e)}")
            return None
    
    async def get_all_subscription_plans(self) -> List[Dict[str, Any]]:
        """Get all subscription plans"""
        try:
            result = self.client.table('subscription_plans').select('*').execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error getting subscription plans: {str(e)}")
            return []
    
    async def get_subscription_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription plan by ID"""
        try:
            result = self.client.table('subscription_plans').select('*').eq('id', plan_id).execute()
            
            if result.data:
                return result.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting subscription plan: {str(e)}")
            return None
    
    async def track_usage(self, user_id: str, resource_type: str, resource_id: str) -> bool:
        """Track resource usage"""
        try:
            usage_record = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            result = self.client.table('usage_tracking').insert(usage_record).execute()
            return bool(result.data)
        except Exception as e:
            logger.error(f"Error tracking usage: {str(e)}")
            return False

# Singleton instance
_supabase_client = None

def get_supabase_client() -> SupabaseClient:
    """Get or create the Supabase client singleton"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client