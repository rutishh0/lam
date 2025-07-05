"""
GCP-Ready Service Manager
Manages local services with GCP Cloud Functions/Cloud Run compatible structure
"""
import os
import asyncio
import logging
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import json
import uuid
from dataclasses import dataclass, asdict
from enum import Enum
import subprocess
import signal

logger = logging.getLogger(__name__)

class ServiceStatus(Enum):
    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"

@dataclass
class ServiceConfig:
    """Service configuration"""
    name: str
    command: str
    working_directory: str
    environment: Dict[str, str]
    auto_restart: bool = True
    max_restarts: int = 3
    restart_delay: int = 5

@dataclass
class ServiceInstance:
    """Service instance tracking"""
    config: ServiceConfig
    status: ServiceStatus
    process: Optional[subprocess.Popen] = None
    start_time: Optional[datetime] = None
    restart_count: int = 0
    last_error: Optional[str] = None

class LocalServiceManager:
    """
    Local service manager with GCP-compatible structure
    This will be easily migrated to Cloud Functions/Cloud Run
    """
    
    def __init__(self):
        self.services: Dict[str, ServiceInstance] = {}
        self.task_queue = asyncio.Queue()
        self.worker_tasks: List[asyncio.Task] = []
        self.monitoring_active = False
        
        # Service definitions (GCP-ready)
        self.service_configs = {
            "browser_automation": ServiceConfig(
                name="browser_automation",
                command="python -m automation.browser_automation",
                working_directory="/app/backend",
                environment={"PYTHONPATH": "/app/backend"}
            ),
            "notification_service": ServiceConfig(
                name="notification_service",
                command="python -m notifications.notification_service",
                working_directory="/app/backend",
                environment={"PYTHONPATH": "/app/backend"}
            ),
            "status_monitor": ServiceConfig(
                name="status_monitor",
                command="python -m monitoring.status_monitor",
                working_directory="/app/backend",
                environment={"PYTHONPATH": "/app/backend"}
            )
        }
    
    async def start_service_manager(self):
        """Start the service manager"""
        logger.info("Starting GCP-ready service manager")
        self.monitoring_active = True
        
        # Start worker tasks (simulates Cloud Functions triggers)
        for i in range(3):  # 3 workers
            task = asyncio.create_task(self._worker(f"worker-{i}"))
            self.worker_tasks.append(task)
        
        # Start monitoring task
        monitor_task = asyncio.create_task(self._monitor_services())
        self.worker_tasks.append(monitor_task)
        
        logger.info("Service manager started successfully")
    
    async def stop_service_manager(self):
        """Stop the service manager"""
        logger.info("Stopping service manager")
        self.monitoring_active = False
        
        # Stop all services
        for service_name in list(self.services.keys()):
            await self.stop_service(service_name)
        
        # Cancel worker tasks
        for task in self.worker_tasks:
            task.cancel()
        
        # Wait for tasks to complete
        await asyncio.gather(*self.worker_tasks, return_exceptions=True)
        self.worker_tasks.clear()
        
        logger.info("Service manager stopped")
    
    async def _worker(self, worker_id: str):
        """Worker task to process service operations (simulates Cloud Functions)"""
        logger.info(f"Worker {worker_id} started")
        
        while self.monitoring_active:
            try:
                # Get task from queue with timeout
                task = await asyncio.wait_for(self.task_queue.get(), timeout=5.0)
                
                # Process task
                await self._process_task(task, worker_id)
                
                # Mark task as done
                self.task_queue.task_done()
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {str(e)}")
                await asyncio.sleep(1)
        
        logger.info(f"Worker {worker_id} stopped")
    
    async def _process_task(self, task: Dict[str, Any], worker_id: str):
        """Process a service task"""
        try:
            action = task.get("action")
            service_name = task.get("service_name")
            
            logger.info(f"Worker {worker_id} processing {action} for {service_name}")
            
            if action == "start":
                await self._start_service_impl(service_name)
            elif action == "stop":
                await self._stop_service_impl(service_name)
            elif action == "restart":
                await self._restart_service_impl(service_name)
            elif action == "health_check":
                await self._health_check_impl(service_name)
            else:
                logger.warning(f"Unknown action: {action}")
                
        except Exception as e:
            logger.error(f"Error processing task: {str(e)}")
    
    async def _monitor_services(self):
        """Monitor service health and restart if needed"""
        logger.info("Service monitoring started")
        
        while self.monitoring_active:
            try:
                for service_name, instance in self.services.items():
                    if instance.status == ServiceStatus.RUNNING:
                        # Check if process is still alive
                        if instance.process and instance.process.poll() is not None:
                            logger.warning(f"Service {service_name} has stopped unexpectedly")
                            instance.status = ServiceStatus.FAILED
                            
                            # Auto-restart if enabled
                            if instance.config.auto_restart and instance.restart_count < instance.config.max_restarts:
                                logger.info(f"Auto-restarting service {service_name}")
                                await self.queue_task("restart", service_name)
                
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in service monitoring: {str(e)}")
                await asyncio.sleep(30)
        
        logger.info("Service monitoring stopped")
    
    async def queue_task(self, action: str, service_name: str, **kwargs):
        """Queue a service task (simulates Cloud Tasks)"""
        task = {
            "action": action,
            "service_name": service_name,
            "timestamp": datetime.utcnow().isoformat(),
            "task_id": str(uuid.uuid4()),
            **kwargs
        }
        
        await self.task_queue.put(task)
        logger.info(f"Queued task: {action} for {service_name}")
    
    async def start_service(self, service_name: str) -> bool:
        """Start a service"""
        await self.queue_task("start", service_name)
        return True
    
    async def stop_service(self, service_name: str) -> bool:
        """Stop a service"""
        await self.queue_task("stop", service_name)
        return True
    
    async def restart_service(self, service_name: str) -> bool:
        """Restart a service"""
        await self.queue_task("restart", service_name)
        return True
    
    async def _start_service_impl(self, service_name: str):
        """Actually start a service"""
        try:
            if service_name not in self.service_configs:
                raise ValueError(f"Unknown service: {service_name}")
            
            config = self.service_configs[service_name]
            
            # Check if already running
            if service_name in self.services:
                instance = self.services[service_name]
                if instance.status == ServiceStatus.RUNNING:
                    logger.info(f"Service {service_name} is already running")
                    return
            
            # Create service instance
            instance = ServiceInstance(
                config=config,
                status=ServiceStatus.STARTING,
                start_time=datetime.utcnow()
            )
            self.services[service_name] = instance
            
            # Start the process (in production, this would be a Cloud Function deployment)
            logger.info(f"Starting service {service_name}")
            
            # For now, we'll simulate service startup
            # In GCP, this would deploy/start a Cloud Function or Cloud Run service
            await asyncio.sleep(2)  # Simulate startup time
            
            instance.status = ServiceStatus.RUNNING
            logger.info(f"Service {service_name} started successfully")
            
        except Exception as e:
            error_msg = f"Failed to start service {service_name}: {str(e)}"
            logger.error(error_msg)
            
            if service_name in self.services:
                self.services[service_name].status = ServiceStatus.FAILED
                self.services[service_name].last_error = error_msg
    
    async def _stop_service_impl(self, service_name: str):
        """Actually stop a service"""
        try:
            if service_name not in self.services:
                logger.warning(f"Service {service_name} is not running")
                return
            
            instance = self.services[service_name]
            instance.status = ServiceStatus.STOPPING
            
            logger.info(f"Stopping service {service_name}")
            
            # Stop the process
            if instance.process:
                instance.process.terminate()
                try:
                    instance.process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    instance.process.kill()
                    instance.process.wait()
            
            instance.status = ServiceStatus.STOPPED
            instance.process = None
            
            logger.info(f"Service {service_name} stopped successfully")
            
        except Exception as e:
            error_msg = f"Failed to stop service {service_name}: {str(e)}"
            logger.error(error_msg)
            
            if service_name in self.services:
                self.services[service_name].last_error = error_msg
    
    async def _restart_service_impl(self, service_name: str):
        """Actually restart a service"""
        logger.info(f"Restarting service {service_name}")
        
        # Stop first
        await self._stop_service_impl(service_name)
        
        # Wait a bit
        if service_name in self.services:
            delay = self.services[service_name].config.restart_delay
            await asyncio.sleep(delay)
        
        # Start again
        await self._start_service_impl(service_name)
        
        # Increment restart count
        if service_name in self.services:
            self.services[service_name].restart_count += 1
    
    async def _health_check_impl(self, service_name: str):
        """Perform health check on a service"""
        try:
            if service_name not in self.services:
                return {"status": "not_running", "healthy": False}
            
            instance = self.services[service_name]
            
            # Basic health check (in GCP, this would be a health check endpoint)
            if instance.status == ServiceStatus.RUNNING:
                if instance.process and instance.process.poll() is None:
                    return {"status": "running", "healthy": True, "uptime": datetime.utcnow() - instance.start_time}
                else:
                    return {"status": "failed", "healthy": False, "error": "Process not responding"}
            else:
                return {"status": instance.status.value, "healthy": False}
                
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {str(e)}")
            return {"status": "error", "healthy": False, "error": str(e)}
    
    def get_service_status(self, service_name: str) -> Dict[str, Any]:
        """Get service status"""
        if service_name not in self.services:
            return {"status": "not_found", "exists": False}
        
        instance = self.services[service_name]
        return {
            "name": service_name,
            "status": instance.status.value,
            "start_time": instance.start_time.isoformat() if instance.start_time else None,
            "restart_count": instance.restart_count,
            "last_error": instance.last_error,
            "config": asdict(instance.config)
        }
    
    def get_all_services_status(self) -> Dict[str, Any]:
        """Get status of all services"""
        return {
            "services": {name: self.get_service_status(name) for name in self.services},
            "total_services": len(self.services),
            "running_services": len([s for s in self.services.values() if s.status == ServiceStatus.RUNNING]),
            "manager_status": "active" if self.monitoring_active else "inactive"
        }

# Global service manager instance
service_manager = LocalServiceManager()

async def start_background_services():
    """Start background service management"""
    try:
        await service_manager.start_service_manager()
    except Exception as e:
        logger.error(f"Error starting service manager: {str(e)}")

def get_service_manager() -> LocalServiceManager:
    """Get the global service manager instance"""
    return service_manager