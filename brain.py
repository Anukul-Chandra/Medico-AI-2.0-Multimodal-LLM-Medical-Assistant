#Step 1: Setup GROQ API key
#Step2 : Convert image to required format
#Step3 : Setup Multimodal LLM



import os
import requests

# Step 1: Setup GROQ API key
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# Step 2: Convert image to required format

import base64

image_path = "C:\dev\Medico-AI-2.0\acne.jpg"
image_file =open(image_path, "rb")
encoded_img = base64.b64encode(open(image_file.read()),decode['utf-8'])


