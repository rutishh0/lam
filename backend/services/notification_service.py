"""
Notification Service for AI LAM

Enhanced notification service following Suna's patterns for user communications.
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from enum import Enum
from services.database_service import get_database_service
from utils.config import get_config

logger = logging.getLogger(__name__)

class NotificationType(Enum):
    """Notification types."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    AUTOMATION_COMPLETE = "automation_complete"
    AUTOMATION_FAILED = "automation_failed"
    APPLICATION_UPDATE = "application_update"

class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationError(Exception):
    """Base exception for notification-related errors."""
    pass

class NotificationService:
    """Enhanced notification service."""
    
    def __init__(self):
        self.config = get_config()
        self.db_service = get_database_service()
        self._initialized = False
    
    async def initialize(self) -> None:
        """Initialize the notification service."""
        if self._initialized:
            return
        
        try:
            # Ensure dependencies are initialized
            await self.db_service.initialize()
            
            self._initialized = True
            logger.info("Notification service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize notification service: {e}")
            raise NotificationError(f"Notification service initialization failed: {str(e)}")
    
    async def send_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType = NotificationType.INFO,
        priority: NotificationPriority = NotificationPriority.MEDIUM,
        data: Optional[Dict[str, Any]] = None,
        send_email: bool = False,
        send_push: bool = True
    ) -> Dict[str, Any]:
        """
        Send a notification to a user.
        
        Args:
            user_id: Target user ID
            title: Notification title
            message: Notification message
            notification_type: Type of notification
            priority: Priority level
            data: Additional data
            send_email: Whether to send email notification
            send_push: Whether to send push notification
        
        Returns:
            Dict containing notification details
        """
        if not self._initialized:
            await self.initialize()
        
        try:
            notification_data = {
                'user_id': user_id,
                'title': title,
                'message': message,
                'type': notification_type.value,
                'priority': priority.value,
                'data': data or {},
                'created_at': datetime.now(timezone.utc).isoformat(),
                'read': False,
                'delivered': False
            }
            
            # Store notification in database
            result = await self.db_service.client.table('notifications').insert(notification_data).execute()
            notification_id = result.data[0]['id']
            
            logger.info(f"Created notification {notification_id} for user {user_id}")
            
            # Send through various channels
            delivery_results = {}
            
            if send_push:
                delivery_results['push'] = await self._send_push_notification(
                    user_id, title, message, notification_type, data
                )
            
            if send_email:
                delivery_results['email'] = await self._send_email_notification(
                    user_id, title, message, notification_type, data
                )
            
            # Update delivery status
            await self.db_service.client.table('notifications').update({
                'delivered': True,
                'delivery_results': delivery_results,
                'delivered_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', notification_id).execute()
            
            return {
                'notification_id': notification_id,
                'user_id': user_id,
                'title': title,
                'type': notification_type.value,
                'priority': priority.value,
                'delivered': True,
                'delivery_results': delivery_results
            }
            
        except Exception as e:
            logger.error(f"Error sending notification to user {user_id}: {e}")
            raise NotificationError(f"Failed to send notification: {str(e)}")
    
    async def _send_push_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send push notification (placeholder for actual implementation)."""
        try:
            # TODO: Implement actual push notification service
            # This could integrate with Firebase, Pusher, etc.
            
            logger.debug(f"Push notification sent to user {user_id}: {title}")
            
            return {
                'success': True,
                'channel': 'push',
                'sent_at': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Push notification failed for user {user_id}: {e}")
            return {
                'success': False,
                'channel': 'push',
                'error': str(e)
            }
    
    async def _send_email_notification(
        self,
        user_id: str,
        title: str,
        message: str,
        notification_type: NotificationType,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send email notification (placeholder for actual implementation)."""
        try:
            # Get user email
            user = await self.db_service.get_user_by_id(user_id)
            if not user or not user.get('email'):
                return {
                    'success': False,
                    'channel': 'email',
                    'error': 'User email not found'
                }
            
            # TODO: Implement actual email service
            # This could integrate with SendGrid, AWS SES, etc.
            
            logger.debug(f"Email notification sent to {user['email']}: {title}")
            
            return {
                'success': True,
                'channel': 'email',
                'recipient': user['email'],
                'sent_at': datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            logger.error(f"Email notification failed for user {user_id}: {e}")
            return {
                'success': False,
                'channel': 'email',
                'error': str(e)
            }
    
    async def mark_as_read(
        self,
        notification_id: str,
        user_id: str
    ) -> bool:
        """Mark a notification as read."""
        try:
            result = await self.db_service.client.table('notifications').update({
                'read': True,
                'read_at': datetime.now(timezone.utc).isoformat()
            }).eq('id', notification_id).eq('user_id', user_id).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error marking notification {notification_id} as read: {e}")
            return False
    
    async def get_user_notifications(
        self,
        user_id: str,
        limit: int = 50,
        unread_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get notifications for a user."""
        try:
            query = self.db_service.client.table('notifications').select('*').eq('user_id', user_id)
            
            if unread_only:
                query = query.eq('read', False)
            
            result = query.order('created_at', desc=True).limit(limit).execute()
            return result.data
            
        except Exception as e:
            logger.error(f"Error getting notifications for user {user_id}: {e}")
            raise NotificationError(f"Failed to get notifications: {str(e)}")
    
    async def send_automation_complete_notification(
        self,
        user_id: str,
        automation_type: str,
        automation_id: str,
        success: bool = True,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Send automation completion notification."""
        if success:
            title = f"Automation Complete: {automation_type}"
            message = f"Your {automation_type} automation has completed successfully."
            notification_type = NotificationType.AUTOMATION_COMPLETE
        else:
            title = f"Automation Failed: {automation_type}"
            message = f"Your {automation_type} automation encountered an error."
            notification_type = NotificationType.AUTOMATION_FAILED
        
        return await self.send_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            priority=NotificationPriority.HIGH,
            data={
                'automation_type': automation_type,
                'automation_id': automation_id,
                'success': success,
                'details': details or {}
            },
            send_email=not success  # Send email for failures
        )
    
    async def send_application_update_notification(
        self,
        user_id: str,
        application_id: str,
        status: str,
        details: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send application status update notification."""
        title = f"Application Update: {status.title()}"
        message = f"Your application status has been updated to {status}."
        
        if details:
            message += f" {details}"
        
        return await self.send_notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=NotificationType.APPLICATION_UPDATE,
            priority=NotificationPriority.MEDIUM,
            data={
                'application_id': application_id,
                'new_status': status,
                'details': details
            }
        )
    
    async def delete_notification(
        self,
        notification_id: str,
        user_id: str
    ) -> bool:
        """Delete a notification."""
        try:
            result = await self.db_service.client.table('notifications').delete().eq(
                'id', notification_id
            ).eq('user_id', user_id).execute()
            
            return len(result.data) > 0
            
        except Exception as e:
            logger.error(f"Error deleting notification {notification_id}: {e}")
            return False

# Global instance
_notification_service = None

def get_notification_service() -> NotificationService:
    """Get or create the global notification service instance."""
    global _notification_service
    if _notification_service is None:
        _notification_service = NotificationService()
    return _notification_service 