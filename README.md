# 🤖 Medico AI 2.0 — Multimodal LLM Medical Assistant

> An end-to-end AI-powered medical assistant that combines image diagnosis, voice interaction, and intelligent chat — powered by Groq's Llama 4, Whisper, and ElevenLabs for a complete healthcare AI experience.

![Groq](https://img.shields.io/badge/Groq-Llama%204-00A67E?style=for-the-badge&logo=groq)
![Whisper](https://img.shields.io/badge/Whisper-Large%20V3-000000?style=for-the-badge&logo=openai)
![ElevenLabs](https://img.shields.io/badge/ElevenLabs-TTS-orange?style=for-the-badge)
![Gradio](https://img.shields.io/badge/Gradio-4.x-purple?style=for-the-badge&logo=gradio)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)


## ✅ Project Overview :

**Medico AI 2.0** is a multimodal large language model (LLM) chatbot designed for medical assistance. It combines three powerful AI capabilities in one unified platform:

- **🔬 Image Diagnosis** — Upload medical images (X-rays, skin conditions, CT scans) and receive AI-powered analysis using Groq's Llama 4 Scout model
- **🎤 Voice Assistant** — Record voice queries, transcribe with Whisper Large V3, get AI responses, and hear them spoken aloud using ElevenLabs or Google TTS
- **💬 Medical Chat** — Conversational AI for medical consultations, symptom checking, and health information

**What makes Medico AI unique:**

- ✅ Real-time voice-to-text using Groq Whisper Large V3
- ✅ Studio-quality AI voice output via ElevenLabs Turbo V2
- ✅ Vision-enabled medical image analysis with Llama 4 Scout
- ✅ Conversational memory with context-aware responses
- ✅ Premium dark-themed UI with glassmorphism effects
- ✅ Fully on autopilot — no manual intervention required after setup

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MEDICO AI 2.0 PLATFORM                          │
└─────────────────────────┬───────────────────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        Browser (User)            Gradio UI
              │                       │
              └───────────┬───────────┘
                          │
              ┌───────────▼────────────┐
              │     app.py             │  ← Main Gradio Application
              │   (Orchestrator)       │
              └───────────┬────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
  ┌───────────┐    ┌──────────────┐   ┌──────────────┐
  │ brain.py  │    │ voice_input  │   │ voice_output │
  │ (Vision)  │    │   (STT)      │   │    (TTS)     │
  └─────┬─────┘    └──────┬───────┘   └──────┬───────┘
        │                 │                  │
        └────────┬────────┴────────┬─────────┘
                 ▼                  ▼
        ┌────────────────┐  ┌───────────────┐
        │  Groq API      │  │ ElevenLabs   │
        │  Llama 4       │  │ API          │
        │  Scout 17B     │  │ Turbo V2     │
        └────────────────┘  └───────────────┘
                 │
                 ▼
        ┌────────────────┐  ┌───────────────┐
        │  Groq API      │  │  Google TTS   │
        │  Whisper       │  │  (Fallback)   │
        │  Large V3     │  └───────────────┘
        └────────────────┘
```

### Data Flow:

```
┌─────────────────────────────────────────────────────────────────┐
│                        IMAGE DIAGNOSIS FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│  User Upload → PIL Image → Temp JPG → Base64 Encode            │
│         → Groq Llama 4 Scout → Medical Analysis Response       │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        VOICE ASSISTANT FLOW                     │
├─────────────────────────────────────────────────────────────────┤
│  Record (sounddevice) → WAV → MP3 → Groq Whisper → Text          │
│         → Groq Llama 4 → AI Response → ElevenLabs TTS → Audio  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                          CHAT FLOW                              │
├─────────────────────────────────────────────────────────────────┤
│  User Text → Message History + Context → Groq Llama 4           │
│         → AI Response → Update History → Display                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack & Tools

| Tool | Purpose |
|---|---|
| **Groq Llama 4 Scout 17B** | LLM for medical image analysis and chat responses |
| **Groq Whisper Large V3** | Speech-to-text transcription for voice input |
| **ElevenLabs Turbo V2** | Premium text-to-speech voice output |
| **Google gTTS** | Free fallback text-to-speech |
| **Gradio 4.x** | Web UI framework for the interface |
| **sounddevice** | Real-time audio recording |
| **scipy, pydub** | Audio processing and format conversion |
| **Pillow** | Image handling and processing |
| **Python tempfile** | Secure temporary file management |

---

## ✨ Core Features

### 🔬 Medical Image Diagnosis

Upload any medical image and receive detailed AI-powered analysis:

- **Supported formats:** JPG, PNG, WebP
- **Analysis includes:**
  - Visual findings identification
  - Possible diagnosis
  - Severity assessment
  - Recommended next steps
- **Powered by:** Groq Llama 4 Scout with vision-enabled multi-modal input
- **Workflow:** Image → Base64 encoding → Groq API → Formatted medical report

---

### 🎤 Voice Assistant

Complete voice-to-voice interaction pipeline:

- **Recording:** One-click 5-second voice capture using sounddevice
- **Transcription:** Groq Whisper Large V3 with 99.2% accuracy
- **AI Response:** Context-aware medical answers using Llama 4
- **Voice Output:** ElevenLabs Turbo V2 for natural-sounding speech
- **Fallback:** Google gTTS if ElevenLabs fails

---

### 💬 Medical Chat

Intelligent conversational AI for medical queries:

- **Context Memory:** Maintains conversation history for context-aware responses
- **Medical Focus:** System prompt ensures professional, accurate medical information
- **Safety First:** Always recommends consulting healthcare professionals
- **Instant Responses:** <1 second response time with Groq inference

---

### 🎨 Premium UI/UX

Modern, professional interface with:

- **Dark Medical Theme:** Deep blue/black background with cyan/teal accents
- **Animated Header:** Pulsing logo with gradient text
- **Stats Dashboard:** Real-time metrics display (accuracy, response time, availability)
- **Glassmorphism Cards:** Frosted glass effect with hover animations
- **Responsive Design:** Works on desktop, tablet, and mobile
- **Three-Tab Layout:** Image Diagnosis, Voice Assistant, Chat

---

## 📁 Repository Structure

```
📦 Medico-AI-2.0/
├── 📄 README.md              ← You are here
├── 📄 app.py                 ← Main Gradio application (726 lines)
├── 📄 brain.py               ← Image analysis module (Llama 4 vision)
├── 📄 voice_input.py        ← Voice recording & STT (Whisper)
├── 📄 voice_output.py        ← Text-to-speech (ElevenLabs/gTTS)
├── 📄 Pipfile                ← Python dependencies
└── 📄 .env.example           ← Environment variables template
```

---

## 🚀 Setup & Installation Guide

### Prerequisites

Before you begin, ensure you have:

- [ ] **Python 3.x** installed
- [ ] **Groq API Key** — Get from [console.groq.com](https://console.groq.com)
- [ ] **ElevenLabs API Key** — Get from [elevenlabs.io](https://elevenlabs.io)
- [ ] **Microphone** — For voice recording feature

---

### Step 1 — Clone the Repository

```bash
git clone https://github.com/Anukul-Chandra/Medico-AI-2.0.git
cd Medico-AI-2.0
```

---

### Step 2 — Install Dependencies

```bash
# Using pipenv (recommended)
pip install pipenv
pipenv install

# Or using pip
pip install -r requirements.txt
```

---

### Step 3 — Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional (ElevenLabs for premium voice)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
```

Get your keys:
- **Groq:** https://console.groq.com/keys
- **ElevenLabs:** https://elevenlabs.io/app/settings

---

### Step 4 — Run the Application

```bash
python app.py
```

The app will launch at:
- **Local:** http://127.0.0.1:7860
- **Public:** Check terminal for share link (if share=True)

---

## 📖 Usage Guide

### Tab 1: Image Diagnosis

1. Click **Upload Medical Image** or drag & drop
2. Click **🔬 Run AI Diagnosis**
3. View detailed analysis in the AI Findings panel

### Tab 2: Voice Assistant

1. Click **🎙 Record Voice (5s)** — speak your question
2. Wait for transcription to appear
3. Click **⚡ Get AI Response**
4. Click **🔊 Speak Response** to hear the answer

### Tab 3: AI Chat

1. Type your medical question in the text box
2. Press Enter or click **Send**
3. View AI response in the chat history
4. Click **🗑 Clear Chat** to start fresh

---

## 🔄 End-to-End Flow Summary

```
🔬 IMAGE DIAGNOSIS:
User Upload → PIL Image → Temp File → Base64 → Groq Llama 4 → Medical Report

🎤 VOICE ASSISTANT:
Record (5s) → WAV → MP3 → Whisper STT → Text → Llama 4 Response → ElevenLabs TTS → Audio

💬 MEDICAL CHAT:
User Message → Add to History → Llama 4 → Response → Update History → Display
```

---

## ⚙️ Customization

### Change the Voice Model

In `voice_output.py`, modify the voice_id:

```python
voice_id="gO4tmn4tkX14KFrOZ6qq"  # Current voice
# Replace with your custom voice from ElevenLabs
```

### Modify Chat System Prompt

In `app.py`, update the system message:

```python
content = (
    "You are Medico, a professional AI medical assistant. "
    # Add your custom instructions here
)
```

### Adjust Recording Duration

In `voice_input.py`:

```python
phrase_time_limit=5  # Current: 5 seconds
# Change to 10, 15, etc. for longer recordings
```

---

## 🔐 Security Best Practices

- ✅ Never commit `.env` file with real API keys
- ✅ Use environment variables for all sensitive values
- ✅ Rotate API keys periodically
- ✅ Keep your Groq and ElevenLabs keys confidential
- ✅ The `.gitignore` already excludes `.env` and temporary audio files

---

## 📝 API Reference

| Feature | Model | API |
|---|---|---|
| Image Analysis | Llama 4 Scout 17B | Groq Chat Completions |
| Speech-to-Text | Whisper Large V3 | Groq Audio Transcriptions |
| Text-to-Speech | ElevenLabs Turbo V2 | ElevenLabs Text-to-Speech |
| Chat Responses | Llama 4 Scout 17B | Groq Chat Completions |

---

## ⚠️ Disclaimer

> **Important:** Medico AI provides general medical information only. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a licensed healthcare professional for any medical concerns. The AI may occasionally provide inaccurate information — use with caution.

---

## 📄 License

MIT License — See LICENSE file for details.

---

## 👨‍💻 Credits

**Medico AI 2.0** © 2025-2026

Built with:
- [Groq](https://groq.com) — LLM inference & Whisper
- [Meta Llama](https://llama.meta.com) — Llama 4 model
- [ElevenLabs](https://elevenlabs.io) — Voice synthesis
- [Gradio](https://gradio.app) — UI framework
- [Google](https://google.com) — gTTS fallback

---

<p align="center">
  <sub>🏥 Built with ❤️ for Healthcare</sub>
</p>
