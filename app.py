import os
import gradio as gr
import requests
import tempfile

API_URL = "http://localhost:8000"

def analyze_image(image):
    if image is None:
        return "Please upload a medical image."
    try:
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        image.save(tmp.name)
        tmp.close()
        
        with open(tmp.name, "rb") as f:
            files = {"file": f}
            resp = requests.post(f"{API_URL}/analyze-image", files=files, timeout=90)
        
        try:
            os.unlink(tmp.name)
        except:
            pass
        
        if resp.status_code == 200:
            return resp.json().get("result", "No result")
        return f"Error: {resp.text}"
    except Exception as e:
        return f"Error: {str(e)}"

def transcribe_file(audio_data):
    if audio_data is None:
        return "Upload an audio file first"
    filepath = audio_data[0] if isinstance(audio_data, tuple) else audio_data
    if not filepath:
        return "No file path"
    try:
        with open(filepath, "rb") as f:
            resp = requests.post(f"{API_URL}/transcribe", files={"file": f}, timeout=45)
        if resp.status_code == 200:
            return resp.json().get("text", "No speech detected")
        return f"Error: {resp.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def chat(msg):
    if not msg.strip():
        return "", ""
    try:
        resp = requests.post(f"{API_URL}/chat", json={"message": msg, "history": []}, timeout=30)
        if resp.status_code == 200:
            return "", resp.json().get("response", "No response")
        return "", f"Error: {resp.status_code}"
    except Exception as e:
        return "", f"Error: {str(e)}"

def speak(text):
    if not text:
        return None
    try:
        resp = requests.post(f"{API_URL}/speak", data={"text": text}, timeout=30)
        if resp.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp.write(resp.content)
            tmp.close()
            return tmp.name
        return None
    except:
        return None

demo = gr.Blocks(title="Medico AI")

with demo:
    gr.Markdown("# 🏥 Medico AI 2.0")
    gr.Markdown("*Upload audio files for voice input*")
    
    with gr.Tabs():
        with gr.Tab("🔬 Image"):
            img = gr.Image(type="pil")
            gr.Button("Analyze", variant="primary").click(fn=analyze_image, inputs=img, outputs=gr.Textbox(lines=8))
                
        with gr.Tab("🎤 Voice"):
            gr.Markdown("**Upload Audio File (mp3, wav, m4a)**")
            audio = gr.Audio(sources=["upload"], type="filepath")
            gr.Button("Transcribe", variant="primary").click(fn=transcribe_file, inputs=audio, outputs=gr.Textbox(lines=4, label="Transcribed Text"))
            
            gr.Markdown("---")
            res = gr.Textbox(label="AI Response", lines=3)
            gr.Button("Play Voice").click(fn=speak, inputs=res, outputs=gr.Audio(label="Audio"))
                
        with gr.Tab("💬 Chat"):
            c = gr.Chatbot()
            m = gr.Textbox(placeholder="Ask a medical question...")
            gr.Button("Send").click(fn=chat, inputs=m, outputs=[m, c])
            m.submit(fn=chat, inputs=m, outputs=[m, c])

if __name__ == "__main__":
    demo.launch(share=True, server_port=7860)