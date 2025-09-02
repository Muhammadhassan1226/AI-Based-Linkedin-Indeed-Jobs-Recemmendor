import streamlit as st
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_indeed_jobs,fetch_linkedin_jobs
st.set_page_config(page_title="Job Recommender",layout="wide")
st.title("AI Job Recommendation System")
st.markdown("Upload your resume and get personalized job recommendations based on your skills and experience from **LinkedIn** and **Indeed**.")


uploaded_file = st.file_uploader("Choose a resume file", type=["pdf"])
if uploaded_file is not None:
    with st.spinner("Processing your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner("Analyzing your resume..."):
        summary = ask_openai(f"Summarize the following resume, highlighting key skills and experiences.:\n\n{resume_text} ", tokens=500)

    with st.spinner("Finding Skills Gaps..."):
        skills_gaps = ask_openai(f"Analyze the resume and highlight missing skills, certifications for better job opportunities in the following resume:\n\n{resume_text} ", tokens=400)

    with st.spinner("Creating Future Roadmaps..."):
        future_roadmap = ask_openai(f"Create a roadmap for the candidate to acquire the missing skills (skills to learn, industry exposure) and certifications identified in the following resume:\n\n{resume_text} ", tokens=400)

    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{skills_gaps}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{future_roadmap}</div>", unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")


    if st.button("🔎Get Job Recommendations"):
        with st.spinner("Fetching job recommendations..."):
                keywords = ask_openai(
                f"Based on this resume summary, suggest the best job titles and keywords for searching jobs. Give a comma-separated list only, no explanation.\n\nSummary: {summary}",
                max_tokens=100
            )
        search_keywords_clean = keywords.replace("\n", "").strip()
        st.success(f"Extracted Job Keywords: {search_keywords_clean}")

        with st.spinner("Fetching jobs from LinkedIn and Indeed..."):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords_clean, rows=60)
            indeed_jobs = fetch_indeed_jobs(search_keywords_clean, rows=60)

        st.markdown("---")
        st.header("💼 Top LinkedIn Jobs")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")


        st.markdown("---")
        st.header("💼 Top Indeed Jobs")

        if indeed_jobs:
            for job in indeed_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('url')})")
                st.markdown("---")
        else:
            st.warning("No Indeed jobs found.")
        


