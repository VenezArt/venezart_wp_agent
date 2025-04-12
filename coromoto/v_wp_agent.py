import time

# Import the necessary modules (the rest of your script remains unchanged)
import os
import logging
import random
import base64
import requests
from dotenv import load_dotenv
from authenticate import open_ai_auth
# from generate_image import generate_image, upload_image_to_wordpress  # Import the image generation function

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

# Other functions...

def generate_post_topic():
    topics = ["Art for Comic book", "Stable Diffusion", "ComfyUI", "Art Styles & Movements, Contemporary Art, Abstract & Surrealism, Street Art & Graffiti", "Digital Art & 3D Art", "Artist Features", "Emerging Artists to Watch", "Interviews with Renowned Artists", "Behind-the-Scenes of Creative Processes", "Art Techniques & Tutorials", "Drawing & Painting Tips", "how to create , draw, Comic book and Graphic novel", "Comic book creation tips", "Comic book and Graphic novel creation tutorials", "Digital Art Tools and Software Tutorials, Mixed Media & Experimental Art", "Generative AI, Text to Image, Text to Video, Text to 3d", "GenAI prompt sharing tips and ideas", "Art History & Culture", "Famous Artworks and Their Stories", "Cultural Significance of Art Across Eras", "Art in World Heritage Sites", "Evolution of Art Mediums, Art and Technology", "AI in Art Creation", "Virtual Reality (VR) Art Exhibits", "NFT Art", "Digital Collectibles", "crypto", "Innovations in Art Tools and Platforms",  "Art in Everyday Life", "Art for Home Decor", "Art for Apparel", "Art for Games",  "DIY Art Projects", "the Role of Art in Public Spaces", "Art Therapy & Mental Health", "Art Events & Exhibition", "Upcoming Art Shows and Galleries", "Reviews of Major Exhibitions", "Art Fairs and Biennales, Virtual Art Events", "Art Business & Careers", "How to Sell Your Art", "How to be a Freelancer Artist", "How to Improve as a Freelance artist", "Freelance Artist tips", "Building a Portfolio", "Art Licensing and Copyright", "Art Collecting Tips for Beginners", "Art and Society", "Art as Activism", "Representation in Art", "Art and Environmental Awareness", "Art Role in Social Movements", "Global Art Perspectives, Indigenous and Tribal Art", "Graffiti Art", "Cross-Cultural Art Influences", "Art from Emerging Regions", "Traditional vs. Modern Art in Different Cultures", "Art Supplies & Reviews", "Best Tools for Artists", "Reviews of Art Materials Paints, Brushes, Tablets, Sustainable Art Supplies", "Innovations in Art Materials", "Art Challenges & Community Engagement", "Monthly Art Challenges", "Collaborative Art Projects", "Online Art Communities and Forums", "Art Contests and Competitions", "Art and Entertainment", "Art in Film and TV", "Video Game Art and Design", "Music Album Covers and Visual Art", "Comics and Graphic Novels", "Future of Art", "Predictions for Art Trends, The Impact of AI and Automation on Art", "Virtual Art Galleries and Museums", "The Changing Role of Artists in Society", "entrepreneurship", "Startup Essentials", "How to Write a Business Plan", "Finding Your Niche Market", "Legal Basics for Startups", "Building Your Brand from Scratch", "Funding & Finance, Venture Capital & Angel Investors, Crowdfunding Strategies, Managing Cash Flow, Financial Tools for Entrepreneurs","Leadership & Management, Building and Leading a Team, Effective Decision-Making, Conflict Resolution in Business, Delegation and Time Management", "Marketing & Sales, Social Media Marketing Strategies, Creating a Winning Sales Funnel, Branding and Storytelling, SEO and Content Marketing for Small Businesses", "Innovation & Trends, Emerging Industries to Watch, Disruptive Technologies in Business, Trends in Sustainable Entrepreneurship, ,Adapting to Market Changes", "Success Stories, Interviews with Successful Entrepreneurs, Case Studies of Startups, Lessons from Failed Businesses, Profiles of Iconic Business Leaders", "Entrepreneurial Mindset, Overcoming Fear of Failure, Building Resilience and Confidence, Cultivating Creativity and Innovation, The Importance of Networking", "Tools & Resources, Productivity Apps for Entrepreneurs, Best CRMs for Small Businesses, Accounting and Finance Software, Project Management Tools", "Small Business Spotlight, Unique Business Ideas, Local Business Success Stories, Challenges Faced by Small Businesses, Tips for Running a Family Business", "Scaling & Growth, When to Expand Your Business, Strategies for Scaling Operations, Franchising Opportunities, Global Market Entry Tips", "Entrepreneurship for Specific Audiences, Women in Business, Young Entrepreneurs and Startups, Minority-Owned Businesses, Social Entrepreneurship", "E-Commerce & Online Business, Starting an Online Store, Dropshipping Pros and Cons, Digital Marketing for E-Commerce, Trends in Online Retail", "Work-Life Balance, Time Management for Entrepreneurs, Mental Health in Entrepreneurship, Tips for Avoiding Burnout, Juggling Family and Business", "Legal & Regulatory Insights, Protecting Your Intellectual Property, Understanding Business Taxes, Contracts and Agreements 101, Regulatory Challenges in Different Industries", "Social Impact & Sustainability,  Starting a Social Enterprise, Green Business Ideas, Measuring Social Impact, Balancing Profit with Purpose", "Digital Entrepreneurship, Monetizing Content and Social Media, Building a Personal Brand Online, Creating and Selling Digital Products, Freelancing and Gig Economy Tips", "entrepreneurship news","entrepreneurship actionable guides to starting, managing and scaling business","entrepreneurship life style","entrepreneurship mind, body and health", "art","art news covering the latest trends in the art world, including emerging artists, art styles, and groundbreaking projects","art tutorials providing step-by-step guides on various artistic techniques, digital tools, or creative projects", "art industry insights, discuss the art industry chanllenges, innovations and market trends in self publishing comicbooks, graphic novels, gaming, animation and cinematography", "tech", "tech news highlighting breakthroughs in tech, from AI advancements to new gadgets","tech tutorials guides that simplify complex tech concepts or explain how to use specific tools", "tech industry insights, analysing the implementation of tech trends and development", "Game Reviews, New Releases, In-depth reviews of the latest games, Indie Spotlight, Focus on lesser-known indie games, Retro Reviews, Revisiting classic titles and their impact, Early Access Reviews, Evaluating games still in development", "Gaming News, Industry Updates Major announcements, acquisitions, and trends, Esports News Tournaments, teams, and standout players, Platform News Updates from PlayStation, Xbox, Nintendo, PC, and mobile gaming, Tech Innovations Hardware, software, and game engine advancements" , "Game Previews, Upcoming Titles Sneak peeks at highly anticipated games, Developer Insights Interviews with developers about their projects, Beta Testing Reports Handson impressions from beta or demo versions", "Esports & Competitive Gaming, Tournaments and Events Coverage of major esports events, Pro Player Profiles Interviews and features on esports athletes, Tips for Competitive Gaming Strategies and techniques for improving gameplay, Esports Industry Trends Growth, challenges, and opportunities in the esports scene", "Gaming Culturen Communities Stories about passionate fanbases and their creations, Streaming and Content Creation Tips for Twitch, YouTube, and other platforms, Cosplay Features Showcasing gaming-inspired cosplay, Memes and Trends Viral moments and cultural phenomena in gaming", "Game Development Behind the Scenes Insights into how games are made, Interviews with Developers Conversations with designers, writers, and artists, Tools and Tutorials Guides for aspiring developers, Indie Dev Stories Challenges and triumphs of small studios", "Hardware & Accessories, Console Reviews Evaluations of gaming consoles and updates, PC Gaming Building and optimizing gaming rigs, Peripheral Reviews Keyboards, mice, headsets, and controllers", "VR and AR Reviews of VR headsets and AR experiences", "Guides and Walkthroughs, Beginners Guides Tutorials for popular games, Advanced Strategies Tips for mastering challenging games, Achievement Hunting Guides for unlocking achievements and trophies, Modding Guides How to mod games for custom experiences", "Gaming History The Evolution of Gaming Milestones in the industry, Iconic Franchises Deep dives into beloved series like Mario, Zelda, or Final Fantasy, Forgotten Gems Highlighting underrated or overlooked games, Gaming Hardware Through the Years The history of consoles and PCs", "Mobile Gaming Top Mobile Games Reviews and recommendations, Casual vs. Hardcore The spectrum of mobile gaming, Free to Play Analysis Pros and cons of popular monetization models, Cloud Gaming on Mobile Exploring services like Xbox Cloud Gaming and GeForce NOW", "Tabletop and Board Games, Digital Adaptations Video game versions of popular tabletop games, Crossover Games Board games inspired by video games", "Role Playing Games Features on D&D and other RPG systems", "Gaming and Society, Representation in Games Diversity and inclusion in characters and stories, Gaming and Mental Health The positive and negative impacts of gaming, Ethics in Gaming Discussions on microtransactions, loot boxes, and crunch culture, Educational Games Games designed for learning and development", "Future of Gaming AI in Gaming How AI is shaping game design and player experiences, The Metaverse Gamings role in virtual worlds, Cross-Platform Play The rise of seamless multiplayer experiences, Blockchain and NFTs The role of blockchain in gaming economies", "Gaming Events Conventions and Expos Coverage of E3, Gamescom, PAX, Launch Events Recaps of major game releases, Community Meetups Highlights from fan-organized events" ]
    topic = random.choice(topics)
    logger.info(f"Selected random topic: {topic}")
    return topic

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



def gpt_generate_v_post(post_topic):
    logger.info(f"Generating a post based on the following topic using ChatGPT API: {post_topic}...")
    response = ai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful writing assistant."},
            {
                "role": "user",
                "content": (
                    f"Create an engaging post on {post_topic} with a title and content. "
                    f"The title should be catchy, between 8-12 words, and suitable for a blog post. "
                    f"The content should have a professional yet conversational tone to keep readers engaged. "
                    f"The content should be structured, using subheadings, bullet points, and short paragraphs for readability. "
                    f"The content should have citations links to credible sources when referencing data and news. "
                    f"The content should be under 500 words and include relevant hashtags and SEO keywords."
                    f"don't include the word Title in the title."
                ),
            },
        ],
    )
    full_content = response.choices[0].message.content.strip()
    lines = full_content.splitlines()
    
    # Extract the title and ensure it does not contain "Title:" prefix
    title = lines[0].strip() if lines else f"{post_topic.capitalize()} Insights"

     # Ensure the title is clean and formatted properly
    title = title.lstrip("*").strip()  # Remove any asterisks and leading/trailing spaces
            
    # Extract content after the title
    content = "\n".join(lines[1:]) if len(lines) > 1 else full_content

    logger.info(f"Generated Post - Title: {title}")
    logger.info(f"Content: {content}")
    return title, content

def create_wordpress_post(title, content, category_ids, tag_ids):
    """ Create a WordPress post with tags, categories, and optionally an image """
    post_data = {
        "title": title,
        "content": content,
        "status": "draft",
        "categories": category_ids,
        "tags": tag_ids
    }

    # Add featured image if available

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

    topic = generate_post_topic()
    topic_category_id = get_category_id(topic)
    just_release_category_id = get_category_id("just-release")

    # Adding tags to match the previous post
    tag_ids = get_tag_ids(["art", "blog", "just-release", "post", "creativity", "engagement"])

    if topic_category_id and just_release_category_id:
        post_title, post_content = gpt_generate_v_post(topic)

        # Try to get an existing image
        existing_image_url = None

        if existing_image_url:
            # If the image is found, use it
            post_content = f"<img src='{existing_image_url}' alt='{topic}' />\n\n" + post_content
        elif enable_image_generation:
            # If no existing image is found, generate a new one
            # image_path = generate_image(topic)  # Generate image based on the topic
            # image_url, image_id = upload_image_to_wordpress(image_path)

            # if image_url:
            #     post_content = f"<img src='{image_url}' alt='{topic}' />\n\n" + post_content

            create_wordpress_post(post_title, post_content, [topic_category_id, just_release_category_id], tag_ids)

# Adding a loop to run continuously
if __name__ == "__main__":
    while True:
        main()  # Run the main function to generate and post content
        # Generate a random sleep time between 12 and 24 hours
        sleep_time = random.uniform(1 * 3600, 2 * 3600)  # Convert hours to seconds
        logger.info(f"Sleeping for {sleep_time / 3600:.2f} hours until the next post...")
        time.sleep(sleep_time)
