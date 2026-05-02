import gradio as gr
import os
import base64
import tempfile
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

from backend.brain import encode_img, analyze_image_with_query
from backend.voice_input import record_audio, transcribe_with_groq
from backend.voice_output import text_to_speech_withgTTS, text_to_speech_with_elevenlabs

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def analyze_image(image):
    if image is None:
        return "Please upload an image first."
    try:
        result = analyze_image_with_query(
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "You are a medical expert. Analyze this image and give detailed diagnosis.",
            encode_img(image)
        )
        return result
    except Exception as e:
        return f"Error: {str(e)}"

def chat(message, history):
    if not message.strip():
        return history + ["", "Please enter a message."]
    try:
        client = Groq(api_key=GROQ_API_KEY)
        messages = [
            {"role": "system", "content": "You are Medico, a professional medical AI assistant. Provide accurate medical information."}
        ]
        for h in history:
            messages.append({"role": "user", "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": message})
        
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=messages,
            max_tokens=1024
        )
        return history + [(message, response.choices[0].message.content)]
    except Exception as e:
        return history + [(message, f"Error: {str(e)}")]

def speak(text):
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tmp.close()
        try:
            text_to_speech_with_elevenlabs(text, tmp.name)
        except:
            text_to_speech_withgTTS(text, tmp.name)
        return tmp.name
    except Exception as e:
        return None

with gr.Blocks(title="Medico AI 2.0") as demo:
    gr.Markdown("# 🏥 Medico AI 2.0 - Medical Assistant")
    gr.Markdown("Upload an image for diagnosis or chat with the AI assistant.")
    
    with gr.Tab("📷 Image Diagnosis"):
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(type="filepath", label="Upload Medical Image")
                analyze_btn = gr.Button("Analyze Image", variant="primary")
            with gr.Column():
                image_output = gr.Textbox(label="Diagnosis Result", lines=10)
        
        analyze_btn.click(analyze_image, inputs=[image_input], outputs=[image_output])
    
    with gr.Tab("💬 Medical Chat"):
        chatbot = gr.Chatbot(label="Conversation History")
        msg = gr.Textbox(label="Your Message", placeholder="Ask about symptoms, medications, etc.")
        with gr.Row():
            send_btn = gr.Button("Send", variant="primary")
            clear_btn = gr.Button("Clear")
        
        def respond(message, history):
            return "", chat(message, history)
        
        send_btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
        msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
        clear_btn.click(lambda: (None, []), outputs=[msg, chatbot])
    
    with gr.Tab("🔊 Text to Speech"):
        tts_input = gr.Textbox(label="Text to Speak", lines=3)
        tts_btn = gr.Button("Speak", variant="primary")
        tts_output = gr.Audio(label="Audio Output")
        
        def text_to_speech(text):
            path = speak(text)
            return path if path else "Error generating audio"
        
        tts_btn.click(text_to_speech, inputs=[tts_input], outputs=[tts_output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)