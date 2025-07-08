"""
AI-Enhanced Universal Automation
Combines Playwright automation with Gemini AI for intelligent form filling
"""

import asyncio
import logging
import base64
from typing import Dict, List, Any, Optional
from datetime import datetime

from playwright.async_api import Page
from .universal_automation import UniversalAutomation
from .ai_analysis_service import AIAnalysisService
from .form_detection import FormFieldDetector

logger = logging.getLogger(__name__)

class AIEnhancedAutomation(UniversalAutomation):
    """AI-powered automation with vision and reasoning"""
    
    def __init__(self):
        super().__init__()
        self.ai_service = AIAnalysisService()
        self.ai_insights = []
        
    async def intelligent_form_automation(self, 
                                        url: str, 
                                        user_data: Dict[str, Any],
                                        session_id: str,
                                        automation_type: str = "general",
                                        progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        AI-enhanced automation with visual understanding
        """
        result = {
            'success': False,
            'automation_type': automation_type,
            'ai_enabled': self.ai_service.enabled,
            'ai_insights': [],
            'steps_completed': [],
            'forms_filled': 0,
            'errors': [],
            'screenshots': [],
            'log': []
        }
        
        try:
            # Initialize browser
            if not self.context:
                await self.initialize_universal_browser()
            
            page = await self.context.new_page()
            
            # Navigate to URL
            await self._update_progress(progress_callback, 10, "Navigating to website")
            await self._navigate_with_retry(page, url)
            
            # Take initial screenshot and analyze with AI
            await self._update_progress(progress_callback, 20, "Analyzing webpage with AI")
            initial_screenshot = await self._capture_screenshot(page, "initial_analysis")
            result['screenshots'].append(initial_screenshot)
            
            # AI Analysis of the webpage
            ai_analysis = await self.ai_service.analyze_webpage_screenshot(
                initial_screenshot['data'],
                automation_type,
                user_data
            )
            result['ai_insights'].append(ai_analysis)
            await self._log_action("AI webpage analysis completed", f"Confidence: {ai_analysis.get('confidence', 0)}")
            
            # Use AI insights to guide automation
            if ai_analysis.get('ai_analysis') and ai_analysis.get('confidence', 0) > 0.5:
                await self._ai_guided_automation(page, user_data, ai_analysis, result, progress_callback)
            else:
                # Fallback to traditional automation
                await self._traditional_automation_fallback(page, user_data, result, progress_callback, automation_type)
            
            # Final success check
            if not result['errors']:
                result['success'] = True
                await self._update_progress(progress_callback, 100, "AI-enhanced automation completed")
            
        except Exception as e:
            logger.error(f"AI-enhanced automation error: {str(e)}")
            result['errors'].append(str(e))
            
            # Try AI error analysis
            try:
                current_screenshot = await self._capture_screenshot(page, "error_state")
                result['screenshots'].append(current_screenshot)
                
                error_analysis = await self.ai_service.analyze_error_scenario(
                    {'error': str(e), 'step': len(result['steps_completed'])},
                    current_screenshot['data']
                )
                result['ai_insights'].append(error_analysis)
                
                # Try recovery if AI suggests it
                if error_analysis.get('recovery_strategy') and error_analysis.get('confidence', 0) > 0.6:
                    await self._attempt_ai_recovery(page, error_analysis, result)
                    
            except Exception as recovery_error:
                logger.error(f"AI error recovery failed: {str(recovery_error)}")
        
        finally:
            result['log'] = self.automation_log
            result['ai_insights'] = self.ai_insights
            if 'page' in locals():
                await page.close()
        
        return result
    
    async def _ai_guided_automation(self, 
                                  page: Page, 
                                  user_data: Dict[str, Any],
                                  ai_analysis: Dict[str, Any],
                                  result: Dict[str, Any],
                                  progress_callback):
        """Use AI analysis to guide the automation process"""
        
        await self._update_progress(progress_callback, 30, "Following AI guidance")
        
        # Execute AI-suggested action sequence
        action_sequence = ai_analysis.get('action_sequence', [])
        
        for i, action in enumerate(action_sequence):
            try:
                progress = 30 + (i * 40 // len(action_sequence))
                await self._update_progress(progress_callback, progress, f"Executing: {action.get('action_type', 'unknown')}")
                
                success = await self._execute_ai_action(page, action, user_data)
                
                if success:
                    result['steps_completed'].append(f"AI Action: {action.get('action_type', 'unknown')}")
                    await self._log_action(f"AI action executed: {action.get('action_type')}", action.get('reason', ''))
                else:
                    await self._log_action(f"AI action failed: {action.get('action_type')}", "Trying fallback")
                    # Continue with next action even if one fails
                
                # Small delay between actions
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"AI action execution failed: {str(e)}")
                result['errors'].append(f"AI action failed: {str(e)}")
        
        # Use AI field mappings for form filling
        field_mappings = ai_analysis.get('field_mappings', {})
        if field_mappings:
            await self._ai_guided_form_filling(page, field_mappings, user_data, result)
        
        # Check for AI success indicators
        success_indicators = ai_analysis.get('success_indicators', [])
        if success_indicators:
            await self._check_success_indicators(page, success_indicators, result)
    
    async def _execute_ai_action(self, page: Page, action: Dict[str, Any], user_data: Dict[str, Any]) -> bool:
        """Execute a single AI-suggested action"""
        action_type = action.get('action_type', '').lower()
        target_selector = action.get('target_selector', '')
        action_data = action.get('action_data', {})
        
        try:
            if action_type == 'click':
                if target_selector:
                    element = await page.wait_for_selector(target_selector, timeout=10000)
                    if element:
                        await element.scroll_into_view_if_needed()
                        await element.click()
                        return True
                        
            elif action_type == 'fill':
                field_name = action_data.get('field_name', '')
                value = action_data.get('value', '')
                
                # Try to get value from user data if not specified
                if not value and field_name in user_data:
                    value = user_data[field_name]
                
                if target_selector and value:
                    element = await page.wait_for_selector(target_selector, timeout=10000)
                    if element:
                        await element.scroll_into_view_if_needed()
                        await element.clear()
                        await self.human_like_typing(element, '', str(value))
                        return True
                        
            elif action_type == 'submit':
                if target_selector:
                    element = await page.wait_for_selector(target_selector, timeout=10000)
                    if element:
                        await element.scroll_into_view_if_needed()
                        await element.click()
                        return True
                        
            elif action_type == 'wait':
                wait_time = action_data.get('seconds', 2)
                await asyncio.sleep(wait_time)
                return True
                
            elif action_type == 'navigate':
                url = action_data.get('url', '')
                if url:
                    await page.goto(url)
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to execute AI action {action_type}: {str(e)}")
            return False
    
    async def _ai_guided_form_filling(self, 
                                    page: Page, 
                                    field_mappings: Dict[str, str],
                                    user_data: Dict[str, Any],
                                    result: Dict[str, Any]):
        """Fill forms using AI-provided field mappings"""
        
        filled_count = 0
        
        for field_purpose, selector in field_mappings.items():
            if field_purpose in user_data:
                try:
                    value = user_data[field_purpose]
                    element = await page.wait_for_selector(selector, timeout=5000)
                    
                    if element:
                        await element.scroll_into_view_if_needed()
                        await element.clear()
                        await self.human_like_typing(element, '', str(value))
                        filled_count += 1
                        
                        await self._log_action(f"AI-guided fill: {field_purpose}", selector)
                        
                except Exception as e:
                    logger.error(f"AI-guided filling failed for {field_purpose}: {str(e)}")
        
        result['forms_filled'] += 1 if filled_count > 0 else 0
        await self._log_action(f"AI-guided form filling completed", f"Fields filled: {filled_count}")
    
    async def _check_success_indicators(self, 
                                      page: Page, 
                                      success_indicators: List[str],
                                      result: Dict[str, Any]):
        """Check for AI-identified success indicators"""
        
        success_found = False
        
        for indicator in success_indicators:
            try:
                # Check if success indicator element exists
                element = await page.query_selector(indicator)
                if element and await element.is_visible():
                    success_found = True
                    result['steps_completed'].append(f"Success indicator found: {indicator}")
                    break
                    
            except Exception as e:
                logger.debug(f"Success indicator check failed: {str(e)}")
        
        if success_found:
            await self._log_action("Success indicators detected", "Automation likely successful")
    
    async def _traditional_automation_fallback(self, 
                                             page: Page, 
                                             user_data: Dict[str, Any],
                                             result: Dict[str, Any],
                                             progress_callback,
                                             automation_type: str):
        """Fallback to traditional automation when AI analysis fails"""
        
        await self._update_progress(progress_callback, 40, "Using traditional automation")
        await self._log_action("AI analysis insufficient, using traditional automation", "")
        
        # Use the original automation logic
        await self._handle_general_form_flow(page, user_data, result, progress_callback)
    
    async def _attempt_ai_recovery(self, 
                                 page: Page, 
                                 error_analysis: Dict[str, Any],
                                 result: Dict[str, Any]):
        """Attempt to recover from errors using AI suggestions"""
        
        recovery_strategy = error_analysis.get('recovery_strategy', '')
        confidence = error_analysis.get('confidence', 0)
        
        if confidence < 0.6:
            return False
        
        try:
            if recovery_strategy == 'retry_with_delay':
                await asyncio.sleep(3)
                # Retry the last action
                return True
                
            elif recovery_strategy == 'find_alternative_selector':
                # AI might suggest alternative selectors
                alternatives = error_analysis.get('alternatives', [])
                for alt_selector in alternatives:
                    try:
                        element = await page.wait_for_selector(alt_selector, timeout=5000)
                        if element:
                            await element.click()
                            result['steps_completed'].append(f"AI recovery: used {alt_selector}")
                            return True
                    except:
                        continue
                        
            elif recovery_strategy == 'wait_for_page_load':
                await page.wait_for_load_state('networkidle', timeout=10000)
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"AI recovery attempt failed: {str(e)}")
            return False
    
    async def enhance_field_detection_with_ai(self, 
                                            page: Page, 
                                            forms: List[Dict[str, Any]],
                                            automation_goal: str) -> List[Dict[str, Any]]:
        """Enhance form field detection using AI"""
        
        if not self.ai_service.enabled:
            return forms
        
        enhanced_forms = []
        
        for form in forms:
            enhanced_fields = []
            
            for field in form.get('fields', []):
                # Get AI classification for each field
                context = {
                    'automation_goal': automation_goal,
                    'page_type': 'form'
                }
                
                enhanced_field = await self.ai_service.classify_form_field(field, context)
                enhanced_fields.append(enhanced_field)
            
            enhanced_form = form.copy()
            enhanced_form['fields'] = enhanced_fields
            enhanced_form['ai_enhanced'] = True
            enhanced_forms.append(enhanced_form)
        
        return enhanced_forms 