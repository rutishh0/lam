"""
Intelligent Form Detection Engine
Detects and classifies form fields on any website using AI and heuristics
"""

import asyncio
import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from playwright.async_api import Page, ElementHandle
import json

logger = logging.getLogger(__name__)

class FieldType:
    """Common field types we can detect"""
    EMAIL = "email"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    FULL_NAME = "full_name"
    PHONE = "phone"
    ADDRESS = "address"
    CITY = "city"
    STATE = "state"
    ZIP_CODE = "zip_code"
    COUNTRY = "country"
    DATE_OF_BIRTH = "date_of_birth"
    COMPANY = "company"
    JOB_TITLE = "job_title"
    PASSWORD = "password"
    CONFIRM_PASSWORD = "confirm_password"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    DROPDOWN = "dropdown"
    FILE_UPLOAD = "file_upload"
    TEXTAREA = "textarea"
    UNKNOWN = "unknown"

class FormFieldDetector:
    """Detects and classifies form fields intelligently"""
    
    def __init__(self):
        # Field detection patterns
        self.patterns = {
            FieldType.EMAIL: [
                r'email', r'e-mail', r'e_mail', r'mail', r'correo', 
                r'courriel', r'email_address', r'emailaddress'
            ],
            FieldType.FIRST_NAME: [
                r'first_?name', r'fname', r'given_?name', r'forename',
                r'nombre', r'prenom', r'firstname', r'first'
            ],
            FieldType.LAST_NAME: [
                r'last_?name', r'lname', r'surname', r'family_?name',
                r'apellido', r'nom', r'lastname', r'last'
            ],
            FieldType.FULL_NAME: [
                r'full_?name', r'name', r'your_?name', r'complete_?name',
                r'nombre_?completo', r'fullname'
            ],
            FieldType.PHONE: [
                r'phone', r'tel', r'telephone', r'mobile', r'cell',
                r'telefono', r'numero', r'contact_?number', r'phone_?number'
            ],
            FieldType.ADDRESS: [
                r'address', r'street', r'addr', r'direccion', r'adresse',
                r'street_?address', r'address_?line'
            ],
            FieldType.CITY: [
                r'city', r'town', r'ciudad', r'ville', r'locality'
            ],
            FieldType.STATE: [
                r'state', r'province', r'region', r'estado', r'provincia'
            ],
            FieldType.ZIP_CODE: [
                r'zip', r'postal', r'postcode', r'zip_?code', r'codigo_?postal',
                r'code_?postal', r'pincode'
            ],
            FieldType.COUNTRY: [
                r'country', r'pais', r'pays', r'nation'
            ],
            FieldType.DATE_OF_BIRTH: [
                r'dob', r'birth', r'birthday', r'date_?of_?birth',
                r'fecha_?nacimiento', r'date_?naissance'
            ],
            FieldType.COMPANY: [
                r'company', r'organization', r'org', r'empresa',
                r'societe', r'business', r'employer'
            ],
            FieldType.JOB_TITLE: [
                r'job_?title', r'position', r'role', r'title',
                r'cargo', r'poste', r'designation'
            ],
            FieldType.PASSWORD: [
                r'password', r'pass', r'pwd', r'contraseña', r'mot_?de_?passe'
            ],
            FieldType.CONFIRM_PASSWORD: [
                r'confirm_?password', r'retype_?password', r'password_?confirm',
                r'verify_?password', r'repeat_?password'
            ]
        }
        
        # Compile regex patterns for efficiency
        self.compiled_patterns = {}
        for field_type, patterns in self.patterns.items():
            self.compiled_patterns[field_type] = re.compile(
                '|'.join(patterns), re.IGNORECASE
            )
    
    async def detect_all_forms(self, page: Page) -> List[Dict[str, Any]]:
        """Detect all forms on the page"""
        forms = []
        
        # Find all form elements
        form_elements = await page.query_selector_all('form')
        
        # Also find inputs not in forms (common in modern SPAs)
        all_inputs = await page.query_selector_all(
            'input:not([type="hidden"]), select, textarea'
        )
        
        # Process formal form elements
        for i, form in enumerate(form_elements):
            form_data = await self.analyze_form(form, f"form_{i}")
            if form_data['fields']:
                forms.append(form_data)
        
        # Check for inputs outside forms
        orphan_inputs = []
        for input_elem in all_inputs:
            in_form = await input_elem.evaluate(
                "el => el.closest('form') !== null"
            )
            if not in_form:
                orphan_inputs.append(input_elem)
        
        if orphan_inputs:
            orphan_form_data = await self.analyze_orphan_inputs(orphan_inputs)
            if orphan_form_data['fields']:
                forms.append(orphan_form_data)
        
        return forms
    
    async def analyze_form(self, form: ElementHandle, form_id: str) -> Dict[str, Any]:
        """Analyze a single form element"""
        form_data = {
            'id': form_id,
            'fields': [],
            'action': await form.get_attribute('action'),
            'method': await form.get_attribute('method') or 'POST'
        }
        
        # Get all input fields within the form
        inputs = await form.query_selector_all(
            'input:not([type="hidden"]), select, textarea'
        )
        
        for input_elem in inputs:
            field_info = await self.analyze_field(input_elem)
            if field_info:
                form_data['fields'].append(field_info)
        
        return form_data
    
    async def analyze_orphan_inputs(self, inputs: List[ElementHandle]) -> Dict[str, Any]:
        """Analyze inputs that are not within a form element"""
        form_data = {
            'id': 'orphan_form',
            'fields': [],
            'action': None,
            'method': 'POST',
            'note': 'Fields detected outside of formal form elements'
        }
        
        for input_elem in inputs:
            field_info = await self.analyze_field(input_elem)
            if field_info:
                form_data['fields'].append(field_info)
        
        return form_data
    
    async def analyze_field(self, element: ElementHandle) -> Optional[Dict[str, Any]]:
        """Analyze a single form field"""
        try:
            # Get basic field attributes
            field_info = {
                'element': element,
                'tag_name': await element.evaluate('el => el.tagName.toLowerCase()'),
                'type': await element.get_attribute('type') or 'text',
                'name': await element.get_attribute('name'),
                'id': await element.get_attribute('id'),
                'placeholder': await element.get_attribute('placeholder'),
                'required': await element.get_attribute('required') is not None,
                'value': await element.get_attribute('value'),
                'class': await element.get_attribute('class'),
                'aria_label': await element.get_attribute('aria-label'),
                'maxlength': await element.get_attribute('maxlength'),
                'pattern': await element.get_attribute('pattern')
            }
            
            # Find associated label
            field_info['label'] = await self.find_label(element, field_info)
            
            # Special handling for different input types
            if field_info['tag_name'] == 'select':
                field_info['type'] = FieldType.DROPDOWN
                field_info['options'] = await self.get_select_options(element)
            elif field_info['type'] == 'checkbox':
                field_info['type'] = FieldType.CHECKBOX
            elif field_info['type'] == 'radio':
                field_info['type'] = FieldType.RADIO
                field_info['radio_group'] = field_info['name']
            elif field_info['type'] == 'file':
                field_info['type'] = FieldType.FILE_UPLOAD
            elif field_info['tag_name'] == 'textarea':
                field_info['type'] = FieldType.TEXTAREA
            
            # Classify the field purpose using AI/heuristics
            field_info['purpose'] = await self.classify_field_purpose(field_info)
            
            # Determine if field is visible
            field_info['visible'] = await element.is_visible()
            
            # Get field position for accurate clicking
            field_info['position'] = await element.bounding_box()
            
            return field_info
            
        except Exception as e:
            logger.error(f"Error analyzing field: {str(e)}")
            return None
    
    async def find_label(self, element: ElementHandle, field_info: Dict[str, Any]) -> Optional[str]:
        """Find the label associated with a form field"""
        label_text = None
        
        # Method 1: Check for label with 'for' attribute
        if field_info['id']:
            label_text = await element.evaluate(
                f"""el => {{
                    const label = document.querySelector('label[for="{field_info['id']}"]');
                    return label ? label.textContent : null;
                }}"""
            )
        
        # Method 2: Check if input is inside a label
        if not label_text:
            parent_label = await element.evaluate(
                "el => el.closest('label') ? el.closest('label').textContent : null"
            )
            if parent_label:
                label_text = parent_label
        
        # Method 3: Check for adjacent text
        if not label_text:
            prev_text = await element.evaluate("""
                el => {
                    let prev = el.previousSibling;
                    while (prev && prev.nodeType !== 3 && prev.nodeType !== 1) {
                        prev = prev.previousSibling;
                    }
                    return prev ? prev.textContent : null;
                }
            """)
            if prev_text and len(prev_text.strip()) < 50:
                label_text = prev_text
        
        # Method 4: Check aria-label
        if not label_text and field_info['aria_label']:
            label_text = field_info['aria_label']
        
        return label_text.strip() if label_text else None
    
    async def get_select_options(self, select_element: ElementHandle) -> List[Dict[str, str]]:
        """Get all options from a select element"""
        options = await select_element.query_selector_all('option')
        option_list = []
        
        for option in options:
            value = await option.get_attribute('value')
            text = await option.text_content()
            if value is not None:  # Skip options without values
                option_list.append({
                    'value': value,
                    'text': text.strip() if text else ''
                })
        
        return option_list
    
    async def classify_field_purpose(self, field_info: Dict[str, Any]) -> str:
        """Classify the purpose of a field using patterns and heuristics"""
        
        # Combine all text indicators
        indicators = ' '.join(filter(None, [
            field_info.get('name', ''),
            field_info.get('id', ''),
            field_info.get('placeholder', ''),
            field_info.get('label', ''),
            field_info.get('aria_label', ''),
            field_info.get('class', '')
        ])).lower()
        
        # Check input type hints
        input_type = field_info.get('type', '').lower()
        
        # Direct type mappings
        if input_type == 'email':
            return FieldType.EMAIL
        elif input_type == 'tel':
            return FieldType.PHONE
        elif input_type == 'password':
            # Check if it's a confirm password field
            if any(term in indicators for term in ['confirm', 'retype', 'verify', 'repeat']):
                return FieldType.CONFIRM_PASSWORD
            return FieldType.PASSWORD
        
        # Pattern matching for field purpose
        for field_type, pattern in self.compiled_patterns.items():
            if pattern.search(indicators):
                return field_type
        
        # Additional heuristics
        
        # Check for date patterns
        if field_info.get('pattern') and 'date' in indicators:
            return FieldType.DATE_OF_BIRTH
        
        # Check maxlength for phone numbers
        if field_info.get('maxlength') in ['10', '11', '14', '15']:
            if any(term in indicators for term in ['phone', 'tel', 'mobile', 'contact']):
                return FieldType.PHONE
        
        # Check for address by field size
        if field_info.get('tag_name') == 'textarea' or field_info.get('maxlength', 0) > 50:
            if any(term in indicators for term in ['address', 'street', 'location']):
                return FieldType.ADDRESS
        
        # Default to unknown
        return FieldType.UNKNOWN
    
    def get_confidence_score(self, field_info: Dict[str, Any]) -> float:
        """Calculate confidence score for field classification"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on indicators
        if field_info.get('type') in ['email', 'tel', 'password']:
            confidence += 0.3
        
        if field_info.get('label'):
            confidence += 0.1
        
        if field_info.get('placeholder'):
            confidence += 0.1
        
        if field_info.get('name') and field_info['purpose'] != FieldType.UNKNOWN:
            confidence += 0.1
        
        return min(confidence, 1.0) 