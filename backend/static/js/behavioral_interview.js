// Behavioral Interview with Emotion Detection
let sessionId = null;
let questions = [];
let currentQuestionIndex = 0;
let stream = null;
let emotionInterval = null;
let timerInterval = null;
let startTime = null;
let emotionSamples = [];

// DOM Elements
const cameraSetup = document.getElementById('cameraSetup');
const interviewSection = document.getElementById('interviewSection');
const resultsSection = document.getElementById('resultsSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const loadingText = document.getElementById('loadingText');

const webcam = document.getElementById('webcam');
const interviewWebcam = document.getElementById('interviewWebcam');
const canvas = document.getElementById('canvas');
const currentEmotion = document.getElementById('currentEmotion');
const cameraStatus = document.getElementById('cameraStatus');

const startCameraBtn = document.getElementById('startCameraBtn');
const beginInterviewBtn = document.getElementById('beginInterviewBtn');

const emotionBadge = document.getElementById('emotionBadge');
const emotionIcon = document.getElementById('emotionIcon');
const emotionText = document.getElementById('emotionText');
const confidenceMeter = document.getElementById('confidenceMeter');

const questionText = document.getElementById('questionText');
const answerInput = document.getElementById('answerInput');
const wordCount = document.getElementById('wordCount');
const sampleCount = document.getElementById('sampleCount');
const currentQuestionSpan = document.getElementById('currentQuestion');
const progressFill = document.getElementById('progressFill');
const timer = document.getElementById('timer');

const submitAnswerBtn = document.getElementById('submitAnswerBtn');
const quickFeedback = document.getElementById('quickFeedback');
const commScore = document.getElementById('commScore');
const confScore = document.getElementById('confScore');
const nextQuestionBtn = document.getElementById('nextQuestionBtn');
const downloadReportBtn = document.getElementById('downloadReportBtn');

if (window.initVoiceInput) {
    window.initVoiceInput({
        textareaId: 'answerInput',
        buttonId: 'voiceBtn',
        statusId: 'voiceStatus'
    });
}

// Emotion icons mapping
const emotionIcons = {
    'confident': '😊',
    'neutral': '😐',
    'nervous': '😰',
    'anxious': '😟',
    'not_detected': '❓'
};

// Start Camera
startCameraBtn.addEventListener('click', async () => {
    await startCamera();
});

// Begin Interview
beginInterviewBtn.addEventListener('click', async () => {
    await beginInterview();
});

// Word Count
answerInput.addEventListener('input', () => {
    const words = answerInput.value.trim().split(/\s+/).filter(w => w.length > 0);
    wordCount.textContent = words.length;
});

// Submit Answer
submitAnswerBtn.addEventListener('click', async () => {
    await submitAnswer();
});

// Next Question
nextQuestionBtn.addEventListener('click', () => {
    nextQuestion();
});

if (downloadReportBtn) {
    downloadReportBtn.addEventListener('click', () => {
        if (!sessionId) {
            alert('Session not found. Please complete an interview first.');
            return;
        }
        window.open(`/api/evaluate/session/${sessionId}/report.pdf`, '_blank');
    });
}

// Functions
async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { width: 640, height: 480 },
            audio: false 
        });
        
        webcam.srcObject = stream;
        cameraStatus.innerHTML = '✅ Camera is ready!';
        cameraStatus.style.color = '#28a745';
        
        startCameraBtn.classList.add('hidden');
        beginInterviewBtn.classList.remove('hidden');
        
        // Start emotion preview
        startEmotionPreview();
    } catch (error) {
        alert('Error accessing camera: ' + error.message + '\nPlease allow camera access.');
        cameraStatus.innerHTML = '❌ Camera access denied';
        cameraStatus.style.color = '#dc3545';
    }
}

function startEmotionPreview() {
    // Simple preview emotion detection
    setInterval(async () => {
        const emotion = await captureAndAnalyzeEmotion(webcam);
        if (emotion) {
            currentEmotion.textContent = `${emotionIcons[emotion.emotion] || '😐'} ${emotion.description}`;
        }
    }, 2000);
}

async function beginInterview() {
    try {
        showLoading('Initializing interview...');
        
        // Get behavioral questions
        const response = await fetch('/api/questions/behavioral');
        const data = await response.json();
        
        if (response.ok) {
            sessionId = data.session_id;
            questions = data.questions;
            currentQuestionIndex = 0;
            emotionSamples = [];
            
            // Transfer video stream
            interviewWebcam.srcObject = stream;
            
            // Hide setup, show interview
            cameraSetup.classList.add('hidden');
            interviewSection.classList.remove('hidden');
            
            // Load first question
            loadQuestion();
            startTimer();
            startEmotionDetection();
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error starting interview: ' + error.message);
    } finally {
        hideLoading();
    }
}

function loadQuestion() {
    questionText.textContent = questions[currentQuestionIndex];
    
    // Update progress
    currentQuestionSpan.textContent = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressFill.style.width = progress + '%';
    
    // Clear answer
    answerInput.value = '';
    wordCount.textContent = '0';
    
    // Hide feedback
    quickFeedback.classList.add('hidden');
    submitAnswerBtn.disabled = false;
    submitAnswerBtn.classList.remove('hidden');
}

function startEmotionDetection() {
    // Capture emotion every 1.5 seconds for better responsiveness
    emotionInterval = setInterval(async () => {
        const emotion = await captureAndAnalyzeEmotion(interviewWebcam);
        if (!emotion) {
            return;
        }

        updateEmotionDisplay(emotion);

        if (emotion.face_detected) {
            emotionSamples.push(emotion);
            sampleCount.textContent = emotionSamples.length;
        }
    }, 1500);
}

async function captureAndAnalyzeEmotion(videoElement) {
    try {
        if (videoElement.readyState < 2) {
            return null;
        }

        if (!videoElement.videoWidth || !videoElement.videoHeight) {
            return null;
        }

        // Capture frame from video
        canvas.width = videoElement.videoWidth;
        canvas.height = videoElement.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(videoElement, 0, 0);
        
        // Get base64 image
        const imageData = canvas.toDataURL('image/jpeg', 0.8);
        
        // Send to backend for analysis
        const response = await fetch('/api/emotion/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: imageData,
                session_id: sessionId
            })
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Emotion detection error:', error);
        return null;
    }
}

function updateEmotionDisplay(emotion) {
    // Update emotion badge
    emotionIcon.textContent = emotionIcons[emotion.emotion] || '😐';
    const emotionLabel = emotion.emotion === 'not_detected'
        ? 'Face Not Detected'
        : emotion.emotion.charAt(0).toUpperCase() + emotion.emotion.slice(1);
    emotionText.textContent = `${emotionLabel} (${Math.round(emotion.confidence || 0)}%)`;
    
    // Update confidence meter
    confidenceMeter.style.width = emotion.confidence + '%';
    
    // Color based on emotion
    const colors = {
        'confident': '#28a745',
        'neutral': '#ffc107',
        'nervous': '#fd7e14',
        'anxious': '#dc3545',
        'not_detected': '#6c757d'
    };
    emotionBadge.style.background = colors[emotion.emotion] || '#6c757d';

    if (emotion.emotion === 'not_detected') {
        confidenceMeter.style.width = '0%';
    }
}

async function submitAnswer() {
    const answer = answerInput.value.trim();
    
    if (!answer) {
        alert('Please provide an answer before submitting.');
        return;
    }
    
    if (answer.split(/\s+/).length < 10) {
        alert('Please provide a more detailed answer (at least 10 words for behavioral questions).');
        return;
    }
    
    try {
        showLoading('Analyzing your response...');
        submitAnswerBtn.disabled = true;
        
        // Get latest emotion
        const latestEmotion = emotionSamples.length > 0 
            ? emotionSamples[emotionSamples.length - 1]
            : { emotion: 'neutral', confidence: 50 };
        
        const response = await fetch('/api/emotion/behavioral/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                question: questions[currentQuestionIndex],
                answer: answer,
                emotion_data: {
                    emotion: latestEmotion.emotion,
                    confidence: latestEmotion.confidence
                }
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayQuickFeedback(result);
        } else {
            alert('Error: ' + result.error);
            submitAnswerBtn.disabled = false;
        }
    } catch (error) {
        alert('Error: ' + error.message);
        submitAnswerBtn.disabled = false;
    } finally {
        hideLoading();
    }
}

function displayQuickFeedback(result) {
    submitAnswerBtn.classList.add('hidden');
    quickFeedback.classList.remove('hidden');
    
    // Animate scores
    animateScore(commScore, result.communication_score);
    animateScore(confScore, result.confidence_score);
}

function animateScore(element, targetValue) {
    let current = 0;
    const increment = targetValue / 20;
    const interval = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(interval);
        }
        element.textContent = current.toFixed(1);
    }, 30);
}

function nextQuestion() {
    currentQuestionIndex++;
    
    if (currentQuestionIndex < questions.length) {
        loadQuestion();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        completeInterview();
    }
}

async function completeInterview() {
    try {
        // Stop emotion detection
        if (emotionInterval) {
            clearInterval(emotionInterval);
        }
        
        // Stop camera
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        
        showLoading('Generating your comprehensive report...');
        
        const response = await fetch(`/api/emotion/behavioral/complete/${sessionId}`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResults(result);
        } else {
            alert('Error: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayResults(result) {
    // Hide interview, show results
    interviewSection.classList.add('hidden');
    resultsSection.classList.remove('hidden');
    
    // Animate final scores
    const totalScore = document.getElementById('totalScore');
    const communicationScore = document.getElementById('communicationScore');
    const confidenceScore = document.getElementById('confidenceScore');
    
    animateScore(totalScore, result.total_score);
    animateScore(communicationScore, result.communication_score);
    animateScore(confidenceScore, result.confidence_score);
    
    // Emotion insights
    const dominantEmotion = document.getElementById('dominantEmotion');
    const emotionConsistency = document.getElementById('emotionConsistency');
    
    dominantEmotion.textContent = emotionIcons[result.emotion_insights.dominant_emotion] + ' ' +
        result.emotion_insights.dominant_emotion.charAt(0).toUpperCase() + 
        result.emotion_insights.dominant_emotion.slice(1);
    
    emotionConsistency.textContent = result.emotion_insights.consistency + '%';
    
    // Emotion distribution chart
    const emotionChart = document.getElementById('emotionChart');
    emotionChart.innerHTML = '';
    
    const distribution = result.emotion_insights.emotion_distribution;
    const total = Object.values(distribution).reduce((a, b) => a + b, 0);
    
    Object.entries(distribution).forEach(([emotion, count]) => {
        const percentage = (count / total) * 100;
        
        const barDiv = document.createElement('div');
        barDiv.className = 'emotion-bar';
        
        const label = document.createElement('span');
        label.className = 'emotion-bar-label';
        label.textContent = emotion.charAt(0).toUpperCase() + emotion.slice(1);
        
        const track = document.createElement('div');
        track.className = 'emotion-bar-track';
        
        const fill = document.createElement('div');
        fill.className = 'emotion-bar-fill';
        fill.style.width = '0%';
        fill.textContent = percentage.toFixed(0) + '%';
        
        track.appendChild(fill);
        barDiv.appendChild(label);
        barDiv.appendChild(track);
        emotionChart.appendChild(barDiv);
        
        // Animate bar
        setTimeout(() => {
            fill.style.width = percentage + '%';
        }, 100);
    });
    
    // Suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = '';
    
    result.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function startTimer() {
    startTime = Date.now();
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        const minutes = Math.floor(elapsed / 60);
        const seconds = elapsed % 60;
        timer.textContent = `Time: ${minutes}:${seconds.toString().padStart(2, '0')}`;
    }, 1000);
}

function showLoading(text = 'Processing...') {
    loadingText.textContent = text;
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

// Cleanup
window.addEventListener('beforeunload', () => {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (emotionInterval) {
        clearInterval(emotionInterval);
    }
    if (timerInterval) {
        clearInterval(timerInterval);
    }
});