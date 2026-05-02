"""
Medical Image Analysis Module
==============================

This module handles:
- Encoding images to base64 for API transmission
- Sending images to Groq's Llama 4 model for medical analysis

Uses: Groq API with Llama 4 Scout 17B model
"""

import os
import base64
from groq import Groq

# Load Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def encode_img(image_path):
    """
    Encode image file to base64 string.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string of the image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Default model for image analysis
model = "meta-llama/llama-4-scout-17b-16e-instruct"
query = "What is in the image and what is the possible diagnosis?"

def analyze_image_with_query(model, query, encoded_img):
    """
    Analyze medical image using Groq Llama 4 model.
    
    Args:
        model: Model name to use
        query: Prompt for analysis
        encoded_img: Base64 encoded image
        
    Returns:
        AI-generated diagnosis result
    """
    client = Groq(api_key=GROQ_API_KEY)

    message = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{encoded_img}",
                    },
                },
            ],
        }
    ]

    chat_completion = client.chat.completions.create(
        model=model,
        messages=message,
        max_tokens=2048,
    )

    return chat_completion.choices[0].message.content


# # ✅ RUN (commented - used by app.py)
# image_path = "C:/dev/Medico-AI-2.0/acne.jpg"

# encoded_img = encode_img(image_path)
# result = analyze_image_with_query(model, query, encoded_img)

# print("\n🧠 AI Diagnosis:\n", result)