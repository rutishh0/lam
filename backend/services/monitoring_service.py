"""
Monitoring Service for AI LAM

Enhanced monitoring service following Suna's patterns for system health and performance tracking.
"""

import asyncio
import logging
import psutil
import time
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from services.database_service import get_database_service
from utils.config import get_config

logger = logging.getLogger(__name__)

class MonitoringError(Exception):
    """Base exception for monitoring-related errors."""
    pass

class MonitoringService:
    """Enhanced monitoring service for system health and performance."""
    
    def __init__(self):
        self.config = get_config()
        self.db_service = get_database_service()
        self._initialized = False
        self._monitoring_task = None
        self._metrics_cache = {}
    
    async def initialize(self) -> None:
        """Initialize the monitoring service."""
        if self._initialized:
            return
        
        try:
            # Ensure dependencies are initialized
            await self.db_service.initialize()
            
            # Start background monitoring
            self._monitoring_task = asyncio.create_task(self._background_monitoring())
            
            self._initialized = True
            logger.info("Monitoring service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize monitoring service: {e}")
            raise MonitoringError(f"Monitoring service initialization failed: {str(e)}")
    
    async def shutdown(self) -> None:
        """Shutdown the monitoring service."""
        if self._monitoring_task:
            self._monitoring_task.cancel()
            try:
                await self._monitoring_task
            except asyncio.CancelledError:
                pass
        
        self._initialized = False
        logger.info("Monitoring service shutdown complete")
    
    async def _background_monitoring(self) -> None:
        """Background task for continuous monitoring."""
        while True:
            try:
                # Collect system metrics
                metrics = await self.collect_system_metrics()
                self._metrics_cache = metrics
                
                # Store metrics in database (optional)
                if self.config.is_production:
                    await self._store_metrics(metrics)
                
                # Check for alerts
                await self._check_alerts(metrics)
                
                # Sleep for monitoring interval (60 seconds)
                await asyncio.sleep(60)
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error in background monitoring: {e}")
                await asyncio.sleep(30)  # Shorter sleep on error
    
    async def collect_system_metrics(self) -> Dict[str, Any]:
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available
            memory_total = memory.total
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            disk_free = disk.free
            disk_total = disk.total
            
            # Network metrics (basic)
            network = psutil.net_io_counters()
            
            # Process metrics
            process = psutil.Process()
            process_memory = process.memory_info()
            process_cpu = process.cpu_percent()
            
            metrics = {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'cpu': {
                    'percent': cpu_percent,
                    'count': cpu_count
                },
                'memory': {
                    'percent': memory_percent,
                    'available_bytes': memory_available,
                    'total_bytes': memory_total,
                    'used_bytes': memory_total - memory_available
                },
                'disk': {
                    'percent': disk_percent,
                    'free_bytes': disk_free,
                    'total_bytes': disk_total,
                    'used_bytes': disk.used
                },
                'network': {
                    'bytes_sent': network.bytes_sent,
                    'bytes_recv': network.bytes_recv,
                    'packets_sent': network.packets_sent,
                    'packets_recv': network.packets_recv
                },
                'process': {
                    'cpu_percent': process_cpu,
                    'memory_rss': process_memory.rss,
                    'memory_vms': process_memory.vms
                }
            }
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            raise MonitoringError(f"Failed to collect metrics: {str(e)}")
    
    async def _store_metrics(self, metrics: Dict[str, Any]) -> None:
        """Store metrics in database."""
        try:
            await self.db_service.client.table('system_metrics').insert({
                'timestamp': metrics['timestamp'],
                'metrics': metrics
            }).execute()
            
        except Exception as e:
            logger.error(f"Error storing metrics: {e}")
    
    async def _check_alerts(self, metrics: Dict[str, Any]) -> None:
        """Check metrics against alert thresholds."""
        alerts = []
        
        # CPU alert
        if metrics['cpu']['percent'] > 90:
            alerts.append({
                'type': 'high_cpu',
                'severity': 'critical',
                'message': f"High CPU usage: {metrics['cpu']['percent']:.1f}%"
            })
        elif metrics['cpu']['percent'] > 75:
            alerts.append({
                'type': 'elevated_cpu',
                'severity': 'warning',
                'message': f"Elevated CPU usage: {metrics['cpu']['percent']:.1f}%"
            })
        
        # Memory alert
        if metrics['memory']['percent'] > 90:
            alerts.append({
                'type': 'high_memory',
                'severity': 'critical',
                'message': f"High memory usage: {metrics['memory']['percent']:.1f}%"
            })
        elif metrics['memory']['percent'] > 80:
            alerts.append({
                'type': 'elevated_memory',
                'severity': 'warning',
                'message': f"Elevated memory usage: {metrics['memory']['percent']:.1f}%"
            })
        
        # Disk alert
        if metrics['disk']['percent'] > 95:
            alerts.append({
                'type': 'disk_full',
                'severity': 'critical',
                'message': f"Disk almost full: {metrics['disk']['percent']:.1f}%"
            })
        elif metrics['disk']['percent'] > 85:
            alerts.append({
                'type': 'disk_high',
                'severity': 'warning',
                'message': f"High disk usage: {metrics['disk']['percent']:.1f}%"
            })
        
        # Process alerts
        if len(alerts) > 0:
            for alert in alerts:
                logger.warning(f"System alert: {alert['message']}")
                
                # Store alert in database
                try:
                    await self.db_service.client.table('system_alerts').insert({
                        'timestamp': metrics['timestamp'],
                        'type': alert['type'],
                        'severity': alert['severity'],
                        'message': alert['message'],
                        'metrics': metrics
                    }).execute()
                except Exception as e:
                    logger.error(f"Error storing alert: {e}")
    
    def get_cached_metrics(self) -> Dict[str, Any]:
        """Get the most recently cached metrics."""
        return self._metrics_cache.copy()
    
    async def get_health_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            metrics = await self.collect_system_metrics()
            
            # Determine overall health
            health_score = 100
            status = "healthy"
            issues = []
            
            # Check CPU
            if metrics['cpu']['percent'] > 90:
                health_score -= 30
                status = "critical"
                issues.append("High CPU usage")
            elif metrics['cpu']['percent'] > 75:
                health_score -= 15
                if status == "healthy":
                    status = "warning"
                issues.append("Elevated CPU usage")
            
            # Check Memory
            if metrics['memory']['percent'] > 90:
                health_score -= 30
                status = "critical"
                issues.append("High memory usage")
            elif metrics['memory']['percent'] > 80:
                health_score -= 15
                if status == "healthy":
                    status = "warning"
                issues.append("Elevated memory usage")
            
            # Check Disk
            if metrics['disk']['percent'] > 95:
                health_score -= 25
                status = "critical"
                issues.append("Disk almost full")
            elif metrics['disk']['percent'] > 85:
                health_score -= 10
                if status == "healthy":
                    status = "warning"
                issues.append("High disk usage")
            
            # Test database connectivity
            try:
                await self.db_service._test_connection()
            except Exception:
                health_score -= 50
                status = "critical"
                issues.append("Database connectivity issues")
            
            health_score = max(0, health_score)
            
            return {
                'status': status,
                'health_score': health_score,
                'timestamp': metrics['timestamp'],
                'issues': issues,
                'metrics': metrics,
                'services': {
                    'database': 'connected' if not any('Database' in issue for issue in issues) else 'disconnected',
                    'monitoring': 'active',
                    'automation': 'active' if self.config.ENABLE_AUTOMATION else 'disabled',
                    'notifications': 'active' if self.config.ENABLE_NOTIFICATIONS else 'disabled'
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting health status: {e}")
            return {
                'status': 'error',
                'health_score': 0,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'issues': [f"Health check failed: {str(e)}"],
                'metrics': {},
                'services': {}
            }
    
    async def get_performance_stats(
        self,
        hours: int = 24
    ) -> Dict[str, Any]:
        """Get performance statistics for the specified time period."""
        try:
            # Query metrics from database
            since = datetime.now(timezone.utc).timestamp() - (hours * 3600)
            
            result = await self.db_service.client.table('system_metrics').select('*').gte(
                'timestamp', datetime.fromtimestamp(since, timezone.utc).isoformat()
            ).order('timestamp', desc=False).execute()
            
            if not result.data:
                return {'message': 'No performance data available'}
            
            # Aggregate statistics
            cpu_values = [m['metrics']['cpu']['percent'] for m in result.data]
            memory_values = [m['metrics']['memory']['percent'] for m in result.data]
            disk_values = [m['metrics']['disk']['percent'] for m in result.data]
            
            return {
                'period_hours': hours,
                'data_points': len(result.data),
                'cpu': {
                    'avg': sum(cpu_values) / len(cpu_values),
                    'max': max(cpu_values),
                    'min': min(cpu_values)
                },
                'memory': {
                    'avg': sum(memory_values) / len(memory_values),
                    'max': max(memory_values),
                    'min': min(memory_values)
                },
                'disk': {
                    'avg': sum(disk_values) / len(disk_values),
                    'max': max(disk_values),
                    'min': min(disk_values)
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting performance stats: {e}")
            raise MonitoringError(f"Failed to get performance stats: {str(e)}")

# Global instance
_monitoring_service = None

def get_monitoring_service() -> MonitoringService:
    """Get or create the global monitoring service instance."""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = MonitoringService()
    return _monitoring_service 