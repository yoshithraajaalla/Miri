# pip install langchain langchain-google-genai google-generativeai streamlit python-dotenv

import streamlit as st

import pandas as pd
import numpy as np

from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv

import os

load_dotenv()

# App config
st.set_page_config(page_title="TalentScout - Miri", page_icon="🔶")
st.markdown("## Miri")
st.markdown("The Smart Hiring Assistant by 🔶TalentScout")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        AIMessage(content="Hi, I'm Miri. Before we get started, can I get your name, please?"),
    ]

# Check if GOOGLE_API_KEY is set
if "GOOGLE_API_KEY" not in os.environ:
    st.error("GOOGLE_API_KEY is not set. Please set it as an environment variable.")
    st.stop()  # Stop the app if the API key is missing

# Initialize Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', google_api_key=os.environ["GOOGLE_API_KEY"])
except Exception as e:
    st.error(f"Error initializing Gemini LLM: {e}")
    st.stop()

def get_response(user_query, convo_history):
    """
    Generates a response using the Gemini API, considering the chat history.

    Args:
        user_query (str): The user's input message.
        convo_history (list): A list of previous messages in the conversation.

    Returns:
        generator: A generator yielding the response chunks from the LLM.
    """
    template = """
    You are Miri, an AI hiring assistant. 
    Your task is to conduct initial candidate screenings for technical roles by generating technical questions based on provided information. 
    First priority gather user information which includes: Full Name, Email Address, Phone Number, Years of Experience, Desired Position(s), Current Location, Tech Stack.
    Once that's done, take into careful consideration the provided tech stack the candidate uses and then generate appropreate technical questions (not more than 3).  
    Maintain a professional and informative tone. Do not get deviated from the conversation. Apologize and repeat previous question if necessary.
    Conversation History: {convo_history}
    Candidate: {user_query}
    Miri: """

    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    try:
        # Use invoke instead of stream for a single response.
        return chain.stream({
            "convo_history": convo_history,
            "user_query": user_query,
        })
        return response
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return "I encountered an error while processing your request. Let's try again."

# Display chat history
for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI"):
            st.write(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.write(message.content)

# User input and response generation
user_query = st.chat_input("Type your response here...")
if user_query:  # Check if user_query is not None or empty
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("Human"):
        st.markdown(user_query)
    with st.chat_message("AI"):
        # Use st.write_stream to display the streaming response
        response = st.write_stream(get_response(user_query, st.session_state.chat_history))
    # Append the full response to chat history.  Important for maintaining context.
    st.session_state.chat_history.append(AIMessage(content=response))

# if st.toggle("Enable editing"):
#     edited_data = st.data_editor(data, column_config=config, use_container_width=True)
# else:
#     st.dataframe(data, column_config=config, use_container_width=True)