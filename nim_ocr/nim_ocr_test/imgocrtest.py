import requests
import base64
import json
import io
from PIL import Image, ImageDraw

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


def visualize_text_detections(image_data, result, output_path):
    """
    Draw bounding boxes on the image based on API results.
    """
    # Load image from data URL or URL
    if image_data.startswith('data:'):
        # Extract base64 data after the comma
        b64_data = image_data.split(',')[1]
        image_bytes = base64.b64decode(b64_data)
        image = Image.open(io.BytesIO(image_bytes))
    else:
        # Download from URL
        response = requests.get(image_data)
        image = Image.open(io.BytesIO(response.content))

    draw = ImageDraw.Draw(image)

    # Get image dimensions
    width, height = image.size

    # Draw detected elements
    for detection in result["data"]:
        for text_detection in detection["text_detections"]:
            box = text_detection["bounding_box"]["points"]
            # Convert normalized coordinates to pixels
            x_min = int(min([point["x"] for point in box]) * width)
            y_min = int(min([point["y"] for point in box]) * height)
            x_max = int(max([point["x"] for point in box]) * width)
            y_max = int(max([point["y"] for point in box]) * height)

            # Draw rectangle
            draw.rectangle([x_min, y_min, x_max, y_max], outline="blue", width=3)

            # Add label with confidence
            label = f"{text_detection['text_prediction']['text']}: {text_detection['text_prediction']['confidence']:.2f}"
            draw.text((x_min, y_min-15), label, fill="blue")

    # Save the annotated image
    image.save(output_path)
    print(f"Annotated image saved to {output_path}")


# Example usage
if __name__ == "__main__":
    # Process the same sample image used in the cURL example
    image_source = "../../img/birthday-party-flyer.jpg"
    # Also works with local files
    # image_source = "path/to/your/image.jpg"
    api_endpoint = "http://localhost:8000"
    output_path = "detected_text_elements.jpg"

    try:
        # Encode the image
        image_data_url = encode_image(image_source)

        # Detect elements
        result = extract_text(image_data_url, api_endpoint)
        print(json.dumps(result, indent=2))

        # Visualize the results
        visualize_text_detections(image_data_url, result, output_path)

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
    except Exception as e:
        print(f"Error: {e}")
