#Phase1 : set up brain 


import os
import base64
from groq import Groq

# Step 1: API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 2: Encode image
image_path = "C:/dev/Medico-AI-2.0/acne.jpg"

with open(image_path, "rb") as image_file:
    encoded_img = base64.b64encode(image_file.read()).decode("utf-8")

# Step 3: Groq client
client = Groq(api_key=GROQ_API_KEY)

model = "meta-llama/llama-4-scout-17b-16e-instruct"
query = "What is in the image and what is the possible diagnosis?"

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

print(chat_completion.choices[0].message.content)