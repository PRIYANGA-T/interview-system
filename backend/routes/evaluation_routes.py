"""
Answer Evaluation Routes
API endpoints for evaluating interview answers
"""

from flask import Blueprint, request, jsonify, send_file
from utils.answer_evaluator import AnswerEvaluator
from utils.report_generator import ReportGenerator
from models.database import save_qa_record, update_session_score, get_session_results, get_dashboard_summary

bp = Blueprint('evaluation', __name__, url_prefix='/api/evaluate')

@bp.route('/answer', methods=['POST'])
def evaluate_answer():
    """Evaluate a single answer"""
    try:
        data = request.json
        session_id = data.get('session_id')
        question = data.get('question')
        answer = data.get('answer')
        keywords = data.get('keywords', [])
        difficulty = data.get('difficulty', 'medium')
        
        if not all([session_id, question, answer]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Evaluate answer
        result = AnswerEvaluator.evaluate_answer(question, answer, keywords, difficulty)
        
        # Save to database
        save_qa_record(
            session_id, 
            question, 
            answer, 
            result['score'], 
            result['feedback'],
            result['matched_keywords']
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/session/<int:session_id>/complete', methods=['POST'])
def complete_session():
    """Mark session as complete and calculate final score"""
    try:
        # Get all QA records for session
        results = get_session_results(session_id)
        
        if not results['session']:
            return jsonify({'error': 'Session not found'}), 404
        
        # Calculate average score
        qa_records = results['qa_records']
        if qa_records:
            total_score = sum(record['score'] for record in qa_records)
            avg_score = total_score / len(qa_records)
        else:
            avg_score = 0
        
        # Update session
        update_session_score(session_id, avg_score, 'completed')
        
        return jsonify({
            'session_id': session_id,
            'total_score': round(avg_score, 2),
            'total_questions': len(qa_records),
            'status': 'completed'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/session/<int:session_id>/results', methods=['GET'])
def get_results():
    """Get complete results for a session"""
    try:
        results = get_session_results(session_id)
        
        if not results['session']:
            return jsonify({'error': 'Session not found'}), 404
        
        return jsonify(results), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/session/<int:session_id>/report.pdf', methods=['GET'])
def download_session_report(session_id):
    """Download detailed session feedback report as PDF"""
    try:
        results = get_session_results(session_id)

        if not results['session']:
            return jsonify({'error': 'Session not found'}), 404

        report_buffer = ReportGenerator.generate_session_report(results)

        return send_file(
            report_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'interview_feedback_session_{session_id}.pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/dashboard/summary', methods=['GET'])
def dashboard_summary():
    """Get dashboard analytics summary"""
    try:
        data = get_dashboard_summary()
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500