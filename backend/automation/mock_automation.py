"""
Mock Automation System for Development/Testing
Provides a fallback when Playwright is not available
"""

import asyncio
import json
import uuid
import base64
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

class MockAutomationManager:
    """Mock automation manager for development/testing"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.active_websockets: Dict[str, Any] = {}
        
    async def initialize(self):
        """Initialize mock automation manager"""
        logger.info("Mock Automation Manager initialized successfully")
        return True

    async def create_session(self, client_id: str, university_name: str, websocket=None) -> str:
        """Create a mock automation session"""
        session_id = str(uuid.uuid4())
        
        session = {
            "session_id": session_id,
            "client_id": client_id,
            "university_name": university_name,
            "status": "idle",
            "current_step": "Ready to start",
            "progress": 0,
            "created_at": datetime.utcnow(),
            "last_activity": datetime.utcnow(),
            "logs": [],
            "screenshots": [],
            "error_message": None
        }
        
        self.sessions[session_id] = session
        if websocket:
            self.active_websockets[session_id] = websocket
        
        logger.info(f"Created mock automation session {session_id}")
        return session_id

    async def start_automation(self, session_id: str, client_data: Dict[str, Any]) -> bool:
        """Start mock automation process"""
        if session_id not in self.sessions:
            return False
            
        session = self.sessions[session_id]
        session["status"] = "running"
        session["current_step"] = "Starting automation"
        session["progress"] = 10
        
        # Simulate automation steps
        await self._simulate_automation_steps(session_id, client_data)
        return True

    async def _simulate_automation_steps(self, session_id: str, client_data: Dict[str, Any]):
        """Simulate automation steps with progress updates"""
        session = self.sessions[session_id]
        
        steps = [
            ("Navigating to university website", 20),
            ("Creating account", 40),
            ("Filling personal details", 60),
            ("Uploading documents", 80),
            ("Submitting application", 95),
            ("Application completed", 100)
        ]
        
        for step_name, progress in steps:
            if session["status"] != "running":
                break
                
            session["current_step"] = step_name
            session["progress"] = progress
            session["last_activity"] = datetime.utcnow()
            
            # Generate mock screenshot
            await self._generate_mock_screenshot(session_id, step_name)
            
            # Send websocket update if available
            await self._send_mock_update(session_id)
            
            # Wait to simulate real work
            await asyncio.sleep(random.uniform(2, 4))
        
        if session["status"] == "running":
            session["status"] = "completed"
            session["current_step"] = "Application completed successfully"

    async def _generate_mock_screenshot(self, session_id: str, step_name: str):
        """Generate a mock browser screenshot"""
        try:
            # Create a simple mock browser screenshot
            img = Image.new('RGB', (1920, 1080), color='white')
            draw = ImageDraw.Draw(img)
            
            # Draw mock browser interface
            # Browser bar
            draw.rectangle([0, 0, 1920, 80], fill='#f1f3f4')
            draw.rectangle([100, 20, 1820, 60], fill='white', outline='#dadce0')
            
            # Mock university website
            draw.rectangle([0, 80, 1920, 1080], fill='#1a73e8')
            
            # University name
            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()
                
            session = self.sessions[session_id]
            university = session["university_name"]
            draw.text((960, 200), university, fill='white', font=font, anchor='mm')
            
            # Current step
            try:
                step_font = ImageFont.truetype("arial.ttf", 24)
            except:
                step_font = ImageFont.load_default()
                
            draw.text((960, 300), f"Current Step: {step_name}", fill='white', font=step_font, anchor='mm')
            
            # Progress indicator
            progress_width = int(1600 * (session["progress"] / 100))
            draw.rectangle([160, 400, 1760, 440], fill='#e8f0fe', outline='#1a73e8')
            draw.rectangle([160, 400, 160 + progress_width, 440], fill='#34a853')
            
            # Convert to base64
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            screenshot_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            session["screenshots"].append(screenshot_b64)
            return screenshot_b64
            
        except Exception as e:
            logger.error(f"Failed to generate mock screenshot: {e}")
            return ""

    async def _send_mock_update(self, session_id: str):
        """Send mock update via websocket if available"""
        if session_id in self.active_websockets:
            websocket = self.active_websockets[session_id]
            session = self.sessions[session_id]
            
            update = {
                "type": "status_update",
                "session_id": session_id,
                "status": session["status"],
                "current_step": session["current_step"],
                "progress": session["progress"],
                "timestamp": datetime.utcnow().isoformat()
            }
            
            try:
                await websocket.send_text(json.dumps(update))
            except Exception as e:
                logger.error(f"Failed to send mock update: {e}")

    async def pause_session(self, session_id: str) -> bool:
        """Pause mock session"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "paused"
            self.sessions[session_id]["current_step"] = "Paused by user"
            return True
        return False

    async def resume_session(self, session_id: str) -> bool:
        """Resume mock session"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "running"
            self.sessions[session_id]["current_step"] = "Resumed"
            return True
        return False

    async def stop_session(self, session_id: str) -> bool:
        """Stop mock session"""
        if session_id in self.sessions:
            self.sessions[session_id]["status"] = "stopped"
            self.sessions[session_id]["current_step"] = "Stopped by user"
            return True
        return False

    async def capture_screenshot(self, session_id: str) -> str:
        """Capture mock screenshot"""
        if session_id in self.sessions:
            step_name = self.sessions[session_id]["current_step"]
            return await self._generate_mock_screenshot(session_id, step_name)
        return ""

    async def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get mock session information"""
        if session_id not in self.sessions:
            return None
            
        session = self.sessions[session_id]
        return {
            "session_id": session["session_id"],
            "client_id": session["client_id"],
            "university_name": session["university_name"],
            "status": session["status"],
            "current_step": session["current_step"],
            "progress": session["progress"],
            "created_at": session["created_at"].isoformat(),
            "last_activity": session["last_activity"].isoformat(),
            "error_message": session["error_message"],
            "logs_count": len(session["logs"]),
            "screenshots_count": len(session["screenshots"])
        }

    async def get_all_sessions(self) -> List[Dict[str, Any]]:
        """Get all mock sessions"""
        sessions = []
        for session_id in self.sessions.keys():
            session_info = await self.get_session_info(session_id)
            if session_info:
                sessions.append(session_info)
        return sessions

    async def handle_websocket_disconnect(self, session_id: str):
        """Handle websocket disconnection"""
        if session_id in self.active_websockets:
            del self.active_websockets[session_id]

    async def cleanup_session(self, session_id: str):
        """Clean up mock session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
        if session_id in self.active_websockets:
            del self.active_websockets[session_id]
        logger.info(f"Cleaned up mock session {session_id}")

    async def cleanup_all(self):
        """Clean up all mock sessions"""
        self.sessions.clear()
        self.active_websockets.clear()
        logger.info("Mock Automation Manager cleanup completed")

# Global mock automation manager instance
mock_automation_manager = MockAutomationManager() 