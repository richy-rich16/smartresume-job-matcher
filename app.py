import streamlit as st
from PyPDF2 import PdfReader
import spacy
from serpapi import GoogleSearch

# --- Config ---
nlp = spacy.load("en_core_web_sm")
SERPAPI_KEY = "a05691cb51b67ab1c55fe6731e37e925cb1248cda6fd0b01727033168cacd257"

# --- Known Skills ---
KNOWN_SKILLS = ["python", "sql", "pandas", "tensorflow", "ml", "ai", "automation", "django"]

def extract_text_from_pdf(uploaded_file):
    pdf = PdfReader(uploaded_file)
    return "".join([p.extract_text() or "" for p in pdf.pages])

def extract_skills(text):
    doc = nlp(text.lower())
    tokens = [t.text for t in doc if not t.is_stop and not t.is_punct]
    return list({skill for skill in KNOWN_SKILLS if skill in tokens})

def search_jobs(skills, location="Hyderabad"):
    params = {
        "engine": "google_jobs",
        "q": f"{', '.join(skills)} jobs in {location}",
        "hl": "en",
        "gl": "in",
        "api_key": SERPAPI_KEY
    }
    return GoogleSearch(params).get_dict().get("jobs_results", [])[:5]

# --- Streamlit UI ---
st.title("🔍 SmartResume AI Job Matcher")
st.write("Upload your resume. Get matching jobs. All AI-powered.")

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type="pdf")
if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(resume_text)
    st.success(f"✅ Extracted Skills: {', '.join(skills)}")

    if skills:
        location = st.text_input("📍 Job Location", "Hyderabad")
        if st.button("Find Matching Jobs"):
            jobs = search_jobs(skills, location)
            for job in jobs:
                st.markdown(f"### {job['title']} at {job['company_name']}")
                st.write(f"📍 {job.get('location', '')}")
                st.write(f"🔗 [Job Link]({job['link']})")
                st.markdown("---")
 
