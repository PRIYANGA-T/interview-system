"""
Question Generation Routes
API endpoints for generating interview questions
"""

from flask import Blueprint, request, jsonify
from utils.question_generator import QuestionGenerator
from utils.aptitude_question_bank import APTITUDE_TOPICS, APTITUDE_QUESTION_BANK
from models.database import create_session, save_qa_record, update_session_score

bp = Blueprint('questions', __name__, url_prefix='/api/questions')

PYTHON_MCQ_QUESTIONS = [
    {
        'id': 1,
        'category': 'beginner',
        'question': 'Which keyword is used to define a function in Python?',
        'options': ['func', 'define', 'def', 'function'],
        'correct_option': 2
    },
    {
        'id': 2,
        'category': 'beginner',
        'question': 'What is the output of print(type(10))?',
        'options': ['<type int>', '<class int>', '<class \'int\'>', 'int'],
        'correct_option': 2
    },
    {
        'id': 3,
        'category': 'beginner',
        'question': 'Which data type is immutable in Python?',
        'options': ['list', 'dict', 'set', 'tuple'],
        'correct_option': 3
    },
    {
        'id': 4,
        'category': 'beginner',
        'question': 'Which operator is used for exponentiation in Python?',
        'options': ['^', '**', '%', '//'],
        'correct_option': 1
    },
    {
        'id': 5,
        'category': 'beginner',
        'question': 'What does len([1, 2, 3, 4]) return?',
        'options': ['3', '4', '5', 'Error'],
        'correct_option': 1
    },
    {
        'id': 6,
        'category': 'beginner',
        'question': 'Which statement is used to handle exceptions?',
        'options': ['catch/throw', 'try/except', 'do/except', 'handle/error'],
        'correct_option': 1
    },
    {
        'id': 7,
        'category': 'beginner',
        'question': 'Which function converts a string to an integer?',
        'options': ['str()', 'float()', 'int()', 'num()'],
        'correct_option': 2
    },
    {
        'id': 8,
        'category': 'beginner',
        'question': 'What is the result of 7 // 2 in Python?',
        'options': ['3', '3.5', '4', 'Error'],
        'correct_option': 0
    },
    {
        'id': 9,
        'category': 'beginner',
        'question': 'Which collection stores unique values only?',
        'options': ['list', 'tuple', 'set', 'dict'],
        'correct_option': 2
    },
    {
        'id': 10,
        'category': 'beginner',
        'question': 'How do you start a comment in Python?',
        'options': ['//', '#', '/*', '--'],
        'correct_option': 1
    },
    {
        'id': 11,
        'category': 'advanced',
        'question': 'What is the output type of a list comprehension?',
        'options': ['tuple', 'list', 'generator', 'set'],
        'correct_option': 1
    },
    {
        'id': 12,
        'category': 'advanced',
        'question': 'Which method is called when an object is created?',
        'options': ['__start__', '__create__', '__init__', '__newobj__'],
        'correct_option': 2
    },
    {
        'id': 13,
        'category': 'advanced',
        'question': 'What does @staticmethod mean?',
        'options': [
            'Method receives self automatically',
            'Method belongs to object instance only',
            'Method can be called without class/instance state',
            'Method is private'
        ],
        'correct_option': 2
    },
    {
        'id': 14,
        'category': 'advanced',
        'question': 'Which module is used for regular expressions?',
        'options': ['regex', 're', 'pyregex', 'expr'],
        'correct_option': 1
    },
    {
        'id': 15,
        'category': 'advanced',
        'question': 'What is returned by map(function, iterable) in Python 3?',
        'options': ['list', 'tuple', 'map object (iterator)', 'set'],
        'correct_option': 2
    },
    {
        'id': 16,
        'category': 'advanced',
        'question': 'Which of these is true about Python decorators?',
        'options': [
            'They can modify function behavior',
            'They only work with classes',
            'They require inheritance',
            'They cannot accept arguments'
        ],
        'correct_option': 0
    },
    {
        'id': 17,
        'category': 'advanced',
        'question': 'What does the with statement primarily help with?',
        'options': ['Loop optimization', 'Context management', 'Type checking', 'Thread control'],
        'correct_option': 1
    },
    {
        'id': 18,
        'category': 'advanced',
        'question': 'Which data type can be used as dictionary keys?',
        'options': ['list', 'set', 'dict', 'tuple'],
        'correct_option': 3
    },
    {
        'id': 19,
        'category': 'advanced',
        'question': 'What is the purpose of __name__ == "__main__"?',
        'options': [
            'To create main class',
            'To run code only when file is executed directly',
            'To import modules automatically',
            'To define package name'
        ],
        'correct_option': 1
    },
    {
        'id': 20,
        'category': 'advanced',
        'question': 'Which of these supports lazy evaluation?',
        'options': ['list', 'tuple', 'generator', 'dict'],
        'correct_option': 2
    },
    {
        'id': 21,
        'category': 'dsa',
        'question': 'Which data structure follows FIFO?',
        'options': ['Stack', 'Queue', 'Tree', 'Heap'],
        'correct_option': 1
    },
    {
        'id': 22,
        'category': 'dsa',
        'question': 'What is the average time complexity of dictionary lookup by key?',
        'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
        'correct_option': 0
    },
    {
        'id': 23,
        'category': 'dsa',
        'question': 'Which traversal of BST gives sorted output?',
        'options': ['Preorder', 'Postorder', 'Inorder', 'Level order'],
        'correct_option': 2
    },
    {
        'id': 24,
        'category': 'dsa',
        'question': 'What is the worst-case time complexity of binary search?',
        'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n^2)'],
        'correct_option': 1
    },
    {
        'id': 25,
        'category': 'dsa',
        'question': 'Which data structure is best for recursion call tracking?',
        'options': ['Queue', 'Stack', 'Graph', 'Hash table'],
        'correct_option': 1
    },
    {
        'id': 26,
        'category': 'dsa',
        'question': 'How many children can a binary tree node have at most?',
        'options': ['1', '2', '3', '4'],
        'correct_option': 1
    },
    {
        'id': 27,
        'category': 'dsa',
        'question': 'Which sorting algorithm is generally fastest on average for large random arrays?',
        'options': ['Bubble sort', 'Selection sort', 'Quick sort', 'Insertion sort'],
        'correct_option': 2
    },
    {
        'id': 28,
        'category': 'dsa',
        'question': 'What is the time complexity of appending to a Python list (amortized)?',
        'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
        'correct_option': 0
    },
    {
        'id': 29,
        'category': 'dsa',
        'question': 'Which algorithmic technique solves overlapping subproblems efficiently?',
        'options': ['Greedy', 'Divide and Conquer', 'Dynamic Programming', 'Backtracking'],
        'correct_option': 2
    },
    {
        'id': 30,
        'category': 'dsa',
        'question': 'In a min-heap, where is the smallest element located?',
        'options': ['Any leaf node', 'At the root', 'Middle level', 'Last node'],
        'correct_option': 1
    }
]

PYTHON_HARD_OUTPUT_QUESTIONS = [
    {
        'id': 1,
        'question': 'What is the output of the following code?',
        'code': 'a = [1, 2, 3]\nb = a\na += [4]\nprint(a, b)',
        'options': [
            '[1, 2, 3, 4] [1, 2, 3]',
            '[1, 2, 3, 4] [1, 2, 3, 4]',
            '[1, 2, 3] [1, 2, 3, 4]',
            'Error'
        ],
        'correct_option': 1,
        'explanation': 'Lists are mutable. `b = a` points to the same list object. `a += [4]` mutates that list in-place, so both references show the updated contents.'
    },
    {
        'id': 2,
        'question': 'What is the output of this function call?',
        'code': 'def f(x, lst=[]):\n    lst.append(x)\n    return lst\n\nprint(f(1))\nprint(f(2))',
        'options': [
            '[1] then [2]',
            '[1] then [1, 2]',
            '[1, 2] then [1, 2]',
            'Error'
        ],
        'correct_option': 1,
        'explanation': 'Default mutable arguments are created once at function definition time. The same `lst` is reused across calls, so second call appends to the same list.'
    },
    {
        'id': 3,
        'question': 'What is printed by this closure example?',
        'code': 'funcs = []\nfor i in range(3):\n    funcs.append(lambda: i)\n\nprint([f() for f in funcs])',
        'options': [
            '[0, 1, 2]',
            '[2, 2, 2]',
            '[3, 3, 3]',
            'Error'
        ],
        'correct_option': 2,
        'explanation': 'Lambdas close over variables by reference, not by value. After loop ends, `i` is 2 for all lambdas. Therefore each call returns 2.'
    },
    {
        'id': 4,
        'question': 'What is the output involving `is` and `==`?',
        'code': 'x = [1, 2]\ny = [1, 2]\nprint(x == y, x is y)',
        'options': [
            'True True',
            'False False',
            'True False',
            'False True'
        ],
        'correct_option': 2,
        'explanation': '`==` compares values, and both lists contain same values so it is True. `is` compares object identity, and these are two different list objects, so False.'
    },
    {
        'id': 5,
        'question': 'What is the output of this generator expression code?',
        'code': 'g = (x * x for x in range(4))\nprint(next(g))\nprint(list(g))',
        'options': [
            '0 then [0, 1, 4, 9]',
            '0 then [1, 4, 9]',
            '1 then [4, 9]',
            'Error'
        ],
        'correct_option': 1,
        'explanation': 'Generators are consumed lazily. `next(g)` consumes first value (0). Remaining values are produced when converting to list, giving [1, 4, 9].'
    }
]


@bp.route('/python-mcq', methods=['GET'])
def get_python_mcq_questions():
    """Get fixed Python MCQ assessment (30 questions)"""
    try:
        session_id = create_session('python_mcq', 'Python')

        public_questions = [
            {
                'id': item['id'],
                'number': item['id'],
                'category': item['category'],
                'question': item['question'],
                'options': item['options']
            }
            for item in PYTHON_MCQ_QUESTIONS
        ]

        return jsonify({
            'session_id': session_id,
            'total_questions': len(public_questions),
            'questions': public_questions,
            'distribution': {
                'beginner': 10,
                'advanced': 10,
                'dsa': 10
            }
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/python-mcq/evaluate', methods=['POST'])
def evaluate_python_mcq():
    """Evaluate submitted Python MCQ responses and return total score"""
    try:
        data = request.json or {}
        session_id = data.get('session_id')
        answers = data.get('answers', [])

        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400

        if not isinstance(answers, list):
            return jsonify({'error': 'answers must be a list'}), 400

        answers_map = {}
        for item in answers:
            if isinstance(item, dict) and 'question_id' in item:
                answers_map[item['question_id']] = item.get('selected_option')

        section_totals = {
            'beginner': {'correct': 0, 'total': 10},
            'advanced': {'correct': 0, 'total': 10},
            'dsa': {'correct': 0, 'total': 10}
        }

        review = []
        total_correct = 0

        for question in PYTHON_MCQ_QUESTIONS:
            selected_option = answers_map.get(question['id'])
            selected_text = (
                question['options'][selected_option]
                if isinstance(selected_option, int) and 0 <= selected_option < len(question['options'])
                else 'Not Answered'
            )

            is_correct = selected_option == question['correct_option']
            if is_correct:
                total_correct += 1
                section_totals[question['category']]['correct'] += 1

            qa_question_text = (
                f"Q{question['id']}: {question['question']}\n"
                + "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(question['options'])])
            )
            feedback_payload = {
                'category': question['category'],
                'is_correct': is_correct,
                'correct_answer': question['options'][question['correct_option']]
            }

            save_qa_record(
                session_id,
                qa_question_text,
                selected_text,
                10 if is_correct else 0,
                feedback_payload,
                []
            )

            review.append({
                'question_id': question['id'],
                'category': question['category'],
                'question': question['question'],
                'selected_option': selected_option,
                'selected_text': selected_text,
                'correct_option': question['correct_option'],
                'correct_text': question['options'][question['correct_option']],
                'is_correct': is_correct
            })

        total_questions = len(PYTHON_MCQ_QUESTIONS)
        score_out_of_30 = total_correct
        percentage = round((total_correct / total_questions) * 100, 2)
        normalized_score = round((total_correct / total_questions) * 10, 2)

        update_session_score(session_id, normalized_score, 'completed')

        return jsonify({
            'session_id': session_id,
            'total_correct': total_correct,
            'total_questions': total_questions,
            'score_out_of_30': score_out_of_30,
            'percentage': percentage,
            'normalized_score': normalized_score,
            'section_scores': section_totals,
            'review': review,
            'status': 'completed'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/python-hard-output', methods=['GET'])
def get_python_hard_output_questions():
    """Get separate hard Python code-output MCQ set (5 questions)"""
    try:
        session_id = create_session('python_hard_output', 'Python')

        public_questions = [
            {
                'id': item['id'],
                'question': item['question'],
                'code': item['code'],
                'options': item['options']
            }
            for item in PYTHON_HARD_OUTPUT_QUESTIONS
        ]

        return jsonify({
            'session_id': session_id,
            'total_questions': len(public_questions),
            'questions': public_questions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/python-hard-output/evaluate', methods=['POST'])
def evaluate_python_hard_output():
    """Evaluate hard code-output Python MCQs and return explanations"""
    try:
        data = request.json or {}
        session_id = data.get('session_id')
        answers = data.get('answers', [])

        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400

        if not isinstance(answers, list):
            return jsonify({'error': 'answers must be a list'}), 400

        answers_map = {}
        for item in answers:
            if isinstance(item, dict) and 'question_id' in item:
                answers_map[item['question_id']] = item.get('selected_option')

        total_correct = 0
        review = []

        for question in PYTHON_HARD_OUTPUT_QUESTIONS:
            selected_option = answers_map.get(question['id'])
            selected_text = (
                question['options'][selected_option]
                if isinstance(selected_option, int) and 0 <= selected_option < len(question['options'])
                else 'Not Answered'
            )

            is_correct = selected_option == question['correct_option']
            if is_correct:
                total_correct += 1

            qa_question_text = f"{question['question']}\n\n{question['code']}"
            feedback_payload = {
                'is_correct': is_correct,
                'correct_answer': question['options'][question['correct_option']],
                'explanation': question['explanation']
            }

            save_qa_record(
                session_id,
                qa_question_text,
                selected_text,
                10 if is_correct else 0,
                feedback_payload,
                []
            )

            review.append({
                'question_id': question['id'],
                'question': question['question'],
                'code': question['code'],
                'selected_option': selected_option,
                'selected_text': selected_text,
                'correct_option': question['correct_option'],
                'correct_text': question['options'][question['correct_option']],
                'is_correct': is_correct,
                'explanation': question['explanation']
            })

        total_questions = len(PYTHON_HARD_OUTPUT_QUESTIONS)
        percentage = round((total_correct / total_questions) * 100, 2)
        normalized_score = round((total_correct / total_questions) * 10, 2)

        update_session_score(session_id, normalized_score, 'completed')

        return jsonify({
            'session_id': session_id,
            'total_correct': total_correct,
            'total_questions': total_questions,
            'score_out_of_5': total_correct,
            'percentage': percentage,
            'normalized_score': normalized_score,
            'review': review,
            'status': 'completed'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/aptitude/topics', methods=['GET'])
def get_aptitude_topics():
    """Get available aptitude topics"""
    try:
        return jsonify({
            'topics': APTITUDE_TOPICS,
            'questions_per_topic': 10,
            'difficulty': 'intermediate_to_advanced'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/aptitude/<string:topic_id>', methods=['GET'])
def get_aptitude_questions(topic_id):
    """Start aptitude topic test and return 10 MCQs"""
    try:
        if topic_id not in APTITUDE_QUESTION_BANK:
            return jsonify({'error': 'Invalid aptitude topic'}), 400

        topic = next((item for item in APTITUDE_TOPICS if item['id'] == topic_id), None)
        topic_title = topic['title'] if topic else topic_id

        session_id = create_session('aptitude_mcq', topic_title)
        question_set = APTITUDE_QUESTION_BANK[topic_id]

        public_questions = [
            {
                'id': item['id'],
                'question': item['question'],
                'options': item['options'],
                'hint': item['hint']
            }
            for item in question_set
        ]

        return jsonify({
            'session_id': session_id,
            'topic_id': topic_id,
            'topic_title': topic_title,
            'total_questions': len(public_questions),
            'questions': public_questions
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/aptitude/evaluate', methods=['POST'])
def evaluate_aptitude_topic():
    """Evaluate aptitude topic MCQ answers and return score"""
    try:
        data = request.json or {}
        session_id = data.get('session_id')
        topic_id = data.get('topic_id')
        answers = data.get('answers', [])

        if not session_id:
            return jsonify({'error': 'session_id is required'}), 400

        if not topic_id or topic_id not in APTITUDE_QUESTION_BANK:
            return jsonify({'error': 'Valid topic_id is required'}), 400

        if not isinstance(answers, list):
            return jsonify({'error': 'answers must be a list'}), 400

        answers_map = {}
        for item in answers:
            if isinstance(item, dict) and 'question_id' in item:
                answers_map[item['question_id']] = item.get('selected_option')

        question_set = APTITUDE_QUESTION_BANK[topic_id]
        total_correct = 0
        review = []

        for question in question_set:
            selected_option = answers_map.get(question['id'])
            selected_text = (
                question['options'][selected_option]
                if isinstance(selected_option, int) and 0 <= selected_option < len(question['options'])
                else 'Not Answered'
            )

            is_correct = selected_option == question['correct_option']
            if is_correct:
                total_correct += 1

            qa_question_text = (
                f"Q{question['id']}: {question['question']}\n"
                + "\n".join([f"{idx + 1}. {option}" for idx, option in enumerate(question['options'])])
                + f"\nHint: {question['hint']}"
            )
            feedback_payload = {
                'topic_id': topic_id,
                'is_correct': is_correct,
                'correct_answer': question['options'][question['correct_option']],
                'hint': question['hint']
            }

            save_qa_record(
                session_id,
                qa_question_text,
                selected_text,
                10 if is_correct else 0,
                feedback_payload,
                []
            )

            review.append({
                'question_id': question['id'],
                'question': question['question'],
                'hint': question['hint'],
                'selected_option': selected_option,
                'selected_text': selected_text,
                'correct_option': question['correct_option'],
                'correct_text': question['options'][question['correct_option']],
                'is_correct': is_correct
            })

        total_questions = len(question_set)
        percentage = round((total_correct / total_questions) * 100, 2)
        normalized_score = round((total_correct / total_questions) * 10, 2)

        update_session_score(session_id, normalized_score, 'completed')

        return jsonify({
            'session_id': session_id,
            'topic_id': topic_id,
            'total_correct': total_correct,
            'total_questions': total_questions,
            'score_out_of_10': total_correct,
            'percentage': percentage,
            'normalized_score': normalized_score,
            'review': review,
            'status': 'completed'
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/domain', methods=['POST'])
def generate_domain_questions():
    """Generate questions for a specific domain"""
    try:
        data = request.json
        domain = data.get('domain')
        num_questions = data.get('num_questions', 5)
        adaptive_mode = data.get('adaptive_mode', False)
        
        if not domain:
            return jsonify({'error': 'Domain is required'}), 400
        
        # Generate questions
        if adaptive_mode:
            adaptive_result = QuestionGenerator.generate_adaptive_domain_question(
                domain=domain,
                target_difficulty='medium',
                exclude_questions=[]
            )

            if 'error' in adaptive_result:
                return jsonify(adaptive_result), 400

            result = {
                'domain': domain,
                'questions': [adaptive_result['question']],
                'total': num_questions,
                'adaptive_mode': True,
                'target_difficulty': adaptive_result['target_difficulty'],
                'selected_difficulty': adaptive_result['selected_difficulty']
            }
        else:
            result = QuestionGenerator.generate_domain_questions(domain, num_questions)
        
        if 'error' in result:
            return jsonify(result), 400
        
        # Create session
        session_id = create_session('domain', domain)
        result['session_id'] = session_id
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/domain/adaptive-next', methods=['POST'])
def get_adaptive_next_domain_question():
    """Get next adaptive question for domain interview"""
    try:
        data = request.json
        domain = data.get('domain')
        target_difficulty = data.get('target_difficulty', 'medium')
        asked_questions = data.get('asked_questions', [])

        if not domain:
            return jsonify({'error': 'Domain is required'}), 400

        result = QuestionGenerator.generate_adaptive_domain_question(
            domain=domain,
            target_difficulty=target_difficulty,
            exclude_questions=asked_questions
        )

        if 'error' in result:
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/behavioral', methods=['GET'])
def get_behavioral_questions():
    """Get behavioral interview questions"""
    try:
        result = QuestionGenerator.get_behavioral_questions()
        
        # Create session
        session_id = create_session('behavioral')
        result['session_id'] = session_id
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500