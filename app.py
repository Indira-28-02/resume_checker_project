import streamlit as st
import pandas as pd
import json
from resume_parser import extract_text, extract_entities, validate_resume
from db import save_to_db

st.set_page_config(page_title="ATS Resume Checker", layout="wide")
st.title("🧠 ATS Resume Checker")

uploaded_file = st.file_uploader("📂 Upload your Resume (PDF or DOCX)", type=['pdf', 'docx'])

def highlight_text(text, spans):
    html = ""
    last = 0
    colors = {"PERSON": "#ffeeba", "EMAIL": "#d4edda", "PHONE": "#f8d7da"}
    for start, end, label in spans:
        html += text[last:start]
        html += f"<mark style='background-color:{colors.get(label, '#ddd')};'>{text[start:end]}</mark>"
        last = end
    html += text[last:]
    return html

if uploaded_file:
    with st.spinner("⏳ Analyzing resume..."):
        raw_text = extract_text(uploaded_file)
        parsed = extract_entities(raw_text)
        structure, completeness, score = validate_resume(raw_text, parsed)

        st.success("✅ Resume analyzed successfully!")

        st.subheader("📌 Extracted Information")
        for k in ['Name', 'Email', 'Phone', 'Skills']:
            st.write(f"**{k}:** {parsed[k]}")

        st.subheader("🧪 Resume Structure Check")
        for k, v in structure.items():
            st.markdown(f"{'✅' if v else '❌'} {k}")

        st.subheader("🔍 Resume Completeness Check")
        for k, v in completeness.items():
            st.markdown(f"{'✅' if v else '❌'} {k}")

        st.subheader("📊 ATS Score")
        st.progress(score)
        st.markdown(f"### Final Score: **{score}/100**")

        if score < 60:
            st.warning("⚠️ Resume score is low. Consider improving structure or adding more content.")

        save_to_db(parsed)

        df = pd.DataFrame([parsed])
        st.download_button("📥 Download JSON", json.dumps(parsed, indent=2), file_name="resume_data.json")
        st.download_button("📥 Download CSV", df[['Name', 'Email', 'Phone', 'Skills']].to_csv(index=False), file_name="resume_data.csv", mime='text/csv')

        st.subheader("🖍 Highlighted Resume Text")
        st.markdown(highlight_text(parsed["raw_text"], parsed["entities"]), unsafe_allow_html=True)

        st.subheader("🧠 Match with Job Description")
        job_desc = st.text_area("Paste Job Description Here")
        if st.button("Match"):
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            vect = TfidfVectorizer()
            vectors = vect.fit_transform([parsed["raw_text"], job_desc])
            sim = cosine_similarity(vectors[0:1], vectors[1:2])[0][0] * 100
            st.markdown(f"**Match Score:** `{sim:.2f}%`")
