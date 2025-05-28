## ** OPTIONAL ** FOR LOCAL OCR READING ##
Use a locally hosted NIM PADDLEOCR instance instead of an LLM for gathering image information in json

* Start a local NeMo Retreiver PADDLEOCR NIM server with docker, and locally read JSON data from images
* A low VRAM OCR Solution https://catalog.ngc.nvidia.com/orgs/nim/teams/baidu/containers/paddleocr

# Usage notes:
- Incorporate these functions into your solution for more sensitive image content, by running locally
- May be more difficult to identify text context from PaddleOCR json, rather than when prompting external vision LLM with exact requirements
- Can be better than using an external LLM, for standard forms etc

# How to start:
* Make sure global NGC_API_KEY variable is available and video card good nvidia-smi
* Also make sure docker is logged into nvcr.io - more info on ngc.nvidia.com api keys section abou this (scroll down)
* Run Nvidia OCR Nim with docker locally, by starting the start_ocr_nim.sh file
>  more info: https://docs.nvidia.com/nim/ingestion/table-extraction/latest/getting-started.html

# How to test:
* In a seperate terminal, run the imgocrtest.py script in the /nim_ocr/nim_ocr_test directory
* This should read the birthday party flyer located in the /img directory and output an image 'detected_text_elements' that shows the bounding boxes detected, and output a json at the same time.

#########

### This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent