# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent
import logging
import base64
import requests
import json

from pydantic import Field

from aiq.builder.builder import Builder
from aiq.builder.function_info import FunctionInfo
from aiq.builder.framework_enum import LLMFrameworkEnum
from aiq.cli.register_workflow import register_function
from aiq.data_models.function import FunctionBaseConfig
from aiq.data_models.component_ref import LLMRef

logger = logging.getLogger(__name__)


class rawrImageExtractorNimOCRFunctionConfig(FunctionBaseConfig, name="rawr_image_extractor_nimocr"):
    """
    Extracts data from images as json data using PaddleOCR NIM
    
    Use only if explicitly asked to use local ocr or paddleocr or nim ocr
    """
    # Add your custom configuration parameters here
    parameter: str = Field(default="default_value", description="Notional description for this parameter")

@register_function(config_type=rawrImageExtractorNimOCRFunctionConfig)
async def rawr_image_extractor_nimocr_function(
    config: rawrImageExtractorNimOCRFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(input_message: str, image_source: str="img/birthday-party-flyer.jpg") -> str:
        # Encode the image provided url - if no image provided, use the included birthday party flyer
        output_gen = run_ocr(image_source)

        return output_gen
    
    try:
        yield FunctionInfo.from_fn(_response_fn, description="    Extracts data from images as json data with PaddleOCR NIM.")
    except GeneratorExit:
        print("Function exited early!")
    finally:
        print("Cleaning up rawr_event_admin workflow.") 
        
                              
def encode_image(image_source):
    """
    Encode an image to base64 data URL.

    Args:
        image_source: A URL or a local file path

    Returns:
        A base64-encoded data URL
    """
    # Check if the source is a URL or local file
    if image_source.startswith(('http://', 'https://')):
        # Handle remote URL
        response = requests.get(image_source)
        response.raise_for_status()
        image_bytes = response.content
    else:
        # Handle local file
        with open(image_source, 'rb') as f:
            image_bytes = f.read()

    # Encode to base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_image}"


def extract_text(image_data_url, api_endpoint):
    """
    Extract text from images using the PaddleOCR NIM API.

    Args:
        image_data_url: Data URL of the image to process
        api_endpoint: Base URL of the NIM service

    Returns:
        API response dict
    """
    # Prepare payload according to PaddleOCR API format
    payload = {
        "input": [
            {
                "type": "image_url",
                "url": image_data_url,
            }
        ]
    }

    # Make inference request
    url = f"{api_endpoint}/v1/infer"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def run_ocr(image_source):
    # Process the same sample image used in the cURL example
    # image_source = "img/birthday-party-flyer.jpg"
    # Also works with local files
    # image_source = "path/to/your/image.jpg"
    api_endpoint = "http://localhost:8010"
    output_path = "detected_text_elements.jpg"

    try:
        # Encode the image
        image_data_url = encode_image(image_source)

        # Detect elements
        result = extract_text(image_data_url, api_endpoint)
        return result
        #return json.dumps(result, indent=2)

    except requests.exceptions.RequestException as e:
        return "API request failed: {e}"
    except Exception as e:
        return "Error: {e}"