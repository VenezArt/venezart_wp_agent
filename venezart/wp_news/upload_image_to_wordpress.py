import os
import requests
import base64
from dotenv import load_dotenv

# The rest of your existing imports...
import logging

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
    image_path = "images/ai_gen_image_entrepreneurship.jpg"
    # Call the image upload function
    image_url = upload_image_to_wordpress(image_path)
    if image_url:
        logger.info(f"Image uploaded successfully: {image_url}")
    else:
        logger.error("Image upload failed. Please check the logs for details.")

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
                image_id = response.json().get('id')  # Get the image ID from the response
                image_url = response.json().get('source_url')
                logger.info(f"Image uploaded successfully: {image_url}")
                return image_id  # Return the image ID instead of the URL
            else:
                logger.error(f"Failed to upload image: {response.status_code}, {response.text}")
    except FileNotFoundError:
        logger.error(f"Image file not found: {image_path}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while uploading the image: {e}")

    return None



if __name__ == "__main__":
    main()