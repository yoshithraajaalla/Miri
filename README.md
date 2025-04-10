# Miri - Hiring Assistant Chatbot

## 1. Project Overview

Miri is a Streamlit-based chatbot designed to streamline the initial candidate screening process for TalentScout, a (fictional) recruitment agency specializing in technology placements. This chatbot interacts with candidates to gather essential information, including their background and technical skills, and assesses their proficiency by asking relevant technical questions. The goal is to automate the early stages of recruitment, ensuring a more efficient and standardized evaluation of potential hires.

Deployed using [Streamlit Commmunity Cloud](https://streamlit.io/cloud). Check it out [here](https://miribot.streamlit.app/).

## 2. Local Installation Instructions

To set up and run the Hiring Assistant chatbot locally, follow these steps:

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yoshithraajaalla/Miri.git
    cd Miri
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**

    * **On Windows:**

        ```bash
        venv\Scripts\activate
        ```

    * **On macOS and Linux:**

        ```bash
        source venv/bin/activate
        ```

4.  **Install the required dependencies:**

    ```bash
    pip install streamlit langchain-google-genai python-dotenv PyPDF2 python-docx pandas
    ```

5.  **Set up the Google API Key:**

    * Obtain a Google API key for the Gemini API. See <https://ai.google.dev/> for instructions.

    * Create a `secrets.toml` file at `~/.streamlit/secrets.toml` for macOS/Linux or `%userprofile%/.streamlit/secrets.toml` for Windows:

    * Add your API key to the `secrets.toml` file:

        ```
        GOOGLE_API_KEY="YOUR_API_KEY"
        ```

        *Replace `YOUR_API_KEY` with your actual API key.*

6.  **Run the Streamlit application:**

    ```bash
    streamlit run src/Welcome.py
    ```

7.  **Access the application:**

    * The application will open in your default web browser. If it doesn't, you should see a URL (usually `http://localhost:8501`) printed in the terminal. Open this URL in your browser.

## 3. Usage Guide

1.  **Welcome Page:**

    * Upon accessing the application, you'll be greeted by Miri and presented with a data privacy notice.

    * Review the notice and click "I Agree" to proceed. If you do not agree, you cannot use the application.

2.  **Chatbot Interaction (Chatbot.py):**

    * **Resume Upload (Optional):** You can upload your resume (PDF or Word document) to automatically fill in some of the form fields (Full Name, Email Address, and Mobile Number).

    * **Information Form:** Fill in the required details:

        * Full Name

        * Email Address

        * Country Code

        * Mobile Number

        * Years of Experience

        * Desired Position(s)

        * Current Location

        * Tech Stack (List the programming languages, frameworks, and tools you are proficient in)

    * Click "Submit Information". Ensure all fields are correctly filled; otherwise, error messages will be displayed.

    * **Chat Interaction:** After submitting your information, the chatbot will initiate a conversation, asking technical questions based on the tech stack you provided.

    * Answer the questions to the best of your ability. The chatbot will guide you through a series of questions.

    * The chatbot will ask a maximum of three questions. After the third question, the conversation will end.

    * **End of Conversation:** Once the technical questions are complete, the chatbot will thank you and inform you about the next steps.

3.  **Thank You Page (Thank\_You.py):**

    * After the chat interaction, you will be redirected to a "Thank You" page.

    * This page confirms that your responses have been recorded.

    * You can close the browser tab at this point.

## 4. Technical Details

* **Programming Language:** Python

* **Libraries:**

    * Streamlit: For building the user interface.

    * Langchain: For LLM orchestration.

    * Langchain-Google-GenAI: For using the Gemini LLM.

    * PyPDF2: For parsing PDF files (for resume upload).

    * docx: For parsing Word files (for resume upload).

    * pandas: Implicit dependency for Streamlit

* **Large Language Model:**

    * Google Gemini (gemini-2.0-flash)

* **Prompt Engineering:** Prompts are designed to guide the LLM through information gathering and technical question generation.

* **Data Handling:**

    * Candidate information is stored in Streamlit's session state (`st.session_state`) for the duration of the session. No external database is used in this implementation.

    * Data privacy is a key consideration, and the application is designed to comply with GDPR principles. The user is informed of data usage and gives consent before proceeding.

* **Architecture:**

    1.  **Welcome.py:** Handles initial user interaction, GDPR consent, and redirection to the main chat page.

    2.  **Chatbot.py:** Manages the main chat flow:

        * Processes user input.

        * Extracts data from uploaded resumes.

        * Validates user-provided information.

        * Generates technical questions using the Gemini LLM and Langchain.

        * Maintains chat history using `st.session_state`.

    3.  **Thank\_You.py:** Displays a confirmation message at the end of the chat.

* **State Management:** Streamlit's `st.session_state` is used to manage user data, chat history, and application state across page transitions.

## 5. Prompt Design

The prompts used in this application are crucial for guiding the LLM to generate the desired behavior. Here's a breakdown of the prompt design:

* **Information Gathering:**

    * The initial instructions in `Chatbot.py` guide the user to input their information, and the application uses Streamlit form elements to collect structured data.

    * The prompt focuses on getting the user to provide key details like name, email, contact number, experience, desired role, and tech stack.

* **Technical Question Generation:**

    * The `get_response` function in `Chatbot.py` uses a carefully crafted prompt to generate technical questions.

    * The prompt includes the following elements:

        * **Role Definition:** The LLM is defined as "Miri, an AI hiring assistant".

        * **Context Setting:** The prompt provides the candidate's declared tech stack and experience level.

        * **Task Definition:** The prompt instructs the LLM to generate *one* relevant technical question.

        * **Conversation History:** The prompt includes the `convo_history` to maintain context and avoid repetition.

        * **Constraints:** The prompt limits the number of questions and enforces a professional tone.

        * **Error Handling:** The prompt instructs the LLM on how to respond if the candidate doesn't know the answer.

    * Example Prompt Template:

        ```
        You are Miri, an AI hiring assistant specialized in technical interviews for {difficulty_level} level candidates.
        Based on the following tech stack provided by the candidate:

        {tech_stack}

        Generate exactly one technical question relevant to these technologies, appropriate for a {difficulty_level} level.
        If the candidate indicates they don't know the answer, briefly acknowledge and move to the next question.
        Do not ask more than a total of three questions.
        Maintain a professional and concise tone.

        Conversation History:
        {convo_history}

        Candidate: {user_query}
        Miri:
        ```

## 6. Challenges & Solutions

* **Challenge 1:** Ensuring the LLM generates relevant and appropriate technical questions.

    * **Solution:** Detailed prompt engineering, including providing the candidate's tech stack, experience level, and conversation history, helps the LLM to stay focused and generate better questions. Iterative testing and refinement of the prompt were crucial.

* **Challenge 2:** Handling user input variations and potential errors.

    * **Solution:** Input validation in the Streamlit form ensures that required information is provided in the correct format. The prompt also instructs the LLM on how to handle cases where the candidate doesn't know the answer.

* **Challenge 3:** Maintaining conversation context.

    * **Solution:** Storing the chat history in `st.session_state` and including it in the prompt allows the LLM to refer to previous interactions and maintain a coherent conversation flow.

* **Challenge 4:** Extracting information from resumes with varying formats.

    * **Solution:** Used both PyPDF2 and docx to handle common resume formats. Regular expressions were used to extract name, email, and phone number. The extraction logic handles cases where some information might be missing from the resume.

## 7. Opportunities

This project provides a foundation for building an AI-powered hiring assistant, but there are several areas for future development and improvement:

1.  **Resume Data Extraction:**
    * The current implementation uses regular expressions for basic data extraction from resumes. This approach can be fragile and may not work reliably with all resume formats.
    * **Future Development:** More robust methods, such as dedicated resume parsing libraries (e.g., resume-parser, tika-python) or cloud-based resume parsing services, could be employed to improve accuracy and handle a wider variety of resume layouts.  Ideally, the solution should be able to extract information such as work experience, education, skills, and projects.

2.  **Cloud Deployment:**
    * The guide provides instructions for local deployment, and while deployment via Streamlit Community Cloud was achieved, it not the ideal choice especially when considering scalability, reliability, and security.
    * **Future Development:** Explore more robust cloud deployment options:
        * **Containerization (Docker):** Containerizing the application with Docker would simplify deployment across different environments and ensure consistency.
        * **Cloud Services:** Deploying the Docker container to a container orchestration service like Google Kubernetes Engine, Amazon Elastic Kubernetes Service, or Azure Kubernetes Service would provide scalability, high availability, and automated management.  Alternatively, serverless platforms like Google Cloud Functions, AWS Lambda, or Azure Functions could be used, though they may require refactoring the application.
        * **Platform-as-a-Service (PaaS):** Services like Google App Engine, Heroku, or similar could streamline deployment, but might introduce vendor lock-in.

3.  **Frontend Limitations:**
    * Streamlit, while excellent for rapid prototyping, has some limitations in terms of frontend structure, customization and complex UI design.
    * **Future Development:** Consider migrating to a more flexible frontend framework:
        * **React/Angular/Vue.js:** Building a separate frontend using a framework like React, Angular, or Vue.js would allow for a more modern, interactive, and customizable user experience.  This would likely involve creating an API (e.g., using Flask or FastAPI) to handle communication between the frontend and the backend (LLM and data processing).
        * **Enhanced Streamlit Components:** If Streamlit is retained, explore the use of custom Streamlit components or advanced layout options to overcome some of the framework's limitations.

