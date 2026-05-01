const totalSessionsEl = document.getElementById('totalSessions');
const completedSessionsEl = document.getElementById('completedSessions');
const averageScoreEl = document.getElementById('averageScore');
const bestScoreEl = document.getElementById('bestScore');
const completionRateEl = document.getElementById('completionRate');
const typeBreakdownEl = document.getElementById('typeBreakdown');
const recentSessionsBody = document.getElementById('recentSessionsBody');
const recommendationLevelEl = document.getElementById('recommendationLevel');
const recommendationFocusEl = document.getElementById('recommendationFocus');
const recommendationWhyEl = document.getElementById('recommendationWhy');
const recommendationActionsEl = document.getElementById('recommendationActions');
const loadingSpinner = document.getElementById('loadingSpinner');
const loadingText = document.getElementById('loadingText');

function showLoading(text = 'Loading...') {
    loadingText.textContent = text;
    loadingSpinner.classList.remove('hidden');
}

function hideLoading() {
    loadingSpinner.classList.add('hidden');
}

function formatSessionType(type) {
    if (!type) return 'N/A';
    return type.charAt(0).toUpperCase() + type.slice(1);
}

function renderOverview(overview) {
    totalSessionsEl.textContent = overview.total_sessions;
    completedSessionsEl.textContent = overview.completed_sessions;
    averageScoreEl.textContent = Number(overview.average_score || 0).toFixed(2);
    bestScoreEl.textContent = Number(overview.best_score || 0).toFixed(2);
    completionRateEl.textContent = `${Number(overview.completion_rate || 0).toFixed(2)}%`;
}

function renderTypeBreakdown(types) {
    typeBreakdownEl.innerHTML = '';

    if (!types || types.length === 0) {
        typeBreakdownEl.innerHTML = '<p class="empty-cell">No sessions available yet.</p>';
        return;
    }

    types.forEach(item => {
        const card = document.createElement('div');
        card.className = 'breakdown-card';
        card.innerHTML = `
            <h3>${formatSessionType(item.session_type)}</h3>
            <p>Total Sessions: <strong>${item.total}</strong></p>
            <p>Avg Score: <strong>${Number(item.avg_score || 0).toFixed(2)}</strong></p>
        `;
        typeBreakdownEl.appendChild(card);
    });
}

function renderRecentSessions(sessions) {
    recentSessionsBody.innerHTML = '';

    if (!sessions || sessions.length === 0) {
        recentSessionsBody.innerHTML = '<tr><td colspan="7" class="empty-cell">No sessions found.</td></tr>';
        return;
    }

    sessions.forEach(session => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>#${session.id}</td>
            <td>${formatSessionType(session.session_type)}</td>
            <td>${session.domain}</td>
            <td>${session.question_count}</td>
            <td>${Number(session.total_score || 0).toFixed(2)}</td>
            <td><span class="status-badge ${session.status === 'completed' ? 'status-completed' : 'status-progress'}">${session.status}</span></td>
            <td>
                ${session.status === 'completed' ? `<a class="table-link" href="/api/evaluate/session/${session.id}/report.pdf" target="_blank">Download</a>` : '-'}
            </td>
        `;
        recentSessionsBody.appendChild(row);
    });
}

function renderRecommendation(recommendation) {
    if (!recommendation) {
        return;
    }

    recommendationLevelEl.textContent = recommendation.focus_level || 'Recommendation';
    recommendationFocusEl.textContent = `Focus Area: ${recommendation.focus_area || '-'}`;
    recommendationWhyEl.textContent = recommendation.why || '';

    recommendationActionsEl.innerHTML = '';
    const actions = recommendation.actions || [];

    if (actions.length === 0) {
        recommendationActionsEl.innerHTML = '<li>No action steps available.</li>';
        return;
    }

    actions.forEach((step) => {
        const li = document.createElement('li');
        li.textContent = step;
        recommendationActionsEl.appendChild(li);
    });
}

async function loadDashboard() {
    try {
        showLoading('Loading dashboard analytics...');

        const response = await fetch('/api/evaluate/dashboard/summary');
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Unable to load dashboard');
        }

        renderOverview(data.overview || {});
        renderTypeBreakdown(data.type_breakdown || []);
        renderRecommendation(data.recommendation || {});
        renderRecentSessions(data.recent_sessions || []);
    } catch (error) {
        recentSessionsBody.innerHTML = `<tr><td colspan="7" class="empty-cell">${error.message}</td></tr>`;
    } finally {
        hideLoading();
    }
}

loadDashboard();
