# 🚀 AI Career Navigator

AI Career Navigator is an advanced, Streamlit-based web application designed to help job seekers optimize their resumes against job descriptions (JD) and practice mock interviews using state-of-the-art Generative AI. 

The application utilizes **Groq's Llama 3** for intelligent mock interviews and advanced Natural Language Processing (NLP) techniques for skill gap analysis.

---

## ✨ Key Features

* **Resume & JD Matcher:** Automatically extracts text from uploaded PDF resumes and computes a match percentage with the provided Job Description using TF-IDF and Cosine Similarity.
* **Skill Gap Analysis:** Scans the resume and job description to identify matched skills and highlights critical missing keywords, displaying the data in interactive visual charts.
* **AI-Powered Mock Interviews:** Dynamically generates 5 highly personalized technical questions targeting your background and the specific job requirements.
* **Intelligent Feedback System:** Evaluates candidate answers, provides scoring out of 10 for each response, leaves expert pro-tips, and calculates the overall 'Selection Probability'.

---

## 🛠️ Project Architecture & Tech Stack

The project is structured into modular components for high readability and easy scalability:

* **`app.py`**: The central Streamlit file that drives the User Interface, Session States, and Dashboard layouts.
* **`interviewer.py`**: Handles API connections with Groq (Llama-3.3-70b-versatile) to fetch smart questions and grade complex answers.
* **`processor.py`**: Holds core algorithms for text extraction via `PyPDF2` and machine learning computations using `scikit-learn`.

**Core Technologies:** Python, Streamlit, Groq API, Scikit-Learn (TF-IDF), Matplotlib, PyPDF2.

---

## ⚙️ Installation & Local Setup

Follow these simple steps to run the project on your local machine:

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
cd YOUR_REPOSITORY_NAME
2. Set up a Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Setup API Key
Go to interviewer.py and ensure your Groq API key is active. (Recommendation: Use environment variables instead of hardcoding for better security!)

5. Run the Application
Bash
streamlit run app.py
📌 Usage Guide
Run the app and go to the dashboard.

Drop your PDF resume in section 1.

Select a pre-built Job Description template or paste your own in section 2.

Click Analyze My Resume to check your score and skill gaps.

Click Start Mock Interview to answer custom AI-generated questions and get detailed, real-time performance feedback!