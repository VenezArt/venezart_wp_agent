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
    "Artificial Intelligence (AI)": "A futuristic Marvel style scene showcasing artificial intelligence with a glowing brain made of circuits and code, symbolizing AI thought processes, and robots collaborating with humans in a sleek, modern workspace.",
    "Machine Learning (ML)": "A visual of interconnected nodes and data points forming a neural network, with layers of algorithms learning from data, depicted by flowing lines and data clusters.",
    "Cybersecurity": "A close-up view of a digital lock and shield on a computer screen, with binary code and complex encryptions swirling around, representing strong digital protection.",
    "Cloud Computing": "A vibrant digital cloud hovering over a landscape of servers and devices, symbolizing data flow from the cloud to various endpoints with futuristic data lines.",
    "Blockchain & Cryptocurrency": "A chain of digital blocks in a high-tech matrix, each block showcasing coins and cryptocurrency symbols like Bitcoin, Ethereum, with glowing connectivity lines.",
    "DevOps & CI/CD": "A pipeline of gears and code showing continuous integration and delivery, with developers and operators collaboratively working on seamless workflows and automated processes.",
    "Artificial Neural Networks (ANN) & Deep Learning": "A complex neural network structure with multiple layers, glowing nodes interconnected by links, symbolizing deep learning processes in vibrant colors.",
    "Data Science & Data Analytics": "A dashboard with charts, graphs, and statistics, alongside scientists analyzing patterns in data streams, representing insights being drawn from big data.",
    "Python (Programming Language)": "A coding environment with Python code snippets, Python logo prominently displayed, and images of friendly snakes intertwined with laptops and scripts.",
    "Tech Trends (2024)": "A futuristic cityscape with holograms of upcoming tech trends, AI-powered devices, wearable tech, and digital interfaces representing 2024’s technology advancements.",
    "Robots & Automation": "A sleek industrial robot arm assembling devices, alongside robots assisting humans in various tasks, representing advanced automation in industries.",
    "Natural Language Processing (NLP)": "A visual of a person speaking, with sound waves transforming into text and code, symbolizing machines understanding human language in real-time.",
    "Hello AI": "A friendly, futuristic AI character waving, with a speech bubble saying 'Hello,' surrounded by small, colorful symbols of AI concepts like brains, data, and circuits.",
    "VenezArt": "An abstract digital painting that incorporates Venezuelan cultural symbols, natural landscapes, and vibrant colors in a modern art style, symbolizing VenezArt’s artistic inspiration.",
    "Cutting-Edge Gadgets": "A display of futuristic gadgets like smart glasses, holographic phones, and wearable tech, with a background of digital tech elements to show innovation.",
    "joke of the day": "A fun cartoon character holding a joke book with a lightbulb above their head, surrounded by laughing emojis and a speech bubble with a funny joke.",
    "Azure DevOps": "A cloud-based development environment with the Azure DevOps logo, featuring project management boards, pipelines, and team collaboration scenes in a cloud setting.",
    "Kubernetes": "A complex structure of containers organized like a digital shipyard, with the Kubernetes logo and nodes managing deployment, symbolizing scalable orchestration.",
    "Docker": "A friendly whale carrying containers on its back in a digital sea, with each container representing an application or service, emphasizing containerization.",
    "Bitbucket": "A development workspace with Bitbucket’s logo, featuring developers collaborating on code repositories, version control, and seamless coding processes.",
    "Jenkins": "An automation pipeline with Jenkins logo, showing various stages of code deployment, testing, and integration represented by gears and coding icons.",
    "Ansible": "A network of servers connected by Ansible playbooks, representing automated configuration management with lines of code efficiently deployed to each server.",
    "Terraform": "A cloud infrastructure landscape with Terraform’s logo, visualizing infrastructure as code as blocks being built and rearranged in a modular fashion.",
    "HelmCharts": "A digital helm steering a ship of charts and graphs, symbolizing application deployment in Kubernetes, with Helm logo and charts as modular templates.",
    "MongoDB": "A lush digital tree with MongoDB leaves, representing the document database structure, with branches connecting various nodes as data storage.",
    "PostgreSQL": "An elephant symbolizing PostgreSQL surrounded by data tables and relational links, showing the robust SQL database in action with rows and columns.",
    "MySQL": "A dolphin icon surrounded by database tables, rows, and SQL commands, representing MySQL’s reliable database management system.",
    "Redis": "A red stack of data blocks symbolizing Redis’s data caching, with lightning bolts indicating fast data retrieval, alongside an icon of Redis’s logo.",
    "Elasticsearch": "A magnifying glass searching through data clusters, representing Elasticsearch’s indexing and search capabilities across massive datasets.",
    "Prometheus": "A digital screen with Prometheus metrics and graphs, visualizing data monitoring and alerting systems for various applications and services.",
    "Grafana": "A modern dashboard with various interactive data charts and metrics, symbolizing Grafana’s powerful visualization capabilities for tracking system health.",
    "Zabbix": "A network of servers and systems being monitored by a central screen, symbolizing Zabbix’s comprehensive monitoring and alerting tools.",
    "Splunk": "A powerful data analytics dashboard with logs and machine data being transformed into actionable insights, symbolizing Splunk’s capabilities.",
    "Logstash": "A pipeline where raw data is cleaned and organized into structured logs, visualizing Logstash’s role in the ELK stack for data processing.",
    "Kafka": "A high-speed stream of data between producers and consumers, symbolizing Kafka’s message-broker system with data flow connecting applications.",
    "RabbitMQ": "A digital message queue with icons of messages being efficiently delivered, symbolizing RabbitMQ’s message-queuing system with consumer-producer interactions.",
    "ActiveMQ": "A message exchange network where ActiveMQ processes messages between various applications, showcasing efficient queue management.",
    "Bash Scripting": "A command line with Bash code, symbolizing scripting in a Linux environment, with commands controlling different system operations.",
    "Shell Scripting": "A shell command-line environment with shell script code for automation and system management, showing multiple scripts in action.",
    "PowerShell": "A Windows console with PowerShell commands, showcasing automation and system tasks with clear syntax and blue console theme.",
    "Python Scripting": "Python code for a task automation script, with clear syntax highlighting, focusing on Python’s versatility in scripting environments.",
    "Go Programming": "A playful scene with the Go gopher mascot coding, surrounded by symbols representing the efficiency and simplicity of Go programming.",
    "Java Programming": "A computer screen with Java code and coffee cups, symbolizing Java programming, with typical syntax and structure of Java applications.",
    "JavaScript Programming": "A 64 bit game screen with JavaScript code, showcasing interactive web development and game programming with JavaScript.",
    "R Programming": "A data analysis environment with R code and statistical graphs, visualizing data science work with the R language in an academic setting.",
    "FastAPI": "A sleek web app interface with FastAPI’s logo and code snippets, representing the lightweight and fast capabilities of FastAPI framework.",
    "Flask": "A small web server icon with Flask logo and Python code, showcasing the simplicity and flexibility of Flask for web application development.",
    "Django": "A full-featured web app dashboard with Django’s logo, code snippets, and database connectivity, showcasing Django’s versatility in web development.",
    "Spring Boot": "A Java-based server with Spring Boot logo, surrounded by APIs and microservices, representing quick and reliable app development.",
    "Restful APIs": "A network of connected APIs with endpoints and HTTP methods, symbolizing a well-structured RESTful API interface with JSON responses."

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
