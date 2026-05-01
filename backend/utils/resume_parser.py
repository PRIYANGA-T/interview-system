"""
Resume Parser
Extracts skills, education, and projects from PDF resumes
"""

import re
import PyPDF2
from pathlib import Path

class ResumeParser:
    """Parse resume and extract relevant information"""
    
    # Common skill keywords to look for
    SKILL_KEYWORDS = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'php', 'swift', 'kotlin',
        'go', 'rust', 'scala', 'r', 'matlab', 'sql', 'html', 'css',
        
        # Frameworks & Libraries
        'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'spring', 'fastapi',
        '.net', 'asp.net', 'laravel', 'rails', 'jquery', 'bootstrap', 'tailwind',
        
        # Databases
        'mysql', 'postgresql', 'mongodb', 'redis', 'oracle', 'sql server', 'dynamodb', 'cassandra',
        'elasticsearch', 'firebase',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
        'ci/cd', 'terraform', 'ansible',
        
        # AI/ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'keras', 'scikit-learn',
        'nlp', 'computer vision', 'opencv', 'pandas', 'numpy',
        
        # Other
        'rest api', 'graphql', 'microservices', 'agile', 'scrum', 'linux', 'unix'
    ]
    
    EDUCATION_KEYWORDS = [
        'bachelor', 'master', 'phd', 'b.tech', 'm.tech', 'b.e', 'm.e', 'bca', 'mca',
        'computer science', 'information technology', 'software engineering',
        'university', 'college', 'institute', 'degree', 'diploma'
    ]
    
    PROJECT_INDICATORS = [
        'project', 'developed', 'built', 'created', 'implemented', 'designed',
        'application', 'system', 'platform', 'website', 'app'
    ]
    
    @staticmethod
    def extract_text_from_pdf(pdf_path):
        """Extract text content from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"
    
    @staticmethod
    def extract_skills(text):
        """Extract skills from resume text"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in ResumeParser.SKILL_KEYWORDS:
            # Use word boundary to avoid partial matches
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        # Remove duplicates and return
        return list(set(found_skills))
    
    @staticmethod
    def extract_education(text):
        """Extract education information from resume text"""
        text_lower = text.lower()
        education_info = []
        
        # Split into lines for better parsing
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if line contains education keywords
            for keyword in ResumeParser.EDUCATION_KEYWORDS:
                if keyword in line_lower:
                    # Get context (current line and next 2 lines)
                    context = ' '.join(lines[i:min(i+3, len(lines))])
                    
                    # Extract degree and institution
                    degree_match = re.search(r'(bachelor|master|phd|b\.tech|m\.tech|b\.e|m\.e|bca|mca)[^,\n]*', 
                                           context, re.IGNORECASE)
                    if degree_match:
                        education_info.append(degree_match.group(0).strip())
                    break
        
        # Remove duplicates
        education_info = list(set(education_info))
        
        if not education_info:
            # Fallback: look for years that might indicate education
            year_pattern = r'(19|20)\d{2}\s*-\s*(19|20)\d{2}|(\d{4})\s*-\s*present'
            years = re.findall(year_pattern, text, re.IGNORECASE)
            if years:
                education_info.append("Education details found (see resume for specifics)")
        
        return education_info[:3]  # Return top 3
    
    @staticmethod
    def extract_projects(text):
        """Extract project information from resume text"""
        projects = []
        lines = text.split('\n')
        
        current_project = None
        
        for i, line in enumerate(lines):
            line_lower = line.lower()
            
            # Check if line mentions project
            if any(indicator in line_lower for indicator in ResumeParser.PROJECT_INDICATORS):
                # Check if it's a project title (usually short and might have dates)
                if len(line.split()) < 15 and len(line.strip()) > 5:
                    # Clean the line
                    project_name = re.sub(r'\d{4}\s*-\s*\d{4}|\d{4}\s*-\s*present', '', line).strip()
                    project_name = re.sub(r'[•\-\*]', '', project_name).strip()
                    
                    if project_name and len(project_name) > 5:
                        projects.append(project_name)
        
        # Remove duplicates and limit to top 5
        projects = list(set(projects))[:5]
        
        if not projects:
            # Fallback: extract sentences mentioning development work
            sentences = text.split('.')
            for sentence in sentences:
                if any(word in sentence.lower() for word in ['developed', 'built', 'created', 'implemented']):
                    if 10 < len(sentence.split()) < 25:
                        projects.append(sentence.strip())
                        if len(projects) >= 3:
                            break
        
        return projects
    
    @staticmethod
    def parse_resume(pdf_path):
        """
        Main function to parse resume and extract all information
        """
        # Extract text
        text = ResumeParser.extract_text_from_pdf(pdf_path)
        
        if text.startswith("Error"):
            return {
                'error': text,
                'skills': [],
                'education': [],
                'projects': []
            }
        
        # Extract components
        skills = ResumeParser.extract_skills(text)
        education = ResumeParser.extract_education(text)
        projects = ResumeParser.extract_projects(text)
        
        return {
            'skills': skills,
            'education': education,
            'projects': projects,
            'text_length': len(text),
            'success': True
        }
    
    @staticmethod
    def get_resume_keywords(parsed_data):
        """Get combined keywords from parsed resume for evaluation"""
        keywords = []
        
        # Add skills
        keywords.extend(parsed_data.get('skills', []))
        
        # Add education keywords
        for edu in parsed_data.get('education', []):
            keywords.extend(edu.lower().split())
        
        # Add project keywords
        for proj in parsed_data.get('projects', []):
            keywords.extend(proj.lower().split()[:3])  # First 3 words of each project
        
        return list(set(keywords))[:20]  # Return top 20 unique keywords