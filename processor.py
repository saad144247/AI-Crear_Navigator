import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

def extract_text_from_pdf(file):
    """To extract text from a PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            content = page.extract_text()
            if content:
                text += content
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def get_match_score(resume_text, jd_text):
    """Calculate the score using Cosine Similarity"""
    # Text to number vectors convert
    documents = [resume_text, jd_text]
    # 'english' stop words common words (the, is, in) to ingnore help
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)
    
    # Similarity calculate karna
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(float(similarity[0][0]) * 100, 2)

def get_skill_analysis(resume_text, jd_text):
    """Analyzing the skill gap between the resume and JD"""
    # Common technical keywords ki list (you can provide a more detail)
    keywords = [
        'Python', 'Java', 'Machine Learning', 'SQL', 'React', 'NLP', 
        'Data Science', 'Tableau', 'Docker', 'AWS', 'Communication', 
        'Pandas', 'NumPy', 'Scikit-Learn', 'TensorFlow', 'PyTorch'
    ]
    
    # Identifying overlapping keywords in the resume and JD
    resume_found = [word for word in keywords if word.lower() in resume_text.lower()]
    jd_required = [word for word in keywords if word.lower() in jd_text.lower()]
    
    # Identify the skills that are present in the JD but missing from the resume
    missing = [word for word in jd_required if word not in resume_found]
    
    return resume_found, jd_required, missing