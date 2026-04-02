import streamlit as st
import matplotlib.pyplot as plt
from processor import extract_text_from_pdf, get_match_score, get_skill_analysis
import interviewer 

# Page Configuration
st.set_page_config(page_title="AI Career Navigator", layout="wide")

# --- Session State Initialize ---
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
    st.session_state.current_question_index = 0
    st.session_state.questions_list = []
    st.session_state.user_answers = []
    st.session_state.analysis_done = False

# --- 1. Main Dashboard (Analysis + Setup) ---
if not st.session_state.interview_started:
    st.title("🚀 AI Career Navigator")
    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1. Upload Resume")
        uploaded_file = st.file_uploader("upload your pdf file here", type=["pdf"])
        
    with col2:
        st.subheader("2. Job Description")
        
        # 1. Dummy job descriptions
        jd_options = {
            "Custom (Paste your own)": "",
            "Python Developer": "We are looking for a Senior Python Developer with experience in Docker, Streamlit, APIs, and Machine Learning. Must have strong problem-solving skills.",
            "Data Scientist": "Required: Strong Python skills, Pandas, NumPy, Scikit-Learn, and experience building data models and visualizing data with Matplotlib.",
            "Full Stack Developer": "Looking for a developer skilled in Python backend, React frontend, database management, and AWS deployment."
        }
        
        # 2. Dropdown banate hain
        selected_template = st.selectbox("Choose a JD or write your own:", list(jd_options.keys()))
        
        # 3 If the user selects a template, the text will automatically appear in the text area.

        default_text = jd_options[selected_template]
        
        # Text area (Height retains at 150 as per your JD section snippet)
        jd_text = st.text_area("JD yahan paste karein...", value=default_text, height=150)

    st.markdown("---")

    # Layout for Buttons
    btn_col1, btn_col2 = st.columns(2)

    with btn_col1:
        if st.button("📊 Analyze My Resume", use_container_width=True):
            if uploaded_file and jd_text:
                with st.spinner('Analyzing...'):
                    resume_content = extract_text_from_pdf(uploaded_file)
                    score = get_match_score(resume_content, jd_text)
                    found, required, missing = get_skill_analysis(resume_content, jd_text)
                    
                    # Saving to state to persist through re-runs
                    st.session_state.resume_content = resume_content
                    st.session_state.jd_text = jd_text
                    st.session_state.analysis_results = {
                        "score": score,
                        "found": found,
                        "missing": missing
                    }
                    st.session_state.analysis_done = True
            else:
                st.info("Humein Resume aur JD dono chahiye.")

    with btn_col2:
        if st.button("🎙️ Start Mock Interview", use_container_width=True):
            if uploaded_file and jd_text:
                with st.spinner("AI sawal soch raha hai..."):
                    resume_content = extract_text_from_pdf(uploaded_file)
                    questions_raw = interviewer.generate_interview_questions(resume_content, jd_text)
                    
                    # Formatting questions into a list
                    st.session_state.questions_list = [q.strip() for q in questions_raw.split("\n") if q.strip() and any(char.isdigit() for char in q[:3])]
                    st.session_state.resume_content = resume_content
                    st.session_state.jd_text = jd_text
                    st.session_state.interview_started = True
                    st.rerun()
            else:
                st.warning("resume and job description upload first!")

    # Display Analysis Results if available
    if st.session_state.analysis_done:
        res = st.session_state.analysis_results
        st.markdown("---")
        st.metric(label="Match Score", value=f"{res['score']}%")
        
        if res['score'] >= 70:
            st.success("🔥 wow! Your profile is strong enough for this job.")
        elif res['score'] >= 40:
            st.warning("⚡ Good effort, But some keywords are missing.")
        else:
            st.error("📉 Score very low.")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown("### 📊 Skill Gap Analysis")
            st.write("**Skills found in Resume:**")
            st.write(", ".join(res['found']) if res['found'] else "None")
            st.write("**Missing Critical Skills:**")
            st.write(", ".join(res['missing']) if res['missing'] else "None (Great!)")
        
        with col_b:
            if res['found'] or res['missing']:
                fig, ax = plt.subplots(figsize=(4, 3))
                ax.pie([len(res['found']), len(res['missing'])], 
                       labels=['Matched', 'Missing'], 
                       autopct='%1.1f%%', startangle=90, 
                       colors=['#4CAF50', '#FF5252'])
                ax.axis('equal')
                st.pyplot(fig)

# --- 2. Interview Screen ---
else:
    st.title("🎙️ Mock Interview in Progress")
    
    questions = st.session_state.questions_list
    total_q = len(questions)
    
    if st.session_state.current_question_index < total_q:
        current_q = questions[st.session_state.current_question_index]
        
        st.subheader(f"Question {st.session_state.current_question_index + 1} of {total_q}")
        st.info(current_q)
        
        user_ans = st.text_area("Your Answer:", key=f"ans_{st.session_state.current_question_index}", height=150)
        
        if st.button("Submit Answer & Next"):
            st.session_state.user_answers.append({"question": current_q, "answer": user_ans})
            st.session_state.current_question_index += 1
            st.rerun()
            
    else:
        # --- 3. Result Screen ---
        st.success("✅ Interview Finished!")
        
        if st.button("Show My Result & Score"):
            with st.spinner("AI your answer check."):
                final_report = interviewer.evaluate_full_interview(st.session_state.user_answers)
                st.markdown("---")
                st.markdown("### 📝 Interview Feedback")
                st.markdown(final_report)
        
        if st.button("Start New Interview"):
            st.session_state.interview_started = False
            st.session_state.current_question_index = 0
            st.session_state.user_answers = []
            st.session_state.analysis_done = False
            st.rerun()
