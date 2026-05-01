"""
Database Models and Initialization
SQLite Database Handler
"""

import sqlite3
import json
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'interview_system.db')

def get_db_connection():
    """Get database connection"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Interview Sessions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interview_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_type TEXT NOT NULL,
            domain TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_score REAL,
            status TEXT DEFAULT 'in_progress'
        )
    ''')
    
    # Questions and Answers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            question TEXT NOT NULL,
            answer TEXT,
            score REAL,
            feedback TEXT,
            keywords_matched TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(id)
        )
    ''')
    
    # Resume Analysis Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resume_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            resume_path TEXT,
            extracted_skills TEXT,
            extracted_education TEXT,
            extracted_projects TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(id)
        )
    ''')
    
    # Behavioral Analysis Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS behavioral_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            question TEXT,
            answer TEXT,
            emotion_detected TEXT,
            confidence_score REAL,
            communication_score REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(id)
        )
    ''')
    
    # Emotion Timeline Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emotion_timeline (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            emotion TEXT,
            confidence REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES interview_sessions(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ Database initialized successfully")

def create_session(session_type, domain=None):
    """Create new interview session"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO interview_sessions (session_type, domain) VALUES (?, ?)',
        (session_type, domain)
    )
    session_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return session_id

def save_qa_record(session_id, question, answer, score, feedback, keywords):
    """Save question-answer record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO qa_records (session_id, question, answer, score, feedback, keywords_matched)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, question, answer, score, json.dumps(feedback), json.dumps(keywords)))
    conn.commit()
    conn.close()

def save_resume_analysis(session_id, resume_path, skills, education, projects):
    """Save resume analysis"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO resume_analysis (session_id, resume_path, extracted_skills, 
                                     extracted_education, extracted_projects)
        VALUES (?, ?, ?, ?, ?)
    ''', (session_id, resume_path, json.dumps(skills), json.dumps(education), json.dumps(projects)))
    conn.commit()
    conn.close()

def save_behavioral_record(session_id, question, answer, emotion, confidence_score, communication_score):
    """Save behavioral analysis record"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO behavioral_analysis (session_id, question, answer, emotion_detected,
                                         confidence_score, communication_score)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (session_id, question, answer, emotion, confidence_score, communication_score))
    conn.commit()
    conn.close()

def save_emotion_timeline(session_id, emotion, confidence):
    """Save emotion to timeline"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO emotion_timeline (session_id, emotion, confidence)
        VALUES (?, ?, ?)
    ''', (session_id, emotion, confidence))
    conn.commit()
    conn.close()

def update_session_score(session_id, total_score, status='completed'):
    """Update session with final score"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE interview_sessions 
        SET total_score = ?, status = ?
        WHERE id = ?
    ''', (total_score, status, session_id))
    conn.commit()
    conn.close()

def get_session_results(session_id):
    """Get complete session results"""
    conn = get_db_connection()
    
    # Get session info
    session = conn.execute(
        'SELECT * FROM interview_sessions WHERE id = ?', (session_id,)
    ).fetchone()
    
    # Get QA records
    qa_records = conn.execute(
        'SELECT * FROM qa_records WHERE session_id = ? ORDER BY created_at',
        (session_id,)
    ).fetchall()
    
    # Get behavioral records
    behavioral_records = conn.execute(
        'SELECT * FROM behavioral_analysis WHERE session_id = ? ORDER BY timestamp',
        (session_id,)
    ).fetchall()
    
    # Get emotion timeline
    emotion_timeline = conn.execute(
        'SELECT * FROM emotion_timeline WHERE session_id = ? ORDER BY timestamp',
        (session_id,)
    ).fetchall()
    
    conn.close()
    
    return {
        'session': dict(session) if session else None,
        'qa_records': [dict(row) for row in qa_records],
        'behavioral_records': [dict(row) for row in behavioral_records],
        'emotion_timeline': [dict(row) for row in emotion_timeline]
    }


def get_dashboard_summary(recent_limit=10):
    """Get dashboard overview metrics and recent session history"""
    conn = get_db_connection()

    total_sessions = conn.execute(
        'SELECT COUNT(*) AS count FROM interview_sessions'
    ).fetchone()['count']

    completed_sessions = conn.execute(
        "SELECT COUNT(*) AS count FROM interview_sessions WHERE status = 'completed'"
    ).fetchone()['count']

    avg_score_row = conn.execute(
        "SELECT AVG(total_score) AS avg_score FROM interview_sessions WHERE total_score IS NOT NULL"
    ).fetchone()
    avg_score = round(float(avg_score_row['avg_score']), 2) if avg_score_row['avg_score'] is not None else 0

    best_score_row = conn.execute(
        "SELECT MAX(total_score) AS best_score FROM interview_sessions WHERE total_score IS NOT NULL"
    ).fetchone()
    best_score = round(float(best_score_row['best_score']), 2) if best_score_row['best_score'] is not None else 0

    type_breakdown = conn.execute('''
        SELECT
            session_type,
            COUNT(*) AS total,
            ROUND(AVG(total_score), 2) AS avg_score
        FROM interview_sessions
        GROUP BY session_type
        ORDER BY total DESC
    ''').fetchall()

    completed_type_breakdown = conn.execute('''
        SELECT
            session_type,
            COUNT(*) AS total,
            ROUND(AVG(total_score), 2) AS avg_score
        FROM interview_sessions
        WHERE status = 'completed' AND total_score IS NOT NULL
        GROUP BY session_type
    ''').fetchall()

    recent_sessions = conn.execute('''
        SELECT
            s.id,
            s.session_type,
            s.domain,
            s.created_at,
            s.total_score,
            s.status,
            (SELECT COUNT(*) FROM qa_records q WHERE q.session_id = s.id) AS qa_count,
            (SELECT COUNT(*) FROM behavioral_analysis b WHERE b.session_id = s.id) AS behavioral_count
        FROM interview_sessions s
        ORDER BY s.created_at DESC
        LIMIT ?
    ''', (recent_limit,)).fetchall()

    conn.close()

    type_data = [
        {
            'session_type': row['session_type'],
            'total': row['total'],
            'avg_score': row['avg_score'] if row['avg_score'] is not None else 0
        }
        for row in type_breakdown
    ]

    recent_data = []
    for row in recent_sessions:
        question_count = int(row['qa_count']) + int(row['behavioral_count'])
        recent_data.append({
            'id': row['id'],
            'session_type': row['session_type'],
            'domain': row['domain'] or 'N/A',
            'created_at': row['created_at'],
            'total_score': row['total_score'] if row['total_score'] is not None else 0,
            'status': row['status'],
            'question_count': question_count
        })

    completed_type_data = [
        {
            'session_type': row['session_type'],
            'total': row['total'],
            'avg_score': row['avg_score'] if row['avg_score'] is not None else 0
        }
        for row in completed_type_breakdown
    ]

    if completed_type_data:
        weakest_type = min(completed_type_data, key=lambda item: item['avg_score'])
        strongest_type = max(completed_type_data, key=lambda item: item['avg_score'])
        weakest_score = float(weakest_type['avg_score'])

        if weakest_score < 5:
            focus_level = 'High Priority'
            actions = [
                f"Practice 5 focused {weakest_type['session_type']} questions daily for 1 week.",
                'After each answer, rewrite it with clearer structure and examples.',
                'Take one full mock interview every 2 days and compare scores.'
            ]
        elif weakest_score < 7:
            focus_level = 'Medium Priority'
            actions = [
                f"Improve depth in {weakest_type['session_type']} answers with trade-offs and use-cases.",
                'Target 3 timed practice questions per day and review feedback points.',
                'Track weekly average and push it above 7.5.'
            ]
        else:
            focus_level = 'Optimization'
            actions = [
                'Maintain consistency with 2 mock interviews per week.',
                f"Use {strongest_type['session_type']} as your anchor and sharpen weaker sections.",
                'Focus on concise delivery and confidence for final polish.'
            ]

        recommendation = {
            'focus_level': focus_level,
            'focus_area': weakest_type['session_type'],
            'focus_score': round(weakest_score, 2),
            'strength_area': strongest_type['session_type'],
            'strength_score': round(float(strongest_type['avg_score']), 2),
            'why': f"Your lowest completed-session average is in {weakest_type['session_type']} ({round(weakest_score, 2)}/10).",
            'actions': actions
        }
    else:
        recommendation = {
            'focus_level': 'Getting Started',
            'focus_area': 'Complete your first interviews',
            'focus_score': 0,
            'strength_area': 'N/A',
            'strength_score': 0,
            'why': 'Complete at least one interview session to generate personalized recommendations.',
            'actions': [
                'Start with one Domain interview and complete all questions.',
                'Try one Behavioral interview to assess communication and confidence.',
                'Download reports and review top weaknesses before your next attempt.'
            ]
        }

    return {
        'overview': {
            'total_sessions': total_sessions,
            'completed_sessions': completed_sessions,
            'average_score': avg_score,
            'best_score': best_score,
            'completion_rate': round((completed_sessions / total_sessions) * 100, 2) if total_sessions else 0
        },
        'type_breakdown': type_data,
        'recent_sessions': recent_data,
        'recommendation': recommendation
    }
