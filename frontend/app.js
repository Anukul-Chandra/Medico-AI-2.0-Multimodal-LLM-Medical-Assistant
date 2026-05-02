const API_URL = "http://localhost:8000";

// DOM Elements
const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');
const loadingOverlay = document.getElementById('loading-overlay');

// Tab Switching
tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const tabId = btn.dataset.tab;
        
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));
        
        btn.classList.add('active');
        document.getElementById(`${tabId}-tab`).classList.add('active');
    });
});

// ==================== IMAGE DIAGNOSIS ====================
const uploadZone = document.getElementById('upload-zone');
const imageInput = document.getElementById('image-input');
const imagePreview = document.getElementById('image-preview');
const previewImg = document.getElementById('preview-img');
const removeImageBtn = document.getElementById('remove-image');
const analyzeBtn = document.getElementById('analyze-btn');
const imageResult = document.getElementById('image-result');
const diagnosisText = document.getElementById('diagnosis-text');

let selectedImage = null;

function formatAIResponse(text) {
    let formatted = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/^### (.+)$/gm, '<h3>$1</h3>')
        .replace(/^## (.+)$/gm, '<h2>$1</h2>')
        .replace(/^# (.+)$/gm, '<h1>$1</h1>')
        .replace(/^\d+\. (.+)$/gm, '<li>$1</li>')
        .replace(/^- (.+)$/gm, '<li>$1</li>')
        .replace(/^\* (.+)$/gm, '<li>$1</li>')
        .replace(/^(Diagnosis|Possible Causes|Possible Treatment Options|Recommendations|Symptoms and Signs|Possible Diagnosis| Causes and Risk Factors|Treatment and Management|Prognosis):/gim, '<h3>$1</h3>');
    
    formatted = formatted.replace(/(<li>.*?<\/li>)+/gs, '<ul>$&</ul>');
    
    formatted = formatted.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>');
    formatted = '<p>' + formatted + '</p>';
    formatted = formatted.replace(/<p><\/p>/g, '').replace(/<p><br>/g, '<p>').replace(/<br><\/p>/g, '</p>');
    
    return formatted;
}

uploadZone.addEventListener('click', () => imageInput.click());
uploadZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--primary)';
});
uploadZone.addEventListener('dragleave', () => {
    uploadZone.style.borderColor = 'var(--border)';
});
uploadZone.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadZone.style.borderColor = 'var(--border)';
    if (e.dataTransfer.files.length) {
        handleImageUpload(e.dataTransfer.files[0]);
    }
});

imageInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        handleImageUpload(e.target.files[0]);
    }
});

function handleImageUpload(file) {
    if (!file.type.startsWith('image/')) {
        alert('Please upload an image file');
        return;
    }
    
    selectedImage = file;
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImg.src = e.target.result;
        uploadZone.style.display = 'none';
        imagePreview.style.display = 'block';
        analyzeBtn.disabled = false;
    };
    reader.readAsDataURL(file);
}

removeImageBtn.addEventListener('click', () => {
    selectedImage = null;
    imageInput.value = '';
    previewImg.src = '';
    imagePreview.style.display = 'none';
    uploadZone.style.display = 'block';
    analyzeBtn.disabled = true;
    imageResult.style.display = 'none';
});

analyzeBtn.addEventListener('click', async () => {
    if (!selectedImage) return;
    
    showLoading();
    
    const formData = new FormData();
    formData.append('file', selectedImage);
    
    try {
        const response = await fetch(`${API_URL}/analyze-image`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            diagnosisText.innerHTML = formatAIResponse(data.result || 'No result returned');
            imageResult.style.display = 'block';
        } else {
            diagnosisText.innerHTML = `Error: ${data.error || 'Unknown error'}`;
            imageResult.style.display = 'block';
        }
    } catch (error) {
        diagnosisText.innerHTML = `Error: ${error.message}`;
        imageResult.style.display = 'block';
    }
    
    hideLoading();
});

// ==================== VOICE TRANSCRIPTION ====================
const audioUploadZone = document.getElementById('audio-upload-zone');
const audioInput = document.getElementById('audio-input');
const transcribeBtn = document.getElementById('transcribe-btn');
const transcribeResult = document.getElementById('transcribe-result');
const transcriptionText = document.getElementById('transcription-text');

let selectedAudio = null;

audioUploadZone.addEventListener('click', () => audioInput.click());
audioInput.addEventListener('change', (e) => {
    if (e.target.files.length) {
        selectedAudio = e.target.files[0];
        audioUploadZone.innerHTML = `
            <i class="fa-solid fa-file-audio"></i>
            <p>${selectedAudio.name}</p>
            <span>Click to change</span>
        `;
        transcribeBtn.disabled = false;
    }
});

transcribeBtn.addEventListener('click', async () => {
    if (!selectedAudio) return;
    
    showLoading();
    
    const formData = new FormData();
    formData.append('file', selectedAudio);
    
    try {
        const response = await fetch(`${API_URL}/transcribe`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            transcriptionText.textContent = data.text || 'No speech detected';
            transcribeResult.style.display = 'block';
            document.getElementById('ai-response-section').style.display = 'block';
            document.getElementById('voice-ai-result').style.display = 'none';
        } else {
            transcriptionText.textContent = `Error: ${data.error || 'Unknown error'}`;
            transcribeResult.style.display = 'block';
        }
    } catch (error) {
        transcriptionText.textContent = `Error: ${error.message}`;
        transcribeResult.style.display = 'block';
    }
    
    hideLoading();
});

// ==================== MICROPHONE RECORDING ====================
const recordBtn = document.getElementById('record-btn');
const recordingIndicator = document.getElementById('recording-indicator');
const recordTimeDisplay = document.getElementById('record-time');

let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let recordingTimer = null;
let isRecording = false;

recordBtn.addEventListener('click', async () => {
    if (!isRecording) {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];
            
            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };
            
            mediaRecorder.onstop = async () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
                selectedAudio = new File([audioBlob], 'recording.webm', { type: 'audio/webm' });
                
                audioUploadZone.innerHTML = `
                    <i class="fa-solid fa-microphone"></i>
                    <p>Recording captured</p>
                    <span>Click to change</span>
                `;
                transcribeBtn.disabled = false;
                
                stream.getTracks().forEach(track => track.stop());
            };
            
            mediaRecorder.start();
            isRecording = true;
            recordingStartTime = Date.now();
            
            recordBtn.innerHTML = '<i class="fa-solid fa-stop"></i><span>Stop Recording</span>';
            recordBtn.classList.add('recording');
            recordingIndicator.style.display = 'flex';
            
            recordingTimer = setInterval(() => {
                const elapsed = Math.floor((Date.now() - recordingStartTime) / 1000);
                const minutes = String(Math.floor(elapsed / 60)).padStart(2, '0');
                const seconds = String(elapsed % 60).padStart(2, '0');
                recordTimeDisplay.textContent = `${minutes}:${seconds}`;
            }, 1000);
            
        } catch (error) {
            alert('Microphone access denied or not available');
            console.error(error);
        }
    } else {
        mediaRecorder.stop();
        isRecording = false;
        
        clearInterval(recordingTimer);
        recordBtn.innerHTML = '<i class="fa-solid fa-microphone"></i><span>Start Recording</span>';
        recordBtn.classList.remove('recording');
        recordingIndicator.style.display = 'none';
    }
});

// ==================== AI RESPONSE FOR VOICE ====================
const askAiBtn = document.getElementById('ask-ai-btn');
const autoAiBtn = document.getElementById('auto-ai-btn');
const voiceAiResult = document.getElementById('voice-ai-result');
const voiceAiText = document.getElementById('voice-ai-text');

askAiBtn.addEventListener('click', async () => {
    const transcribedText = transcriptionText.textContent.trim();
    if (!transcribedText || transcribedText === 'No speech detected') {
        alert('No transcription available');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: transcribedText, history: [] })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            voiceAiText.innerHTML = formatAIResponse(data.response || 'No response');
            voiceAiResult.style.display = 'block';
        } else {
            voiceAiText.textContent = `Error: ${data.error || 'Unknown error'}`;
            voiceAiResult.style.display = 'block';
        }
    } catch (error) {
        voiceAiText.textContent = `Error: ${error.message}`;
        voiceAiResult.style.display = 'block';
    }
    
    hideLoading();
});

autoAiBtn.addEventListener('click', async () => {
    const transcribedText = transcriptionText.textContent.trim();
    if (!transcribedText || transcribedText === 'No speech detected') {
        alert('No transcription available');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: transcribedText, history: [] })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            voiceAiText.innerHTML = formatAIResponse(data.response || 'No response');
            voiceAiResult.style.display = 'block';
            
            ttsInput.value = data.response || '';
        } else {
            voiceAiText.textContent = `Error: ${data.error || 'Unknown error'}`;
            voiceAiResult.style.display = 'block';
        }
    } catch (error) {
        voiceAiText.textContent = `Error: ${error.message}`;
        voiceAiResult.style.display = 'block';
    }
    
    hideLoading();
});

// ==================== TEXT TO SPEECH ====================
const ttsInput = document.getElementById('tts-input');
const speakBtn = document.getElementById('speak-btn');
const audioPlayer = document.getElementById('audio-player');

speakBtn.addEventListener('click', async () => {
    const text = ttsInput.value.trim();
    if (!text) {
        alert('Please enter text to convert to speech');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/speak`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `text=${encodeURIComponent(text)}`
        });
        
        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            audioPlayer.src = url;
            audioPlayer.style.display = 'block';
            audioPlayer.play();
        } else {
            alert('Error generating speech');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
    
    hideLoading();
});

// ==================== CHAT ====================
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const chatMessages = document.getElementById('chat-messages');

let chatHistory = [];

async function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    
    addMessage(message, 'user');
    chatInput.value = '';
    
    showLoading();
    
    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: chatHistory
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            const botResponse = data.response || 'No response';
            addMessage(botResponse, 'bot');
            chatHistory.push([message, botResponse]);
        } else {
            addMessage(`Error: ${data.error || 'Unknown error'}`, 'bot');
        }
    } catch (error) {
        addMessage(`Error: ${error.message}`, 'bot');
    }
    
    hideLoading();
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const avatarIcon = sender === 'bot' ? 'fa-robot' : 'fa-user';
    
    let formattedText = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fa-solid ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <p>${formattedText}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// ==================== UTILITIES ====================
function showLoading() {
    loadingOverlay.classList.add('active');
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
}