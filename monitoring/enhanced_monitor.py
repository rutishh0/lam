"""
Enhanced Monitoring System for GCP-ready architecture
"""
import psutil
import time
import random
from datetime import datetime, timedelta
import logging
import json
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class EnhancedMonitoringService:
    """Enhanced monitoring service with metrics collection and alerting"""
    
    def __init__(self):
        self.monitoring_active = True
        self._metrics_history = {}
        self._alerts = []
        self._alert_thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0,
            "error_rate": 5.0,
            "response_time": 2.0
        }
        
        # Initialize with some mock history data
        self._initialize_mock_history()
    
    def _initialize_mock_history(self):
        """Initialize mock history data for testing"""
        now = datetime.utcnow()
        history = {}
        
        # Generate 24 hours of mock data
        for i in range(24):
            timestamp = (now - timedelta(hours=24-i)).isoformat()
            history[timestamp] = {
                "system": {
                    "cpu_usage": random.uniform(10, 70),
                    "memory_usage": random.uniform(20, 80),
                    "disk_usage": random.uniform(30, 70),
                    "network_in": random.uniform(100, 5000),
                    "network_out": random.uniform(100, 3000)
                },
                "application": {
                    "active_users": random.randint(5, 50),
                    "requests_per_minute": random.randint(50, 500),
                    "error_rate": random.uniform(0, 3),
                    "average_response_time": random.uniform(0.1, 1.5)
                },
                "database": {
                    "connections": random.randint(5, 20),
                    "query_time": random.uniform(0.01, 0.2),
                    "active_transactions": random.randint(1, 10)
                }
            }
        
        self._metrics_history = history
        
        # Generate some mock alerts
        severities = ["INFO", "WARNING", "CRITICAL"]
        alert_types = [
            "High CPU Usage", "Memory Pressure", "Disk Space Low",
            "High Error Rate", "Slow Response Time", "Database Connection Issues"
        ]
        
        for i in range(10):
            timestamp = (now - timedelta(hours=random.randint(1, 24))).isoformat()
            self._alerts.append({
                "id": f"alert-{i+1}",
                "timestamp": timestamp,
                "type": random.choice(alert_types),
                "severity": random.choice(severities),
                "message": f"Alert triggered for {random.choice(alert_types).lower()}",
                "value": random.uniform(70, 95) if "High" in alert_types[i % len(alert_types)] else random.uniform(1, 5),
                "threshold": random.uniform(70, 90) if "High" in alert_types[i % len(alert_types)] else random.uniform(1, 3),
                "component": random.choice(["system", "application", "database"]),
                "resolved": random.choice([True, False])
            })
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system and application metrics"""
        try:
            # Get real system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Mock application metrics
            current_metrics = {
                "timestamp": datetime.utcnow().isoformat(),
                "system": {
                    "cpu_usage": round(cpu_percent, 1),
                    "memory_usage": round(memory.percent, 1),
                    "memory_available_gb": round(memory.available / (1024**3), 2),
                    "disk_usage": round(disk.percent, 1),
                    "disk_free_gb": round(disk.free / (1024**3), 2),
                    "network_in_kbps": round(random.uniform(100, 5000), 1),
                    "network_out_kbps": round(random.uniform(100, 3000), 1)
                },
                "application": {
                    "active_users": random.randint(5, 50),
                    "requests_per_minute": random.randint(50, 500),
                    "error_rate": round(random.uniform(0, 3), 2),
                    "average_response_time": round(random.uniform(0.1, 1.5), 2),
                    "active_sessions": random.randint(10, 100)
                },
                "database": {
                    "connections": random.randint(5, 20),
                    "query_time_ms": round(random.uniform(10, 200), 1),
                    "active_transactions": random.randint(1, 10),
                    "connection_pool_usage": round(random.uniform(10, 80), 1)
                }
            }
            
            # Check for alert conditions
            self._check_alert_conditions(current_metrics)
            
            # Store in history
            self._metrics_history[current_metrics["timestamp"]] = current_metrics
            
            return current_metrics
            
        except Exception as e:
            logger.error(f"Error getting current metrics: {str(e)}")
            return {
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "status": "error"
            }
    
    def _check_alert_conditions(self, metrics: Dict[str, Any]):
        """Check for alert conditions based on current metrics"""
        now = datetime.utcnow().isoformat()
        
        # Check CPU usage
        if metrics["system"]["cpu_usage"] > self._alert_thresholds["cpu_usage"]:
            self._alerts.append({
                "id": f"alert-{len(self._alerts)+1}",
                "timestamp": now,
                "type": "High CPU Usage",
                "severity": "WARNING" if metrics["system"]["cpu_usage"] < 90 else "CRITICAL",
                "message": f"CPU usage is {metrics['system']['cpu_usage']}%, above threshold of {self._alert_thresholds['cpu_usage']}%",
                "value": metrics["system"]["cpu_usage"],
                "threshold": self._alert_thresholds["cpu_usage"],
                "component": "system",
                "resolved": False
            })
        
        # Check memory usage
        if metrics["system"]["memory_usage"] > self._alert_thresholds["memory_usage"]:
            self._alerts.append({
                "id": f"alert-{len(self._alerts)+1}",
                "timestamp": now,
                "type": "Memory Pressure",
                "severity": "WARNING" if metrics["system"]["memory_usage"] < 95 else "CRITICAL",
                "message": f"Memory usage is {metrics['system']['memory_usage']}%, above threshold of {self._alert_thresholds['memory_usage']}%",
                "value": metrics["system"]["memory_usage"],
                "threshold": self._alert_thresholds["memory_usage"],
                "component": "system",
                "resolved": False
            })
        
        # Check disk usage
        if metrics["system"]["disk_usage"] > self._alert_thresholds["disk_usage"]:
            self._alerts.append({
                "id": f"alert-{len(self._alerts)+1}",
                "timestamp": now,
                "type": "Disk Space Low",
                "severity": "WARNING" if metrics["system"]["disk_usage"] < 95 else "CRITICAL",
                "message": f"Disk usage is {metrics['system']['disk_usage']}%, above threshold of {self._alert_thresholds['disk_usage']}%",
                "value": metrics["system"]["disk_usage"],
                "threshold": self._alert_thresholds["disk_usage"],
                "component": "system",
                "resolved": False
            })
        
        # Check error rate
        if metrics["application"]["error_rate"] > self._alert_thresholds["error_rate"]:
            self._alerts.append({
                "id": f"alert-{len(self._alerts)+1}",
                "timestamp": now,
                "type": "High Error Rate",
                "severity": "WARNING" if metrics["application"]["error_rate"] < 10 else "CRITICAL",
                "message": f"Error rate is {metrics['application']['error_rate']}%, above threshold of {self._alert_thresholds['error_rate']}%",
                "value": metrics["application"]["error_rate"],
                "threshold": self._alert_thresholds["error_rate"],
                "component": "application",
                "resolved": False
            })
        
        # Check response time
        if metrics["application"]["average_response_time"] > self._alert_thresholds["response_time"]:
            self._alerts.append({
                "id": f"alert-{len(self._alerts)+1}",
                "timestamp": now,
                "type": "Slow Response Time",
                "severity": "WARNING" if metrics["application"]["average_response_time"] < 5 else "CRITICAL",
                "message": f"Average response time is {metrics['application']['average_response_time']}s, above threshold of {self._alert_thresholds['response_time']}s",
                "value": metrics["application"]["average_response_time"],
                "threshold": self._alert_thresholds["response_time"],
                "component": "application",
                "resolved": False
            })
    
    def get_metrics_history(self, hours: int = 24) -> Dict[str, Any]:
        """Get metrics history for the specified number of hours"""
        try:
            now = datetime.utcnow()
            cutoff = now - timedelta(hours=hours)
            
            # Filter history by timestamp
            filtered_history = {
                ts: metrics for ts, metrics in self._metrics_history.items()
                if datetime.fromisoformat(ts) >= cutoff
            }
            
            # Prepare time series data
            time_series = {
                "timestamps": [],
                "cpu_usage": [],
                "memory_usage": [],
                "disk_usage": [],
                "active_users": [],
                "requests_per_minute": [],
                "error_rate": [],
                "response_time": []
            }
            
            # Sort by timestamp
            for ts in sorted(filtered_history.keys()):
                metrics = filtered_history[ts]
                time_series["timestamps"].append(ts)
                time_series["cpu_usage"].append(metrics["system"]["cpu_usage"])
                time_series["memory_usage"].append(metrics["system"]["memory_usage"])
                time_series["disk_usage"].append(metrics["system"]["disk_usage"])
                time_series["active_users"].append(metrics["application"]["active_users"])
                time_series["requests_per_minute"].append(metrics["application"]["requests_per_minute"])
                time_series["error_rate"].append(metrics["application"]["error_rate"])
                time_series["response_time"].append(metrics["application"]["average_response_time"])
            
            return {
                "time_series": time_series,
                "start_time": cutoff.isoformat(),
                "end_time": now.isoformat(),
                "data_points": len(time_series["timestamps"])
            }
            
        except Exception as e:
            logger.error(f"Error getting metrics history: {str(e)}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    def get_recent_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent monitoring alerts"""
        try:
            # Sort alerts by timestamp (newest first)
            sorted_alerts = sorted(
                self._alerts,
                key=lambda x: datetime.fromisoformat(x["timestamp"]),
                reverse=True
            )
            
            return sorted_alerts[:limit]
            
        except Exception as e:
            logger.error(f"Error getting recent alerts: {str(e)}")
            return [{"error": str(e), "status": "error"}]
    
    def clear_alerts(self) -> bool:
        """Clear all monitoring alerts"""
        try:
            self._alerts = []
            return True
        except Exception as e:
            logger.error(f"Error clearing alerts: {str(e)}")
            return False
    
    def set_alert_threshold(self, metric: str, value: float) -> bool:
        """Set alert threshold for a specific metric"""
        try:
            if metric in self._alert_thresholds:
                self._alert_thresholds[metric] = value
                return True
            return False
        except Exception as e:
            logger.error(f"Error setting alert threshold: {str(e)}")
            return False

# Singleton instance
_monitoring_service = None

def get_monitoring_service() -> EnhancedMonitoringService:
    """Get or create the monitoring service singleton"""
    global _monitoring_service
    if _monitoring_service is None:
        _monitoring_service = EnhancedMonitoringService()
    return _monitoring_service