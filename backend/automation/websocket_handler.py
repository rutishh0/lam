"""
WebSocket Handler for Real-time Automation Control and Browser Streaming
"""

import json
import logging
from typing import Dict, Any
from fastapi import WebSocket, WebSocketDisconnect
from .automation_manager import automation_manager

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manages WebSocket connections for automation control"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept WebSocket connection"""
        await websocket.accept()
        self.active_connections[session_id] = websocket
        logger.info(f"WebSocket connected for session {session_id}")
        
    def disconnect(self, session_id: str):
        """Remove WebSocket connection"""
        if session_id in self.active_connections:
            del self.active_connections[session_id]
            logger.info(f"WebSocket disconnected for session {session_id}")
            
    async def send_message(self, session_id: str, message: Dict[str, Any]):
        """Send message to specific session"""
        if session_id in self.active_connections:
            websocket = self.active_connections[session_id]
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to send message to session {session_id}: {e}")
                self.disconnect(session_id)
                
    async def broadcast(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        disconnected = []
        for session_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Failed to broadcast to session {session_id}: {e}")
                disconnected.append(session_id)
        
        # Remove disconnected clients
        for session_id in disconnected:
            self.disconnect(session_id)

# Global WebSocket manager
ws_manager = WebSocketManager()

async def handle_automation_websocket(websocket: WebSocket, session_id: str):
    """Handle WebSocket connection for automation control"""
    await ws_manager.connect(websocket, session_id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            await handle_websocket_message(session_id, message)
            
    except WebSocketDisconnect:
        logger.info(f"Client disconnected from session {session_id}")
        ws_manager.disconnect(session_id)
        await automation_manager.handle_websocket_disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for session {session_id}: {e}")
        ws_manager.disconnect(session_id)

async def handle_websocket_message(session_id: str, message: Dict[str, Any]):
    """Handle incoming WebSocket messages"""
    message_type = message.get("type")
    
    if message_type == "start_automation":
        client_data = message.get("client_data", {})
        success = await automation_manager.start_automation(session_id, client_data)
        
        response = {
            "type": "automation_response",
            "action": "start",
            "success": success,
            "session_id": session_id
        }
        await ws_manager.send_message(session_id, response)
        
    elif message_type == "pause_automation":
        success = await automation_manager.pause_session(session_id)
        
        response = {
            "type": "automation_response", 
            "action": "pause",
            "success": success,
            "session_id": session_id
        }
        await ws_manager.send_message(session_id, response)
        
    elif message_type == "resume_automation":
        success = await automation_manager.resume_session(session_id)
        
        response = {
            "type": "automation_response",
            "action": "resume", 
            "success": success,
            "session_id": session_id
        }
        await ws_manager.send_message(session_id, response)
        
    elif message_type == "stop_automation":
        success = await automation_manager.stop_session(session_id)
        
        response = {
            "type": "automation_response",
            "action": "stop",
            "success": success,
            "session_id": session_id
        }
        await ws_manager.send_message(session_id, response)
        
    elif message_type == "get_status":
        session_info = await automation_manager.get_session_info(session_id)
        
        response = {
            "type": "status_response",
            "session_info": session_info
        }
        await ws_manager.send_message(session_id, response)
        
    elif message_type == "request_screenshot":
        screenshot = await automation_manager.capture_screenshot(session_id)
        
        response = {
            "type": "screenshot_response",
            "screenshot": screenshot,
            "timestamp": message.get("timestamp")
        }
        await ws_manager.send_message(session_id, response)
        
    elif message_type == "browser_action":
        # Handle browser interaction (click, type, etc.)
        await handle_browser_action(session_id, message.get("action", {}))
        
    else:
        logger.warning(f"Unknown message type: {message_type}")

async def handle_browser_action(session_id: str, action: Dict[str, Any]):
    """Handle browser interaction commands from admin panel"""
    action_type = action.get("type")
    
    if session_id not in automation_manager.sessions:
        return
        
    session = automation_manager.sessions[session_id]
    page = session.page
    
    if not page:
        return
        
    try:
        if action_type == "click":
            x = action.get("x", 0)
            y = action.get("y", 0)
            await page.mouse.click(x, y)
            
        elif action_type == "type":
            text = action.get("text", "")
            await page.keyboard.type(text)
            
        elif action_type == "key_press":
            key = action.get("key", "")
            await page.keyboard.press(key)
            
        elif action_type == "scroll":
            delta_y = action.get("delta_y", 0)
            await page.mouse.wheel(0, delta_y)
            
        elif action_type == "navigate":
            url = action.get("url", "")
            await page.goto(url)
            
        # Send confirmation back to admin panel
        response = {
            "type": "browser_action_response",
            "action": action_type,
            "success": True
        }
        await ws_manager.send_message(session_id, response)
        
    except Exception as e:
        logger.error(f"Browser action failed for session {session_id}: {e}")
        
        response = {
            "type": "browser_action_response",
            "action": action_type,
            "success": False,
            "error": str(e)
        }
        await ws_manager.send_message(session_id, response) 