"""
Universal Automation Engine
Handles ANY type of website form automation - job applications, signups, visa forms, appointments, etc.
"""

import asyncio
import logging
import random
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import base64

from playwright.async_api import Page, Browser, BrowserContext, ElementHandle, expect
from .intelligent_automation import IntelligentFormAutomation
from .form_detection import FormFieldDetector, FieldType

logger = logging.getLogger(__name__)

class UniversalAutomation(IntelligentFormAutomation):
    """Universal automation that works on ANY website"""
    
    def __init__(self):
        super().__init__()
        self.retry_attempts = 3
        self.wait_timeout = 30000
        self.navigation_timeout = 60000
        
    async def universal_form_automation(self, 
                                      url: str, 
                                      user_data: Dict[str, Any],
                                      session_id: str,
                                      automation_type: str = "general",
                                      progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Universal automation for ANY type of form
        
        Args:
            url: Target website URL
            user_data: User data to fill
            session_id: Session ID
            automation_type: Type of automation (signup, job_application, visa, appointment, etc.)
            progress_callback: Progress callback
            
        Returns:
            Automation results
        """
        result = {
            'success': False,
            'automation_type': automation_type,
            'steps_completed': [],
            'forms_filled': 0,
            'files_uploaded': 0,
            'pages_navigated': 0,
            'errors': [],
            'screenshots': [],
            'log': []
        }
        
        try:
            # Initialize browser with enhanced stealth
            if not self.context:
                await self.initialize_universal_browser()
            
            page = await self.context.new_page()
            
            # Navigate with retry mechanism
            await self._update_progress(progress_callback, 5, "Navigating to website")
            await self._navigate_with_retry(page, url)
            result['pages_navigated'] += 1
            
            # Take initial screenshot
            initial_screenshot = await self._capture_screenshot(page, "initial_page")
            result['screenshots'].append(initial_screenshot)
            
            # Handle different automation types
            if automation_type == "signup":
                await self._handle_signup_flow(page, user_data, result, progress_callback)
            elif automation_type == "job_application":
                await self._handle_job_application_flow(page, user_data, result, progress_callback)
            elif automation_type == "visa_application":
                await self._handle_visa_application_flow(page, user_data, result, progress_callback)
            elif automation_type == "appointment_booking":
                await self._handle_appointment_booking_flow(page, user_data, result, progress_callback)
            else:
                # General form automation
                await self._handle_general_form_flow(page, user_data, result, progress_callback)
            
            # Mark as successful if no errors
            if not result['errors']:
                result['success'] = True
                await self._update_progress(progress_callback, 100, "Automation completed successfully")
            
        except Exception as e:
            logger.error(f"Universal automation error: {str(e)}")
            result['errors'].append(str(e))
            await self._log_action(f"Critical error: {str(e)}", None)
        
        finally:
            result['log'] = self.automation_log
            if 'page' in locals():
                await page.close()
        
        return result
    
    async def initialize_universal_browser(self):
        """Initialize browser with enhanced anti-detection"""
        from playwright.async_api import async_playwright
        from playwright_stealth import stealth_async
        
        self.playwright = await async_playwright().start()
        
        # Enhanced browser args for better stealth
        browser_args = [
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-blink-features=AutomationControlled',
            '--disable-features=VizDisplayCompositor',
            '--disable-ipc-flooding-protection',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-field-trial-config',
            '--disable-back-forward-cache',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-sync',
            '--disable-translate',
            '--metrics-recording-only',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-background-timer-throttling',
            '--disable-renderer-backgrounding',
            '--disable-backgrounding-occluded-windows',
            '--disable-restore-session-state',
            '--disable-ipc-flooding-protection'
        ]
        
        self.browser = await self.playwright.chromium.launch(
            headless=False,  # Set to False to see automation
            args=browser_args
        )
        
        # Create context with realistic settings
        self.context = await self.browser.new_context(
            viewport={'width': 1366, 'height': 768},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York',
            permissions=['notifications', 'geolocation'],
            color_scheme='light'
        )
        
        # Apply stealth to all pages
        await stealth_async(self.context)
    
    async def _navigate_with_retry(self, page: Page, url: str, max_retries: int = 3):
        """Navigate with retry mechanism"""
        for attempt in range(max_retries):
            try:
                await page.goto(url, wait_until='networkidle', timeout=self.navigation_timeout)
                await self._log_action(f"Successfully navigated to {url}", f"Attempt {attempt + 1}")
                return
            except Exception as e:
                if attempt < max_retries - 1:
                    await self._log_action(f"Navigation attempt {attempt + 1} failed, retrying", str(e))
                    await asyncio.sleep(2)
                else:
                    raise Exception(f"Failed to navigate after {max_retries} attempts: {str(e)}")
    
    async def _handle_signup_flow(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback):
        """Handle signup/registration forms"""
        await self._update_progress(progress_callback, 20, "Looking for signup forms")
        
        # Look for signup/register buttons first
        signup_selectors = [
            'a:has-text("Sign up")', 'a:has-text("Register")', 'a:has-text("Create account")',
            'button:has-text("Sign up")', 'button:has-text("Register")', 'button:has-text("Join")',
            'a:has-text("Get started")', 'a:has-text("Join now")', '[data-testid*="signup"]',
            '.signup-button', '.register-button', '#signup', '#register'
        ]
        
        signup_found = await self._try_click_elements(page, signup_selectors, "signup button")
        if signup_found:
            await asyncio.sleep(2)  # Wait for page load
            result['steps_completed'].append("Found and clicked signup button")
        
        # Now fill forms
        await self._fill_all_forms_on_page(page, user_data, result, progress_callback, "signup")
    
    async def _handle_job_application_flow(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback):
        """Handle job application forms"""
        await self._update_progress(progress_callback, 20, "Analyzing job application form")
        
        # Look for "Apply" buttons
        apply_selectors = [
            'button:has-text("Apply")', 'a:has-text("Apply")', 'button:has-text("Apply Now")',
            'a:has-text("Apply Now")', '.apply-button', '#apply-button', '[data-testid*="apply"]',
            'button:has-text("Submit Application")', 'input[value*="Apply"]'
        ]
        
        apply_found = await self._try_click_elements(page, apply_selectors, "apply button")
        if apply_found:
            await asyncio.sleep(3)
            result['steps_completed'].append("Found and clicked apply button")
        
        # Handle multi-step application process
        await self._handle_multi_step_form(page, user_data, result, progress_callback, "job_application")
    
    async def _handle_visa_application_flow(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback):
        """Handle visa application forms"""
        await self._update_progress(progress_callback, 20, "Processing visa application form")
        
        # Visa forms often have specific flows
        start_selectors = [
            'button:has-text("Start Application")', 'a:has-text("Apply Online")',
            'button:has-text("Begin")', 'a:has-text("New Application")',
            '.start-application', '#start-button'
        ]
        
        start_found = await self._try_click_elements(page, start_selectors, "start application button")
        if start_found:
            await asyncio.sleep(3)
            result['steps_completed'].append("Started visa application")
        
        # Handle multi-step visa process with file uploads
        await self._handle_multi_step_form(page, user_data, result, progress_callback, "visa", handle_uploads=True)
    
    async def _handle_appointment_booking_flow(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback):
        """Handle appointment booking systems"""
        await self._update_progress(progress_callback, 20, "Looking for available appointments")
        
        # Look for book appointment buttons
        booking_selectors = [
            'button:has-text("Book")', 'a:has-text("Schedule")', 'button:has-text("Schedule")',
            'a:has-text("Book Appointment")', 'button:has-text("Book Appointment")',
            '.book-button', '.schedule-button', '#book-appointment'
        ]
        
        booking_found = await self._try_click_elements(page, booking_selectors, "booking button")
        if booking_found:
            await asyncio.sleep(2)
            result['steps_completed'].append("Found booking interface")
        
        # Handle calendar/date selection
        await self._handle_date_selection(page, user_data, result)
        
        # Fill remaining form details
        await self._fill_all_forms_on_page(page, user_data, result, progress_callback, "appointment")
    
    async def _handle_general_form_flow(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback):
        """Handle any general form"""
        await self._update_progress(progress_callback, 20, "Analyzing page for forms")
        await self._fill_all_forms_on_page(page, user_data, result, progress_callback, "general")
    
    async def _fill_all_forms_on_page(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback, form_type: str):
        """Fill all forms found on the current page"""
        forms = await self.form_detector.detect_all_forms(page)
        
        if not forms:
            # Try to wait for dynamic forms to load
            await asyncio.sleep(3)
            forms = await self.form_detector.detect_all_forms(page)
        
        await self._update_progress(progress_callback, 40, f"Found {len(forms)} forms to fill")
        
        for i, form in enumerate(forms):
            # Map data to fields
            field_mapping = await self._enhanced_data_mapping(user_data, form['fields'], form_type)
            
            # Fill the form
            filled_count = await self._fill_form_with_enhancements(page, form, field_mapping, progress_callback)
            result['forms_filled'] += 1
            
            # Handle file uploads
            upload_count = await self._handle_file_uploads(page, form, user_data)
            result['files_uploaded'] += upload_count
            
            # Take screenshot after each form
            screenshot = await self._capture_screenshot(page, f"form_{i}_completed")
            result['screenshots'].append(screenshot)
        
        # Try to submit
        await self._smart_form_submission(page, result)
    
    async def _handle_multi_step_form(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any], progress_callback, form_type: str, handle_uploads: bool = False):
        """Handle multi-step forms (common in job/visa applications)"""
        step_count = 0
        max_steps = 10  # Safety limit
        
        while step_count < max_steps:
            # Fill current step
            await self._fill_all_forms_on_page(page, user_data, result, progress_callback, form_type)
            
            # Look for "Next" or "Continue" buttons
            next_selectors = [
                'button:has-text("Next")', 'button:has-text("Continue")', 'button:has-text("Proceed")',
                'a:has-text("Next")', 'a:has-text("Continue")', 'input[value*="Next"]',
                'input[value*="Continue"]', '.next-button', '.continue-button', '#next-btn'
            ]
            
            next_found = await self._try_click_elements(page, next_selectors, "next button")
            
            if not next_found:
                # Try to submit if no next button
                await self._smart_form_submission(page, result)
                break
            
            step_count += 1
            await asyncio.sleep(2)  # Wait for next step to load
            await self._update_progress(progress_callback, 50 + (step_count * 10), f"Completed step {step_count}")
            
            # Take screenshot of each step
            screenshot = await self._capture_screenshot(page, f"step_{step_count}")
            result['screenshots'].append(screenshot)
            
            result['steps_completed'].append(f"Completed step {step_count}")
    
    async def _enhanced_data_mapping(self, user_data: Dict[str, Any], form_fields: List[Dict[str, Any]], form_type: str) -> Dict[str, Any]:
        """Enhanced data mapping based on form type"""
        mapping = await self._map_data_to_fields(user_data, form_fields)
        
        # Add form-type specific mappings
        if form_type == "job_application":
            mapping.update(await self._map_job_specific_fields(user_data, form_fields))
        elif form_type == "visa":
            mapping.update(await self._map_visa_specific_fields(user_data, form_fields))
        elif form_type == "appointment":
            mapping.update(await self._map_appointment_fields(user_data, form_fields))
        
        return mapping
    
    async def _map_job_specific_fields(self, user_data: Dict[str, Any], form_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map job application specific fields"""
        job_mapping = {}
        
        for field in form_fields:
            field_name = field.get('name', '').lower()
            field_label = field.get('label', '').lower()
            field_placeholder = field.get('placeholder', '').lower()
            
            field_text = f"{field_name} {field_label} {field_placeholder}"
            
            # Resume/CV upload
            if any(term in field_text for term in ['resume', 'cv', 'curriculum']):
                if 'resume_file' in user_data:
                    job_mapping[field['name']] = user_data['resume_file']
            
            # Cover letter
            elif any(term in field_text for term in ['cover', 'letter', 'motivation']):
                if 'cover_letter' in user_data:
                    job_mapping[field['name']] = user_data['cover_letter']
            
            # Salary expectations
            elif any(term in field_text for term in ['salary', 'compensation', 'expected']):
                if 'expected_salary' in user_data:
                    job_mapping[field['name']] = user_data['expected_salary']
            
            # Years of experience
            elif any(term in field_text for term in ['experience', 'years']):
                if 'years_experience' in user_data:
                    job_mapping[field['name']] = user_data['years_experience']
        
        return job_mapping
    
    async def _map_visa_specific_fields(self, user_data: Dict[str, Any], form_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map visa application specific fields"""
        visa_mapping = {}
        
        for field in form_fields:
            field_name = field.get('name', '').lower()
            field_label = field.get('label', '').lower()
            field_text = f"{field_name} {field_label}"
            
            # Passport information
            if any(term in field_text for term in ['passport', 'document']):
                if 'passport_number' in user_data:
                    visa_mapping[field['name']] = user_data['passport_number']
            
            # Travel dates
            elif any(term in field_text for term in ['arrival', 'departure', 'travel']):
                if 'travel_date' in user_data:
                    visa_mapping[field['name']] = user_data['travel_date']
            
            # Purpose of visit
            elif any(term in field_text for term in ['purpose', 'reason', 'visit']):
                if 'visit_purpose' in user_data:
                    visa_mapping[field['name']] = user_data['visit_purpose']
        
        return visa_mapping
    
    async def _map_appointment_fields(self, user_data: Dict[str, Any], form_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map appointment booking specific fields"""
        appointment_mapping = {}
        
        for field in form_fields:
            field_name = field.get('name', '').lower()
            field_label = field.get('label', '').lower()
            field_text = f"{field_name} {field_label}"
            
            # Preferred time
            if any(term in field_text for term in ['time', 'hour', 'minute']):
                if 'preferred_time' in user_data:
                    appointment_mapping[field['name']] = user_data['preferred_time']
            
            # Service type
            elif any(term in field_text for term in ['service', 'type', 'category']):
                if 'service_type' in user_data:
                    appointment_mapping[field['name']] = user_data['service_type']
        
        return appointment_mapping
    
    async def _handle_file_uploads(self, page: Page, form: Dict[str, Any], user_data: Dict[str, Any]) -> int:
        """Handle file upload fields"""
        upload_count = 0
        
        for field in form['fields']:
            if field.get('type') == FieldType.FILE_UPLOAD:
                field_name = field.get('name', '').lower()
                field_label = field.get('label', '').lower()
                
                # Determine what type of file to upload
                file_data = None
                if any(term in f"{field_name} {field_label}" for term in ['resume', 'cv']):
                    file_data = user_data.get('resume_file')
                elif any(term in f"{field_name} {field_label}" for term in ['photo', 'image', 'picture']):
                    file_data = user_data.get('photo_file')
                elif any(term in f"{field_name} {field_label}" for term in ['document', 'attachment']):
                    file_data = user_data.get('document_file')
                
                if file_data:
                    try:
                        element = field['element']
                        await element.set_input_files(file_data)
                        upload_count += 1
                        await self._log_action(f"Uploaded file to {field_name}", None)
                    except Exception as e:
                        await self._log_action(f"Failed to upload file to {field_name}", str(e))
        
        return upload_count
    
    async def _handle_date_selection(self, page: Page, user_data: Dict[str, Any], result: Dict[str, Any]):
        """Handle date/calendar selection for appointments"""
        try:
            # Look for date pickers
            date_selectors = [
                'input[type="date"]', '.datepicker', '.calendar', '[data-testid*="date"]',
                '.date-input', '#date', '.date-selector'
            ]
            
            for selector in date_selectors:
                try:
                    date_element = await page.wait_for_selector(selector, timeout=5000)
                    if date_element:
                        # Use preferred date or default to next week
                        target_date = user_data.get('preferred_date', 
                                                  (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'))
                        await date_element.fill(target_date)
                        result['steps_completed'].append(f"Selected date: {target_date}")
                        break
                except:
                    continue
                    
        except Exception as e:
            await self._log_action("Date selection failed", str(e))
    
    async def _try_click_elements(self, page: Page, selectors: List[str], element_type: str) -> bool:
        """Try to click any of the given selectors"""
        for selector in selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=3000)
                if element and await element.is_visible():
                    await element.scroll_into_view_if_needed()
                    await self.human_like_delay(500, 1000)
                    await element.click()
                    await self._log_action(f"Clicked {element_type}", selector)
                    return True
            except:
                continue
        return False
    
    async def _smart_form_submission(self, page: Page, result: Dict[str, Any]):
        """Smart form submission with multiple strategies"""
        submission_strategies = [
            # Strategy 1: Submit buttons
            ['button[type="submit"]', 'input[type="submit"]'],
            
            # Strategy 2: Common submit text
            ['button:has-text("Submit")', 'button:has-text("Send")', 'button:has-text("Apply")',
             'button:has-text("Register")', 'button:has-text("Sign up")', 'button:has-text("Book")'],
            
            # Strategy 3: Form submission via JavaScript
            ['form'],
            
            # Strategy 4: Generic buttons that might submit
            ['.submit-btn', '.send-btn', '.apply-btn', '#submit', '#send']
        ]
        
        for strategy in submission_strategies:
            for selector in strategy:
                try:
                    if selector == 'form':
                        # Try JavaScript form submission
                        await page.evaluate("""
                            () => {
                                const forms = document.querySelectorAll('form');
                                if (forms.length > 0) {
                                    forms[0].submit();
                                    return true;
                                }
                                return false;
                            }
                        """)
                        result['steps_completed'].append("Submitted form via JavaScript")
                        return True
                    else:
                        element = await page.wait_for_selector(selector, timeout=3000)
                        if element and await element.is_visible():
                            await element.scroll_into_view_if_needed()
                            await self.human_like_delay(1000, 2000)
                            await element.click()
                            result['steps_completed'].append(f"Submitted form via {selector}")
                            return True
                except:
                    continue
        
        return False
    
    async def _fill_form_with_enhancements(self, page: Page, form: Dict[str, Any], field_mapping: Dict[str, Any], progress_callback) -> int:
        """Enhanced form filling with better error handling"""
        filled_count = 0
        total_fields = len([f for f in form['fields'] if f['name'] in field_mapping])
        
        for i, field in enumerate(form['fields']):
            field_name = field.get('name', '')
            
            if field_name not in field_mapping:
                continue
            
            value = field_mapping[field_name]
            element = field['element']
            
            try:
                # Wait for element to be ready
                await element.wait_for_element_state('visible', timeout=10000)
                await element.wait_for_element_state('enabled', timeout=5000)
                
                # Scroll into view
                await element.scroll_into_view_if_needed()
                await self.human_like_delay(200, 500)
                
                # Focus element
                await element.focus()
                await self.human_like_delay(100, 300)
                
                field_type = field.get('type', 'text')
                
                if field_type in ['text', 'email', 'tel', 'password', 'number', 'url']:
                    # Clear and fill text fields
                    await element.clear()
                    await self.human_like_typing(element, '', str(value), mistakes=True)
                    
                elif field_type == FieldType.DROPDOWN:
                    # Handle select elements with multiple strategies
                    try:
                        await element.select_option(value=str(value))
                    except:
                        try:
                            await element.select_option(label=str(value))
                        except:
                            # Try clicking and selecting
                            await element.click()
                            await asyncio.sleep(0.5)
                            option = await page.query_selector(f'option:has-text("{value}")')
                            if option:
                                await option.click()
                    
                elif field_type == FieldType.CHECKBOX:
                    if value and str(value).lower() in ['true', '1', 'yes', 'on']:
                        await element.check()
                    else:
                        await element.uncheck()
                    
                elif field_type == FieldType.RADIO:
                    await element.click()
                    
                elif field_type == FieldType.TEXTAREA:
                    await element.clear()
                    await element.fill(str(value))
                
                filled_count += 1
                await self._log_action(f"Successfully filled field '{field_name}'", f"Value length: {len(str(value))}")
                
                # Random delay between fields
                await self.human_like_delay(300, 800)
                
            except Exception as e:
                await self._log_action(f"Failed to fill field '{field_name}'", str(e))
        
        return filled_count 