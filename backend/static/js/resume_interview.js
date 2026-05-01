// Resume Interview Logic
let sessionId = null;
let questions = [];
let currentQuestionIndex = 0;
let resumeKeywords = [];
let parsedData = null;
let timerInterval = null;
let startTime = null;

// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const analysisSection = document.getElementById('analysisSection');
const interviewSection = document.getElementById('interviewSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const loadingText = document.getElementById('loadingText');

const uploadArea = document.getElementById('uploadArea');
const resumeInput = document.getElementById('resumeInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFileBtn');
const analyzeBtn = document.getElementById('analyzeBtn');

const skillsList = document.getElementById('skillsList');
const educationList = document.getElementById('educationList');
const projectsList = document.getElementById('projectsList');
const startInterviewBtn = document.getElementById('startInterviewBtn');

const questionText = document.getElementById('questionText');
const questionTypeBadge = document.getElementById('questionTypeBadge');
const answerInput = document.getElementById('answerInput');
const wordCount = document.getElementById('wordCount');
const currentQuestionSpan = document.getElementById('currentQuestion');
const progressFill = document.getElementById('progressFill');
const timer = document.getElementById('timer');

const submitAnswerBtn = document.getElementById('submitAnswerBtn');
const skipBtn = document.getElementById('skipBtn');
const nextQuestionBtn = document.getElementById('nextQuestionBtn');

const feedbackContainer = document.getElementById('feedbackContainer');
const scoreValue = document.getElementById('scoreValue');
const alignmentValue = document.getElementById('alignmentValue');
const strengthsList = document.getElementById('strengthsList');
const weaknessList = document.getElementById('weaknessList');
const suggestionsList = document.getElementById('suggestionsList');

if (window.initVoiceInput) {
    window.initVoiceInput({
        textareaId: 'answerInput',
        buttonId: 'voiceBtn',
        statusId: 'voiceStatus'
    });
}

let selectedFile = null;

// Upload Area Click
uploadArea.addEventListener('click', () => {
    resumeInput.click();
});

// Drag and Drop
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.style.background = 'rgba(102, 126, 234, 0.1)';
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.style.background = '';
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.style.background = '';
    
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

// File Input Change
resumeInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

// Remove File
removeFileBtn.addEventListener('click', () => {
    selectedFile = null;
    fileInfo.classList.add('hidden');
    uploadArea.style.display = 'block';
    analyzeBtn.disabled = true;
});

// Analyze Resume
analyzeBtn.addEventListener('click', async () => {
    await analyzeResume();
});

// Start Interview
startInterviewBtn.addEventListener('click', () => {
    analysisSection.classList.add('hidden');
    interviewSection.classList.remove('hidden');
    loadQuestion();
    startTimer();
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

// Skip Question
skipBtn.addEventListener('click', () => {
    nextQuestion();
});

// Next Question
nextQuestionBtn.addEventListener('click', () => {
    nextQuestion();
});

// Functions
function handleFileSelect(file) {
    if (file.type !== 'application/pdf') {
        alert('Please select a PDF file');
        return;
    }
    
    if (file.size > 5 * 1024 * 1024) { // 5MB
        alert('File size should be less than 5MB');
        return;
    }
    
    selectedFile = file;
    fileName.textContent = file.name;
    fileInfo.classList.remove('hidden');
    uploadArea.style.display = 'none';
    analyzeBtn.disabled = false;
}

async function analyzeResume() {
    if (!selectedFile) return;
    
    try {
        showLoading('Analyzing your resume...');
        
        const formData = new FormData();
        formData.append('resume', selectedFile);
        
        const response = await fetch('/api/resume/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            sessionId = data.session_id;
            parsedData = data.parsed_data;
            questions = data.questions;
            currentQuestionIndex = 0;
            
            // Extract keywords for evaluation
            resumeKeywords = parsedData.skills.concat(
                parsedData.education.join(' ').split(' '),
                parsedData.projects.join(' ').split(' ')
            ).slice(0, 20);
            
            // Display analysis
            displayAnalysis(parsedData);
            
            // Show analysis section
            uploadSection.classList.add('hidden');
            analysisSection.classList.remove('hidden');
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error analyzing resume: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayAnalysis(data) {
    // Skills
    skillsList.innerHTML = '';
    if (data.skills && data.skills.length > 0) {
        data.skills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'tag';
            tag.textContent = skill;
            skillsList.appendChild(tag);
        });
    } else {
        skillsList.innerHTML = '<p style="color: #999;">No skills detected</p>';
    }
    
    // Education
    educationList.innerHTML = '';
    if (data.education && data.education.length > 0) {
        data.education.forEach(edu => {
            const li = document.createElement('li');
            li.textContent = edu;
            educationList.appendChild(li);
        });
    } else {
        educationList.innerHTML = '<li style="color: #999;">No education information detected</li>';
    }
    
    // Projects
    projectsList.innerHTML = '';
    if (data.projects && data.projects.length > 0) {
        data.projects.forEach(project => {
            const li = document.createElement('li');
            li.textContent = project;
            projectsList.appendChild(li);
        });
    } else {
        projectsList.innerHTML = '<li style="color: #999;">No projects detected</li>';
    }
}

function loadQuestion() {
    const question = questions[currentQuestionIndex];
    
    questionText.textContent = question.question;
    
    // Set question type badge
    const typeLabels = {
        'skill': 'Skill-Based',
        'project': 'Project-Based',
        'education': 'Education-Based',
        'general': 'General'
    };
    questionTypeBadge.textContent = typeLabels[question.type] || 'General';
    
    // Update progress
    currentQuestionSpan.textContent = `Question ${currentQuestionIndex + 1} of ${questions.length}`;
    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;
    progressFill.style.width = progress + '%';
    
    // Clear answer
    answerInput.value = '';
    wordCount.textContent = '0';
    
    // Hide feedback
    feedbackContainer.classList.add('hidden');
    submitAnswerBtn.disabled = false;
}

async function submitAnswer() {
    const answer = answerInput.value.trim();
    
    if (!answer) {
        alert('Please provide an answer before submitting.');
        return;
    }
    
    if (answer.split(/\s+/).length < 5) {
        alert('Please provide a more detailed answer (at least 5 words).');
        return;
    }
    
    try {
        showLoading('Evaluating your answer...');
        submitAnswerBtn.disabled = true;
        
        const question = questions[currentQuestionIndex];
        
        const response = await fetch('/api/resume/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                question: question.question,
                answer: answer,
                question_type: question.type,
                resume_keywords: resumeKeywords
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayFeedback(result);
        } else {
            alert('Error evaluating answer: ' + result.error);
            submitAnswerBtn.disabled = false;
        }
    } catch (error) {
        alert('Error: ' + error.message);
        submitAnswerBtn.disabled = false;
    } finally {
        hideLoading();
    }
}

function displayFeedback(result) {
    // Show feedback container
    feedbackContainer.classList.remove('hidden');
    
    // Animate scores
    scoreValue.textContent = '0';
    alignmentValue.textContent = '0';
    
    setTimeout(() => {
        animateValue(scoreValue, result.score);
        animateValue(alignmentValue, result.resume_alignment);
    }, 100);
    
    // Strengths
    strengthsList.innerHTML = '';
    result.feedback.strengths.forEach(strength => {
        const li = document.createElement('li');
        li.textContent = strength;
        strengthsList.appendChild(li);
    });
    
    // Weaknesses
    weaknessList.innerHTML = '';
    result.feedback.weaknesses.forEach(weakness => {
        const li = document.createElement('li');
        li.textContent = weakness;
        weaknessList.appendChild(li);
    });
    
    // Suggestions
    suggestionsList.innerHTML = '';
    result.feedback.suggestions.forEach(suggestion => {
        const li = document.createElement('li');
        li.textContent = suggestion;
        suggestionsList.appendChild(li);
    });
    
    // Scroll to feedback
    feedbackContainer.scrollIntoView({ behavior: 'smooth' });
}

function animateValue(element, targetValue) {
    let current = 0;
    const increment = targetValue / 30;
    const interval = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(interval);
        }
        element.textContent = Math.round(current);
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
        showLoading('Generating your final report...');
        
        const response = await fetch(`/api/evaluate/session/${sessionId}/complete`, {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (response.ok) {
            const shouldDownload = confirm(
                `Interview Complete!\n\nYour Final Score: ${result.total_score}/10\nQuestions Answered: ${result.total_questions}\n\nClick OK to download your detailed PDF report.`
            );

            if (shouldDownload) {
                window.open(`/api/evaluate/session/${sessionId}/report.pdf`, '_blank');
            }

            window.location.href = '/';
        } else {
            alert('Error completing interview: ' + result.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
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
    if (timerInterval) {
        clearInterval(timerInterval);
    }
});