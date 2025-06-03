# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent
import logging
import base64
import requests
import mimetypes
from urllib.parse import urlparse
import imghdr
from PIL import Image
import io

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.builder.framework_enum import LLMFrameworkEnum
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef

logger = logging.getLogger(__name__)


class rawrImageExtractorFunctionConfig(FunctionBaseConfig, name="rawr_image_extractor_llm"):
    """
    Extracts data from images as json data using an vision enabled LLM. Json schema should be in prompt provided.
    """
    # Add your custom configuration parameters here
    parameter: str = Field(default="default_value", description="Notional description for this parameter")
    llm_name: LLMRef = Field(description="LLM to use for extracting data from images")
    max_image_size_kb: int = Field(default=100, description="Maximum image size in KB before resizing")

@register_function(config_type=rawrImageExtractorFunctionConfig, framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
async def rawr_image_extractor_llm_function(
    config: rawrImageExtractorFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(context: str, image_source: str="img/birthday-party-flyer.jpg") -> str:
        # Encode the image provided url - if no image provided, use the included birthday party flyer
        image_data_url = encode_image(image_source, config.max_image_size_kb)
        
        # Prepare the data for sending to the LLM
        payload = f"{context} <img src=\"{image_data_url}\" />"
        
        llm_n = await builder.get_llm(llm_name=config.llm_name, wrapper_type=LLMFrameworkEnum.LANGCHAIN)
        result = await llm_n.ainvoke(payload)
        output_message = f"{result}"
        return output_message

    try:
        yield FunctionInfo.from_fn(_response_fn, description="    Extracts data from images as json data. Json schema is based on prompt provided.")
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up rawr_event_admin workflow.") 
        
        
        
        
def _get_mime_type_from_imghdr(img_type_short):
    """Maps imghdr short type to full MIME type."""
    mapping = {
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'tiff': 'image/tiff',
        'webp': 'image/webp',
        'bmp': 'image/bmp',
    }
    return mapping.get(img_type_short)

def determine_image_mime_type(image_source_path_or_url, image_bytes=None, http_headers=None):
    """
    Determines the MIME type of an image.
    Prioritizes HTTP Content-Type, then file extension, then content sniffing.
    """
    mime_type = None
    explicitly_supported_mimes = ['image/jpeg', 'image/png', 'image/gif', 'image/tiff', 'image/webp']

    # 1. Try HTTP Content-Type header if available (for URLs)
    if http_headers:
        content_type = http_headers.get('Content-Type')
        if content_type:
            ct_lower = content_type.lower().split(';')[0].strip()
            if ct_lower in explicitly_supported_mimes:
                return ct_lower
            elif ct_lower.startswith('image/'):
                mime_type = ct_lower

    # 2. Try guessing from file extension
    path_for_guessing = urlparse(image_source_path_or_url).path if image_source_path_or_url.startswith(('http://', 'https://')) else image_source_path_or_url
    guessed_mime_type, _ = mimetypes.guess_type(path_for_guessing)
    if guessed_mime_type:
        guessed_mime_lower = guessed_mime_type.lower()
        if guessed_mime_lower in explicitly_supported_mimes:
            return guessed_mime_lower
        elif guessed_mime_lower.startswith('image/'):
            if not mime_type:
                mime_type = guessed_mime_lower

    # 3. Try content sniffing using imghdr if image_bytes are available
    if image_bytes:
        img_type_short = imghdr.what(None, h=image_bytes)
        if img_type_short:
            sniffed_mime_type = _get_mime_type_from_imghdr(img_type_short)
            if sniffed_mime_type and sniffed_mime_type in explicitly_supported_mimes:
                return sniffed_mime_type
            elif sniffed_mime_type and not mime_type:
                mime_type = sniffed_mime_type

    # 4. Fallback or final decision
    if mime_type and mime_type.startswith('image/'):
        logger.info(f"Determined MIME type '{mime_type}' for {image_source_path_or_url} (may not be in primary support list).")
        return mime_type

    logger.warning(f"Could not reliably determine a supported image MIME type for {image_source_path_or_url}. Defaulting to 'image/jpeg'.")
    return 'image/jpeg'

def convert_image_to_target_format(image_bytes, original_mime_type):
    """
    Converts images from WEBP, TIFF, or GIF to JPG. PNGs and JPGs are passed through.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert WEBP, TIFF, or GIF to JPG
        if original_mime_type in ['image/webp', 'image/tiff', 'image/gif']:
            # Convert to RGB mode to handle transparency
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create a white background for transparency
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save as JPEG
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=85)
            converted_bytes = output_buffer.getvalue()
            logger.info(f"Converted {original_mime_type} to JPEG")
            return converted_bytes, 'image/jpeg'
        
        # PNG and JPEG pass through unchanged
        elif original_mime_type in ['image/png', 'image/jpeg']:
            return image_bytes, original_mime_type
        
        # Unknown format, try to convert to JPEG as fallback
        else:
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            output_buffer = io.BytesIO()
            img.save(output_buffer, format='JPEG', quality=85)
            converted_bytes = output_buffer.getvalue()
            logger.warning(f"Unknown format {original_mime_type}, converted to JPEG")
            return converted_bytes, 'image/jpeg'
            
    except Exception as e:
        logger.error(f"Error converting image format: {e}")
        # Return original bytes as fallback
        return image_bytes, original_mime_type

def resize_image_if_needed(image_bytes, current_mime_type, target_kb=100):
    """
    Resizes the given image if its size exceeds target_kb.
    """
    target_bytes = target_kb * 1024
    
    if len(image_bytes) <= target_bytes:
        logger.info(f"Image size {len(image_bytes)} bytes is within target of {target_bytes} bytes")
        return image_bytes, current_mime_type
    
    logger.info(f"Image size {len(image_bytes)} bytes exceeds target of {target_bytes} bytes, resizing...")
    
    try:
        img = Image.open(io.BytesIO(image_bytes))
        original_size = img.size
        
        if current_mime_type == 'image/jpeg':
            # For JPEG, try reducing quality first
            for quality in range(85, 19, -10):
                output_buffer = io.BytesIO()
                img.save(output_buffer, format='JPEG', quality=quality)
                if len(output_buffer.getvalue()) <= target_bytes:
                    logger.info(f"Reduced JPEG quality to {quality}, new size: {len(output_buffer.getvalue())} bytes")
                    return output_buffer.getvalue(), current_mime_type
            
            # If quality reduction isn't enough, reduce dimensions
            scale_factor = 0.9
            while scale_factor > 0.3:
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                output_buffer = io.BytesIO()
                resized_img.save(output_buffer, format='JPEG', quality=75)
                if len(output_buffer.getvalue()) <= target_bytes:
                    logger.info(f"Resized JPEG to {new_size}, new size: {len(output_buffer.getvalue())} bytes")
                    return output_buffer.getvalue(), current_mime_type
                
                scale_factor -= 0.1
        
        elif current_mime_type == 'image/png':
            # For PNG, try reducing dimensions first
            scale_factor = 0.9
            while scale_factor > 0.3:
                new_size = (int(original_size[0] * scale_factor), int(original_size[1] * scale_factor))
                resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                output_buffer = io.BytesIO()
                resized_img.save(output_buffer, format='PNG', optimize=True)
                if len(output_buffer.getvalue()) <= target_bytes:
                    logger.info(f"Resized PNG to {new_size}, new size: {len(output_buffer.getvalue())} bytes")
                    return output_buffer.getvalue(), current_mime_type
                
                scale_factor -= 0.1
            
            # If PNG is still too large, convert to JPEG
            logger.info("PNG still too large after resizing, converting to JPEG")
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Try JPEG with quality reduction
            for quality in range(75, 19, -10):
                output_buffer = io.BytesIO()
                img.save(output_buffer, format='JPEG', quality=quality)
                if len(output_buffer.getvalue()) <= target_bytes:
                    logger.info(f"Converted PNG to JPEG with quality {quality}, new size: {len(output_buffer.getvalue())} bytes")
                    return output_buffer.getvalue(), 'image/jpeg'
        
        # If we get here, we couldn't reduce the size enough
        logger.warning(f"Could not reduce image size below {target_kb}KB, using best attempt")
        return image_bytes, current_mime_type
        
    except Exception as e:
        logger.error(f"Error resizing image: {e}")
        return image_bytes, current_mime_type

def encode_image(image_source, target_kb=100):
    """
    Encode an image to base64 data URL with format conversion and resizing.
    Supports PNG, GIF, TIF, JPG, WEBP. Converts WEBP, TIFF, GIF to JPG.
    Resizes images larger than target_kb.
    """
    image_bytes = None
    http_headers = None

    # Fetch image bytes
    if image_source.startswith(('http://', 'https://')):
        try:
            response = requests.get(image_source, timeout=10)
            response.raise_for_status()
            image_bytes = response.content
            http_headers = response.headers
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching image from URL {image_source}: {e}")
            raise
    else:
        try:
            with open(image_source, 'rb') as f:
                image_bytes = f.read()
        except FileNotFoundError:
            logger.error(f"Local image file not found: {image_source}")
            raise
        except IOError as e:
            logger.error(f"IOError reading local image file {image_source}: {e}")
            raise

    if not image_bytes:
        raise ValueError(f"Failed to load image bytes from {image_source}")

    # Determine original MIME type
    original_mime_type = determine_image_mime_type(image_source, image_bytes, http_headers)
    logger.info(f"Original image format: {original_mime_type}")
    
    # Convert to target format (JPG or PNG)
    processed_image_bytes, current_mime_type = convert_image_to_target_format(image_bytes, original_mime_type)
    
    # Resize if needed
    final_image_bytes, final_mime_type = resize_image_if_needed(processed_image_bytes, current_mime_type, target_kb)
    
    # Encode to base64
    base64_image = base64.b64encode(final_image_bytes).decode('utf-8')
    data_url = f"data:{final_mime_type};base64,{base64_image}"
    
    logger.info(f"Encoded {image_source} as {final_mime_type}, final size: {len(final_image_bytes)} bytes")
    return data_url
