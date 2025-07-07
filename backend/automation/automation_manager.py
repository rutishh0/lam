"""
Advanced Automation Manager with Real-time Browser Control and Streaming
Integrates with admin panel for live monitoring and control
"""

import asyncio
import json
import uuid
import base64
import logging
from typing import Dict, Any, Optional, List, Callable
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from enum import Enum
import os
import platform

from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from fastapi import WebSocket, WebSocketDisconnect

from .browser_automation import EnhancedBrowserAutomation

logger = logging.getLogger(__name__)

class SessionStatus(Enum):
    IDLE = "idle"
    INITIALIZING = "initializing"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"
    STOPPED = "stopped"

@dataclass
class AutomationSession:
    """Represents an active automation session"""
    session_id: str
    client_id: str
    university_name: str
    status: SessionStatus
    browser: Optional[Browser]
    context: Optional[BrowserContext]
    page: Optional[Page]
    websocket: Optional[WebSocket]
    created_at: datetime
    last_activity: datetime
    logs: List[Dict[str, Any]]
    screenshots: List[str]
    current_step: str
    progress: int
    error_message: Optional[str]

class AutomationManager:
    """Manages multiple automation sessions with real-time control"""
    
    def __init__(self):
        self.sessions: Dict[str, AutomationSession] = {}
        self.active_websockets: Dict[str, WebSocket] = {}
        self.playwright = None
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    async def initialize(self):
        """Initialize the automation manager with production optimizations"""
        try:
            # Production environment detection
            is_production = os.getenv("ENVIRONMENT") == "production"
            is_linux = platform.system() == "Linux"
            
            if is_production and is_linux:
                logger.info("Initializing Automation Manager for production Linux environment")
            
            self.playwright = await async_playwright().start()
            
            # Test browser launch with production settings
            if is_production and is_linux:
                # Launch browser with production settings
                browser = await self.playwright.chromium.launch(
                    headless=True,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--no-first-run',
                        '--no-zygote',
                        '--single-process',
                        '--disable-gpu'
                    ]
                )
                await browser.close()
                logger.info("Production browser test successful")
            
            logger.info("Automation Manager initialized successfully")
            return True
            
        except NotImplementedError as e:
            logger.warning(f"Playwright not supported on this platform: {e}")
            logger.warning("Automation features will be limited - browser automation disabled")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Automation Manager: {e}")
            logger.warning("Automation features will be limited")
            return False

    async def create_session(self, client_id: str, university_name: str, websocket: WebSocket) -> str:
        """Create a new automation session"""
        session_id = str(uuid.uuid4())
        
        session = AutomationSession(
            session_id=session_id,
            client_id=client_id,
            university_name=university_name,
            status=SessionStatus.INITIALIZING,
            browser=None,
            context=None,
            page=None,
            websocket=websocket,
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow(),
            logs=[],
            screenshots=[],
            current_step="Initializing",
            progress=0,
            error_message=None
        )
        
        self.sessions[session_id] = session
        self.active_websockets[session_id] = websocket
        
        # Send initial status to websocket
        await self.send_status_update(session_id)
        
        logger.info(f"Created automation session {session_id} for client {client_id}")
        return session_id

    async def start_automation(self, session_id: str, client_data: Dict[str, Any]) -> bool:
        """Start the automation process for a session"""
        if session_id not in self.sessions:
            logger.error(f"Session {session_id} not found")
            return False
            
        session = self.sessions[session_id]
        
        try:
            session.status = SessionStatus.RUNNING
            session.current_step = "Starting browser"
            session.progress = 10
            await self.send_status_update(session_id)
            
            # Initialize browser with stealth mode
            browser_automation = EnhancedBrowserAutomation()
            session.context = await browser_automation.initialize_stealth_browser()
            session.browser = session.context.browser
            session.page = await session.context.new_page()
            
            # Set up page event listeners for real-time monitoring
            await self.setup_page_monitoring(session_id)
            
            session.current_step = "Browser ready"
            session.progress = 20
            await self.send_status_update(session_id)
            
            # Start the automation process
            await self.run_automation_steps(session_id, client_data)
            
            return True
            
        except Exception as e:
            session.status = SessionStatus.ERROR
            session.error_message = str(e)
            session.current_step = f"Error: {str(e)}"
            await self.send_status_update(session_id)
            logger.error(f"Failed to start automation for session {session_id}: {e}")
            return False

    async def setup_page_monitoring(self, session_id: str):
        """Set up real-time page monitoring"""
        session = self.sessions[session_id]
        page = session.page
        
        # Page load event
        page.on("load", lambda: asyncio.create_task(
            self.on_page_event(session_id, "page_load", {"url": page.url})
        ))
        
        # Request events
        page.on("request", lambda request: asyncio.create_task(
            self.on_page_event(session_id, "request", {
                "url": request.url,
                "method": request.method,
                "resource_type": request.resource_type
            })
        ))
        
        # Response events
        page.on("response", lambda response: asyncio.create_task(
            self.on_page_event(session_id, "response", {
                "url": response.url,
                "status": response.status,
                "headers": dict(response.headers)
            })
        ))
        
        # Console messages
        page.on("console", lambda msg: asyncio.create_task(
            self.on_page_event(session_id, "console", {
                "type": msg.type,
                "text": msg.text
            })
        ))
        
        # Page errors
        page.on("pageerror", lambda error: asyncio.create_task(
            self.on_page_event(session_id, "error", {"message": str(error)})
        ))

    async def on_page_event(self, session_id: str, event_type: str, data: Dict[str, Any]):
        """Handle page events and send to websocket"""
        if session_id not in self.sessions:
            return
            
        session = self.sessions[session_id]
        session.last_activity = datetime.utcnow()
        
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": event_type,
            "data": data
        }
        
        session.logs.append(log_entry)
        
        # Send to websocket
        await self.send_websocket_message(session_id, {
            "type": "page_event",
            "event": event_type,
            "data": data,
            "timestamp": log_entry["timestamp"]
        })

    async def run_automation_steps(self, session_id: str, client_data: Dict[str, Any]):
        """Run the main automation steps"""
        session = self.sessions[session_id]
        page = session.page
        
        try:
            steps = [
                ("Navigate to university", 30),
                ("Create account", 50),
                ("Fill personal details", 70),
                ("Upload documents", 85),
                ("Submit application", 95),
                ("Confirmation", 100)
            ]
            
            for step_name, progress in steps:
                if session.status != SessionStatus.RUNNING:
                    break
                    
                session.current_step = step_name
                session.progress = progress
                await self.send_status_update(session_id)
                
                # Take screenshot
                await self.capture_screenshot(session_id)
                
                # Execute step
                await self.execute_automation_step(session_id, step_name, client_data)
                
                # Wait between steps
                await asyncio.sleep(2)
            
            if session.status == SessionStatus.RUNNING:
                session.status = SessionStatus.COMPLETED
                session.current_step = "Application completed successfully"
                await self.send_status_update(session_id)
                
        except Exception as e:
            session.status = SessionStatus.ERROR
            session.error_message = str(e)
            session.current_step = f"Error: {str(e)}"
            await self.send_status_update(session_id)
            logger.error(f"Automation step failed for session {session_id}: {e}")

    async def execute_automation_step(self, session_id: str, step_name: str, client_data: Dict[str, Any]):
        """Execute a specific automation step"""
        session = self.sessions[session_id]
        page = session.page
        
        # Mock automation steps - replace with actual implementation
        if step_name == "Navigate to university":
            await page.goto("https://www.ox.ac.uk/admissions/undergraduate/applying-to-oxford/application-process")
            
        elif step_name == "Create account":
            # Simulate account creation
            await asyncio.sleep(3)
            
        elif step_name == "Fill personal details":
            # Simulate form filling
            await asyncio.sleep(4)
            
        elif step_name == "Upload documents":
            # Simulate document upload
            await asyncio.sleep(3)
            
        elif step_name == "Submit application":
            # Simulate submission
            await asyncio.sleep(2)
            
        elif step_name == "Confirmation":
            # Final confirmation
            await asyncio.sleep(1)

    async def capture_screenshot(self, session_id: str) -> str:
        """Capture screenshot and return base64 encoded image"""
        if session_id not in self.sessions:
            return ""
            
        session = self.sessions[session_id]
        if not session.page:
            return ""
            
        try:
            # Capture screenshot
            screenshot_bytes = await session.page.screenshot(
                type="png",
                full_page=False,
                clip={"x": 0, "y": 0, "width": 1920, "height": 1080}
            )
            
            # Convert to base64
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            # Store in session
            session.screenshots.append(screenshot_b64)
            
            # Send to websocket
            await self.send_websocket_message(session_id, {
                "type": "screenshot",
                "data": screenshot_b64,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            return screenshot_b64
            
        except Exception as e:
            logger.error(f"Failed to capture screenshot for session {session_id}: {e}")
            return ""

    async def pause_session(self, session_id: str) -> bool:
        """Pause an automation session"""
        if session_id not in self.sessions:
            return False
            
        session = self.sessions[session_id]
        if session.status == SessionStatus.RUNNING:
            session.status = SessionStatus.PAUSED
            session.current_step = "Paused by user"
            await self.send_status_update(session_id)
            return True
        return False

    async def resume_session(self, session_id: str) -> bool:
        """Resume a paused session"""
        if session_id not in self.sessions:
            return False
            
        session = self.sessions[session_id]
        if session.status == SessionStatus.PAUSED:
            session.status = SessionStatus.RUNNING
            session.current_step = "Resumed"
            await self.send_status_update(session_id)
            return True
        return False

    async def stop_session(self, session_id: str) -> bool:
        """Stop an automation session"""
        if session_id not in self.sessions:
            return False
            
        session = self.sessions[session_id]
        session.status = SessionStatus.STOPPED
        session.current_step = "Stopped by user"
        
        # Cleanup browser resources
        try:
            if session.context:
                await session.context.close()
            if session.browser:
                await session.browser.close()
        except Exception as e:
            logger.error(f"Error closing browser for session {session_id}: {e}")
        
        await self.send_status_update(session_id)
        return True

    async def send_status_update(self, session_id: str):
        """Send status update to websocket"""
        if session_id not in self.sessions:
            return
            
        session = self.sessions[session_id]
        
        status_data = {
            "type": "status_update",
            "session_id": session_id,
            "status": session.status.value,
            "current_step": session.current_step,
            "progress": session.progress,
            "error_message": session.error_message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_websocket_message(session_id, status_data)

    async def send_websocket_message(self, session_id: str, message: Dict[str, Any]):
        """Send message to websocket client"""
        if session_id not in self.active_websockets:
            return
            
        websocket = self.active_websockets[session_id]
        
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Failed to send websocket message for session {session_id}: {e}")
            # Remove dead websocket
            if session_id in self.active_websockets:
                del self.active_websockets[session_id]

    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a session"""
        if session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        
        return {
            "session_id": session.session_id,
            "client_id": session.client_id,
            "university_name": session.university_name,
            "status": session.status.value,
            "current_step": session.current_step,
            "progress": session.progress,
            "created_at": session.created_at.isoformat(),
            "last_activity": session.last_activity.isoformat(),
            "error_message": session.error_message,
            "logs_count": len(session.logs),
            "screenshots_count": len(session.screenshots)
        }

    async def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get information about all sessions"""
        return [await self.get_session_info(session_id) for session_id in self.sessions.keys()]

    async def handle_websocket_disconnect(self, session_id: str):
        """Handle websocket disconnection"""
        if session_id in self.active_websockets:
            del self.active_websockets[session_id]
            
        # Optionally pause the session when websocket disconnects
        if session_id in self.sessions:
            session = self.sessions[session_id]
            if session.status == SessionStatus.RUNNING:
                await self.pause_session(session_id)

    async def cleanup_session(self, session_id: str):
        """Clean up a session and its resources"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            
            # Close browser resources
            try:
                if session.context:
                    await session.context.close()
                if session.browser:
                    await session.browser.close()
            except Exception as e:
                logger.error(f"Error cleaning up session {session_id}: {e}")
            
            # Remove from active sessions
            del self.sessions[session_id]
            
            if session_id in self.active_websockets:
                del self.active_websockets[session_id]
            
            logger.info(f"Cleaned up session {session_id}")

    async def cleanup_all(self):
        """Clean up all sessions and resources"""
        for session_id in list(self.sessions.keys()):
            await self.cleanup_session(session_id)
            
        if self.playwright:
            await self.playwright.stop()
            
        logger.info("Automation Manager cleanup completed")

# Global automation manager instance
automation_manager = AutomationManager() 