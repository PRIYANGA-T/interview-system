"""
PDF Report Generator
Generates detailed interview feedback reports
"""

import json
from io import BytesIO
from collections import Counter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, ListFlowable, ListItem


class ReportGenerator:
    """Generate detailed PDF feedback reports for interview sessions"""

    @staticmethod
    def _safe_json_loads(raw_value, default):
        if raw_value is None:
            return default
        if isinstance(raw_value, (dict, list)):
            return raw_value
        try:
            return json.loads(raw_value)
        except (json.JSONDecodeError, TypeError):
            return default

    @staticmethod
    def _normalize_session_results(results):
        qa_records = []
        for row in results.get('qa_records', []):
            feedback = ReportGenerator._safe_json_loads(row.get('feedback'), {})
            matched_keywords = ReportGenerator._safe_json_loads(row.get('keywords_matched'), [])
            qa_records.append({
                **row,
                'feedback': feedback,
                'keywords_matched': matched_keywords
            })

        behavioral_records = results.get('behavioral_records', [])
        emotion_timeline = results.get('emotion_timeline', [])
        session = results.get('session') or {}

        return session, qa_records, behavioral_records, emotion_timeline

    @staticmethod
    def _build_overview(session, qa_records, behavioral_records):
        score = session.get('total_score')
        total_questions = len(qa_records) if qa_records else len(behavioral_records)

        avg_communication = None
        avg_confidence = None
        if behavioral_records:
            avg_communication = sum(float(r.get('communication_score', 0) or 0) for r in behavioral_records) / len(behavioral_records)
            avg_confidence = sum(float(r.get('confidence_score', 0) or 0) for r in behavioral_records) / len(behavioral_records)

        return {
            'score': round(float(score), 2) if score is not None else 0,
            'total_questions': total_questions,
            'avg_communication': round(avg_communication, 2) if avg_communication is not None else None,
            'avg_confidence': round(avg_confidence, 2) if avg_confidence is not None else None
        }

    @staticmethod
    def _collect_feedback_points(qa_records, behavioral_records):
        strengths = []
        mistakes = []

        for row in qa_records:
            feedback = row.get('feedback', {})
            strengths.extend(feedback.get('strengths', []))
            mistakes.extend(feedback.get('weaknesses', []))

        if behavioral_records:
            communication_scores = [float(r.get('communication_score', 0) or 0) for r in behavioral_records]
            confidence_scores = [float(r.get('confidence_score', 0) or 0) for r in behavioral_records]

            avg_comm = sum(communication_scores) / len(communication_scores)
            avg_conf = sum(confidence_scores) / len(confidence_scores)

            if avg_comm >= 7:
                strengths.append('Strong communication clarity in behavioral answers')
            else:
                mistakes.append('Behavioral answers need clearer structure and storytelling')

            if avg_conf >= 7:
                strengths.append('Confident delivery maintained through interview')
            else:
                mistakes.append('Confidence signals can be improved with more practice')

        if not strengths:
            strengths.append('Consistent participation and attempt across questions')
        if not mistakes:
            mistakes.append('No major recurring mistakes detected')

        strength_counter = Counter(strengths)
        mistake_counter = Counter(mistakes)

        top_strengths = [item for item, _ in strength_counter.most_common(5)]
        top_mistakes = [item for item, _ in mistake_counter.most_common(5)]

        return top_strengths, top_mistakes

    @staticmethod
    def _generate_model_answer(question, session_type, matched_keywords):
        keywords = matched_keywords[:4] if matched_keywords else []
        keyword_line = f"Include terms like: {', '.join(keywords)}." if keywords else "Include relevant domain terms and one concrete example."

        if session_type == 'behavioral':
            return (
                "Use STAR format: Situation (set context), Task (your responsibility), "
                "Action (specific steps you took), and Result (measurable impact). "
                "Keep the answer concise, confident, and reflective of what you learned."
            )

        return (
            "Start with a clear definition or high-level approach, then explain your implementation "
            "or thought process step by step, and end with trade-offs or outcomes. "
            f"{keyword_line}"
        )

    @staticmethod
    def _build_next_step_plan(session_type, overview, mistakes):
        score = overview.get('score', 0)
        plan = []

        if score < 5:
            plan.append('Spend 30 minutes daily revising fundamentals and common interview patterns.')
            plan.append('Practice answering 5 questions/day with a timer and self-review each response.')
        elif score < 7.5:
            plan.append('Focus on depth: add examples, trade-offs, and measurable outcomes in each answer.')
            plan.append('Run 2 mock interviews per week and compare score trends by topic.')
        else:
            plan.append('Maintain performance with weekly mock interviews and targeted advanced questions.')
            plan.append('Refine concise delivery and clarity to convert strong answers into standout answers.')

        if session_type == 'behavioral':
            plan.append('Use STAR structure in every behavioral response and emphasize impact metrics.')

        common_issues = [m for m in mistakes if m and 'No major recurring mistakes' not in m][:2]
        for issue in common_issues:
            plan.append(f'Address this recurring issue: {issue}')

        return plan[:6]

    @staticmethod
    def generate_session_report(results):
        """Generate detailed PDF report for an interview session"""
        session, qa_records, behavioral_records, emotion_timeline = ReportGenerator._normalize_session_results(results)
        overview = ReportGenerator._build_overview(session, qa_records, behavioral_records)
        strengths, mistakes = ReportGenerator._collect_feedback_points(qa_records, behavioral_records)
        next_steps = ReportGenerator._build_next_step_plan(session.get('session_type', 'general'), overview, mistakes)

        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            leftMargin=0.7 * inch,
            rightMargin=0.7 * inch,
            topMargin=0.7 * inch,
            bottomMargin=0.7 * inch
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=10,
            textColor=colors.HexColor('#1f2937')
        )
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=13,
            spaceBefore=10,
            spaceAfter=6,
            textColor=colors.HexColor('#111827')
        )

        content = []

        content.append(Paragraph('Interview Feedback Report', title_style))
        content.append(Paragraph('Generated by AI Interview Evaluation System', styles['Normal']))
        content.append(Spacer(1, 8))

        meta_table_data = [
            ['Session ID', str(session.get('id', '-'))],
            ['Session Type', str(session.get('session_type', 'general')).title()],
            ['Domain', str(session.get('domain') or 'N/A')],
            ['Created At', str(session.get('created_at', 'N/A'))],
            ['Status', str(session.get('status', 'completed')).title()]
        ]
        meta_table = Table(meta_table_data, colWidths=[1.6 * inch, 4.8 * inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 6)
        ]))
        content.append(meta_table)

        content.append(Paragraph('Summary', section_style))
        summary_rows = [
            ['Overall Score', f"{overview['score']}/10"],
            ['Questions Answered', str(overview['total_questions'])]
        ]
        if overview['avg_communication'] is not None:
            summary_rows.append(['Avg Communication Score', f"{overview['avg_communication']}/10"])
        if overview['avg_confidence'] is not None:
            summary_rows.append(['Avg Confidence Score', f"{overview['avg_confidence']}/10"])
        summary_table = Table(summary_rows, colWidths=[2.4 * inch, 4.0 * inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e5e7eb')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        content.append(summary_table)

        content.append(Paragraph('Strengths', section_style))
        strengths_list = ListFlowable([
            ListItem(Paragraph(item, styles['Normal'])) for item in strengths
        ], bulletType='bullet')
        content.append(strengths_list)

        content.append(Paragraph('Mistakes / Improvement Areas', section_style))
        mistakes_list = ListFlowable([
            ListItem(Paragraph(item, styles['Normal'])) for item in mistakes
        ], bulletType='bullet')
        content.append(mistakes_list)

        content.append(Paragraph('Suggested Model Answers', section_style))
        if qa_records:
            for idx, row in enumerate(qa_records, start=1):
                content.append(Paragraph(f"Q{idx}: {row.get('question', '')}", styles['BodyText']))
                model_answer = ReportGenerator._generate_model_answer(
                    row.get('question', ''),
                    session.get('session_type', 'general'),
                    row.get('keywords_matched', [])
                )
                content.append(Paragraph(f"Model Direction: {model_answer}", styles['Normal']))
                content.append(Spacer(1, 4))
        elif behavioral_records:
            for idx, row in enumerate(behavioral_records, start=1):
                content.append(Paragraph(f"Q{idx}: {row.get('question', '')}", styles['BodyText']))
                content.append(Paragraph(
                    "Model Direction: Use STAR format, include your role, concrete actions, and measurable outcome.",
                    styles['Normal']
                ))
                content.append(Spacer(1, 4))

        content.append(Paragraph('Next-Step Plan', section_style))
        plan_list = ListFlowable([
            ListItem(Paragraph(step, styles['Normal'])) for step in next_steps
        ], bulletType='1')
        content.append(plan_list)

        if emotion_timeline:
            emotion_counter = Counter([e.get('emotion', 'neutral') for e in emotion_timeline])
            emotion_summary = ', '.join([f"{k}: {v}" for k, v in emotion_counter.items()])
            content.append(Paragraph('Emotion Snapshot', section_style))
            content.append(Paragraph(f'Emotion samples recorded: {len(emotion_timeline)}', styles['Normal']))
            content.append(Paragraph(f'Distribution: {emotion_summary}', styles['Normal']))

        doc.build(content)
        buffer.seek(0)
        return buffer
