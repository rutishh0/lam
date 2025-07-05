"""
Supabase client for university application agent
"""
import logging
import os
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class SupabaseClient:
    """Mock Supabase client for testing"""
    
    def __init__(self):
        self.api_url = os.environ.get("SUPABASE_URL", "https://mock-supabase-url.com")
        self.api_key = os.environ.get("SUPABASE_KEY", "mock-supabase-key")
        
        # Mock database
        self.db = {
            "clients": [],
            "applications": [],
            "users": [
                {
                    "id": "admin-user-id",
                    "name": "Admin User",
                    "email": "admin@example.com",
                    "role": "admin",
                    "is_active": True,
                    "email_verified": True,
                    "created_at": (datetime.utcnow() - timedelta(days=30)).isoformat()
                },
                {
                    "id": "regular-user-id",
                    "name": "Regular User",
                    "email": "user@example.com",
                    "role": "user",
                    "is_active": True,
                    "email_verified": True,
                    "created_at": (datetime.utcnow() - timedelta(days=15)).isoformat()
                }
            ],
            "subscriptions": [
                {
                    "id": "subscription-1",
                    "user_id": "admin-user-id",
                    "plan_id": "plan-premium",
                    "status": "active",
                    "start_date": (datetime.utcnow() - timedelta(days=30)).isoformat(),
                    "end_date": (datetime.utcnow() + timedelta(days=335)).isoformat()
                },
                {
                    "id": "subscription-2",
                    "user_id": "regular-user-id",
                    "plan_id": "plan-basic",
                    "status": "active",
                    "start_date": (datetime.utcnow() - timedelta(days=15)).isoformat(),
                    "end_date": (datetime.utcnow() + timedelta(days=350)).isoformat()
                }
            ],
            "plans": [
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
            ],
            "usage": []
        }
        
    def table(self, table_name: str):
        """Get table reference"""
        return TableQuery(self, table_name)
    
    async def create_client(self, client_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new client"""
        try:
            # Add to mock database
            self.db["clients"].append(client_data)
            return {"id": client_data["id"], "status": "success"}
        except Exception as e:
            logger.error(f"Error creating client: {str(e)}")
            return {"error": str(e)}
    
    async def get_client(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client by ID"""
        try:
            for client in self.db["clients"]:
                if client["id"] == client_id:
                    return client
            return None
        except Exception as e:
            logger.error(f"Error getting client: {str(e)}")
            return None
    
    async def get_user_clients(self, user_id: str) -> List[Dict[str, Any]]:
        """Get all clients for a user"""
        try:
            return [client for client in self.db["clients"] if client.get("user_id") == user_id]
        except Exception as e:
            logger.error(f"Error getting user clients: {str(e)}")
            return []
    
    async def create_application(self, application_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new application"""
        try:
            # Add to mock database
            self.db["applications"].append(application_data)
            return {"id": application_data["id"], "status": "success"}
        except Exception as e:
            logger.error(f"Error creating application: {str(e)}")
            return {"error": str(e)}
    
    async def get_application(self, application_id: str) -> Optional[Dict[str, Any]]:
        """Get application by ID"""
        try:
            for application in self.db["applications"]:
                if application["id"] == application_id:
                    return application
            return None
        except Exception as e:
            logger.error(f"Error getting application: {str(e)}")
            return None
    
    async def get_all_application_tasks(self) -> List[Dict[str, Any]]:
        """Get all application tasks"""
        try:
            return self.db["applications"]
        except Exception as e:
            logger.error(f"Error getting all applications: {str(e)}")
            return []
    
    async def get_client_application_tasks(self, client_id: str) -> List[Dict[str, Any]]:
        """Get application tasks for a client"""
        try:
            return [app for app in self.db["applications"] if app.get("client_id") == client_id]
        except Exception as e:
            logger.error(f"Error getting client applications: {str(e)}")
            return []
    
    async def update_application_status(self, application_id: str, status: str) -> bool:
        """Update application status"""
        try:
            for application in self.db["applications"]:
                if application["id"] == application_id:
                    application["status"] = status
                    application["last_checked"] = datetime.utcnow().isoformat()
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating application status: {str(e)}")
            return False
    
    async def get_client_analytics(self, client_id: str) -> Dict[str, Any]:
        """Get analytics for a client"""
        try:
            client_apps = [app for app in self.db["applications"] if app.get("client_id") == client_id]
            
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
            return self.db["users"]
        except Exception as e:
            logger.error(f"Error getting all users: {str(e)}")
            return []
    
    async def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription for a user"""
        try:
            for subscription in self.db["subscriptions"]:
                if subscription["user_id"] == user_id:
                    return subscription
            return None
        except Exception as e:
            logger.error(f"Error getting user subscription: {str(e)}")
            return None
    
    async def get_all_subscription_plans(self) -> List[Dict[str, Any]]:
        """Get all subscription plans"""
        try:
            return self.db["plans"]
        except Exception as e:
            logger.error(f"Error getting subscription plans: {str(e)}")
            return []
    
    async def get_subscription_plan_by_id(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """Get subscription plan by ID"""
        try:
            for plan in self.db["plans"]:
                if plan["id"] == plan_id:
                    return plan
            return None
        except Exception as e:
            logger.error(f"Error getting subscription plan: {str(e)}")
            return None
    
    async def track_usage(self, user_id: str, resource_type: str, resource_id: str) -> bool:
        """Track resource usage"""
        try:
            usage_record = {
                "id": f"usage-{len(self.db['usage'])+1}",
                "user_id": user_id,
                "resource_type": resource_type,
                "resource_id": resource_id,
                "timestamp": datetime.utcnow().isoformat()
            }
            self.db["usage"].append(usage_record)
            return True
        except Exception as e:
            logger.error(f"Error tracking usage: {str(e)}")
            return False

class TableQuery:
    """Mock table query builder"""
    
    def __init__(self, client, table_name):
        self.client = client
        self.table_name = table_name
        self._select_fields = "*"
        self._limit_val = None
        
    def select(self, fields):
        """Select fields"""
        self._select_fields = fields
        return self
    
    def limit(self, limit_val):
        """Limit results"""
        self._limit_val = limit_val
        return self
    
    def execute(self):
        """Execute query"""
        # Mock execution - return empty result
        return {"data": []}

# Singleton instance
_supabase_client = None

def get_supabase_client() -> SupabaseClient:
    """Get or create the Supabase client singleton"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client