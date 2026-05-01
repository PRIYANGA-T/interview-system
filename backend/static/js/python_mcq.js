let sessionId = null;
let questions = [];
let currentIndex = 0;
let answers = [];
let hardSessionId = null;
let hardQuestions = [];
let hardCurrentIndex = 0;
let hardAnswers = [];

const mcqIntro = document.getElementById('mcqIntro');
const mcqSection = document.getElementById('mcqSection');
const mcqResultSection = document.getElementById('mcqResultSection');
const hardMcqSection = document.getElementById('hardMcqSection');
const hardResultSection = document.getElementById('hardResultSection');

const startMcqBtn = document.getElementById('startMcqBtn');
const startHardMcqBtn = document.getElementById('startHardMcqBtn');
const prevMcqBtn = document.getElementById('prevMcqBtn');
const nextMcqBtn = document.getElementById('nextMcqBtn');
const submitMcqBtn = document.getElementById('submitMcqBtn');

const mcqProgressFill = document.getElementById('mcqProgressFill');
const mcqCurrentQuestion = document.getElementById('mcqCurrentQuestion');
const mcqCategoryBadge = document.getElementById('mcqCategoryBadge');
const mcqQuestionText = document.getElementById('mcqQuestionText');
const mcqOptions = document.getElementById('mcqOptions');

const mcqTotalScore = document.getElementById('mcqTotalScore');
const mcqPercentage = document.getElementById('mcqPercentage');
const beginnerScore = document.getElementById('beginnerScore');
const advancedScore = document.getElementById('advancedScore');
const dsaScore = document.getElementById('dsaScore');

const hardProgressFill = document.getElementById('hardProgressFill');
const hardCurrentQuestion = document.getElementById('hardCurrentQuestion');
const hardQuestionText = document.getElementById('hardQuestionText');
const hardCodeBlock = document.getElementById('hardCodeBlock');
const hardOptions = document.getElementById('hardOptions');
const prevHardBtn = document.getElementById('prevHardBtn');
const nextHardBtn = document.getElementById('nextHardBtn');
const submitHardBtn = document.getElementById('submitHardBtn');
const hardTotalScore = document.getElementById('hardTotalScore');
const hardPercentage = document.getElementById('hardPercentage');
const hardExplanationList = document.getElementById('hardExplanationList');
const downloadHardReportBtn = document.getElementById('downloadHardReportBtn');

const loadingSpinner = document.getElementById('loadingSpinner');
const loadingText = document.getElementById('loadingText');

startMcqBtn.addEventListener('click', async () => {
    await startMcqAssessment();
});

startHardMcqBtn.addEventListener('click', async () => {
    await startHardAssessment();
});

prevMcqBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex -= 1;
        renderQuestion();
    }
});

nextMcqBtn.addEventListener('click', () => {
    if (currentIndex < questions.length - 1) {
        currentIndex += 1;
        renderQuestion();
    }
});

submitMcqBtn.addEventListener('click', async () => {
    await submitAssessment();
});

prevHardBtn.addEventListener('click', () => {
    if (hardCurrentIndex > 0) {
        hardCurrentIndex -= 1;
        renderHardQuestion();
    }
});

nextHardBtn.addEventListener('click', () => {
    if (hardCurrentIndex < hardQuestions.length - 1) {
        hardCurrentIndex += 1;
        renderHardQuestion();
    }
});

submitHardBtn.addEventListener('click', async () => {
    await submitHardAssessment();
});

function formatCategory(category) {
    if (category === 'beginner') return 'Beginner';
    if (category === 'advanced') return 'Advanced';
    return 'Python DSA';
}

function showLoading(message) {
    loadingText.textContent = message;
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

async function startMcqAssessment() {
    try {
        showLoading('Loading Python MCQ questions...');

        const response = await fetch('/api/questions/python-mcq');
        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Unable to load questions');
            return;
        }

        sessionId = data.session_id;
        questions = data.questions || [];
        answers = new Array(questions.length).fill(null);
        currentIndex = 0;

        mcqIntro.classList.add('hidden');
        mcqSection.classList.remove('hidden');

        renderQuestion();
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

async function startHardAssessment() {
    try {
        showLoading('Loading hard code-output questions...');

        const response = await fetch('/api/questions/python-hard-output');
        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Unable to load hard questions');
            return;
        }

        hardSessionId = data.session_id;
        hardQuestions = data.questions || [];
        hardAnswers = new Array(hardQuestions.length).fill(null);
        hardCurrentIndex = 0;

        mcqIntro.classList.add('hidden');
        hardMcqSection.classList.remove('hidden');
        mcqSection.classList.add('hidden');
        mcqResultSection.classList.add('hidden');
        hardResultSection.classList.add('hidden');

        renderHardQuestion();
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function renderQuestion() {
    const currentQuestion = questions[currentIndex];
    if (!currentQuestion) return;

    mcqCurrentQuestion.textContent = `Question ${currentIndex + 1} of ${questions.length}`;
    mcqCategoryBadge.textContent = formatCategory(currentQuestion.category);

    const progress = ((currentIndex + 1) / questions.length) * 100;
    mcqProgressFill.style.width = progress + '%';

    mcqQuestionText.textContent = `${currentQuestion.number}. ${currentQuestion.question}`;

    mcqOptions.innerHTML = '';
    currentQuestion.options.forEach((option, optionIndex) => {
        const optionWrapper = document.createElement('label');
        optionWrapper.className = 'mcq-option';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'mcqOption';
        radio.value = optionIndex;
        radio.checked = answers[currentIndex] === optionIndex;

        radio.addEventListener('change', () => {
            answers[currentIndex] = optionIndex;
        });

        const optionText = document.createElement('span');
        optionText.textContent = option;

        optionWrapper.appendChild(radio);
        optionWrapper.appendChild(optionText);
        mcqOptions.appendChild(optionWrapper);
    });

    prevMcqBtn.disabled = currentIndex === 0;

    const isLastQuestion = currentIndex === questions.length - 1;
    nextMcqBtn.classList.toggle('hidden', isLastQuestion);
    submitMcqBtn.classList.toggle('hidden', !isLastQuestion);
}

async function submitAssessment() {
    try {
        showLoading('Evaluating your MCQ test...');

        const payload = {
            session_id: sessionId,
            answers: questions.map((question, index) => ({
                question_id: question.id,
                selected_option: answers[index]
            }))
        };

        const response = await fetch('/api/questions/python-mcq/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || 'Unable to evaluate test');
            return;
        }

        showResult(result);
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function showResult(result) {
    mcqSection.classList.add('hidden');
    mcqResultSection.classList.remove('hidden');

    mcqTotalScore.textContent = result.score_out_of_30;
    mcqPercentage.textContent = `Percentage: ${result.percentage}% | Normalized Score: ${result.normalized_score}/10`;

    beginnerScore.textContent = `${result.section_scores.beginner.correct} / ${result.section_scores.beginner.total}`;
    advancedScore.textContent = `${result.section_scores.advanced.correct} / ${result.section_scores.advanced.total}`;
    dsaScore.textContent = `${result.section_scores.dsa.correct} / ${result.section_scores.dsa.total}`;

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function renderHardQuestion() {
    const currentQuestion = hardQuestions[hardCurrentIndex];
    if (!currentQuestion) return;

    hardCurrentQuestion.textContent = `Question ${hardCurrentIndex + 1} of ${hardQuestions.length}`;
    hardQuestionText.textContent = currentQuestion.question;
    hardCodeBlock.textContent = currentQuestion.code;

    const progress = ((hardCurrentIndex + 1) / hardQuestions.length) * 100;
    hardProgressFill.style.width = progress + '%';

    hardOptions.innerHTML = '';
    currentQuestion.options.forEach((option, optionIndex) => {
        const optionWrapper = document.createElement('label');
        optionWrapper.className = 'mcq-option';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'hardOption';
        radio.value = optionIndex;
        radio.checked = hardAnswers[hardCurrentIndex] === optionIndex;

        radio.addEventListener('change', () => {
            hardAnswers[hardCurrentIndex] = optionIndex;
        });

        const optionText = document.createElement('span');
        optionText.textContent = option;

        optionWrapper.appendChild(radio);
        optionWrapper.appendChild(optionText);
        hardOptions.appendChild(optionWrapper);
    });

    prevHardBtn.disabled = hardCurrentIndex === 0;
    const isLastQuestion = hardCurrentIndex === hardQuestions.length - 1;
    nextHardBtn.classList.toggle('hidden', isLastQuestion);
    submitHardBtn.classList.toggle('hidden', !isLastQuestion);
}

async function submitHardAssessment() {
    try {
        showLoading('Evaluating hard test and generating explanations...');

        const payload = {
            session_id: hardSessionId,
            answers: hardQuestions.map((question, index) => ({
                question_id: question.id,
                selected_option: hardAnswers[index]
            }))
        };

        const response = await fetch('/api/questions/python-hard-output/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (!response.ok) {
            alert(result.error || 'Unable to evaluate hard test');
            return;
        }

        showHardResult(result);
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function showHardResult(result) {
    hardMcqSection.classList.add('hidden');
    hardResultSection.classList.remove('hidden');

    hardTotalScore.textContent = result.score_out_of_5;
    hardPercentage.textContent = `Percentage: ${result.percentage}% | Normalized Score: ${result.normalized_score}/10`;

    if (downloadHardReportBtn) {
        downloadHardReportBtn.href = `/api/evaluate/session/${result.session_id}/report.pdf`;
        downloadHardReportBtn.classList.remove('hidden');
    }

    hardExplanationList.innerHTML = '';
    (result.review || []).forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = `feedback-card ${item.is_correct ? 'success' : 'warning'}`;

        const title = document.createElement('h4');
        title.textContent = `Q${idx + 1}: ${item.is_correct ? 'Correct' : 'Incorrect'}`;

        const details = document.createElement('ul');

        const selected = document.createElement('li');
        selected.textContent = `Your Answer: ${item.selected_text}`;

        const correct = document.createElement('li');
        correct.textContent = `Correct Answer: ${item.correct_text}`;

        const explanation = document.createElement('li');
        explanation.textContent = `Code Explanation: ${item.explanation}`;

        details.appendChild(selected);
        details.appendChild(correct);
        details.appendChild(explanation);

        card.appendChild(title);
        card.appendChild(details);
        hardExplanationList.appendChild(card);
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}
