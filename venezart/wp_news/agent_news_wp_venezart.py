import time

# Import the necessary modules (the rest of your script remains unchanged)
import os
import logging
import random
# import ollama
import base64
import requests
from dotenv import load_dotenv
from authenticate import open_ai_auth
from generate_image import generate_image, upload_image_to_wordpress  # Import the image generation function
from get_news import fetch_latest_news, extract_image  # Import the function to fetch the latest news
# Import functions from the other modules
from upload_image_to_wordpress import upload_image_to_wordpress  # Import the function to upload image to WordPress
from io import BytesIO

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from a .env file
load_dotenv()

# Environment variables
wordpress_url = os.getenv("WORDPRESS_URL")
username = os.getenv("WORDPRESS_USERNAME")
password = os.getenv("WORDPRESS_PASSWORD")

ai_client = open_ai_auth()

# Prepare the credentials for Basic Auth
auth_string = f"{username}:{password}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

# Headers with encoded authorization
headers = {
    "Authorization": f"Basic {encoded_auth}",
    "Content-Type": "application/json"
}



def download_image(image_url):
    """ Download an image from the given URL and save it locally """
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            # Save image locally
            image_path = "temp_image.jpg"
            with open(image_path, "wb") as f:
                f.write(response.content)
            logger.info(f"Image downloaded successfully from {image_url}")
            return image_path
        else:
            logger.error(f"Failed to download image: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while downloading the image: {e}")

    return None


def get_category_id(slug):
    """ Get category ID by slug """
    category_response = requests.get(f"{wordpress_url}/categories?slug={slug}", headers=headers)
    if category_response.status_code == 200:
        categories = category_response.json()
        if categories:
            category_id = categories[0]["id"]
            logger.info(f"Category ID for '{slug}': {category_id}")
            return category_id
        else:
            logger.error(f"Category with slug '{slug}' not found.")
    else:
        logger.error("Failed to retrieve categories:", category_response.status_code, category_response.text)
    return None


def get_tag_ids(slugs):
    """ Get tag IDs by slugs """
    tag_ids = []
    for slug in slugs:
        tag_response = requests.get(f"{wordpress_url}/tags?slug={slug}", headers=headers)
        if tag_response.status_code == 200:
            tags = tag_response.json()
            if tags:
                tag_id = tags[0]["id"]
                tag_ids.append(tag_id)
                logger.info(f"Tag ID for '{slug}': {tag_id}")
            else:
                logger.error(f"Tag with slug '{slug}' not found.")
        else:
            logger.error(f"Failed to retrieve tag '{slug}': {tag_response.status_code}, {tag_response.text}")
    return tag_ids


def gpt_generate_post(article):
    logger.info(f"Generating a post based on the following topic using ChatGPT API: {article}...")
    
    try:
        response = ai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful writing assistant."},
                {
                    "role": "user",
                    "content": (
                        f"Create a unique and engaging post about this article, {article} with a title and content. "
                        f"The title should be catchy, between 8-12 words, and suitable for a blog post. "
                        f"The content should be under 500 words and include relevant hashtags, SEO keywords, and emojis. "
                        f"Do not include the word 'Title' in the title."
                    ),
                },
            ],
        )
        
        full_content = response.choices[0].message.content.strip()
        lines = full_content.splitlines()
        
        # Extract the title from the first non-empty line, without a "Title:" prefix.
        title = None
        for line in lines:
            line = line.strip()
            if line and not line.lower().startswith("title:"):
                title = line.lstrip("*").strip()  # Remove any asterisks or leading/trailing spaces
                break
        
        if not title:
            title = f"{article.capitalize()} Insights"  # Fallback title if none detected

        # Extract the content after the title
        content_start_index = lines.index(title) + 1 if title in lines else 1
        content = "\n".join(lines[content_start_index:]).strip()

        logger.info(f"Generated Post - Title: {title}")
        logger.info(f"Content: {content}")
        
        return title, content

    except Exception as e:
        logger.error(f"Failed to generate post: {str(e)}")
        return None, None
    

def create_wordpress_post(title, content, category_ids, tag_ids, featured_image_id=None):
    """ Create a WordPress post with tags, categories, and optionally an image """
    post_data = {
        "title": title,
        "content": content,
        "status": "draft",
        "categories": category_ids,
        "tags": tag_ids
    }

    # Add featured image if available
    if featured_image_id:
        post_data["featured_media"] = featured_image_id

    try:
        response = requests.post(f"{wordpress_url}/posts", json=post_data, headers=headers)
        if response.status_code == 201:
            logger.info("Post created successfully: " + response.json().get("link"))
        else:
            logger.error(f"Failed to create post: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while creating the post: {e}")

# Main function to generate and create a WordPress post
def main():
    # Toggle for enabling or disabling image generation and upload
    enable_image_generation = os.getenv("ENABLE_IMAGE_GENERATION", "true").lower() == "true"
    
    articles = fetch_latest_news()
    if not articles:
        logger.error("No articles found. Stopping the app.")
        return

    article_index = random.randint(0, len(articles) - 1)  # Randomly select an article
    logger.info(f"Randomly selected article index: {article_index}")
    article = articles[article_index]  # Get the first article from the list
    logger.info(f"The randomly selected article for the post is: {article}")

    
    topic_category_id = get_category_id("Blog")
    just_release_category_id = get_category_id("just-release")

    # Adding tags
    tag_ids = get_tag_ids(["art", "blog", "creativity", "3D", "AiArt", "Artists", "ArtLovers", "Artwork", "DigitalArt", "Innovation", "Tech"])

    if topic_category_id and just_release_category_id:
        post_title, post_content = gpt_generate_post(article)

        # Create the WordPress post with the extracted image
        create_wordpress_post(post_title, post_content, [topic_category_id, just_release_category_id], tag_ids)


# Adding a loop to run continuously
if __name__ == "__main__":
    main()  # Run the main function to generate and post content