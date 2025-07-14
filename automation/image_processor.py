from PIL import Image
import io
from typing import Union

class ImageProcessor:
    async def _prepare_image(self, image_data: Union[str, bytes]) -> Image.Image:
        if isinstance(image_data, str):
            return Image.open(image_data)
        elif isinstance(image_data, bytes):
            return Image.open(io.BytesIO(image_data))
        else:
            raise TypeError("Unsupported image data type")
