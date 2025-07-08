"""
AI Analysis Service using Gemini API
Provides intelligent webpage analysis and automation guidance
"""

import os
import logging
import base64
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import asyncio

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)

class AIAnalysisService:
    """AI-powered webpage analysis using Gemini"""
    
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.enabled = os.getenv('ENABLE_AI_ANALYSIS', 'true').lower() == 'true'
        
        if not GEMINI_AVAILABLE:
            logger.warning("Gemini API not available. Install: pip install google-generativeai")
            self.enabled = False
            return
        
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found in environment")
            self.enabled = False
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"AI Analysis Service initialized with {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini: {str(e)}")
            self.enabled = False
    
    async def analyze_webpage_screenshot(self, 
                                       screenshot_b64: str, 
                                       automation_goal: str,
                                       user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze webpage screenshot to understand form structure and suggest actions
        
        Args:
            screenshot_b64: Base64 encoded screenshot
            automation_goal: What we're trying to automate (signup, job_application, etc.)
            user_data: User data to be filled
            
        Returns:
            AI analysis with form insights and action suggestions
        """
        if not self.enabled:
            return self._fallback_analysis()
        
        try:
            # Prepare the prompt
            prompt = self._create_webpage_analysis_prompt(automation_goal, user_data)
            
            # Convert base64 to image for Gemini
            image_data = base64.b64decode(screenshot_b64)
            
            # Create image part for Gemini
            image_part = {
                "mime_type": "image/png",
                "data": image_data
            }
            
            # Generate analysis
            response = await self._generate_response(prompt, image_part)
            
            # Parse and structure the response
            analysis = await self._parse_ai_response(response, automation_goal)
            
            return analysis
            
        except Exception as e:
            logger.error(f"AI webpage analysis failed: {str(e)}")
            return self._fallback_analysis()
    
    async def classify_form_field(self, 
                                field_info: Dict[str, Any], 
                                context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Use AI to classify what a form field is for
        
        Args:
            field_info: Information about the form field
            context: Page context and automation goal
            
        Returns:
            Enhanced field classification
        """
        if not self.enabled:
            return field_info
        
        try:
            prompt = self._create_field_classification_prompt(field_info, context)
            
            response = await self._generate_text_response(prompt)
            
            # Parse the AI response
            classification = await self._parse_field_classification(response, field_info)
            
            return classification
            
        except Exception as e:
            logger.error(f"AI field classification failed: {str(e)}")
            return field_info
    
    async def suggest_next_action(self, 
                                current_state: Dict[str, Any],
                                automation_goal: str,
                                screenshot_b64: Optional[str] = None) -> Dict[str, Any]:
        """
        Suggest the next best action for automation
        
        Args:
            current_state: Current automation state
            automation_goal: What we're trying to achieve
            screenshot_b64: Optional current screenshot
            
        Returns:
            Suggested next action
        """
        if not self.enabled:
            return {"action": "continue", "confidence": 0.5}
        
        try:
            prompt = self._create_action_suggestion_prompt(current_state, automation_goal)
            
            if screenshot_b64:
                image_data = base64.b64decode(screenshot_b64)
                image_part = {"mime_type": "image/png", "data": image_data}
                response = await self._generate_response(prompt, image_part)
            else:
                response = await self._generate_text_response(prompt)
            
            suggestion = await self._parse_action_suggestion(response)
            
            return suggestion
            
        except Exception as e:
            logger.error(f"AI action suggestion failed: {str(e)}")
            return {"action": "continue", "confidence": 0.5}
    
    async def analyze_error_scenario(self, 
                                   error_info: Dict[str, Any],
                                   screenshot_b64: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze automation errors and suggest recovery
        """
        if not self.enabled:
            return {"recovery": "retry", "confidence": 0.3}
        
        try:
            prompt = f"""
            An automation error occurred. Please analyze and suggest recovery:
            
            Error Information:
            {json.dumps(error_info, indent=2)}
            
            Suggest:
            1. What likely went wrong
            2. Recovery strategy
            3. Alternative approach
            4. Confidence level (0-1)
            
            Return as JSON with: analysis, recovery_strategy, alternatives, confidence
            """
            
            if screenshot_b64:
                image_data = base64.b64decode(screenshot_b64)
                image_part = {"mime_type": "image/png", "data": image_data}
                response = await self._generate_response(prompt, image_part)
            else:
                response = await self._generate_text_response(prompt)
            
            return await self._parse_error_analysis(response)
            
        except Exception as e:
            logger.error(f"AI error analysis failed: {str(e)}")
            return {"recovery": "retry", "confidence": 0.3}
    
    def _create_webpage_analysis_prompt(self, automation_goal: str, user_data: Dict[str, Any]) -> str:
        """Create prompt for webpage analysis"""
        return f"""
        You are an expert web automation analyst. Analyze this webpage screenshot for a {automation_goal} automation task.
        
        User data available:
        {json.dumps(user_data, indent=2)}
        
        Please analyze the webpage and provide:
        
        1. **Form Structure**: Identify all visible forms, fields, and their purposes
        2. **Field Mapping**: Map user data to form fields
        3. **Required Actions**: Sequence of actions needed (click buttons, fill fields, etc.)
        4. **Challenges**: Any potential issues (CAPTCHAs, complex validation, etc.)
        5. **Success Indicators**: How to know if the automation succeeded
        6. **Next Steps**: What should happen after current visible elements
        
        Return as structured JSON with keys:
        - forms_detected: array of form objects
        - field_mappings: object mapping user data to field selectors
        - action_sequence: array of recommended actions
        - challenges: array of potential issues
        - success_indicators: array of success signs
        - confidence: number 0-1 for analysis confidence
        
        Be specific about CSS selectors, field types, and exact action sequences.
        """
    
    def _create_field_classification_prompt(self, field_info: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Create prompt for field classification"""
        return f"""
        Classify this form field for automation:
        
        Field Information:
        - Name: {field_info.get('name', 'unknown')}
        - ID: {field_info.get('id', 'unknown')}
        - Type: {field_info.get('type', 'unknown')}
        - Label: {field_info.get('label', 'unknown')}
        - Placeholder: {field_info.get('placeholder', 'unknown')}
        - Class: {field_info.get('class', 'unknown')}
        
        Context:
        - Automation Goal: {context.get('automation_goal', 'unknown')}
        - Page Type: {context.get('page_type', 'unknown')}
        
        Determine:
        1. Field Purpose (email, first_name, phone, etc.)
        2. Data Type Expected
        3. Validation Requirements
        4. Priority (high/medium/low)
        5. Required vs Optional
        
        Return JSON with: purpose, data_type, validation, priority, required, confidence
        """
    
    def _create_action_suggestion_prompt(self, current_state: Dict[str, Any], automation_goal: str) -> str:
        """Create prompt for action suggestions"""
        return f"""
        Current automation state:
        {json.dumps(current_state, indent=2)}
        
        Automation goal: {automation_goal}
        
        What should be the next action? Consider:
        1. Forms filled so far
        2. Buttons clicked
        3. Current page state
        4. Remaining tasks
        
        Suggest the next best action:
        - action_type: click, fill, submit, navigate, wait, etc.
        - target_selector: CSS selector or description
        - action_data: any data needed for the action
        - reason: why this action
        - confidence: 0-1
        
        Return as JSON.
        """
    
    async def _generate_response(self, prompt: str, image_part: Dict[str, Any]) -> str:
        """Generate response with image"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                [prompt, image_part]
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini image generation failed: {str(e)}")
            raise
    
    async def _generate_text_response(self, prompt: str) -> str:
        """Generate text-only response"""
        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini text generation failed: {str(e)}")
            raise
    
    async def _parse_ai_response(self, response: str, automation_goal: str) -> Dict[str, Any]:
        """Parse and structure AI response"""
        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                
                # Ensure required fields
                analysis = {
                    'forms_detected': parsed.get('forms_detected', []),
                    'field_mappings': parsed.get('field_mappings', {}),
                    'action_sequence': parsed.get('action_sequence', []),
                    'challenges': parsed.get('challenges', []),
                    'success_indicators': parsed.get('success_indicators', []),
                    'confidence': parsed.get('confidence', 0.7),
                    'ai_analysis': True,
                    'timestamp': datetime.utcnow().isoformat()
                }
                
                return analysis
            else:
                # Fallback parsing if JSON not found
                return self._parse_text_response(response, automation_goal)
                
        except json.JSONDecodeError:
            return self._parse_text_response(response, automation_goal)
    
    async def _parse_field_classification(self, response: str, field_info: Dict[str, Any]) -> Dict[str, Any]:
        """Parse field classification response"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                parsed = json.loads(json_str)
                
                # Enhance the original field info
                enhanced = field_info.copy()
                enhanced.update({
                    'ai_purpose': parsed.get('purpose', field_info.get('purpose', 'unknown')),
                    'ai_data_type': parsed.get('data_type', 'text'),
                    'ai_validation': parsed.get('validation', {}),
                    'ai_priority': parsed.get('priority', 'medium'),
                    'ai_required': parsed.get('required', False),
                    'ai_confidence': parsed.get('confidence', 0.5)
                })
                
                return enhanced
            else:
                return field_info
                
        except:
            return field_info
    
    async def _parse_action_suggestion(self, response: str) -> Dict[str, Any]:
        """Parse action suggestion response"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"action": "continue", "confidence": 0.5}
                
        except:
            return {"action": "continue", "confidence": 0.5}
    
    async def _parse_error_analysis(self, response: str) -> Dict[str, Any]:
        """Parse error analysis response"""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                return {"recovery": "retry", "confidence": 0.3}
                
        except:
            return {"recovery": "retry", "confidence": 0.3}
    
    def _parse_text_response(self, response: str, automation_goal: str) -> Dict[str, Any]:
        """Fallback text parsing when JSON fails"""
        return {
            'forms_detected': [],
            'field_mappings': {},
            'action_sequence': [{"action": "analyze_manually", "reason": "AI parsing failed"}],
            'challenges': ["AI response parsing failed"],
            'success_indicators': [],
            'confidence': 0.3,
            'ai_analysis': True,
            'raw_response': response[:500],  # First 500 chars
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _fallback_analysis(self) -> Dict[str, Any]:
        """Fallback when AI is not available"""
        return {
            'forms_detected': [],
            'field_mappings': {},
            'action_sequence': [],
            'challenges': ["AI analysis not available"],
            'success_indicators': [],
            'confidence': 0.5,
            'ai_analysis': False,
            'timestamp': datetime.utcnow().isoformat()
        } 