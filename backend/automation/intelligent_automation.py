"""
Intelligent General-Purpose Form Automation Engine
Handles form filling on any website using AI and smart detection
"""

import asyncio
import logging
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import base64
import json

from playwright.async_api import Page, Browser, BrowserContext, ElementHandle
from .browser_automation import EnhancedBrowserAutomation
from .form_detection import FormFieldDetector, FieldType

logger = logging.getLogger(__name__)

class IntelligentFormAutomation(EnhancedBrowserAutomation):
    """Advanced form automation that works on any website"""
    
    def __init__(self):
        super().__init__()
        self.form_detector = FormFieldDetector()
        self.filled_fields = []
        self.automation_log = []
        
    async def automate_form_filling(self, 
                                   url: str, 
                                   user_data: Dict[str, Any],
                                   session_id: str,
                                   progress_callback: Optional[callable] = None) -> Dict[str, Any]:
        """
        Main automation method that handles the entire form filling process
        
        Args:
            url: Target website URL
            user_data: Structured data to fill into forms
            session_id: Session ID for tracking
            progress_callback: Callback for progress updates
            
        Returns:
            Dict with automation results and status
        """
        result = {
            'success': False,
            'fields_filled': 0,
            'forms_detected': 0,
            'errors': [],
            'screenshots': [],
            'log': []
        }
        
        try:
            # Initialize browser if not already done
            if not self.context:
                await self.initialize_stealth_browser()
            
            # Create new page
            page = await self.context.new_page()
            
            # Navigate to URL
            await self._update_progress(progress_callback, 10, "Navigating to website")
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await self._log_action("Navigated to website", url)
            
            # Take initial screenshot
            initial_screenshot = await self._capture_screenshot(page, "initial")
            result['screenshots'].append(initial_screenshot)
            
            # Detect forms on the page
            await self._update_progress(progress_callback, 20, "Detecting forms")
            forms = await self.form_detector.detect_all_forms(page)
            result['forms_detected'] = len(forms)
            await self._log_action(f"Detected {len(forms)} forms", None)
            
            if not forms:
                # Try to find login/register links if no forms found
                await self._update_progress(progress_callback, 25, "No forms found, looking for registration links")
                registration_found = await self._find_and_navigate_to_registration(page)
                
                if registration_found:
                    # Re-detect forms after navigation
                    await asyncio.sleep(2)  # Wait for page load
                    forms = await self.form_detector.detect_all_forms(page)
                    result['forms_detected'] = len(forms)
            
            if not forms:
                raise Exception("No forms detected on the page")
            
            # Process each form
            for i, form in enumerate(forms):
                await self._update_progress(
                    progress_callback, 
                    30 + (i * 40 // len(forms)), 
                    f"Processing form {i + 1} of {len(forms)}"
                )
                
                # Map user data to form fields
                field_mapping = await self._map_data_to_fields(user_data, form['fields'])
                
                # Fill the form
                filled_count = await self._fill_form_fields(page, form, field_mapping, progress_callback)
                result['fields_filled'] += filled_count
                
                # Take screenshot after filling
                form_screenshot = await self._capture_screenshot(page, f"form_{i}_filled")
                result['screenshots'].append(form_screenshot)
            
            # Look for submit button
            await self._update_progress(progress_callback, 80, "Looking for submit button")
            submit_success = await self._find_and_click_submit(page)
            
            if submit_success:
                await self._update_progress(progress_callback, 90, "Form submitted successfully")
                await asyncio.sleep(3)  # Wait for submission response
                
                # Take final screenshot
                final_screenshot = await self._capture_screenshot(page, "submission_result")
                result['screenshots'].append(final_screenshot)
                
                result['success'] = True
                await self._log_action("Form submitted successfully", None)
            else:
                await self._log_action("Submit button not found or clicked", None)
            
            await self._update_progress(progress_callback, 100, "Automation completed")
            
        except Exception as e:
            logger.error(f"Automation error: {str(e)}")
            result['errors'].append(str(e))
            await self._log_action(f"Error: {str(e)}", None)
        
        finally:
            result['log'] = self.automation_log
            if 'page' in locals():
                await page.close()
        
        return result
    
    async def _find_and_navigate_to_registration(self, page: Page) -> bool:
        """Find and navigate to registration/signup page"""
        try:
            # Common registration link patterns
            registration_patterns = [
                'a:has-text("Sign up")',
                'a:has-text("Register")', 
                'a:has-text("Create account")',
                'a:has-text("Join")',
                'a:has-text("Get started")',
                'button:has-text("Sign up")',
                'button:has-text("Register")'
            ]
            
            for pattern in registration_patterns:
                try:
                    element = await page.wait_for_selector(pattern, timeout=5000)
                    if element:
                        await element.click()
                        await page.wait_for_load_state('networkidle')
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding registration link: {str(e)}")
            return False
    
    async def _map_data_to_fields(self, 
                                 user_data: Dict[str, Any], 
                                 form_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Intelligently map user data to detected form fields"""
        mapping = {}
        
        # Create a normalized version of user data keys
        normalized_user_data = {k.lower().replace('_', ''): v for k, v in user_data.items()}
        
        for field in form_fields:
            field_purpose = field.get('purpose', FieldType.UNKNOWN)
            field_name = field.get('name', '')
            
            # Skip hidden, submit, and button fields
            if field.get('type') in ['hidden', 'submit', 'button']:
                continue
            
            # Direct purpose mapping
            if field_purpose == FieldType.EMAIL and 'email' in normalized_user_data:
                mapping[field_name] = normalized_user_data['email']
                
            elif field_purpose == FieldType.FIRST_NAME:
                if 'firstname' in normalized_user_data:
                    mapping[field_name] = normalized_user_data['firstname']
                elif 'first_name' in user_data:
                    mapping[field_name] = user_data['first_name']
                elif 'fullname' in normalized_user_data:
                    # Split full name
                    parts = normalized_user_data['fullname'].split(' ')
                    mapping[field_name] = parts[0]
                    
            elif field_purpose == FieldType.LAST_NAME:
                if 'lastname' in normalized_user_data:
                    mapping[field_name] = normalized_user_data['lastname']
                elif 'last_name' in user_data:
                    mapping[field_name] = user_data['last_name']
                elif 'fullname' in normalized_user_data:
                    # Split full name
                    parts = normalized_user_data['fullname'].split(' ')
                    if len(parts) > 1:
                        mapping[field_name] = ' '.join(parts[1:])
                        
            elif field_purpose == FieldType.FULL_NAME:
                if 'fullname' in normalized_user_data:
                    mapping[field_name] = normalized_user_data['fullname']
                elif 'full_name' in user_data:
                    mapping[field_name] = user_data['full_name']
                elif 'firstname' in normalized_user_data and 'lastname' in normalized_user_data:
                    mapping[field_name] = f"{normalized_user_data['firstname']} {normalized_user_data['lastname']}"
                    
            elif field_purpose == FieldType.PHONE:
                for key in ['phone', 'telephone', 'mobile', 'cell', 'phonenumber']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.ADDRESS:
                for key in ['address', 'streetaddress', 'street']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.CITY:
                if 'city' in normalized_user_data:
                    mapping[field_name] = normalized_user_data['city']
                    
            elif field_purpose == FieldType.STATE:
                for key in ['state', 'province', 'region']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.ZIP_CODE:
                for key in ['zip', 'zipcode', 'postalcode', 'postal']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.COUNTRY:
                if 'country' in normalized_user_data:
                    mapping[field_name] = normalized_user_data['country']
                    
            elif field_purpose == FieldType.COMPANY:
                for key in ['company', 'organization', 'employer']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.JOB_TITLE:
                for key in ['jobtitle', 'position', 'title', 'role']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.DATE_OF_BIRTH:
                for key in ['dob', 'dateofbirth', 'birthdate', 'birthday']:
                    if key in normalized_user_data:
                        mapping[field_name] = normalized_user_data[key]
                        break
                        
            elif field_purpose == FieldType.PASSWORD:
                if 'password' in normalized_user_data:
                    mapping[field_name] = normalized_user_data['password']
                else:
                    # Generate a secure password if not provided
                    mapping[field_name] = self._generate_password()
                    
            elif field_purpose == FieldType.CONFIRM_PASSWORD:
                # Use the same password as the password field
                mapping[field_name] = mapping.get(
                    next((f['name'] for f in form_fields if f.get('purpose') == FieldType.PASSWORD), ''),
                    ''
                )
            
            # Log mapping
            if field_name in mapping:
                await self._log_action(
                    f"Mapped field '{field_name}' ({field_purpose}) to value",
                    f"Length: {len(str(mapping[field_name]))}"
                )
        
        return mapping
    
    async def _fill_form_fields(self, 
                               page: Page, 
                               form: Dict[str, Any],
                               field_mapping: Dict[str, Any],
                               progress_callback: Optional[callable] = None) -> int:
        """Fill form fields with mapped data"""
        filled_count = 0
        total_fields = len([f for f in form['fields'] if f['name'] in field_mapping])
        
        for i, field in enumerate(form['fields']):
            field_name = field.get('name', '')
            
            if field_name not in field_mapping:
                continue
            
            value = field_mapping[field_name]
            element = field['element']
            
            try:
                # Update progress
                if progress_callback and total_fields > 0:
                    progress = 40 + (i * 30 // total_fields)
                    await self._update_progress(
                        progress_callback, 
                        progress, 
                        f"Filling field: {field.get('label', field_name)}"
                    )
                
                # Ensure element is visible and enabled
                await element.wait_for_element_state('visible', timeout=5000)
                
                # Fill based on field type
                field_type = field.get('type', 'text')
                
                if field_type in ['text', 'email', 'tel', 'password', 'number']:
                    # Clear existing value
                    await element.click()
                    await element.fill('')
                    
                    # Type with human-like behavior
                    await self.human_like_typing(element, '', value, mistakes=False)
                    filled_count += 1
                    
                elif field_type == FieldType.DROPDOWN:
                    # Handle select elements
                    await element.select_option(value=value)
                    filled_count += 1
                    
                elif field_type == FieldType.CHECKBOX:
                    # Check the checkbox if value is truthy
                    if value:
                        is_checked = await element.is_checked()
                        if not is_checked:
                            await element.check()
                        filled_count += 1
                        
                elif field_type == FieldType.RADIO:
                    # Click radio button if value matches
                    radio_value = await element.get_attribute('value')
                    if radio_value == value:
                        await element.click()
                        filled_count += 1
                        
                elif field_type == FieldType.TEXTAREA:
                    # Fill textarea
                    await element.click()
                    await element.fill(value)
                    filled_count += 1
                
                # Log successful fill
                await self._log_action(
                    f"Filled field '{field.get('label', field_name)}'",
                    f"Type: {field_type}"
                )
                
                # Small delay between fields
                await self.human_like_delay(300, 600)
                
            except Exception as e:
                logger.error(f"Error filling field {field_name}: {str(e)}")
                await self._log_action(
                    f"Failed to fill field '{field_name}'",
                    str(e)
                )
        
        return filled_count
    
    async def _find_and_click_submit(self, page: Page) -> bool:
        """Find and click the submit button"""
        try:
            # Common submit button patterns
            submit_patterns = [
                'button[type="submit"]',
                'input[type="submit"]',
                'button:has-text("Submit")',
                'button:has-text("Sign up")',
                'button:has-text("Register")',
                'button:has-text("Create account")',
                'button:has-text("Continue")',
                'button:has-text("Next")',
                '.submit-button',
                '#submit-button'
            ]
            
            for pattern in submit_patterns:
                try:
                    submit_button = await page.wait_for_selector(pattern, timeout=3000)
                    if submit_button and await submit_button.is_visible():
                        # Scroll into view and click
                        await submit_button.scroll_into_view_if_needed()
                        await self.human_like_delay(500, 1000)
                        await submit_button.click()
                        return True
                except:
                    continue
            
            # If no submit button found, try to submit the form directly
            await page.evaluate("""
                () => {
                    const form = document.querySelector('form');
                    if (form) {
                        form.submit();
                        return true;
                    }
                    return false;
                }
            """)
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding/clicking submit button: {str(e)}")
            return False
    
    async def _capture_screenshot(self, page: Page, name: str) -> str:
        """Capture and return base64 encoded screenshot"""
        try:
            screenshot_bytes = await page.screenshot(type='png', full_page=False)
            screenshot_b64 = base64.b64encode(screenshot_bytes).decode('utf-8')
            
            return {
                'name': name,
                'timestamp': datetime.utcnow().isoformat(),
                'data': screenshot_b64
            }
        except Exception as e:
            logger.error(f"Error capturing screenshot: {str(e)}")
            return None
    
    async def _update_progress(self, callback: Optional[callable], progress: int, status: str):
        """Update progress through callback"""
        if callback:
            await callback({
                'progress': progress,
                'status': status,
                'timestamp': datetime.utcnow().isoformat()
            })
    
    async def _log_action(self, action: str, details: Any):
        """Log automation actions"""
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'action': action,
            'details': details
        }
        self.automation_log.append(log_entry)
        logger.info(f"Automation: {action} - {details}")
    
    def _generate_password(self) -> str:
        """Generate a secure password"""
        import string
        import secrets
        
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(secrets.choice(alphabet) for _ in range(12))
        return password + "Aa1!"  # Ensure it meets common requirements 