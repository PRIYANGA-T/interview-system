"""
AI Answer Evaluator
Evaluates interview answers using NLP and keyword matching
"""

import re
import math
from collections import Counter

class AnswerEvaluator:
    """Evaluate answers using AI-based scoring"""
    
    @staticmethod
    def preprocess_text(text):
        """Preprocess text for analysis"""
        if not text:
            return []
        # Convert to lowercase and remove special characters
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', ' ', text)
        # Tokenize
        words = text.split()
        return words
    
    @staticmethod
    def calculate_keyword_score(answer, keywords):
        """Calculate score based on keyword matching"""
        answer_words = set(AnswerEvaluator.preprocess_text(answer))
        keywords_lower = [k.lower() for k in keywords]
        
        matched_keywords = []
        for keyword in keywords_lower:
            keyword_words = keyword.split()
            # Check if all words in the keyword phrase are in the answer
            if all(word in answer_words for word in keyword_words):
                matched_keywords.append(keyword)
        
        # Calculate percentage match
        if len(keywords) == 0:
            return 0, []
        
        match_percentage = len(matched_keywords) / len(keywords)
        return match_percentage, matched_keywords
    
    @staticmethod
    def calculate_semantic_similarity(answer, keywords):
        """Calculate semantic similarity using cosine similarity"""
        answer_words = AnswerEvaluator.preprocess_text(answer)
        
        # Create word frequency vectors
        answer_counter = Counter(answer_words)
        keyword_counter = Counter()
        for keyword in keywords:
            keyword_words = AnswerEvaluator.preprocess_text(keyword)
            keyword_counter.update(keyword_words)
        
        # Get common words
        common_words = set(answer_counter.keys()) & set(keyword_counter.keys())
        
        if not common_words:
            return 0.0
        
        # Calculate dot product
        dot_product = sum(answer_counter[word] * keyword_counter[word] for word in common_words)
        
        # Calculate magnitudes
        answer_magnitude = math.sqrt(sum(count ** 2 for count in answer_counter.values()))
        keyword_magnitude = math.sqrt(sum(count ** 2 for count in keyword_counter.values()))
        
        if answer_magnitude == 0 or keyword_magnitude == 0:
            return 0.0
        
        # Cosine similarity
        similarity = dot_product / (answer_magnitude * keyword_magnitude)
        return similarity
    
    @staticmethod
    def calculate_length_score(answer, min_words=20, optimal_words=100):
        """Calculate score based on answer length"""
        words = AnswerEvaluator.preprocess_text(answer)
        word_count = len(words)
        
        if word_count < min_words:
            return word_count / min_words * 0.5  # Penalty for too short
        elif word_count > optimal_words * 2:
            return 0.7  # Slight penalty for being too verbose
        else:
            return min(1.0, word_count / optimal_words)
    
    @staticmethod
    def evaluate_answer(question, answer, keywords, difficulty='medium'):
        """
        Comprehensive answer evaluation
        Returns score out of 10 with detailed feedback
        """
        if not answer or len(answer.strip()) < 10:
            return {
                'score': 0,
                'feedback': {
                    'strengths': [],
                    'weaknesses': ['Answer is too short or empty'],
                    'suggestions': ['Provide a more detailed answer', 'Include relevant technical concepts']
                },
                'matched_keywords': [],
                'breakdown': {
                    'keyword_score': 0,
                    'semantic_score': 0,
                    'length_score': 0
                }
            }
        
        # Calculate individual scores
        keyword_match, matched_keywords = AnswerEvaluator.calculate_keyword_score(answer, keywords)
        semantic_score = AnswerEvaluator.calculate_semantic_similarity(answer, keywords)
        length_score = AnswerEvaluator.calculate_length_score(answer)
        
        # Weighted scoring based on difficulty
        difficulty_weights = {
            'easy': {'keyword': 0.5, 'semantic': 0.3, 'length': 0.2},
            'medium': {'keyword': 0.4, 'semantic': 0.4, 'length': 0.2},
            'hard': {'keyword': 0.3, 'semantic': 0.5, 'length': 0.2}
        }
        
        weights = difficulty_weights.get(difficulty, difficulty_weights['medium'])
        
        final_score = (
            keyword_match * weights['keyword'] * 10 +
            semantic_score * weights['semantic'] * 10 +
            length_score * weights['length'] * 10
        )
        
        # Generate feedback
        strengths = []
        weaknesses = []
        suggestions = []
        
        # Keyword analysis
        if keyword_match >= 0.7:
            strengths.append(f'Excellent coverage of key concepts ({len(matched_keywords)}/{len(keywords)} keywords)')
        elif keyword_match >= 0.4:
            strengths.append(f'Good understanding shown ({len(matched_keywords)}/{len(keywords)} keywords)')
        else:
            weaknesses.append(f'Limited coverage of key concepts ({len(matched_keywords)}/{len(keywords)} keywords)')
            suggestions.append('Include more relevant technical terms and concepts')
        
        # Semantic analysis
        if semantic_score >= 0.6:
            strengths.append('Strong contextual understanding')
        elif semantic_score < 0.3:
            weaknesses.append('Answer lacks depth and context')
            suggestions.append('Provide more detailed explanations with examples')
        
        # Length analysis
        word_count = len(AnswerEvaluator.preprocess_text(answer))
        if word_count < 20:
            weaknesses.append('Answer is too brief')
            suggestions.append('Expand your answer with more details')
        elif word_count > 200:
            suggestions.append('Consider being more concise while maintaining completeness')
        else:
            strengths.append('Well-structured answer with appropriate length')
        
        # Missing important keywords
        missing_keywords = set(keywords) - set(matched_keywords)
        if missing_keywords and len(missing_keywords) <= 3:
            suggestions.append(f'Consider mentioning: {", ".join(list(missing_keywords)[:3])}')
        
        return {
            'score': round(final_score, 2),
            'feedback': {
                'strengths': strengths if strengths else ['Keep learning and practicing'],
                'weaknesses': weaknesses if weaknesses else ['No major weaknesses detected'],
                'suggestions': suggestions if suggestions else ['Continue with the same approach']
            },
            'matched_keywords': matched_keywords,
            'breakdown': {
                'keyword_score': round(keyword_match * 10, 2),
                'semantic_score': round(semantic_score * 10, 2),
                'length_score': round(length_score * 10, 2),
                'word_count': word_count
            }
        }
    
    @staticmethod
    def evaluate_resume_answer(question, answer, question_type, resume_keywords):
        """Evaluate resume-based answer with alignment check"""
        # Extract keywords from question
        question_keywords = AnswerEvaluator.preprocess_text(question)
        
        # Combine with resume keywords for evaluation
        all_keywords = resume_keywords + question_keywords[:5]
        
        # Use standard evaluation
        result = AnswerEvaluator.evaluate_answer(question, answer, all_keywords)
        
        # Add resume alignment score
        resume_words = set(AnswerEvaluator.preprocess_text(' '.join(resume_keywords)))
        answer_words = set(AnswerEvaluator.preprocess_text(answer))
        
        alignment = len(resume_words & answer_words) / max(len(resume_words), 1)
        
        result['resume_alignment'] = round(alignment * 100, 2)
        
        if alignment > 0.3:
            result['feedback']['strengths'].append('Good alignment with your resume')
        else:
            result['feedback']['suggestions'].append('Try to relate your answer more to your resume')
        
        return result
    
    @staticmethod
    def evaluate_behavioral_answer(answer):
        """Evaluate behavioral interview answer"""
        word_count = len(AnswerEvaluator.preprocess_text(answer))
        
        # Communication score based on structure and clarity
        communication_score = 0
        
        # Check for structure indicators
        structure_words = ['first', 'second', 'then', 'finally', 'because', 'therefore', 'for example']
        has_structure = any(word in answer.lower() for word in structure_words)
        
        if has_structure:
            communication_score += 3
        
        # Check for personal examples
        personal_indicators = ['i ', 'my ', 'we ', 'our ', 'team']
        has_examples = any(indicator in answer.lower() for indicator in personal_indicators)
        
        if has_examples:
            communication_score += 2
        
        # Length appropriateness
        if 30 <= word_count <= 150:
            communication_score += 3
        elif 20 <= word_count < 30 or 150 < word_count <= 200:
            communication_score += 2
        elif word_count < 20:
            communication_score += 1
        
        # Confidence indicators (positive words)
        confidence_words = ['confident', 'successfully', 'achieved', 'led', 'improved', 'created']
        confidence_count = sum(1 for word in confidence_words if word in answer.lower())
        communication_score += min(2, confidence_count)
        
        return {
            'communication_score': min(10, communication_score),
            'word_count': word_count,
            'has_structure': has_structure,
            'has_examples': has_examples
        }