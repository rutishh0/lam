import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import aiosmtplib
import asyncio
from twilio.rest import Client as TwilioClient
from jinja2 import Template

logger = logging.getLogger(__name__)

class NotificationService:
    """Service for sending notifications via email and SMS"""
    
    def __init__(self):
        # Email configuration
        self.smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        self.smtp_user = os.environ.get('SMTP_USER', '')
        self.smtp_password = os.environ.get('SMTP_PASSWORD', '')
        self.from_email = os.environ.get('FROM_EMAIL', self.smtp_user)
        
        # Twilio configuration for SMS
        self.twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID', '')
        self.twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN', '')
        self.twilio_from_number = os.environ.get('TWILIO_FROM_NUMBER', '')
        
        # Initialize Twilio client if credentials provided
        self.twilio_client = None
        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = TwilioClient(self.twilio_account_sid, self.twilio_auth_token)
    
    async def send_email(self, to_email: str, subject: str, body: str, 
                        html_body: Optional[str] = None, 
                        attachments: Optional[List[Dict[str, Any]]] = None) -> bool:
        """Send email notification"""
        try:
            message = MIMEMultipart('alternative')
            message['From'] = self.from_email
            message['To'] = to_email
            message['Subject'] = subject
            
            # Add plain text part
            text_part = MIMEText(body, 'plain')
            message.attach(text_part)
            
            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                message.attach(html_part)
            
            # Add attachments if provided
            if attachments:
                for attachment in attachments:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment['content'])
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f"attachment; filename= {attachment['filename']}"
                    )
                    message.attach(part)
            
            # Send email
            async with aiosmtplib.SMTP(hostname=self.smtp_host, port=self.smtp_port) as server:
                await server.starttls()
                await server.login(self.smtp_user, self.smtp_password)
                await server.send_message(message)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS notification via Twilio"""
        try:
            if not self.twilio_client:
                logger.warning("Twilio client not initialized")
                return False
            
            # Send SMS
            message = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_from_number,
                to=to_phone
            )
            
            logger.info(f"SMS sent successfully to {to_phone}: {message.sid}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS to {to_phone}: {str(e)}")
            return False
    
    async def send_application_status_update(self, client_data: Dict[str, Any], 
                                           application_data: Dict[str, Any],
                                           old_status: str, new_status: str):
        """Send notification about application status change"""
        
        # Email template
        email_template = Template("""
        Dear {{ client_name }},
        
        Your application status for {{ university_name }} - {{ course_name }} has been updated.
        
        Previous Status: {{ old_status }}
        New Status: {{ new_status }}
        
        {% if new_status == 'accepted' %}
        🎉 Congratulations! Your application has been accepted!
        
        Next Steps:
        1. Log in to the university portal to view your offer details
        2. Check for any conditions attached to your offer
        3. Respond to the offer before the deadline
        
        {% elif new_status == 'interview_scheduled' %}
        📅 Great news! You've been invited for an interview!
        
        Please log in to the university portal to:
        - View interview details (date, time, location/online link)
        - Prepare required documents
        - Confirm your attendance
        
        {% elif new_status == 'rejected' %}
        😔 Unfortunately, your application was not successful this time.
        
        Don't be discouraged! You still have other options:
        - Check your other university applications
        - Consider applying through clearing
        - Seek advice from our support team
        
        {% endif %}
        
        Application Details:
        - University: {{ university_name }}
        - Course: {{ course_name }} ({{ course_code }})
        - Applied on: {{ application_date }}
        - Last updated: {{ update_time }}
        
        You can track all your applications at: {{ dashboard_url }}
        
        Best regards,
        University Application Agent
        """)
        
        # Prepare template data
        template_data = {
            'client_name': client_data.get('full_name', 'Applicant'),
            'university_name': application_data.get('university_name'),
            'course_name': application_data.get('course_name'),
            'course_code': application_data.get('course_code'),
            'old_status': old_status.replace('_', ' ').title(),
            'new_status': new_status.replace('_', ' ').title(),
            'application_date': application_data.get('created_at', ''),
            'update_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
            'dashboard_url': os.environ.get('FRONTEND_URL', 'http://localhost:3000') + '/monitor'
        }
        
        # Render email
        email_body = email_template.render(**template_data)
        
        # Create HTML version
        html_body = email_body.replace('\n', '<br>')
        
        # Send email
        email_sent = await self.send_email(
            to_email=client_data.get('email'),
            subject=f"Application Status Update - {application_data.get('university_name')}",
            body=email_body,
            html_body=f"<html><body>{html_body}</body></html>"
        )
        
        # Send SMS for important updates
        if new_status in ['accepted', 'interview_scheduled', 'rejected']:
            sms_message = f"University App Update: Your {application_data.get('university_name')} application status changed to {new_status.replace('_', ' ').upper()}. Check your email for details."
            
            if client_data.get('phone'):
                await self.send_sms(client_data.get('phone'), sms_message)
        
        return email_sent
    
    async def send_daily_summary(self, client_data: Dict[str, Any], 
                               applications: List[Dict[str, Any]]):
        """Send daily summary of all applications"""
        
        email_template = Template("""
        Dear {{ client_name }},
        
        Here's your daily university application summary:
        
        📊 Overview:
        - Total Applications: {{ total_apps }}
        - Accepted: {{ accepted_count }}
        - Pending: {{ pending_count }}
        - In Progress: {{ in_progress_count }}
        
        📋 Application Details:
        {% for app in applications %}
        {{ loop.index }}. {{ app.university_name }}
           Course: {{ app.course_name }}
           Status: {{ app.status }}
           Last Updated: {{ app.last_checked }}
           {% if app.notes %}Notes: {{ app.notes }}{% endif %}
           
        {% endfor %}
        
        🔔 Recent Updates:
        {% for update in recent_updates %}
        - {{ update }}
        {% endfor %}
        
        💡 Tips:
        - Keep your documents up to date
        - Check university portals regularly for messages
        - Respond promptly to any requests
        
        Track your applications: {{ dashboard_url }}
        
        Best regards,
        University Application Agent
        """)
        
        # Calculate statistics
        status_counts = {
            'accepted': 0,
            'pending': 0,
            'in_progress': 0
        }
        
        for app in applications:
            status = app.get('status', 'pending')
            if status == 'accepted':
                status_counts['accepted'] += 1
            elif status in ['pending', 'submitted']:
                status_counts['pending'] += 1
            else:
                status_counts['in_progress'] += 1
        
        # Prepare template data
        template_data = {
            'client_name': client_data.get('full_name', 'Applicant'),
            'total_apps': len(applications),
            'accepted_count': status_counts['accepted'],
            'pending_count': status_counts['pending'],
            'in_progress_count': status_counts['in_progress'],
            'applications': applications,
            'recent_updates': self._get_recent_updates(applications),
            'dashboard_url': os.environ.get('FRONTEND_URL', 'http://localhost:3000') + '/monitor'
        }
        
        # Render and send email
        email_body = email_template.render(**template_data)
        
        return await self.send_email(
            to_email=client_data.get('email'),
            subject="Daily University Application Summary",
            body=email_body
        )
    
    def _get_recent_updates(self, applications: List[Dict[str, Any]]) -> List[str]:
        """Get recent updates from applications"""
        updates = []
        for app in applications:
            if app.get('last_checked'):
                # Check if updated in last 24 hours
                last_checked = datetime.fromisoformat(app['last_checked'].replace('Z', '+00:00'))
                if (datetime.utcnow() - last_checked).days < 1:
                    updates.append(f"{app['university_name']} - {app['status']}")
        
        return updates[:5]  # Return top 5 recent updates


# Email templates for different scenarios
class EmailTemplates:
    """Pre-defined email templates"""
    
    WELCOME_TEMPLATE = """
    Welcome to the University Application Agent!
    
    We've successfully received your information and are ready to help you with your university applications.
    
    What happens next:
    1. We'll create accounts on your selected university portals
    2. Fill out application forms with your provided information
    3. Monitor application status daily
    4. Notify you of any updates
    
    You can track your applications at any time by visiting your dashboard.
    """
    
    APPLICATION_SUBMITTED_TEMPLATE = """
    Great news! We've successfully submitted your application to {university_name}.
    
    Application Details:
    - Course: {course_name}
    - Reference Number: {reference_number}
    - Submitted: {submission_date}
    
    We'll monitor this application daily and notify you of any status changes.
    """
    
    DOCUMENT_REMINDER_TEMPLATE = """
    Reminder: Some of your applications are missing required documents.
    
    Please upload the following documents to complete your applications:
    {missing_documents}
    
    Upload documents at: {upload_url}
    """ 