import torch
import os
from diffusers import StableDiffusionPipeline
from PIL import Image

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
        "entrepreneurship": (
            "A hyper-realistic 3D render of a skyscraper rooftop at dusk, overlooking a cityscape with glowing lights. "
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
    
    prompt = prompts.get(topic.lower(), (
        "An imaginative and thought-provoking image capturing the essence of the topic with attention to details and aesthetics. "
        "Vivid colors and a combination of realistic and surreal elements to convey depth and inspiration."
    ))
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
    image_filename = f"ai_gen_image_{topic}.jpg" if image_format.upper() == "JPEG" else f"ai_gen_image_{topic}.{image_format.lower()}"
    image_path = os.path.join(save_path, image_filename)
    
    try:
        image = image.convert("RGB")  # Convert to RGB for JPEG compatibility
        image.save(image_path, format=image_format.upper())
        print(f"Image saved to {image_path} as {image_format.upper()}.")
    except Exception as e:
        print(f"Error saving image: {e}")
        return None

    return image_path  # Return the path for further use

