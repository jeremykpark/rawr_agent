# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent
import logging
import base64
import requests

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
    Extracts data from images as json data. Json schema is based on prompt provided.
    """
    # Add your custom configuration parameters here
    parameter: str = Field(default="default_value", description="Notional description for this parameter")
    llm_name: LLMRef = Field(description="LLM to use for extracting data from images")

@register_function(config_type=rawrImageExtractorFunctionConfig, framework_wrappers=[LLMFrameworkEnum.LANGCHAIN])
async def rawr_image_extractor_llm_function(
    config: rawrImageExtractorFunctionConfig, builder: Builder
):
    # Implement your function logic here
    async def _response_fn(context: str, image_source: str="img/birthday-party-flyer.jpg") -> str:
        # Encode the image provided url - if no image provided, use the included birthday party flyer
        image_data_url = encode_image(image_source)
        
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
        
        
        
        
def encode_image(encode_image_source):
    """
    Encode an image to base64 data URL.

    Args:
        image_source: A URL or a local file path

    Returns:
        A base64-encoded data URL
    """
    # Check if the source is a URL or local file
    if encode_image_source.startswith(('http://', 'https://')):
        # Handle remote URL
        response = requests.get(encode_image_source)
        response.raise_for_status()
        image_bytes = response.content
    else:
        # Handle local file
        with open(encode_image_source, 'rb') as f:
            image_bytes = f.read()

    # Encode to base64
    base64_image = base64.b64encode(image_bytes).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_image}"

