import openai
from PIL import Image
import requests
import os
import uuid

# ⚡ Set your API key here OR use an environment variable for safety
# Option 1: Directly in code (quick, not recommended for public repos)
# openai.api_key = "YOUR_OPENAI_API_KEY"

# Option 2: Environment variable (recommended)
openai.api_key = os.getenv("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")

# Folder to save generated images
IMAGE_FOLDER = "data/images"
os.makedirs(IMAGE_FOLDER, exist_ok=True)

def generate_image_from_text(prompt):
    """
    Generates an image from a text prompt using OpenAI's GPT Image model
    and saves it locally in IMAGE_FOLDER.

    Args:
        prompt (str): The text prompt for image generation.

    Returns:
        str: File path of the saved image.
    """
    try:
        # Generate the image
        response = openai.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="512x512",
            n=1
        )

        # Get the image URL from the response
        img_url = response.data[0].url

        # Download the image
        img_data = requests.get(img_url).content

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.png"
        file_path = os.path.join(IMAGE_FOLDER, filename)

        # Save the image locally
        with open(file_path, "wb") as f:
            f.write(img_data)

        return file_path

    except Exception as e:
        print(f"[ERROR] Failed to generate image: {e}")
        return None