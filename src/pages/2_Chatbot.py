import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

import pandas as pd

import os
from dotenv import load_dotenv

load_dotenv()

# App config
st.set_page_config(page_title="TalentScout - Miri", page_icon="🔶",initial_sidebar_state="collapsed")
st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

if "user_data_submitted" in st.session_state and st.session_state.user_data_submitted:
    user_name = st.session_state.user_data.get("Full Name", "Candidate")
    desired_position = st.session_state.user_data.get("Desired Position(s)", "role")
    tech_stack = st.session_state.user_data.get("Tech Stack", "technologies")

    # --- Session state initialization for chat ---
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content=f"Hi {user_name}! I see you're interested in the {desired_position} role and have experience with {tech_stack}. Let's dive into some technical questions based on your tech stack. Are you ready?"),
        ]
    if "data_collection_done" not in st.session_state:
        st.session_state.data_collection_done = True # Data is now collected via form
    if "submission_submitted" not in st.session_state:
        st.session_state.submission_submitted = False
    if "final_data" not in st.session_state:
        st.session_state.final_data = pd.DataFrame([st.session_state.user_data])

    # --- Check if GOOGLE_API_KEY is set ---
    if "GOOGLE_API_KEY" not in os.environ:
        st.error("GOOGLE_API_KEY is not set. Please set it as an environment variable.")
        st.stop()  # Stop the app if the API key is missing

    # --- Initialize Gemini LLM ---
    try:
        llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=os.environ["GOOGLE_API_KEY"])
    except Exception as e:
        st.error(f"Error initializing Gemini LLM: {e}")
        st.stop()

    def get_response(user_query, convo_history):
        template = """
        You are Miri, an AI hiring assistant.
        Your task is to conduct initial candidate screenings for technical roles.
        Generate exactly 3 relevant technical questions based on this tech stack.
        If the candidate says he doesn't know, then skip the question and continue on but do not ask more that a total of three questions.
        Maintain a professional and informative tone. Do not get deviated from the conversation. Apologize and repeat previous question if necessary.
        After receiving answers to all three questions, thank the user and say "Your responses have been recorded. We'll get back to you via email. You may close the tab now." [THIS IS MANDATORY, ALWAYS DISPLAY THIS AT THE END]
        Conversation History: {convo_history}
        Candidate: {user_query}
        Miri: """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | llm | StrOutputParser()
        try:
            return chain.stream({
                "convo_history": convo_history,
                "user_query": user_query,
            })
        except Exception as e:
            st.error(f"Error generating response: {e}")
            return "I encountered an error while processing your request. Let's try again."

    st.title("Miri")

    # --- Display chat history ---
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)

    # --- User input and response generation ---
    user_query = st.chat_input("Type your response here...")
    if user_query:  # Check if user_query is not None or empty
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            response_stream = get_response(user_query, st.session_state.chat_history)
            full_response = ""
            response_container = st.empty()
            for chunk in response_stream:
                full_response += chunk
                response_container.write(full_response)
            st.session_state.chat_history.append(AIMessage(content=full_response))
else:
    st.warning("Please submit your information on the previous page first.")