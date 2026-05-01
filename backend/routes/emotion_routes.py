"""
Emotion Detection Routes
API endpoints for behavioral interview with emotion analysis
"""

from flask import Blueprint, request, jsonify
from utils.emotion_detector import EmotionDetector
from utils.answer_evaluator import AnswerEvaluator
from models.database import (
    save_behavioral_record, 
    save_emotion_timeline,
    update_session_score,
    get_session_results
)

bp = Blueprint('emotion', __name__, url_prefix='/api/emotion')

# Initialize emotion detector
emotion_detector = EmotionDetector()
last_detected_emotion = {}

@bp.route('/analyze', methods=['POST'])
def analyze_emotion():
    """Analyze emotion from webcam image"""
    try:
        data = request.json
        image_data = data.get('image')
        session_id = data.get('session_id')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Analyze emotion
        result = emotion_detector.analyze_emotion_from_base64(image_data)

        if session_id:
            session_key = str(session_id)
            if result.get('face_detected'):
                last_detected_emotion[session_key] = {
                    'emotion': result.get('emotion', 'neutral'),
                    'confidence': result.get('confidence', 50),
                    'description': result.get('description', 'Calm and composed')
                }
            elif session_key in last_detected_emotion:
                cached = last_detected_emotion[session_key]
                result['emotion'] = cached['emotion']
                result['confidence'] = cached['confidence']
                result['description'] = f"{cached['description']} (tracking fallback)"
                result['face_detected'] = False
        
        # Save to timeline if session provided
        if session_id and result.get('face_detected'):
            save_emotion_timeline(
                session_id,
                result['emotion'],
                result['confidence']
            )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/behavioral/submit', methods=['POST'])
def submit_behavioral_answer():
    """Submit behavioral interview answer with emotion data"""
    try:
        data = request.json
        session_id = data.get('session_id')
        question = data.get('question')
        answer = data.get('answer')
        emotion_data = data.get('emotion_data', {})
        
        if not all([session_id, question, answer]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Evaluate behavioral answer
        evaluation = AnswerEvaluator.evaluate_behavioral_answer(answer)
        
        # Extract emotion info
        emotion = emotion_data.get('emotion', 'neutral')
        emotion_confidence = emotion_data.get('confidence', 50)
        
        # Calculate confidence score from emotion
        if emotion == 'confident':
            confidence_score = min(10, 7 + (emotion_confidence / 20))
        elif emotion == 'neutral':
            confidence_score = 6
        elif emotion == 'nervous':
            confidence_score = 4
        else:  # anxious
            confidence_score = 3
        
        # Save behavioral record
        save_behavioral_record(
            session_id,
            question,
            answer,
            emotion,
            confidence_score,
            evaluation['communication_score']
        )
        
        return jsonify({
            'communication_score': evaluation['communication_score'],
            'confidence_score': confidence_score,
            'emotion': emotion,
            'word_count': evaluation['word_count'],
            'analysis': {
                'has_structure': evaluation['has_structure'],
                'has_examples': evaluation['has_examples']
            }
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/behavioral/complete/<int:session_id>', methods=['POST'])
def complete_behavioral_interview():
    """Complete behavioral interview and generate final report"""
    try:
        # Get session results
        results = get_session_results(session_id)
        
        if not results['session']:
            return jsonify({'error': 'Session not found'}), 404
        
        behavioral_records = results['behavioral_records']
        emotion_timeline = results['emotion_timeline']
        
        if not behavioral_records:
            return jsonify({'error': 'No behavioral records found'}), 404
        
        # Calculate average scores
        avg_communication = sum(r['communication_score'] for r in behavioral_records) / len(behavioral_records)
        avg_confidence = sum(r['confidence_score'] for r in behavioral_records) / len(behavioral_records)
        
        # Calculate overall confidence from emotion timeline
        timeline_confidence = emotion_detector.calculate_confidence_from_emotions(
            [{'emotion': e['emotion'], 'confidence': e['confidence']} 
             for e in emotion_timeline]
        )
        
        # Combine scores (70% from answers, 30% from emotion timeline)
        final_confidence = (avg_confidence * 0.7) + (timeline_confidence * 0.3)
        
        # Generate emotion insights
        insights = emotion_detector.generate_emotion_insights(
            [{'emotion': e['emotion'], 'confidence': e['confidence']} 
             for e in emotion_timeline]
        )
        
        # Calculate total score (average of communication and confidence)
        total_score = (avg_communication + final_confidence) / 2
        
        # Update session
        update_session_score(session_id, total_score, 'completed')
        
        # Generate personalized suggestions
        suggestions = insights['suggestions'].copy()
        
        if avg_communication < 5:
            suggestions.append('Work on structuring your answers using STAR method')
            suggestions.append('Practice articulating your thoughts clearly')
        elif avg_communication > 8:
            suggestions.append('Excellent communication skills!')
        
        if final_confidence < 5:
            suggestions.append('Build confidence through regular practice')
            suggestions.append('Prepare well-rehearsed examples for common questions')
        elif final_confidence > 8:
            suggestions.append('Great confidence level maintained!')
        
        return jsonify({
            'session_id': session_id,
            'total_score': round(total_score, 2),
            'communication_score': round(avg_communication, 2),
            'confidence_score': round(final_confidence, 2),
            'emotion_insights': insights,
            'suggestions': suggestions,
            'total_questions': len(behavioral_records),
            'emotion_samples': len(emotion_timeline)
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500