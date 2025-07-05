"""
Enhanced Local Monitoring Service
Provides comprehensive system monitoring capabilities that will be GCP-ready
"""
import os
import psutil
import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import json
import uuid
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import aiofiles

logger = logging.getLogger(__name__)

@dataclass
class SystemMetric:
    """System performance metric"""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    memory_available: float
    disk_usage: float
    disk_free: float
    active_connections: int
    error_count: int

@dataclass
class ApplicationMetric:
    """Application performance metric"""
    timestamp: datetime
    active_sessions: int
    requests_per_minute: int
    average_response_time: float
    error_rate: float
    successful_operations: int
    failed_operations: int

class LocalMonitoringService:
    """
    Enhanced monitoring service for local development
    Structured to be easily migrated to GCP Cloud Monitoring
    """
    
    def __init__(self, storage_path: str = "/tmp/monitoring_data"):
        self.storage_path = storage_path
        self.metrics_buffer = deque(maxlen=1000)  # Keep last 1000 metrics
        self.application_metrics = deque(maxlen=1000)
        self.alerts = []
        self.monitoring_active = False
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Performance thresholds
        self.thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "error_rate": 5.0,
            "response_time": 2.0
        }
        
    async def start_monitoring(self, interval: int = 60):
        """Start continuous monitoring"""
        self.monitoring_active = True
        logger.info("Starting enhanced monitoring service")
        
        while self.monitoring_active:
            try:
                # Collect system metrics
                system_metric = await self._collect_system_metrics()
                self.metrics_buffer.append(system_metric)
                
                # Collect application metrics
                app_metric = await self._collect_application_metrics()
                self.application_metrics.append(app_metric)
                
                # Check for alerts
                await self._check_alerts(system_metric, app_metric)
                
                # Persist metrics
                await self._persist_metrics()
                
                await asyncio.sleep(interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                await asyncio.sleep(interval)
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring_active = False
        logger.info("Monitoring service stopped")
    
    async def _collect_system_metrics(self) -> SystemMetric:
        """Collect system performance metrics"""
        try:
            # CPU usage
            cpu_usage = psutil.cpu_percent(interval=1)
            
            # Memory usage
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            memory_available = memory.available / (1024**3)  # GB
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_usage = disk.percent
            disk_free = disk.free / (1024**3)  # GB
            
            # Network connections
            connections = len(psutil.net_connections())
            
            return SystemMetric(
                timestamp=datetime.utcnow(),
                cpu_usage=round(cpu_usage, 2),
                memory_usage=round(memory_usage, 2),
                memory_available=round(memory_available, 2),
                disk_usage=round(disk_usage, 2),
                disk_free=round(disk_free, 2),
                active_connections=connections,
                error_count=0  # To be implemented with actual error tracking
            )
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {str(e)}")
            return SystemMetric(
                timestamp=datetime.utcnow(),
                cpu_usage=0, memory_usage=0, memory_available=0,
                disk_usage=0, disk_free=0, active_connections=0, error_count=1
            )
    
    async def _collect_application_metrics(self) -> ApplicationMetric:
        """Collect application performance metrics"""
        try:
            # Mock application metrics for now
            # In production, these would come from actual application monitoring
            import random
            
            return ApplicationMetric(
                timestamp=datetime.utcnow(),
                active_sessions=random.randint(10, 100),
                requests_per_minute=random.randint(50, 500),
                average_response_time=round(random.uniform(0.1, 2.0), 3),
                error_rate=round(random.uniform(0.0, 10.0), 2),
                successful_operations=random.randint(100, 1000),
                failed_operations=random.randint(0, 50)
            )
            
        except Exception as e:
            logger.error(f"Error collecting application metrics: {str(e)}")
            return ApplicationMetric(
                timestamp=datetime.utcnow(),
                active_sessions=0, requests_per_minute=0,
                average_response_time=0, error_rate=100,
                successful_operations=0, failed_operations=1
            )
    
    async def _check_alerts(self, system_metric: SystemMetric, app_metric: ApplicationMetric):
        """Check metrics against thresholds and generate alerts"""
        alerts = []
        
        # System alerts
        if system_metric.cpu_usage > self.thresholds["cpu_usage"]:
            alerts.append({
                "type": "HIGH_CPU_USAGE",
                "message": f"CPU usage is {system_metric.cpu_usage}% (threshold: {self.thresholds['cpu_usage']}%)",
                "severity": "WARNING",
                "timestamp": system_metric.timestamp.isoformat()
            })
        
        if system_metric.memory_usage > self.thresholds["memory_usage"]:
            alerts.append({
                "type": "HIGH_MEMORY_USAGE",
                "message": f"Memory usage is {system_metric.memory_usage}% (threshold: {self.thresholds['memory_usage']}%)",
                "severity": "WARNING",
                "timestamp": system_metric.timestamp.isoformat()
            })
        
        if system_metric.disk_usage > self.thresholds["disk_usage"]:
            alerts.append({
                "type": "HIGH_DISK_USAGE",
                "message": f"Disk usage is {system_metric.disk_usage}% (threshold: {self.thresholds['disk_usage']}%)",
                "severity": "CRITICAL",
                "timestamp": system_metric.timestamp.isoformat()
            })
        
        # Application alerts
        if app_metric.error_rate > self.thresholds["error_rate"]:
            alerts.append({
                "type": "HIGH_ERROR_RATE",
                "message": f"Error rate is {app_metric.error_rate}% (threshold: {self.thresholds['error_rate']}%)",
                "severity": "CRITICAL",
                "timestamp": app_metric.timestamp.isoformat()
            })
        
        if app_metric.average_response_time > self.thresholds["response_time"]:
            alerts.append({
                "type": "SLOW_RESPONSE_TIME",
                "message": f"Average response time is {app_metric.average_response_time}s (threshold: {self.thresholds['response_time']}s)",
                "severity": "WARNING",
                "timestamp": app_metric.timestamp.isoformat()
            })
        
        # Store alerts
        self.alerts.extend(alerts)
        
        # Log critical alerts
        for alert in alerts:
            if alert["severity"] == "CRITICAL":
                logger.critical(f"ALERT: {alert['message']}")
            else:
                logger.warning(f"ALERT: {alert['message']}")
    
    async def _persist_metrics(self):
        """Persist metrics to local storage (GCP-ready format)"""
        try:
            # Create timestamped filename
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H")
            
            # Save system metrics
            system_file = f"{self.storage_path}/system_metrics_{timestamp}.json"
            if len(self.metrics_buffer) > 0:
                system_data = [asdict(metric) for metric in list(self.metrics_buffer)[-10:]]  # Last 10 metrics
                async with aiofiles.open(system_file, 'w') as f:
                    await f.write(json.dumps(system_data, default=str, indent=2))
            
            # Save application metrics
            app_file = f"{self.storage_path}/app_metrics_{timestamp}.json"
            if len(self.application_metrics) > 0:
                app_data = [asdict(metric) for metric in list(self.application_metrics)[-10:]]  # Last 10 metrics
                async with aiofiles.open(app_file, 'w') as f:
                    await f.write(json.dumps(app_data, default=str, indent=2))
            
            # Save alerts
            if self.alerts:
                alerts_file = f"{self.storage_path}/alerts_{timestamp}.json"
                async with aiofiles.open(alerts_file, 'w') as f:
                    await f.write(json.dumps(self.alerts[-10:], default=str, indent=2))  # Last 10 alerts
                    
        except Exception as e:
            logger.error(f"Error persisting metrics: {str(e)}")
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system and application metrics"""
        try:
            system_metric = list(self.metrics_buffer)[-1] if self.metrics_buffer else None
            app_metric = list(self.application_metrics)[-1] if self.application_metrics else None
            
            return {
                "system": asdict(system_metric) if system_metric else {},
                "application": asdict(app_metric) if app_metric else {},
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting current metrics: {str(e)}")
            return {}
    
    def get_metrics_history(self, hours: int = 24) -> Dict[str, List[Dict]]:
        """Get metrics history for the specified number of hours"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours)
            
            # Filter system metrics
            system_history = [
                asdict(metric) for metric in self.metrics_buffer
                if metric.timestamp >= cutoff_time
            ]
            
            # Filter application metrics
            app_history = [
                asdict(metric) for metric in self.application_metrics
                if metric.timestamp >= cutoff_time
            ]
            
            return {
                "system": system_history,
                "application": app_history,
                "period_hours": hours
            }
        except Exception as e:
            logger.error(f"Error getting metrics history: {str(e)}")
            return {"system": [], "application": [], "period_hours": hours}
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Get recent alerts"""
        return self.alerts[-limit:] if self.alerts else []
    
    def clear_alerts(self):
        """Clear all alerts"""
        self.alerts.clear()
        logger.info("Alerts cleared")
    
    def update_thresholds(self, new_thresholds: Dict[str, float]):
        """Update monitoring thresholds"""
        self.thresholds.update(new_thresholds)
        logger.info(f"Monitoring thresholds updated: {new_thresholds}")

# Global monitoring service instance
monitoring_service = LocalMonitoringService()

async def start_background_monitoring():
    """Start background monitoring task"""
    try:
        await monitoring_service.start_monitoring(interval=60)  # Monitor every minute
    except Exception as e:
        logger.error(f"Error starting background monitoring: {str(e)}")

def get_monitoring_service() -> LocalMonitoringService:
    """Get the global monitoring service instance"""
    return monitoring_service