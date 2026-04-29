import os
import base64
from groq import Groq

# Step 1: API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 2: Encode image
def encode_img(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


# Step 3: Groq client
model = "meta-llama/llama-4-scout-17b-16e-instruct"
query = "What is in the image and what is the possible diagnosis?"

def analyze_image_with_query(model, query, encoded_img):
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


# ✅ RUN
image_path = "C:/dev/Medico-AI-2.0/acne.jpg"

encoded_img = encode_img(image_path)
result = analyze_image_with_query(model, query, encoded_img)

print("\n🧠 AI Diagnosis:\n", result)