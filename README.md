# 🏥 Medico AI - Intelligent Medical Assistant Platform

<p align="center">
  <img src="https://img.shields.io/badge/Llama-4-blue?style=for-the-badge&logo=meta" alt="Llama 4">
  <img src="https://img.shields.io/badge/Groq-Whisper-green?style=for-the-badge&logo=openai" alt="Whisper">
  <img src="https://img.shields.io/badge/ElevenLabs-TTS-orange?style=for-the-badge" alt="ElevenLabs">
  <img src="https://img.shields.io/badge/Gradio-Purple?style=for-the-badge&logo=gradio" alt="Gradio">
</p>

---

## 📋 Project Overview

**Medico AI** is an intelligent medical assistant platform that leverages cutting-edge AI technologies to provide comprehensive healthcare support. The application offers three core capabilities:

1. **🔬 Image Diagnosis** - AI-powered medical image analysis using Groq's Llama 4 model
2. **🎤 Voice Assistant** - Voice-to-text input with automatic AI response and text-to-speech output
3. **💬 Medical Chat** - Conversational AI for medical consultations and health inquiries

This platform is designed for healthcare professionals, patients, and medical researchers seeking quick, reliable AI-assisted medical information.

---

## 🛠 Tech Stack & Tools

### Core Technologies
| Category | Technology | Purpose |
|----------|------------|---------|
| **LLM Model** | Meta Llama 4 Scout 17B | Medical image analysis & chat responses |
| **Speech-to-Text** | Groq Whisper Large V3 | Voice transcription |
| **Text-to-Speech** | ElevenLabs Turbo V2 | AI voice output |
| **TTS Backup** | Google gTTS | Fallback voice synthesis |
| **UI Framework** | Gradio 4.x | Web interface |
| **Audio Processing** | sounddevice, scipy, pydub | Voice recording |
| **Image Handling** | Pillow, base64 | Medical image processing |

### API Services
- **Groq API** - LLM inference and Whisper transcription
- **ElevenLabs API** - Premium text-to-speech
- **Google TTS** - Free fallback text-to-speech

### Environment
- Python 3.x
- Pipenv (package management)

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        MEDICO AI PLATFORM                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐ │
│  │  🔬 Image Tab    │  │  🎤 Voice Tab    │  │  💬 Chat Tab │ │
│  │                  │  │                  │  │              │ │
│  │  • Upload Image  │  │  • Record Voice  │  │  • Text Chat │ │
│  │  • AI Analysis  │  │  • Transcription │  │  • AI Reply  │ │
│  │  • Get Diagnosis│  │  • AI Response   │  │              │ │
│  └────────┬─────────┘  └────────┬─────────┘  └──────┬───────┘ │
│           │                     │                    │         │
│           ▼                     ▼                    ▼         │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                    CORE MODULES                             ││
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   ││
│  │  │   brain.py  │  │ voice_input  │  │  voice_output   │   ││
│  │  │ (Image AI)  │  │   (STT)      │  │     (TTS)       │   ││
│  │  └─────────────┘  └──────────────┘  └──────────────────┘   ││
│  └────────────────────────────────────────────────────────────┘│
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                    API LAYER                                ││
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐   ││
│  │  │ Groq Llama  │  │ Whisper STT  │  │  ElevenLabs TTS  │   ││
│  │  │    4        │  │   Large V3   │  │   Turbo V2       │   ││
│  │  └─────────────┘  └──────────────┘  └──────────────────┘   ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## ✨ Core Features

### 1. 🔬 Medical Image Diagnosis
- **Upload medical images** (X-rays, skin conditions, scans)
- **AI-powered analysis** using Llama 4 Scout model
- **Detailed diagnosis** including:
  - Findings
  - Possible conditions
  - Severity assessment
  - Recommended next steps

### 2. 🎤 Voice Assistant
- **One-click voice recording** (5-second clips)
- **Real-time transcription** using Groq Whisper
- **AI response generation** for health queries
- **Text-to-speech output** using ElevenLabs or gTTS

### 3. 💬 Medical Chat
- **Conversational AI** powered by Llama 4
- **Context-aware responses** with conversation history
- **Medical knowledge** across symptoms, conditions, medications
- **Professional disclaimer** for safe usage

### 4. 🎨 Premium UI Features
- **Dark medical theme** with cyan/teal accents
- **Animated header** with pulsing logo
- **Stats dashboard** showing accuracy & response times
- **Responsive design** for all screen sizes
- **Glassmorphism cards** with hover effects

---

## 🚀 Getting Started

### Prerequisites
```bash
# Install Python 3.x
# Get API keys:
# - GROQ_API_KEY from https://console.groq.com
# - ELEVENLABS_API_KEY from https://elevenlabs.io
```

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/medico-ai.git
cd medico-ai

# Install dependencies
pip install pipenv
pipenv install

# Set environment variables
# Create .env file:
# GROQ_API_KEY=your_groq_key
# ELEVENLABS_API_KEY=your_elevenlabs_key
```

### Run the Application

```bash
# Launch the app
python app.py

# Access in browser
# Local: http://127.0.0.1:7860
# Public: Check terminal for share link
```

---

## 📁 Project Structure

```
medico-ai/
├── app.py              # Main Gradio application
├── brain.py            # Image analysis module
├── voice_input.py      # Voice recording & STT
├── voice_output.py     # Text-to-speech module
├── Pipfile             # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # Project documentation
```

---

## ⚠️ Disclaimer

> **Important:** This AI assistant provides general medical information only. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a licensed healthcare professional for any medical concerns.

---

## 📄 License

MIT License - See LICENSE file for details.

---

## 👨‍💻 Credits

**Medico AI** © 2025-2026

Built with:
- [Groq](https://groq.com) - AI inference
- [Meta Llama](https://llama.meta.com) - LLM model
- [ElevenLabs](https://elevenlabs.io) - Voice synthesis
- [Gradio](https://gradio.app) - UI framework

---

<p align="center">
  <sub>Built with ❤️ for Healthcare</sub>
</p>