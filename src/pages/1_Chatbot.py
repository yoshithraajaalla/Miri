import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
from datetime import datetime, timezone
import time
import re
try:
    from PyPDF2 import PdfReader
    import docx
    resume_parsing_enabled = True
except ImportError:
    resume_parsing_enabled = False
    st.warning("Please install PyPDF2 and python-docx for resume parsing functionality.")

if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "information_collected" not in st.session_state:
    st.session_state.information_collected = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "data_saved" not in st.session_state:
    st.session_state.data_saved = False
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False
if "redirected" not in st.session_state:
    st.session_state.redirected = False
if "question_number" not in st.session_state:
    st.session_state.question_number = 0
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = []
if "uploaded_file_data" not in st.session_state:
    st.session_state.uploaded_file_data = None

# App Config
st.set_page_config(page_title="TalentScout - Miri", page_icon="🔶",initial_sidebar_state="collapsed")
st.markdown("""<style> [data-testid="collapsedControl"] { display: none } </style>""", unsafe_allow_html=True,)
st.title("Welcome, I'm Miri!")
st.markdown("Please enter your information to in the provided fields:")

# File Upload Module
uploaded_file = st.file_uploader("Upload your resume (PDF or Word) to auto-fill the form", type=["pdf", "docx"], key="file_uploader")
extracted_name = st.session_state.user_data.get("Full Name", "")
extracted_email = st.session_state.user_data.get("Email Address", "")
extracted_mobile = st.session_state.user_data.get("Mobile Number", "")

# Compiled regular expressions
name_regex = re.compile(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+)")
email_regex = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
mobile_regex = re.compile(r"(\+?\d{1,4}[-.\s]?\(?\d{1,}\)?[-.\s]?\d+)")

def extract_name(text):
    match = name_regex.search(text)
    return match.group(0) if match else None

def extract_email(text):
    match = email_regex.search(text)
    return match.group(0) if match else None

def extract_mobile(text):
    match = mobile_regex.search(text)
    return match.group(0) if match else None

if uploaded_file and resume_parsing_enabled:
    st.session_state.uploaded_file_data = uploaded_file
    file_type = uploaded_file.type
    try:
        text = ""
        if file_type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = docx.Document(uploaded_file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

        if text:
            extracted_name = extract_name(text)
            if extracted_name and not st.session_state.user_data.get("Full Name"):
                st.session_state.user_data["Full Name"] = extracted_name

            extracted_email = extract_email(text)
            if extracted_email and not st.session_state.user_data.get("Email Address"):
                st.session_state.user_data["Email Address"] = extracted_email

            extracted_mobile = extract_mobile(text)
            if extracted_mobile and not st.session_state.user_data.get("Mobile Number"):
                if extracted_mobile:
                    st.session_state.user_data["Mobile Number"] = extracted_mobile
                else:
                    st.warning("Could not extract a valid mobile number from the resume.")

            st.success("Resume uploaded and basic data extracted!")

    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")

# Form Structure
with st.form("user_info_form"):
    col1, col2 = st.columns(2)
    full_name = col1.text_input("Full Name", value=st.session_state.user_data.get("Full Name", ""))
    email = col2.text_input("E-mail", value=st.session_state.user_data.get("Email Address", ""))
    country_code = col1.text_input("Country Code", value = "+91")
    mobile_number = col2.text_input("Mobile Number", value=st.session_state.user_data.get("Mobile Number", ""))
    years_exp = col1.number_input("Year(s) of Experience", min_value=0, step=1, value=st.session_state.user_data.get("Years of Experience", 0))
    desired_positions = col2.text_input("Desired Postion(s)", value=st.session_state.user_data.get("Desired Position(s)", ""))
    current_location = st.text_input("Current Location", value=st.session_state.user_data.get("Current Location", ""))
    tech_stack = st.text_area("Enter your key skills:", value=st.session_state.user_data.get("Tech Stack", ""))
    submit_button = st.form_submit_button("Submit Information", disabled=st.session_state.form_submitted)
    
    # Form contraints
    if submit_button:
        if not st.session_state.form_submitted:
            st.session_state.form_submitted = True
        errors = []
        if not full_name:
            errors.append("Full Name cannot be empty.")
        if not email or "@" not in email or "." not in email:
            errors.append("Please enter a valid E-mail address.")
        if not country_code:
            errors.append("Country Code cannot be empty.")
        if not mobile_number:
            errors.append("Mobile Number cannot be empty.")
        if not desired_positions:
            errors.append("Desired Position(s) cannot be empty.")
        if not current_location:
            errors.append("Current Location cannot be empty.")
        if not tech_stack:
            errors.append("Tech Stack cannot be empty.")
        if errors:
            for error in errors:
                st.error(error)
            st.session_state.form_submitted = False
        else:
            st.session_state.user_data["Full Name"] = full_name
            st.session_state.user_data["Email Address"] = email
            st.session_state.user_data["Country Code"] = country_code
            st.session_state.user_data["Mobile Number"] = mobile_number
            st.session_state.user_data["Years of Experience"] = years_exp
            st.session_state.user_data["Desired Position(s)"] = desired_positions
            st.session_state.user_data["Current Location"] = current_location
            st.session_state.user_data["Tech Stack"] = tech_stack
            st.session_state.information_collected = True
            st.success("Information submitted successfully! Starting chat...")
            user_name = st.session_state.user_data.get("Full Name", "Candidate")
            desired_position = st.session_state.user_data.get("Desired Position(s)", "role")
            tech_stack = st.session_state.user_data.get("Tech Stack", "technologies")
            initial_message = f"Hi {user_name}! I see you're interested in the {desired_position} role and have experience with {tech_stack}. Let's dive into some technical questions based on your tech stack. Are you ready?"
            st.session_state.chat_history.append(AIMessage(content=initial_message))

# Information sorting
if st.session_state.information_collected:
    user_name = st.session_state.user_data.get("Full Name", "Candidate")
    desired_position = st.session_state.user_data.get("Desired Position(s)", "role")
    tech_stack = st.session_state.user_data.get("Tech Stack", "technologies")
    years_of_experience = st.session_state.user_data.get("Years of Experience", 0)
    
    # Difficulty Mapping
    if years_of_experience == 0:
        difficulty_level = "Fresher"
    elif 1 <= years_of_experience <= 2:
        difficulty_level = "Junior"
    elif 3 <= years_of_experience <= 5:
        difficulty_level = "Mid-Level"
    else:
        difficulty_level = "Senior"

    # Initialize Gemini LLM
    if "llm" not in st.session_state:
        try:
            st.session_state.llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=st.secrets["GOOGLE_API_KEY"])
        except Exception as e:
            st.error(f"Error initializing Gemini LLM: {e}")
            st.stop()
    # Gemini Prompt Template and Langchain
    def get_response(user_query, convo_history, tech_stack, difficulty_level):
        template = """ You are Miri, an AI hiring assistant specialized in technical interviews for {difficulty_level} level candidates. Based on the following tech stack provided by the candidate: ``` {tech_stack} ``` Generate exactly one technical question relevant to these technologies, appropriate for a {difficulty_level} level. If the candidate indicates they don't know the answer, briefly acknowledge and move to the next question. Do not ask more than a total of three questions. Maintain a professional and concise tone. Conversation History: {convo_history} Candidate: {user_query} Miri: """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | st.session_state.llm | StrOutputParser()
        try:
            return chain.stream({ "tech_stack": tech_stack, "convo_history": convo_history, "user_query": user_query, "difficulty_level": difficulty_level })
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return "I encountered an error while processing your request. Let's try again."
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
    user_query = st.chat_input("Type your response here...")
    if user_query:
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            if st.session_state.question_number < 3:
                response_stream = get_response(user_query, st.session_state.chat_history, tech_stack, difficulty_level)
                full_response = ""
                response_container = st.empty()
                for chunk in response_stream:
                    full_response += chunk
                    response_container.write(full_response)
                st.session_state.chat_history.append(AIMessage(content=full_response))
                st.session_state.question_number += 1
                st.session_state.questions_asked.append(full_response)
            elif st.session_state.question_number == 3 and not st.session_state.redirected:
                final_message = "Your responses have been recorded. We'll get back to you via email. You may close the tab now."
                st.session_state.chat_history.append(AIMessage(content=final_message))
                st.success(final_message)
                st.session_state.redirected = True
                time.sleep(2)
                if "uploaded_file_data" in st.session_state:
                    del st.session_state.uploaded_file_data
                st.switch_page("pages/2_Thank_You.py")
else:
    st.markdown("---")
    st.info("Please fill out the information form above to start the chat.")