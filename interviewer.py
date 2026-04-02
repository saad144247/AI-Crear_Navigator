import os
from groq import Groq

# Groq Client setup
client = Groq(api_key="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")

def generate_interview_questions(resume_text, jd_text):
    """
    Use Groq AI (Llama 3) to generate dynamic questions.
    """
    try:
        # Powerful Prompt taake random keywords ki bajaye asli sawal ayen
        prompt = f"""
        Act as a Senior Technical Interviewer. 
        Analyze the Resume and Job Description (JD) provided below.
        
        Tasks:
        1. Identify 3 core technical gaps or strengths.
        2. Generate 5 personalized interview questions.
        
        RESUME:
        {resume_text[:3000]}
        
        JD:
        {jd_text[:3000]}
        
        Return the response in a clear, professional numbered list.
        Important: Ensure the questions are numbered like '1. ', '2. ', etc.
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful career coach and interviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return completion.choices[0].message.content

    except Exception as e:
        return f"Interviewer Error: {str(e)}"

def evaluate_full_interview(qa_pairs):
    """
    Analyze questions and answers and provide scores and feedback.
    """
    try:
        data_string = ""
        for item in qa_pairs:
            data_string += f"Q: {item['question']}\nA: {item['answer']}\n\n"

        prompt = f"""
        Act as an Expert Hiring Manager. Evaluate these interview answers.
        
        For each answer provided in the DATA:
        1. Give a Score (out of 10).
        2. Assessment: Tell if it was Correct, Partially Correct, or Wrong.
        3. Pro Tip: Give a brief, actionable 'Pro Tip' to improve.

        DATA:
        {data_string}

        Finally, provide:
        - Overall 'Selection Probability' percentage.
        - A short summary of the candidate's performance.
        """

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert HR analyst providing constructive feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500,
        )
        
        return completion.choices[0].message.content

    except Exception as e:
        return f"Evaluation Error: {str(e)}"