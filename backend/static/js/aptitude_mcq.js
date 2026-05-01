let aptitudeSessionId = null;
let selectedTopicId = null;
let selectedTopicTitle = null;
let aptitudeQuestions = [];
let aptitudeAnswers = [];
let aptitudeCurrentIndex = 0;

const topicSection = document.getElementById('topicSection');
const topicGrid = document.getElementById('topicGrid');

const aptitudeQuizSection = document.getElementById('aptitudeQuizSection');
const aptitudeProgressFill = document.getElementById('aptitudeProgressFill');
const aptitudeCurrentQuestion = document.getElementById('aptitudeCurrentQuestion');
const aptitudeTopicBadge = document.getElementById('aptitudeTopicBadge');
const aptitudeQuestionText = document.getElementById('aptitudeQuestionText');
const aptitudeHint = document.getElementById('aptitudeHint');
const aptitudeOptions = document.getElementById('aptitudeOptions');

const prevAptitudeBtn = document.getElementById('prevAptitudeBtn');
const nextAptitudeBtn = document.getElementById('nextAptitudeBtn');
const submitAptitudeBtn = document.getElementById('submitAptitudeBtn');

const aptitudeResultSection = document.getElementById('aptitudeResultSection');
const aptitudeResultTopic = document.getElementById('aptitudeResultTopic');
const aptitudeScore = document.getElementById('aptitudeScore');
const aptitudePercentage = document.getElementById('aptitudePercentage');
const aptitudeReviewList = document.getElementById('aptitudeReviewList');
const chooseAnotherTopicBtn = document.getElementById('chooseAnotherTopicBtn');
const downloadAptitudeReportBtn = document.getElementById('downloadAptitudeReportBtn');

const loadingSpinner = document.getElementById('loadingSpinner');
const loadingText = document.getElementById('loadingText');

prevAptitudeBtn.addEventListener('click', () => {
    if (aptitudeCurrentIndex > 0) {
        aptitudeCurrentIndex -= 1;
        renderAptitudeQuestion();
    }
});

nextAptitudeBtn.addEventListener('click', () => {
    if (aptitudeCurrentIndex < aptitudeQuestions.length - 1) {
        aptitudeCurrentIndex += 1;
        renderAptitudeQuestion();
    }
});

submitAptitudeBtn.addEventListener('click', async () => {
    await submitAptitudeTopicTest();
});

chooseAnotherTopicBtn.addEventListener('click', () => {
    aptitudeResultSection.classList.add('hidden');
    topicSection.classList.remove('hidden');
});

function showLoading(message) {
    loadingText.textContent = message;
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

async function loadAptitudeTopics() {
    try {
        showLoading('Loading aptitude topics...');

        const response = await fetch('/api/questions/aptitude/topics');
        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Unable to load aptitude topics');
            return;
        }

        renderTopicCards(data.topics || []);
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function renderTopicCards(topics) {
    topicGrid.innerHTML = '';

    topics.forEach((topic) => {
        const card = document.createElement('div');
        card.className = 'aptitude-topic-card';

        const title = document.createElement('h3');
        title.textContent = topic.title;

        const description = document.createElement('p');
        description.textContent = topic.description;

        const details = document.createElement('span');
        details.className = 'aptitude-topic-meta';
        details.textContent = '10 MCQs • Hint Included • Intermediate to Advanced';

        const startButton = document.createElement('button');
        startButton.className = 'btn btn-primary';
        startButton.textContent = `Start ${topic.title}`;
        startButton.addEventListener('click', async () => {
            await startAptitudeTopic(topic.id, topic.title);
        });

        card.appendChild(title);
        card.appendChild(description);
        card.appendChild(details);
        card.appendChild(startButton);

        topicGrid.appendChild(card);
    });
}

async function startAptitudeTopic(topicId, topicTitle) {
    try {
        showLoading(`Loading ${topicTitle} questions...`);

        const response = await fetch(`/api/questions/aptitude/${topicId}`);
        const data = await response.json();

        if (!response.ok) {
            alert(data.error || 'Unable to start topic test');
            return;
        }

        aptitudeSessionId = data.session_id;
        selectedTopicId = data.topic_id;
        selectedTopicTitle = data.topic_title;
        aptitudeQuestions = data.questions || [];
        aptitudeAnswers = new Array(aptitudeQuestions.length).fill(null);
        aptitudeCurrentIndex = 0;

        topicSection.classList.add('hidden');
        aptitudeResultSection.classList.add('hidden');
        aptitudeQuizSection.classList.remove('hidden');

        renderAptitudeQuestion();
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function renderAptitudeQuestion() {
    const currentQuestion = aptitudeQuestions[aptitudeCurrentIndex];
    if (!currentQuestion) return;

    aptitudeCurrentQuestion.textContent = `Question ${aptitudeCurrentIndex + 1} of ${aptitudeQuestions.length}`;
    aptitudeTopicBadge.textContent = selectedTopicTitle || 'Aptitude';

    const progress = ((aptitudeCurrentIndex + 1) / aptitudeQuestions.length) * 100;
    aptitudeProgressFill.style.width = progress + '%';

    aptitudeQuestionText.textContent = `${aptitudeCurrentIndex + 1}. ${currentQuestion.question}`;
    aptitudeHint.textContent = `Hint: ${currentQuestion.hint}`;

    aptitudeOptions.innerHTML = '';
    currentQuestion.options.forEach((option, optionIndex) => {
        const optionWrapper = document.createElement('label');
        optionWrapper.className = 'mcq-option';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'aptitudeOption';
        radio.value = optionIndex;
        radio.checked = aptitudeAnswers[aptitudeCurrentIndex] === optionIndex;

        radio.addEventListener('change', () => {
            aptitudeAnswers[aptitudeCurrentIndex] = optionIndex;
        });

        const optionText = document.createElement('span');
        optionText.textContent = option;

        optionWrapper.appendChild(radio);
        optionWrapper.appendChild(optionText);
        aptitudeOptions.appendChild(optionWrapper);
    });

    prevAptitudeBtn.disabled = aptitudeCurrentIndex === 0;
    const isLast = aptitudeCurrentIndex === aptitudeQuestions.length - 1;
    nextAptitudeBtn.classList.toggle('hidden', isLast);
    submitAptitudeBtn.classList.toggle('hidden', !isLast);
}

async function submitAptitudeTopicTest() {
    try {
        showLoading('Evaluating topic test...');

        const payload = {
            session_id: aptitudeSessionId,
            topic_id: selectedTopicId,
            answers: aptitudeQuestions.map((question, index) => ({
                question_id: question.id,
                selected_option: aptitudeAnswers[index]
            }))
        };

        const response = await fetch('/api/questions/aptitude/evaluate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        if (!response.ok) {
            alert(result.error || 'Unable to evaluate topic test');
            return;
        }

        showAptitudeResult(result);
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

function showAptitudeResult(result) {
    aptitudeQuizSection.classList.add('hidden');
    aptitudeResultSection.classList.remove('hidden');

    aptitudeResultTopic.textContent = `Topic: ${selectedTopicTitle}`;
    aptitudeScore.textContent = result.score_out_of_10;
    aptitudePercentage.textContent = `Percentage: ${result.percentage}% | Normalized Score: ${result.normalized_score}/10`;

    if (downloadAptitudeReportBtn) {
        downloadAptitudeReportBtn.href = `/api/evaluate/session/${result.session_id}/report.pdf`;
        downloadAptitudeReportBtn.classList.remove('hidden');
    }

    aptitudeReviewList.innerHTML = '';
    (result.review || []).forEach((item, index) => {
        const card = document.createElement('div');
        card.className = `feedback-card ${item.is_correct ? 'success' : 'warning'}`;

        const title = document.createElement('h4');
        title.textContent = `Q${index + 1}: ${item.is_correct ? 'Correct' : 'Incorrect'}`;

        const details = document.createElement('ul');

        const selected = document.createElement('li');
        selected.textContent = `Your Answer: ${item.selected_text}`;

        const correct = document.createElement('li');
        correct.textContent = `Correct Answer: ${item.correct_text}`;

        const hint = document.createElement('li');
        hint.textContent = `Hint: ${item.hint}`;

        details.appendChild(selected);
        details.appendChild(correct);
        details.appendChild(hint);

        card.appendChild(title);
        card.appendChild(details);

        aptitudeReviewList.appendChild(card);
    });

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

loadAptitudeTopics();
