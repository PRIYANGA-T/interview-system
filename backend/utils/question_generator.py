"""
AI Question Generator
Generates domain-specific and resume-based interview questions
"""

import random
import re

class QuestionGenerator:
    """Generate interview questions based on domain or resume"""

    DIFFICULTY_ORDER = ['easy', 'medium', 'hard']
    
    # Domain-specific question banks
    QUESTION_BANK = {
        'Frontend': [
            {
                'question': 'Explain the difference between var, let, and const in JavaScript.',
                'keywords': ['var', 'let', 'const', 'scope', 'hoisting', 'block', 'function', 'reassignment'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is the Virtual DOM in React and how does it improve performance?',
                'keywords': ['virtual dom', 'react', 'performance', 'reconciliation', 'diffing', 'rendering', 'real dom'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain CSS Flexbox and its main properties.',
                'keywords': ['flexbox', 'flex', 'justify-content', 'align-items', 'flex-direction', 'layout', 'responsive'],
                'difficulty': 'easy'
            },
            {
                'question': 'What are HTTP methods? Explain GET, POST, PUT, and DELETE.',
                'keywords': ['http', 'get', 'post', 'put', 'delete', 'rest', 'api', 'crud'],
                'difficulty': 'easy'
            },
            {
                'question': 'Explain event bubbling and event capturing in JavaScript.',
                'keywords': ['event', 'bubbling', 'capturing', 'propagation', 'dom', 'event listener', 'parent', 'child'],
                'difficulty': 'hard'
            }
        ],
        'Backend': [
            {
                'question': 'Explain the difference between SQL and NoSQL databases.',
                'keywords': ['sql', 'nosql', 'relational', 'schema', 'scalability', 'acid', 'base', 'mongodb', 'mysql'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is REST API? Explain its principles and constraints.',
                'keywords': ['rest', 'api', 'stateless', 'http', 'resources', 'uniform interface', 'client-server'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain authentication vs authorization with examples.',
                'keywords': ['authentication', 'authorization', 'jwt', 'token', 'session', 'oauth', 'security', 'login'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is middleware in Express.js/Flask and how does it work?',
                'keywords': ['middleware', 'express', 'flask', 'request', 'response', 'pipeline', 'next', 'decorator'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain database indexing and its importance.',
                'keywords': ['index', 'indexing', 'performance', 'query', 'optimization', 'b-tree', 'primary key', 'foreign key'],
                'difficulty': 'hard'
            }
        ],
        'Python': [
            {
                'question': 'Explain the difference between list, tuple, set, and dictionary in Python.',
                'keywords': ['list', 'tuple', 'set', 'dictionary', 'mutable', 'immutable', 'ordered', 'unordered'],
                'difficulty': 'easy'
            },
            {
                'question': 'What are decorators in Python? Provide an example.',
                'keywords': ['decorator', 'function', 'wrapper', '@', 'higher order', 'closure', 'syntax'],
                'difficulty': 'hard'
            },
            {
                'question': 'Explain list comprehension and its advantages.',
                'keywords': ['list comprehension', 'comprehension', 'loop', 'concise', 'readable', 'performance'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is the difference between deep copy and shallow copy?',
                'keywords': ['deep copy', 'shallow copy', 'copy', 'reference', 'nested', 'objects', 'memory'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain generators and yield keyword in Python.',
                'keywords': ['generator', 'yield', 'iterator', 'memory', 'lazy evaluation', 'next', 'performance'],
                'difficulty': 'hard'
            }
        ],
        'AI/ML': [
            {
                'question': 'Explain the difference between supervised and unsupervised learning.',
                'keywords': ['supervised', 'unsupervised', 'labeled', 'unlabeled', 'classification', 'clustering', 'training'],
                'difficulty': 'easy'
            },
            {
                'question': 'What is overfitting and how can you prevent it?',
                'keywords': ['overfitting', 'generalization', 'regularization', 'dropout', 'validation', 'cross-validation', 'bias-variance'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain the working of a neural network.',
                'keywords': ['neural network', 'layers', 'neurons', 'weights', 'bias', 'activation', 'backpropagation', 'forward pass'],
                'difficulty': 'hard'
            },
            {
                'question': 'What is the difference between precision and recall?',
                'keywords': ['precision', 'recall', 'true positive', 'false positive', 'false negative', 'f1-score', 'confusion matrix'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain gradient descent and its variants.',
                'keywords': ['gradient descent', 'optimization', 'learning rate', 'batch', 'stochastic', 'mini-batch', 'convergence'],
                'difficulty': 'hard'
            }
        ],
        'DBMS': [
            {
                'question': 'Explain ACID properties in database transactions.',
                'keywords': ['acid', 'atomicity', 'consistency', 'isolation', 'durability', 'transaction', 'commit', 'rollback'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is database normalization? Explain 1NF, 2NF, and 3NF.',
                'keywords': ['normalization', '1nf', '2nf', '3nf', 'redundancy', 'dependency', 'primary key', 'functional'],
                'difficulty': 'hard'
            },
            {
                'question': 'Explain different types of JOINs in SQL.',
                'keywords': ['join', 'inner join', 'left join', 'right join', 'full outer join', 'cross join', 'tables'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is a primary key and foreign key?',
                'keywords': ['primary key', 'foreign key', 'unique', 'constraint', 'relationship', 'referential integrity'],
                'difficulty': 'easy'
            },
            {
                'question': 'Explain the difference between DELETE, TRUNCATE, and DROP.',
                'keywords': ['delete', 'truncate', 'drop', 'rollback', 'ddl', 'dml', 'table', 'transaction'],
                'difficulty': 'medium'
            }
        ],
        'Cloud': [
            {
                'question': 'Explain the difference between IaaS, PaaS, and SaaS.',
                'keywords': ['iaas', 'paas', 'saas', 'infrastructure', 'platform', 'software', 'service', 'cloud'],
                'difficulty': 'easy'
            },
            {
                'question': 'What is Docker and how does it differ from virtual machines?',
                'keywords': ['docker', 'container', 'virtual machine', 'vm', 'image', 'lightweight', 'isolation', 'kernel'],
                'difficulty': 'medium'
            },
            {
                'question': 'Explain horizontal vs vertical scaling.',
                'keywords': ['horizontal', 'vertical', 'scaling', 'load balancing', 'resources', 'capacity', 'performance'],
                'difficulty': 'medium'
            },
            {
                'question': 'What is Kubernetes and why is it used?',
                'keywords': ['kubernetes', 'orchestration', 'containers', 'deployment', 'pods', 'clusters', 'scaling', 'management'],
                'difficulty': 'hard'
            },
            {
                'question': 'Explain the concept of microservices architecture.',
                'keywords': ['microservices', 'architecture', 'monolith', 'distributed', 'independent', 'services', 'api', 'scalability'],
                'difficulty': 'hard'
            }
        ]
    }
    
    # Behavioral questions
    BEHAVIORAL_QUESTIONS = [
        "Introduce yourself and tell me about your background.",
        "Why should I hire you? What makes you the best candidate?",
        "Where do you see yourself after 5 years?",
        "Why did you choose this company? What interests you about us?",
        "Why did you choose this degree? What motivated your educational path?"
    ]
    
    @classmethod
    def generate_domain_questions(cls, domain, num_questions=5):
        """Generate questions for a specific domain"""
        if domain not in cls.QUESTION_BANK:
            return {'error': f'Domain {domain} not supported'}
        
        questions = cls.QUESTION_BANK[domain]
        selected = random.sample(questions, min(num_questions, len(questions)))
        
        return {
            'domain': domain,
            'questions': selected,
            'total': len(selected)
        }

    @classmethod
    def generate_adaptive_domain_question(cls, domain, target_difficulty='medium', exclude_questions=None):
        """Generate one adaptive domain question based on target difficulty"""
        if domain not in cls.QUESTION_BANK:
            return {'error': f'Domain {domain} not supported'}

        exclude_questions = set(exclude_questions or [])
        all_questions = cls.QUESTION_BANK[domain]

        remaining_questions = [q for q in all_questions if q['question'] not in exclude_questions]
        if not remaining_questions:
            return {'error': 'No more questions available for this domain'}

        target = target_difficulty if target_difficulty in cls.DIFFICULTY_ORDER else 'medium'

        # Try exact difficulty first
        exact_pool = [q for q in remaining_questions if q.get('difficulty') == target]
        if exact_pool:
            selected_question = random.choice(exact_pool)
            return {
                'domain': domain,
                'question': selected_question,
                'target_difficulty': target,
                'selected_difficulty': selected_question.get('difficulty', 'medium')
            }

        # Fallback to nearest difficulty by order distance
        target_index = cls.DIFFICULTY_ORDER.index(target)
        sorted_pool = sorted(
            remaining_questions,
            key=lambda q: abs(cls.DIFFICULTY_ORDER.index(q.get('difficulty', 'medium')) - target_index)
        )

        selected_question = sorted_pool[0]
        return {
            'domain': domain,
            'question': selected_question,
            'target_difficulty': target,
            'selected_difficulty': selected_question.get('difficulty', 'medium')
        }
    
    @classmethod
    def generate_resume_questions(cls, skills, education, projects, num_questions=5):
        """Generate personalized questions based on resume"""
        questions = []
        
        # Skill-based questions
        for skill in skills[:3]:
            skill_lower = skill.lower()
            if 'python' in skill_lower:
                questions.append({
                    'question': f'You mentioned {skill} in your resume. Can you explain your experience with Python decorators?',
                    'keywords': ['decorator', 'python', 'function', 'wrapper', 'experience'],
                    'type': 'skill'
                })
            elif 'react' in skill_lower or 'javascript' in skill_lower:
                questions.append({
                    'question': f'You have {skill} listed. Explain how you would optimize a React application for better performance.',
                    'keywords': ['react', 'performance', 'optimization', 'virtual dom', 'memo', 'usememo'],
                    'type': 'skill'
                })
            elif 'ml' in skill_lower or 'machine learning' in skill_lower:
                questions.append({
                    'question': f'Given your {skill} background, explain a machine learning project you worked on and the challenges faced.',
                    'keywords': ['machine learning', 'project', 'model', 'training', 'data', 'challenges'],
                    'type': 'skill'
                })
            elif 'sql' in skill_lower or 'database' in skill_lower:
                questions.append({
                    'question': f'With your {skill} expertise, how would you optimize a slow database query?',
                    'keywords': ['query', 'optimization', 'index', 'explain', 'performance', 'database'],
                    'type': 'skill'
                })
            else:
                questions.append({
                    'question': f'Describe a challenging problem you solved using {skill}.',
                    'keywords': [skill.lower(), 'problem', 'solution', 'challenge', 'experience'],
                    'type': 'skill'
                })
        
        # Project-based questions
        for project in projects[:2]:
            questions.append({
                'question': f'Tell me about your {project} project. What was your role and what technologies did you use?',
                'keywords': ['project', 'role', 'technology', 'implementation', 'team', 'responsibility'],
                'type': 'project'
            })
        
        # Education-based question
        if education:
            questions.append({
                'question': f'How has your {education[0] if education else "education"} helped you in practical software development?',
                'keywords': ['education', 'learning', 'practical', 'application', 'knowledge', 'skills'],
                'type': 'education'
            })
        
        # General technical question
        questions.append({
            'question': 'Explain a situation where you had to learn a new technology quickly. How did you approach it?',
            'keywords': ['learn', 'new technology', 'approach', 'quickly', 'adapt', 'self-learning'],
            'type': 'general'
        })
        
        return {
            'questions': questions[:num_questions],
            'total': len(questions[:num_questions]),
            'resume_based': True
        }
    
    @classmethod
    def get_behavioral_questions(cls):
        """Get behavioral interview questions"""
        return {
            'questions': cls.BEHAVIORAL_QUESTIONS,
            'total': len(cls.BEHAVIORAL_QUESTIONS)
        }