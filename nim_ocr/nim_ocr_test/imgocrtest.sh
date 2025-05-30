# This file is from RAWR Agent - https://github.com/jeremykpark/rawr_agent

API_ENDPOINT="http://localhost:8010"

# Create JSON payload with base64 encoded image

IMAGE_SOURCE="../../img/birthday-party-flyer.jpg"
# IMAGE_SOURCE="path/to/your/image.jpg"  # Uncomment to use a local file instead

# Encode the image to base64 (handles both URLs and local files)
if [[ $IMAGE_SOURCE == http* ]]; then
  # Handle URL
  BASE64_IMAGE=$(curl -s ${IMAGE_SOURCE} | base64 -w 0)
else
  # Handle local file
  BASE64_IMAGE=$(base64 -w 0 ${IMAGE_SOURCE})
fi

# Construct the full JSON payload
JSON_PAYLOAD='{
  "input": [{
    "type": "image_url",
    "url": "data:image/jpeg;base64,'${BASE64_IMAGE}'"
  }]
}'

# Send POST request to inference endpoint
echo "${JSON_PAYLOAD}" | \
  curl -X POST "${API_ENDPOINT}/v1/infer" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d @-
