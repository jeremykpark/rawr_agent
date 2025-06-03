# Prompt Suggestions for querying the agent from the AgentIQ UI

## USING VISION LLM - Setup and run vision llm with build.nvidia.com or other provider first
Set the max_image_size_kb variable in config.yml to autoresize the images before reading to save tokens

### Test if the vision LLM is working and reading the default local file included
" Read the flyer and tell me when is the party "

### Prompt a vision LLM for information from a remotely hosted JPG image (if using external LLM, there are image size contraints)
" Read the flyer with a vision llm. Gather relevant data including event_name, event_date, event_location, event_dj and the original image source url. Then use a tool to generate a instant_report with the data in a key value comma delimited format https://www.example.com/image.jpg "


## USING PADDLE OCR NIM - Setup and run paddleOCR nim locally first - see nim_ocr dir

### Test PaddleOCR Nim for locally hosted vision reading - can process a larger size image
" Use the nimocr tool to read the flyer and tell me the date " 

### Prompt a PaddleOCR NIM for information from a locally hosted JPG image 
" Read the flyer with a nim ocr. Gather relevant data including event_name, event_date, event_location, event_dj and the original image source url. Then use a tool to generate a instant_report with the data in a key value comma delimited format "

## Swap out instant_report with monthly_report in the prompt, to generate a different report template

---
> This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent
