// Domain Interview Logic
let selectedDomain = null;
let sessionId = null;
let questions = [];
let currentQuestionIndex = 0;
let timerInterval = null;
let startTime = null;
let adaptiveMode = true;
let totalQuestions = 5;
let lastAnswerScore = null;
let targetDifficulty = 'medium';

// DOM Elements
const domainSelection = document.getElementById('domainSelection');
const interviewSection = document.getElementById('interviewSection');
const loadingSpinner = document.getElementById('loadingSpinner');
const loadingText = document.getElementById('loadingText');

const domainCards = document.querySelectorAll('.domain-card');
const startBtn = document.getElementById('startBtn');

const questionText = document.getElementById('questionText');
const difficultyBadge = document.getElementById('difficultyBadge');
const answerInput = document.getElementById('answerInput');
const wordCount = document.getElementById('wordCount');
const currentQuestionSpan = document.getElementById('currentQuestion');
const progressFill = document.getElementById('progressFill');
const timer = document.getElementById('timer');
const adaptiveStatus = document.getElementById('adaptiveStatus');

const submitAnswerBtn = document.getElementById('submitAnswerBtn');
const skipBtn = document.getElementById('skipBtn');
const nextQuestionBtn = document.getElementById('nextQuestionBtn');

const feedbackContainer = document.getElementById('feedbackContainer');
const scoreValue = document.getElementById('scoreValue');
const keywordTags = document.getElementById('keywordTags');
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

// Domain Selection
domainCards.forEach(card => {
    card.addEventListener('click', () => {
        // Remove previous selection
        domainCards.forEach(c => c.classList.remove('selected'));
        
        // Select current
        card.classList.add('selected');
        selectedDomain = card.dataset.domain;
        
        // Enable start button
        startBtn.disabled = false;
    });
});

// Start Interview
startBtn.addEventListener('click', async () => {
    if (!selectedDomain) {
        alert('Please select a domain first');
        return;
    }
    
    await startInterview();
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
nextQuestionBtn.addEventListener('click', async () => {
    await nextQuestion();
});

function toTitleCase(value) {
    if (!value) return '';
    return value.charAt(0).toUpperCase() + value.slice(1);
}

function getNextDifficultyByScore(score, currentDifficulty = 'medium') {
    if (score === null || score === undefined) {
        return currentDifficulty;
    }

    if (score >= 8) return 'hard';
    if (score < 5) return 'easy';
    return 'medium';
}

function updateAdaptiveStatus(nextDifficulty) {
    if (!adaptiveStatus) return;
    adaptiveStatus.textContent = `Next Difficulty: ${toTitleCase(nextDifficulty)}`;
}

async function fetchAdaptiveQuestion(nextDifficulty) {
    const askedQuestions = questions.map((q) => q.question);
    const response = await fetch('/api/questions/domain/adaptive-next', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            domain: selectedDomain,
            target_difficulty: nextDifficulty,
            asked_questions: askedQuestions
        })
    });

    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.error || 'Unable to fetch adaptive question');
    }

    return data.question;
}

// Functions
async function startInterview() {
    try {
        showLoading('Generating questions for ' + selectedDomain + '...');
        
        const response = await fetch('/api/questions/domain', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                domain: selectedDomain,
                num_questions: 5,
                adaptive_mode: adaptiveMode
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            sessionId = data.session_id;
            questions = data.questions;
            currentQuestionIndex = 0;
            totalQuestions = data.total || 5;
            targetDifficulty = data.target_difficulty || 'medium';
            updateAdaptiveStatus(targetDifficulty);
            
            // Hide domain selection, show interview
            domainSelection.classList.add('hidden');
            interviewSection.classList.remove('hidden');
            
            // Load first question
            loadQuestion();
            startTimer();
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
    const question = questions[currentQuestionIndex];
    
    questionText.textContent = question.question;
    difficultyBadge.textContent = question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1);
    
    // Update difficulty badge color
    const colors = {
        'easy': '#28a745',
        'medium': '#ffc107',
        'hard': '#dc3545'
    };
    difficultyBadge.style.background = colors[question.difficulty] || '#ffc107';
    
    // Update progress
    currentQuestionSpan.textContent = `Question ${currentQuestionIndex + 1} of ${totalQuestions}`;
    const progress = ((currentQuestionIndex + 1) / totalQuestions) * 100;
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
        
        const response = await fetch('/api/evaluate/answer', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                session_id: sessionId,
                question: question.question,
                answer: answer,
                keywords: question.keywords,
                difficulty: question.difficulty
            })
        });
        
        const result = await response.json();
        
        if (response.ok) {
            lastAnswerScore = result.score;
            targetDifficulty = getNextDifficultyByScore(result.score, question.difficulty);
            updateAdaptiveStatus(targetDifficulty);
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
    
    // Animate score
    scoreValue.textContent = '0';
    setTimeout(() => {
        animateScore(scoreValue, result.score);
    }, 100);
    
    // Keywords
    keywordTags.innerHTML = '';
    if (result.matched_keywords && result.matched_keywords.length > 0) {
        result.matched_keywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            keywordTags.appendChild(tag);
        });
    } else {
        keywordTags.innerHTML = '<p style="color: #999;">No keywords matched</p>';
    }
    
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

function animateScore(element, targetValue) {
    let current = 0;
    const increment = targetValue / 30;
    const interval = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(interval);
        }
        element.textContent = current.toFixed(1);
    }, 30);
}

async function nextQuestion() {
    currentQuestionIndex++;
    
    if (currentQuestionIndex < totalQuestions) {
        try {
            if (!questions[currentQuestionIndex] && adaptiveMode) {
                showLoading('Generating your next adaptive question...');
                const nextDifficulty = targetDifficulty || getNextDifficultyByScore(lastAnswerScore, 'medium');
                const nextQuestionData = await fetchAdaptiveQuestion(nextDifficulty);
                questions.push(nextQuestionData);
                updateAdaptiveStatus(nextDifficulty);
            }
        } catch (error) {
            alert('Error generating next question: ' + error.message);
            completeInterview();
            return;
        } finally {
            hideLoading();
        }

        loadQuestion();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } else {
        completeInterview();
    }
}

async function completeInterview() {
    try {
        showLoading('Calculating your final score...');
        
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