import streamlit as st

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

st.title("Welcome, I'm Miri!")

# st.markdown("""<p style="text-align:center;"><h1><b>Welcome! I'm Miri.</b></h1></p>""",
#     unsafe_allow_html=True,
# )

st.markdown("""
<p>The Smart Hiring Assistant by 🔶<b>TalentScout</b></p>
""",
    unsafe_allow_html=True,
)

# --- GDPR Disclaimer and Consent ---
if "gdpr_consent" not in st.session_state:
    st.session_state.gdpr_consent = False

if not st.session_state.gdpr_consent:
    st.subheader("Data Privacy and Consent")
    st.markdown("""
    Before proceeding, please read the following disclaimer regarding your data:

    We are GDPR compliant and are committed to protecting your personal data.
    By using this chatbot, you consent to the use of your data for recruitment purposes only.
    Your information will be stored securely and will only be used for evaluating your suitability for potential job opportunities.

    For more information about GDPR, please refer to [https://gdpr.eu/](https://gdpr.eu/).
    """)
    if st.button("I Agree"):
        st.session_state.gdpr_consent = True

if st.session_state.gdpr_consent:
    st.switch_page("pages/1_Chatbot.py")