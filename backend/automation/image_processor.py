"""
Image Processing and OCR Module
Extracts text and data from images for form automation
"""

import logging
import base64
import io
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
import re
from PIL import Image

# OCR imports
try:
    import pytesseract
    OCR_SUPPORT = True
except ImportError:
    OCR_SUPPORT = False

# Advanced OCR imports
try:
    import easyocr
    EASYOCR_SUPPORT = True
except ImportError:
    EASYOCR_SUPPORT = False

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Process images and extract text/data for automation"""
    
    def __init__(self):
        self.ocr_reader = None
        if EASYOCR_SUPPORT:
            try:
                self.ocr_reader = easyocr.Reader(['en'])
            except:
                logger.warning("Failed to initialize EasyOCR")
    
    async def process_image(self, image_data: Union[str, bytes], filename: str = '') -> Dict[str, Any]:
        """
        Process image and extract structured data
        
        Args:
            image_data: Image data as base64 string or bytes
            filename: Original filename for context
            
        Returns:
            Extracted structured data
        """
        if not OCR_SUPPORT:
            raise Exception("OCR support not available. Install: pip install pytesseract pillow")
        
        try:
            # Convert to PIL Image
            image = await self._prepare_image(image_data)
            
            # Extract text using OCR
            extracted_text = await self._extract_text_from_image(image)
            
            # Parse extracted text into structured data
            structured_data = await self._parse_extracted_text(extracted_text)
            
            # Add metadata
            structured_data['_image_processed_at'] = datetime.utcnow().isoformat()
            structured_data['_filename'] = filename
            structured_data['_extracted_text'] = extracted_text
            structured_data['_confidence'] = await self._calculate_ocr_confidence(extracted_text)
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return {'error': str(e), '_confidence': 0.0}
    
    async def _prepare_image(self, image_data: Union[str, bytes]) -> Image.Image:
        """Prepare image for OCR processing"""
        if isinstance(image_data, str):
            # Assume base64 encoded
            if image_data.startswith('data:image'):
                # Remove data URL prefix
                image_data = image_data.split(',')[1]
            image_bytes = base64.b64decode(image_data)
        else:
            image_bytes = image_data
        
        # Open with PIL
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance image quality for better OCR
        image = await self._enhance_image_for_ocr(image)
        
        return image
    
    async def _enhance_image_for_ocr(self, image: Image.Image) -> Image.Image:
        """Enhance image quality for better OCR results"""
        try:
            from PIL import ImageEnhance, ImageFilter
            
            # Resize if too small
            width, height = image.size
            if width < 800 or height < 600:
                scale_factor = max(800/width, 600/height)
                new_width = int(width * scale_factor)
                new_height = int(height * scale_factor)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.2)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.1)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.SMOOTH_MORE)
            
            return image
        except:
            # Return original if enhancement fails
            return image
    
    async def _extract_text_from_image(self, image: Image.Image) -> str:
        """Extract text from image using available OCR methods"""
        extracted_text = ""
        
        # Try EasyOCR first (usually better results)
        if EASYOCR_SUPPORT and self.ocr_reader:
            try:
                # Convert PIL to numpy array for EasyOCR
                import numpy as np
                image_array = np.array(image)
                
                results = self.ocr_reader.readtext(image_array)
                texts = [result[1] for result in results if result[2] > 0.5]  # Confidence > 50%
                extracted_text = ' '.join(texts)
                
                logger.info(f"EasyOCR extracted {len(texts)} text segments")
                
            except Exception as e:
                logger.warning(f"EasyOCR failed: {str(e)}")
        
        # Fallback to Tesseract OCR
        if not extracted_text and OCR_SUPPORT:
            try:
                extracted_text = pytesseract.image_to_string(image, config='--psm 6')
                logger.info("Tesseract OCR extraction completed")
            except Exception as e:
                logger.warning(f"Tesseract OCR failed: {str(e)}")
        
        # Final fallback - basic processing
        if not extracted_text:
            logger.warning("OCR extraction failed, image processing incomplete")
            extracted_text = "OCR_FAILED"
        
        return extracted_text.strip()
    
    async def _parse_extracted_text(self, text: str) -> Dict[str, Any]:
        """Parse extracted text into structured data"""
        if text == "OCR_FAILED":
            return {"error": "OCR extraction failed"}
        
        data = {}
        
        # Extract emails
        email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        emails = email_pattern.findall(text)
        if emails:
            data['email'] = emails[0]
        
        # Extract phone numbers
        phone_patterns = [
            re.compile(r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'),
            re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b'),
            re.compile(r'\b\+\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{3,4}[-.\s]?\d{3,4}\b')
        ]
        
        for pattern in phone_patterns:
            phones = pattern.findall(text)
            if phones:
                if isinstance(phones[0], tuple):
                    data['phone'] = ''.join(phones[0])
                else:
                    data['phone'] = phones[0]
                break
        
        # Extract names using common patterns
        name_patterns = [
            re.compile(r'(?:Name|Contact)[:\s]+([A-Za-z\s]{2,30})(?:\n|$)', re.I),
            re.compile(r'([A-Z][a-z]+\s+[A-Z][a-z]+)', re.M),  # Capitalized names
        ]
        
        for pattern in name_patterns:
            names = pattern.findall(text)
            if names:
                full_name = names[0].strip()
                if len(full_name.split()) >= 2:
                    data['full_name'] = full_name
                    name_parts = full_name.split()
                    data['first_name'] = name_parts[0]
                    data['last_name'] = ' '.join(name_parts[1:])
                    break
        
        # Extract addresses
        address_patterns = [
            re.compile(r'(?:Address|Location)[:\s]+(.+?)(?:\n|$)', re.I),
            re.compile(r'\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln)', re.I)
        ]
        
        for pattern in address_patterns:
            addresses = pattern.findall(text)
            if addresses:
                data['address'] = addresses[0].strip()
                break
        
        # Extract dates
        date_patterns = [
            re.compile(r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b'),
            re.compile(r'(?:DOB|Date of Birth)[:\s]+(.+?)(?:\n|$)', re.I)
        ]
        
        for pattern in date_patterns:
            dates = pattern.findall(text)
            if dates:
                data['date_of_birth'] = dates[0].strip()
                break
        
        # Extract company/organization
        company_patterns = [
            re.compile(r'(?:Company|Organization|Employer)[:\s]+(.+?)(?:\n|$)', re.I),
            re.compile(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:Inc|LLC|Corp|Company|Ltd))', re.M)
        ]
        
        for pattern in company_patterns:
            companies = pattern.findall(text)
            if companies:
                data['company'] = companies[0].strip()
                break
        
        # Extract ID numbers (passport, SSN, etc.)
        id_patterns = [
            re.compile(r'(?:Passport|ID)[:\s#]*([A-Z0-9]{6,12})', re.I),
            re.compile(r'\b[0-9]{3}-[0-9]{2}-[0-9]{4}\b'),  # SSN pattern
            re.compile(r'\b[A-Z]{1,2}[0-9]{6,8}\b')  # Passport-like pattern
        ]
        
        for pattern in id_patterns:
            ids = pattern.findall(text)
            if ids:
                data['document_number'] = ids[0].strip()
                break
        
        # Extract any additional structured data
        # Look for key-value pairs
        kv_pattern = re.compile(r'([A-Za-z\s]+):\s*([^\n:]+)', re.M)
        kv_matches = kv_pattern.findall(text)
        
        for key, value in kv_matches:
            key = key.strip().lower().replace(' ', '_')
            value = value.strip()
            
            # Only add if not already captured and looks valid
            if (key not in data and 
                len(value) > 1 and len(value) < 100 and 
                not key.startswith('_')):
                data[key] = value
        
        return data
    
    async def _calculate_ocr_confidence(self, extracted_text: str) -> float:
        """Calculate confidence score for OCR extraction"""
        if not extracted_text or extracted_text == "OCR_FAILED":
            return 0.0
        
        confidence = 0.5  # Base confidence
        
        # Increase confidence for structured data found
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', extracted_text):
            confidence += 0.15  # Email found
        
        if re.search(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', extracted_text):
            confidence += 0.15  # Phone found
        
        if re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+', extracted_text):
            confidence += 0.1   # Name-like pattern found
        
        # Decrease confidence for very short or garbled text
        if len(extracted_text) < 20:
            confidence -= 0.2
        
        # Check for common OCR errors
        error_indicators = ['|||', '...', '???', 'lll', '000', 'OOO']
        for indicator in error_indicators:
            if indicator in extracted_text:
                confidence -= 0.1
                break
        
        return max(0.0, min(1.0, confidence))
    
    async def process_multiple_images(self, image_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple images and return combined structured data"""
        results = []
        
        for image_info in image_list:
            try:
                image_data = image_info.get('data')
                filename = image_info.get('filename', '')
                
                if image_data:
                    result = await self.process_image(image_data, filename)
                    result['_image_source'] = filename
                    results.append(result)
                    
            except Exception as e:
                logger.error(f"Failed to process image {filename}: {str(e)}")
                results.append({
                    'error': str(e),
                    '_image_source': filename,
                    '_confidence': 0.0
                })
        
        return results
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported image formats"""
        return [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif',
            'webp', 'ico', 'svg'
        ]
    
    def is_image_file(self, filename: str) -> bool:
        """Check if file is a supported image format"""
        if not filename:
            return False
        
        extension = filename.lower().split('.')[-1]
        return extension in self.get_supported_formats() 