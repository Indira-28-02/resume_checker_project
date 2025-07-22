import spacy
import fitz
import docx2txt
import re

nlp = spacy.load('en_core_web_sm')

def extract_text(file):
    if file.name.endswith('.pdf'):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return ''.join([page.get_text() for page in doc])
    elif file.name.endswith('.docx'):
        return docx2txt.process(file)
    return ""

def extract_entities(text):
    doc = nlp(text)
    entities = {"Name": None, "Email": None, "Phone": None, "Skills": [], "entities": [], "raw_text": text}
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not entities["Name"]:
            entities["Name"] = ent.text
        elif ent.label_ == "EMAIL":
            entities["Email"] = ent.text
        elif ent.label_ == "PHONE":
            entities["Phone"] = ent.text
        entities["entities"].append((ent.start_char, ent.end_char, ent.label_))

    if not entities["Email"]:
        match = re.search(r'[\w\.-]+@[\w\.-]+', text)
        entities["Email"] = match.group(0) if match else None

    if not entities["Phone"]:
        match = re.search(r'\+?\d[\d\s\-]{8,}', text)
        entities["Phone"] = match.group(0) if match else None

    skills_list = ["python", "java", "sql", "html", "css", "javascript", "machine learning", "data science", "django"]
    entities["Skills"] = [skill for skill in skills_list if skill.lower() in text.lower()]

    return entities

def validate_resume(text, parsed):
    structure = {
        "Education": "education" in text.lower(),
        "Experience": "experience" in text.lower() or "work history" in text.lower(),
        "Skills": "skills" in text.lower(),
        "Projects": "project" in text.lower(),
    }

    completeness = {
        "Name": bool(parsed["Name"]),
        "Email": bool(parsed["Email"]),
        "Phone": bool(parsed["Phone"]),
        "Minimum Skills (3+)": len(parsed["Skills"]) >= 3
    }

    total = list(structure.values()) + list(completeness.values())
    score = int((sum(total) / len(total)) * 100)

    return structure, completeness, score
