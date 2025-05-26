## Prompt Suggestions for querying the agent from the AgentIQ UI

## Test if the vision LLM is working and reading the default local file included
Read the flyer and tell me when is the party

## Prompt for information from a remotely hosted JPG image
Create a json with the data from this image with event name, event date, venue name, original url of image, artist names, url of event, and other additional info. When done, use a tool to create an instant report with the string encoded json output https://www.example.com/image.jpg

## Prompt LLM for information from a locally hosted JPG image (if using external LLM, there are image size contraints)
Create a json with the data from this image with event name, event date, venue name, original url of image, artist names, url of event, and other additional info. When done, use a tool to create an instant report with the string encoded json output <img href="base64"> </img>

## Prompt PaddleOCR Nim for locally hosted JPG image (unlimited size)
Use the nimocr tool to read the flyer and tell me the date

# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent