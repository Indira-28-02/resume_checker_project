---
sdk: streamlit
app_file: app.py
title: ATS Resume Checker
emoji: 🪪
colorFrom: green
colorTo: red
pinned: false
license: other
---

# 🧠 ATS Resume Checker

This project is a **Streamlit-based web application** that allows users to upload resumes and evaluates them like an ATS (Applicant Tracking System). It performs the following:

### ✅ Features

- 📄 Upload resume in PDF or DOCX format  
- 🧬 Parse resume and extract key sections  
- 🔍 Named Entity Recognition using SpaCy  
- 📝 Score the resume based on job relevance  
- 📊 Match resumes with job descriptions  
- 💾 Save parsed data to a database  
- 📥 Download parsed results as JSON or CSV

---

### 🚀 How It Works

1. **Upload your resume**
2. The system will extract content using `pymupdf` or `python-docx`
3. Resume is analyzed using SpaCy NLP (`en_core_web_sm`)
4. Results are displayed with entity highlights and matching score

---

### 🧱 Tech Stack

- Python
- Streamlit
- SpaCy
- pandas
- scikit-learn
- sqlalchemy
- pymupdf
- python-docx

---

### 📦 Installation (for local use)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
