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


def generate_image(topic, save_path="images", image_format="JPEG"):
    print(f"Generating image for topic: {topic}")
    model_id = "stabilityai/stable-diffusion-2-1"
    
    # Check CUDA availability
    if not torch.cuda.is_available():
        print("CUDA not available. Please run on a system with CUDA support.")
        return None
    
    # Load model
    try:
        print(f"Loading model: {model_id}")
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
        pipe = pipe.to("cuda")
        print(f"Using CUDA device: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    # Updated prompts for each topic
    prompts = {

        "startup culture": (
            "Modern tech office with casual, creative work environment, diverse team brainstorming with whiteboards and sticky notes, laptops open, startup vibe. "
            "Bright, open space with plants, natural light, and colorful decor. Relaxed, collaborative atmosphere that fosters innovation and teamwork."
        ),

        "bootstrapping vs. venture funding": (
            "A conceptual illustration comparing bootstrapping and venture funding in a business context. "
            "Bootstrapping side shows a person lifting themselves up by their bootstraps, symbolizing self-reliance and limited resources. "
            "Venture funding side features a rocket ship launching into space, representing rapid growth and external investment. "
            "Contrast between organic growth and accelerated scaling."
        ),

        "growth hacking techniques": (
            "A dynamic and visually engaging infographic showcasing various growth hacking techniques. "
            "Includes elements like viral loops, A/B testing, influencer marketing, and SEO optimization. "
            "Colorful charts, graphs, and icons illustrate the strategies and tactics used to drive rapid business growth."
        ),

        "business planning and strategy": (
            "A strategic planning session in a boardroom with executives discussing business goals, market analysis, and growth strategies. "
            "Whiteboard filled with diagrams, charts, and post-it notes. Team collaboration, decision-making, and brainstorming in a professional setting."
        ),

        "risk management in startups": (
            "A conceptual image illustrating risk management in startups. A tightrope walker balancing on a high wire, representing the delicate balance "
            "between risk and reward. Safety net below symbolizes risk mitigation strategies, contingency plans, and resilience in the face of uncertainty."
        ),

        "entrepreneurial mindset and mental health": (
            "A visual representation of the entrepreneurial mindset and mental health. "
            "A person juggling multiple tasks, wearing different hats, and balancing work-life demands. "
            "Emphasis on self-care, stress management, and maintaining a healthy work-life balance for sustainable success."
        ),

        "effective networking strategies": (
            "A networking event with professionals mingling, exchanging business cards, and engaging in conversations. "
            "Diverse group of people from various industries, backgrounds, and expertise. Networking strategies, relationship building, and community engagement."
        ),

        "product-market fit": (
            "A Venn diagram illustrating the concept of product-market fit. Overlapping circles representing the alignment between a product's features "
            "and the needs of the target market. Intersection point symbolizes the optimal match that drives customer satisfaction and business success."
        ),

        "leadership in startups": (
            "A visionary leader guiding a team of diverse professionals in a startup environment. "
            "Inspirational figure with a clear vision, strategic direction, and effective communication. "
            "Empowering leadership style that fosters innovation, collaboration, and growth."
        ),

        "building effective teams": (
            "A team-building exercise with employees collaborating, problem-solving, and building trust. "
            "Group activities, team challenges, and workshops that promote communication, teamwork, and synergy. "
            "Creating a positive team culture and fostering strong relationships for high performance and success."
        ),

        "social entrepreneurship": (
            "A social entrepreneur working on a community project, making a positive impact on society. "
            "Engagement with diverse stakeholders, social innovation, and sustainable business practices. "
            "Balancing social mission with financial sustainability to create meaningful change and address social challenges."
        ),

        "overcoming challenges as a founder": (
            "A founder facing obstacles and overcoming challenges in the entrepreneurial journey. "
            "Navigating setbacks, failures, and uncertainties with resilience, determination, and adaptability. "
            "Growth mindset, problem-solving skills, and perseverance in the face of adversity."
        ),

        "digital art trends": (
            "A digital art gallery showcasing the latest trends in digital art. "
            "Interactive installations, AR/VR experiences, and digital sculptures. "
            "Innovative techniques, digital mediums, and creative expressions in the digital art world."
        ),

        "the impact of AI in art": (
            "An AI-powered art studio with generative art tools, machine learning"
            "algorithms, and AI-assisted creativity. "
            "Collaboration between artists and AI systems, exploring new forms of artistic expression and creativity. "
            "Blending human creativity with artificial intelligence to push the boundaries of art."
        ),

        "mixed media techniques": (
            "A mixed media artwork combining traditional and digital techniques. "
            "Collage of textures, colors, and materials, blending painting, photography, and digital elements. "
            "Experimental, layered composition that explores the intersection of different art forms and mediums."
        ),

        "history of abstract art": (
            "A visual timeline of abstract art movements from the early 20th century to contemporary styles. "
            "Key artists, artworks, and influences that shaped the evolution of abstract art. "
            "Exploration of abstraction, non-representation, and artistic experimentation in the history of art."
        ),

        "surrealism explained": (
            "A surrealistic landscape with dreamlike elements, unexpected juxtapositions, and symbolic imagery. "
            "Influences of surrealism, subconscious exploration, and artistic freedom. "
            "Interpretation of dreams, the unconscious mind, and the surrealistic movement in art."
        ),

        "exploring street art": (
            "A vibrant street art mural in an urban setting, showcasing graffiti, murals, and public art. "
            "Colorful, expressive artworks that engage with the local community and urban environment. "
            "Exploration of street art culture, social commentary, and artistic activism."
        ),

        "art therapy techniques": (
            "An art therapy session with a therapist and client engaging in creative expression. "
            "Art materials, therapeutic techniques, and emotional exploration through art-making. "
            "Healing, self-discovery, and personal growth through art therapy interventions."
        ),

        "NFT art market": (
            "A digital art marketplace for NFTs, showcasing blockchain-based art collections, digital assets, and crypto art. "
            "NFT minting, trading, and ownership of unique digital artworks. "
            "Emerging trends, opportunities, and challenges in the NFT art market."
        ),

        "traditional vs. digital art": (
            "A comparison between traditional and digital art mediums, techniques, and processes. "
            "Traditional art tools like paint, canvas, and brushes contrasted with digital tools like tablets, software, and styluses. "
            "Exploration of artistic expression, creativity, and innovation in traditional and digital art forms."
        ),

        "art movements of the 20th century": (
            "A visual overview of major art movements in the 20th century, from Cubism and Surrealism to Abstract Expressionism and Pop Art. "
            "Key artists, artworks, and characteristics of each movement. "
            "Influence of historical events, cultural shifts, and artistic experimentation on 20th-century art."
        ),

        "portrait drawing techniques": (
            "Generate an image to portrait drawing techniques, from sketching and proportions to shading and details. "
            "Portrait artist demonstrating drawing process, techniques, and tips for capturing likeness and expression. "
            "Exploration of portraiture, anatomy, and observational drawing skills."
        ),

        "sculpting and its significance": (
            "A sculptor working on a clay sculpture, exploring form, texture, and composition. "
            "Sculpting tools, techniques, and materials used in traditional and contemporary sculpture. "
            "Expression, creativity, and three-dimensional art forms in sculpting and its cultural significance."
        ),

        "blockchain beyond cryptocurrency": (
            "A conceptual illustration of blockchain technology beyond cryptocurrency, showcasing decentralized applications, smart contracts, and digital assets. "
            "Blockchain network, nodes, and transactions visualized in a digital ecosystem. "
            "Exploration of blockchain technology, security, transparency, and decentralized innovation."
        ),

        "AI and machine learning in everyday life": (
            "An AI-powered smart home with connected devices, IoT sensors, and machine learning algorithms. "
            "Automation, personalization, and predictive analytics in everyday life. "
            "Integration of AI technology, data-driven insights, and intelligent systems for convenience and efficiency."
        ),

        "virtual reality trends": (
            "A virtual reality experience with VR headsets, immersive environments, and interactive simulations. "
            "Virtual worlds, gaming, training, and entertainment applications of VR technology. "
            "Emerging trends, advancements, and future possibilities in the virtual reality industry."
        ),

        "the future of quantum computing": (
            "A futuristic quantum computing lab with qubits, quantum gates, and superposition. "
            "Quantum algorithms, quantum supremacy, and quantum computing applications. "
            "Exploration of quantum mechanics, quantum information, and the future of computing technology."
        ),

        "emerging programming languages": (
            "A coding environment with emerging programming languages like Rust, Kotlin, and TypeScript. "
            "Syntax, features, and applications of modern programming languages. "
            "Exploration of software development, coding practices, and programming language trends."
        ),

        "ethical concerns in AI development": (
            "An ethical AI framework with principles, guidelines, and considerations for responsible AI development. "
            "Fairness, transparency, accountability, and privacy in AI systems. "
            "Ethical challenges, biases, and implications of AI technology on society and individuals."
        ),

        "advances in renewable tech": (
            "A renewable energy farm with solar panels, wind turbines, and energy storage systems. "
            "Clean energy technologies, sustainability, and environmental impact of renewable energy sources. "
            "Innovations, advancements, and future prospects in renewable energy technology."
        ),

        "internet of things (IoT) innovations": (
            "An IoT ecosystem with interconnected devices, sensors, and data networks. "
            "Smart cities, wearables, and industrial IoT applications. "
            "Integration of IoT technology, data analytics, and connectivity for smart solutions and innovations."
        ),

        "cloud computing vs. edge computing": (
            "A comparison between cloud computing and edge computing architectures, services, and applications. "
            "Cloud data centers, edge devices, and network infrastructure visualized in a digital environment. "
            "Exploration of computing paradigms, latency, scalability, and distributed computing models."
        ),

        "the rise of 5G and its impacts": (
            "A 5G network infrastructure with high-speed connectivity, low latency, and IoT integration. "
            "5G technology, applications, and impacts on industries, communication, and digital transformation. "
            "Emerging trends, opportunities, and challenges in the 5G ecosystem."
        ),

        "cybersecurity threats and best practices": (
            "A cybersecurity landscape with hackers, malware, and security breaches. "
            "Cyber threats, vulnerabilities, and best practices for protecting data and systems. "
            "Cybersecurity awareness, risk mitigation, and defense strategies in the digital age."
        ),

        "tech for social good": (
            "A social impact project using technology for positive change and social good. "
            "Tech solutions, innovation, and digital tools for addressing social challenges and global issues. "
            "Empowerment, inclusivity, and sustainability through technology for social impact."
        ),

        "entrepreneurship": (
            "A realistic 3D render of a skyscraper rooftop at dusk, overlooking a cityscape with glowing lights. "
            "Deep blues, warm oranges, and metallic tones give the city a vibrant, dynamic look. Photorealistic style "
            "with cinematic lighting and depth, conveying ambition, innovation, and growth."
        ),
        "art": (
            "A surreal and colorful abstract painting with vibrant swirls, bold geometric shapes, and dynamic brushstrokes. "
            "The composition bursts with energy, blending warm and cool tones, and creates a mesmerizing scene that invites "
            "viewers to explore creativity and imagination. Artistic, expressive, and captivating."
        ),
        "tech": (
            "A futuristic high-tech lab interior filled with holographic screens, robotic arms, and cutting-edge machinery. "
            "Cool blue and neon lights illuminate the room, casting a sleek and modern ambiance. Digital schematics and "
            "AI interfaces are displayed, capturing the innovation and possibilities of advanced technology."
        ),
    }
    
    prompt = prompts.get(
        topic,
        f"An imaginative and thought-provoking image capturing the essence of {topic} with attention to details and aesthetics. Vivid colors and a combination of realistic and surreal elements to convey depth and inspiration.",

    )
    print(f"Using prompt: {prompt}")

    # Image generation settings
    num_inference_steps = 50
    guidance_scale = 7.5

    # Generate image
    try:
        with torch.cuda.amp.autocast(dtype=torch.float16):
            image = pipe(prompt, guidance_scale=guidance_scale, num_inference_steps=num_inference_steps).images[0]
        print("Image generated successfully.")
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

    # Save generated image
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"Created '{save_path}' directory.")

    # Define file path and save image
    image_filename = "ai_gen_image.jpg" if image_format.upper() == "JPEG" else "ai_gen_image.{image_format.lower()}"
    image_path = os.path.join(save_path, image_filename)
    
    try:
        image = image.convert("RGB")  # Convert to RGB for JPEG compatibility
        image.save(image_path, format=image_format.upper())
        print(f"Image saved to {image_path} as {image_format.upper()}.")
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

    return image_path  # Return the path for further use


if __name__ == "__main__":
    main()
