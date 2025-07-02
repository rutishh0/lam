import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict
import json

logger = logging.getLogger(__name__)

class ApplicationMonitor:
    """Monitor and track application statuses with analytics"""
    
    def __init__(self, db, notification_service=None):
        self.db = db
        self.notification_service = notification_service
        self.status_history = defaultdict(list)
        self.monitoring_interval = 3600  # 1 hour in seconds
        
    async def track_status_change(self, application_id: str, old_status: str, new_status: str, metadata: Dict[str, Any] = None):
        """Track status changes for analytics"""
        change_record = {
            'application_id': application_id,
            'old_status': old_status,
            'new_status': new_status,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': metadata or {}
        }
        
        # Store in history
        self.status_history[application_id].append(change_record)
        
        # Store in database
        await self.db.status_changes.insert_one(change_record)
        
        logger.info(f"Tracked status change for {application_id}: {old_status} -> {new_status}")
    
    async def get_application_timeline(self, application_id: str) -> List[Dict[str, Any]]:
        """Get complete timeline of an application"""
        timeline = []
        
        # Get from database
        cursor = self.db.status_changes.find({'application_id': application_id}).sort('timestamp', 1)
        async for change in cursor:
            timeline.append({
                'timestamp': change['timestamp'],
                'status': change['new_status'],
                'details': change.get('metadata', {})
            })
        
        return timeline
    
    async def get_client_analytics(self, client_id: str) -> Dict[str, Any]:
        """Get analytics for a specific client"""
        applications = await self.db.application_tasks.find({'client_id': client_id}).to_list(None)
        
        analytics = {
            'total_applications': len(applications),
            'status_breakdown': defaultdict(int),
            'university_breakdown': defaultdict(int),
            'average_response_time': None,
            'success_rate': 0,
            'timeline': []
        }
        
        response_times = []
        
        for app in applications:
            # Status breakdown
            analytics['status_breakdown'][app['status']] += 1
            
            # University breakdown
            analytics['university_breakdown'][app['university_name']] += 1
            
            # Calculate response time if available
            if app.get('status') in ['accepted', 'rejected'] and app.get('created_at') and app.get('last_checked'):
                created = datetime.fromisoformat(app['created_at'].replace('Z', '+00:00'))
                responded = datetime.fromisoformat(app['last_checked'].replace('Z', '+00:00'))
                response_times.append((responded - created).days)
        
        # Calculate averages
        if response_times:
            analytics['average_response_time'] = sum(response_times) / len(response_times)
        
        if applications:
            accepted = analytics['status_breakdown'].get('accepted', 0)
            analytics['success_rate'] = (accepted / len(applications)) * 100
        
        return dict(analytics)
    
    async def generate_insights(self, client_id: str) -> List[str]:
        """Generate actionable insights for a client"""
        insights = []
        
        analytics = await self.get_client_analytics(client_id)
        applications = await self.db.application_tasks.find({'client_id': client_id}).to_list(None)
        
        # Insight 1: Application success rate
        if analytics['success_rate'] > 0:
            insights.append(f"Your acceptance rate is {analytics['success_rate']:.1f}% - {'above' if analytics['success_rate'] > 30 else 'below'} average")
        
        # Insight 2: Response time
        if analytics['average_response_time']:
            insights.append(f"Universities typically respond within {int(analytics['average_response_time'])} days")
        
        # Insight 3: Pending applications
        pending = analytics['status_breakdown'].get('pending', 0) + analytics['status_breakdown'].get('submitted', 0)
        if pending > 0:
            insights.append(f"You have {pending} applications awaiting response")
        
        # Insight 4: Interview opportunities
        interviews = analytics['status_breakdown'].get('interview_scheduled', 0)
        if interviews > 0:
            insights.append(f"Prepare for {interviews} upcoming interview{'s' if interviews > 1 else ''}")
        
        # Insight 5: Action required
        for app in applications:
            if app.get('status') == 'accepted':
                insights.append(f"Action required: Respond to offer from {app['university_name']}")
        
        return insights
    
    async def check_deadlines(self, client_id: str) -> List[Dict[str, Any]]:
        """Check for upcoming deadlines"""
        deadlines = []
        
        applications = await self.db.application_tasks.find({
            'client_id': client_id,
            'status': {'$in': ['accepted', 'interview_scheduled']}
        }).to_list(None)
        
        for app in applications:
            # Check if deadline info exists in metadata
            if app.get('application_data', {}).get('deadline'):
                deadline_date = datetime.fromisoformat(app['application_data']['deadline'])
                days_remaining = (deadline_date - datetime.utcnow()).days
                
                if days_remaining > 0 and days_remaining <= 30:
                    deadlines.append({
                        'university': app['university_name'],
                        'action': 'Respond to offer' if app['status'] == 'accepted' else 'Attend interview',
                        'deadline': deadline_date.isoformat(),
                        'days_remaining': days_remaining,
                        'urgency': 'high' if days_remaining < 7 else 'medium'
                    })
        
        return sorted(deadlines, key=lambda x: x['days_remaining'])
    
    async def monitor_application_health(self) -> Dict[str, Any]:
        """Monitor overall system health and application processing"""
        health_report = {
            'timestamp': datetime.utcnow().isoformat(),
            'total_applications': 0,
            'status_distribution': defaultdict(int),
            'processing_delays': [],
            'error_rate': 0,
            'recommendations': []
        }
        
        # Get all applications
        all_applications = await self.db.application_tasks.find({}).to_list(None)
        health_report['total_applications'] = len(all_applications)
        
        errors = 0
        stuck_applications = []
        
        for app in all_applications:
            # Status distribution
            health_report['status_distribution'][app['status']] += 1
            
            # Check for errors
            if app.get('error_log'):
                errors += len(app['error_log'])
            
            # Check for stuck applications (no update in 7 days)
            if app.get('last_checked'):
                last_checked = datetime.fromisoformat(app['last_checked'].replace('Z', '+00:00'))
                if (datetime.utcnow() - last_checked).days > 7 and app['status'] not in ['accepted', 'rejected']:
                    stuck_applications.append({
                        'id': app['id'],
                        'university': app['university_name'],
                        'days_since_update': (datetime.utcnow() - last_checked).days
                    })
        
        # Calculate error rate
        if all_applications:
            health_report['error_rate'] = (errors / len(all_applications)) * 100
        
        # Add stuck applications
        if stuck_applications:
            health_report['processing_delays'] = stuck_applications
            health_report['recommendations'].append(
                f"Check {len(stuck_applications)} applications with no updates in 7+ days"
            )
        
        # High error rate warning
        if health_report['error_rate'] > 10:
            health_report['recommendations'].append(
                f"High error rate detected ({health_report['error_rate']:.1f}%) - investigate automation issues"
            )
        
        return dict(health_report)
    
    async def generate_weekly_report(self, client_id: str) -> Dict[str, Any]:
        """Generate comprehensive weekly report for a client"""
        report = {
            'client_id': client_id,
            'report_date': datetime.utcnow().isoformat(),
            'period': {
                'start': (datetime.utcnow() - timedelta(days=7)).isoformat(),
                'end': datetime.utcnow().isoformat()
            },
            'summary': {},
            'details': [],
            'insights': [],
            'upcoming': []
        }
        
        # Get analytics
        analytics = await self.get_client_analytics(client_id)
        report['summary'] = analytics
        
        # Get recent status changes
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_changes = await self.db.status_changes.find({
            'timestamp': {'$gte': week_ago.isoformat()}
        }).to_list(None)
        
        for change in recent_changes:
            report['details'].append({
                'date': change['timestamp'],
                'application': change['application_id'],
                'change': f"{change['old_status']} -> {change['new_status']}"
            })
        
        # Add insights
        report['insights'] = await self.generate_insights(client_id)
        
        # Add upcoming deadlines
        report['upcoming'] = await self.check_deadlines(client_id)
        
        return report


class PerformanceMonitor:
    """Monitor system performance and automation success rates"""
    
    def __init__(self):
        self.metrics = {
            'automation_success_rate': 0,
            'average_processing_time': 0,
            'error_types': defaultdict(int),
            'university_success_rates': defaultdict(lambda: {'attempts': 0, 'successes': 0})
        }
    
    async def track_automation_attempt(self, university: str, success: bool, 
                                     processing_time: float, error_type: Optional[str] = None):
        """Track automation attempt metrics"""
        # Update university-specific metrics
        self.metrics['university_success_rates'][university]['attempts'] += 1
        if success:
            self.metrics['university_success_rates'][university]['successes'] += 1
        
        # Track errors
        if error_type:
            self.metrics['error_types'][error_type] += 1
        
        # Calculate overall success rate
        total_attempts = sum(
            data['attempts'] for data in self.metrics['university_success_rates'].values()
        )
        total_successes = sum(
            data['successes'] for data in self.metrics['university_success_rates'].values()
        )
        
        if total_attempts > 0:
            self.metrics['automation_success_rate'] = (total_successes / total_attempts) * 100
        
        # Update average processing time (running average)
        if self.metrics['average_processing_time'] == 0:
            self.metrics['average_processing_time'] = processing_time
        else:
            self.metrics['average_processing_time'] = (
                self.metrics['average_processing_time'] * 0.9 + processing_time * 0.1
            )
        
        logger.info(f"Tracked automation attempt for {university}: "
                   f"{'Success' if success else 'Failed'} in {processing_time:.2f}s")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        report = {
            'overall_success_rate': f"{self.metrics['automation_success_rate']:.1f}%",
            'average_processing_time': f"{self.metrics['average_processing_time']:.1f}s",
            'university_performance': {},
            'common_errors': []
        }
        
        # University-specific success rates
        for uni, data in self.metrics['university_success_rates'].items():
            if data['attempts'] > 0:
                success_rate = (data['successes'] / data['attempts']) * 100
                report['university_performance'][uni] = {
                    'success_rate': f"{success_rate:.1f}%",
                    'total_attempts': data['attempts']
                }
        
        # Top errors
        sorted_errors = sorted(
            self.metrics['error_types'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        report['common_errors'] = [
            {'type': error, 'count': count} 
            for error, count in sorted_errors[:5]
        ]
        
        return report 