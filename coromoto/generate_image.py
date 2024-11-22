import os
import torch
import logging
import base64
import requests
from diffusers import StableDiffusionPipeline
from dotenv import load_dotenv
from PIL import Image  # Import for image format conversion

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Load environment variables from a .env file
load_dotenv()
# Headers with encoded authorization for other requests.
# We'll update headers in the `upload_image_to_wordpress` function specifically to handle image uploads.

# Environment variables loaded as previously described
wordpress_url = os.getenv("WORDPRESS_URL")
username = os.getenv("WORDPRESS_USERNAME")
password = os.getenv("WORDPRESS_PASSWORD")

# Prepare the credentials for Basic Auth
auth_string = f"{username}:{password}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()


def main():
    topic = "Entrepreneurship"  # Choose the topic here or dynamically
    image_path = generate_image(topic)
    if image_path:
        print(f"Image generated and saved at: {image_path}")
    else:
        print("Image generation failed.")

    upload_image_to_wordpress(image_path)

def upload_image_to_wordpress(image_path):
    """ Upload an image to WordPress media library """
    url = f"{wordpress_url}/media"
    
    # Headers for the image upload, with Basic Auth and specific content type for the file
    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Content-Disposition": f"attachment; filename={os.path.basename(image_path)}"
    }

    # Open the file in binary mode
    try:
        with open(image_path, 'rb') as img_file:
            # Prepare the file for upload
            files = {
                'file': (os.path.basename(image_path), img_file, 'image/jpeg')
            }

            logger.info(f"Uploading image {os.path.basename(image_path)} to WordPress...")
            
            response = requests.post(url, headers=headers, files=files)
            
            # Check if the image was uploaded successfully
            if response.status_code == 201:
                response_json = response.json()
                image_url = response_json.get('source_url')
                image_id = response_json.get('id')  # Get the ID of the uploaded image
                logger.info(f"Image uploaded successfully: {image_url}")
                return image_url, image_id 
            else:
                logger.error(f"Failed to upload image: {response.status_code}, {response.text}")
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while uploading the image: {e}")

    return None, None



def generate_image(topic):
    print(f"Generating image for topic: {topic}")
    model_id = "nitrosocke/redshift-diffusion"
    print(f"Loading model: {model_id}")

    if not torch.cuda.is_available():
        print("CUDA not available. Please run on a system with CUDA support.")
        return None

    try:
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    num_inference_steps = 25
    guidance_scale = 10

    # Updated prompts for each topic
    prompts = {
        "entrepreneurship": (
            "Western comic book art style, full shot, hero stands, cinematic, vector, inked lines"
            "vibrant colors, halftone shading, panel layout, action, movement"
            "with cinematic lighting and depth, conveying ambition, innovation, and growth."
        ),
        "art": (
            "Western comic book art style, full shot, cinematic, vector, inked lines"
            ""vibrant colors, halftone shading, panel layout, action, movement and creates a mesmerizing scene that invites "
            "viewers to explore creativity and imagination, with cinematic lighting and depth, conveying action and movement."
        ),
        "tech": (
            "Western comic book art style, cyberpunk, hero stands, cinematic, vector, inked lines"
            "Cool blue and neon lights illuminate the room, casting a sleek and modern ambiance. Digital schematics and "
            "AI interfaces are displayed, capturing the innovation and possibilities of advanced technology."
        ),
    }
    
    prompt = prompts.get(topic.lower(), "Default prompt if topic not found.")
    print(f"Using prompt: {prompt}")

    try:
        with torch.cuda.amp.autocast(dtype=torch.float16):
            image = pipe(prompt, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps).images[0]
        print("Image generated successfully.")
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

    # Convert image to RGB and save as JPEG
    if not os.path.exists("images"):
        os.makedirs("images")
        print("Created 'images' directory.")

    image_path = f"images/ai_gen_image_{topic}.jpg"  # Save as JPEG with .jpg extension
    image = image.convert("RGB")  # Convert to RGB for JPEG compatibility
    image.save(image_path, format="JPEG")
    print(f"Image saved to {image_path} as JPEG.")

    return image_path  # Return the path for further use

if __name__ == "__main__":
    main()
