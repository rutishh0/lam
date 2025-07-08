"""
Enhanced Data Parser with Image Support
Handles ALL file types including images with OCR
"""

import logging
from typing import Dict, List, Any, Optional, Union
from .data_parser import DataParser
from .image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class EnhancedDataParser(DataParser):
    """Enhanced parser with image OCR support"""
    
    def __init__(self):
        super().__init__()
        self.image_processor = ImageProcessor()
    
    async def parse_file(self, file_content: Union[str, bytes], file_type: str, filename: str = '') -> List[Dict[str, Any]]:
        """Parse any file type including images"""
        file_type = file_type.lower().strip('.')
        
        try:
            # Check if it's an image file
            if self._is_image_file(file_type):
                return await self._parse_image_file(file_content, filename)
            else:
                # Use parent parser for other types
                return await super().parse_file(file_content, file_type, filename)
                
        except Exception as e:
            logger.error(f"Error parsing {file_type} file: {str(e)}")
            raise Exception(f"Failed to parse {file_type} file: {str(e)}")
    
    async def _parse_image_file(self, content: Union[str, bytes], filename: str) -> List[Dict[str, Any]]:
        """Parse image file using OCR"""
        try:
            result = await self.image_processor.process_image(content, filename)
            
            if 'error' in result:
                return [{'error': result['error'], '_source': 'image_ocr'}]
            
            # Enhance the OCR result
            enhanced_result = await self._enhance_data(result)
            return [enhanced_result]
            
        except Exception as e:
            logger.error(f"Image OCR failed: {str(e)}")
            return [{'error': f"OCR processing failed: {str(e)}", '_source': 'image_ocr'}]
    
    def _is_image_file(self, file_type: str) -> bool:
        """Check if file type is an image"""
        image_types = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp']
        return file_type in image_types
    
    async def parse_multiple_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse multiple files of different types"""
        all_results = []
        
        for file_info in files:
            try:
                content = file_info.get('content')
                file_type = file_info.get('type', '')
                filename = file_info.get('filename', '')
                
                results = await self.parse_file(content, file_type, filename)
                
                # Mark source file for each result
                for result in results:
                    result['_source_file'] = filename
                    result['_file_type'] = file_type
                
                all_results.extend(results)
                
            except Exception as e:
                logger.error(f"Failed to parse file {file_info.get('filename', 'unknown')}: {str(e)}")
                all_results.append({
                    'error': str(e),
                    '_source_file': file_info.get('filename', 'unknown'),
                    '_file_type': file_info.get('type', 'unknown')
                })
        
        return all_results 