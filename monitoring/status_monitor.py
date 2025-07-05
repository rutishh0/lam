"""
Status monitoring services for university application agent
"""
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ApplicationMonitor:
    """Monitor application status and progress"""
    
    def __init__(self, supabase_client, notification_service):
        self.supabase_client = supabase_client
        self.notification_service = notification_service
        
    async def check_application_status(self, application_id: str) -> Dict[str, Any]:
        """Check status of a specific application"""
        try:
            # This would normally query the university portal
            # For now, return mock data
            statuses = ["submitted", "under_review", "interview_scheduled", "accepted", "rejected"]
            current_status = random.choice(statuses)
            
            return {
                "application_id": application_id,
                "status": current_status,
                "last_checked": datetime.utcnow().isoformat(),
                "next_check": (datetime.utcnow() + timedelta(days=1)).isoformat()
            }
        except Exception as e:
            logger.error(f"Error checking application status: {str(e)}")
            return {
                "application_id": application_id,
                "status": "error",
                "error": str(e),
                "last_checked": datetime.utcnow().isoformat()
            }
        
    async def get_application_history(self, application_id: str) -> List[Dict[str, Any]]:
        """Get status history for an application"""
        try:
            # This would normally query the database
            # For now, return mock data
            now = datetime.utcnow()
            
            return [
                {
                    "timestamp": (now - timedelta(days=7)).isoformat(),
                    "status": "submitted",
                    "notes": "Application submitted successfully"
                },
                {
                    "timestamp": (now - timedelta(days=5)).isoformat(),
                    "status": "under_review",
                    "notes": "Application is under review"
                },
                {
                    "timestamp": (now - timedelta(days=2)).isoformat(),
                    "status": "interview_scheduled",
                    "notes": "Interview scheduled for next week"
                }
            ]
        except Exception as e:
            logger.error(f"Error getting application history: {str(e)}")
            return []
        
    async def send_status_notification(self, application_id: str, client_id: str, status: str) -> bool:
        """Send notification about status change"""
        try:
            # Get client data
            client = await self.supabase_client.get_client(client_id)
            
            if not client:
                logger.error(f"Client not found: {client_id}")
                return False
            
            # Get application data
            application = await self.supabase_client.get_application(application_id)
            
            if not application:
                logger.error(f"Application not found: {application_id}")
                return False
            
            # Send notification
            return await self.notification_service.send_application_update(
                client.get("email"),
                client.get("full_name"),
                application.get("university_name"),
                status,
                client.get("phone")
            )
        except Exception as e:
            logger.error(f"Error sending status notification: {str(e)}")
            return False

class PerformanceMonitor:
    """Monitor system performance"""
    
    def __init__(self):
        self.performance_history = []
        
    def record_performance_metrics(self):
        """Record current performance metrics"""
        try:
            import psutil
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available,
                "disk_usage": disk.percent,
                "disk_free": disk.free
            }
            
            self.performance_history.append(metrics)
            
            # Keep only the last 1000 records
            if len(self.performance_history) > 1000:
                self.performance_history = self.performance_history[-1000:]
                
            return metrics
        except Exception as e:
            logger.error(f"Error recording performance metrics: {str(e)}")
            return {}
        
    def get_performance_report(self) -> Dict[str, Any]:
        """Get performance report"""
        try:
            if not self.performance_history:
                return {
                    "status": "no_data",
                    "timestamp": datetime.utcnow().isoformat()
                }
            
            # Calculate averages
            cpu_values = [m["cpu_usage"] for m in self.performance_history if "cpu_usage" in m]
            memory_values = [m["memory_usage"] for m in self.performance_history if "memory_usage" in m]
            disk_values = [m["disk_usage"] for m in self.performance_history if "disk_usage" in m]
            
            avg_cpu = sum(cpu_values) / len(cpu_values) if cpu_values else 0
            avg_memory = sum(memory_values) / len(memory_values) if memory_values else 0
            avg_disk = sum(disk_values) / len(disk_values) if disk_values else 0
            
            # Get current metrics
            current = self.record_performance_metrics()
            
            return {
                "status": "healthy" if avg_cpu < 80 and avg_memory < 80 and avg_disk < 80 else "warning",
                "timestamp": datetime.utcnow().isoformat(),
                "current": current,
                "averages": {
                    "cpu_usage": round(avg_cpu, 1),
                    "memory_usage": round(avg_memory, 1),
                    "disk_usage": round(avg_disk, 1)
                },
                "history_size": len(self.performance_history)
            }
        except Exception as e:
            logger.error(f"Error generating performance report: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }