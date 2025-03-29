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
        Data Privacy Notice

        Your privacy matters to us. Before continuing, please review how we handle your information:

        We fully comply with GDPR regulations and prioritize the protection of your personal data. By engaging with this chatbot, you provide consent for us to process your information exclusively for recruitment evaluation. Your data will be stored using industry-standard security measures and used solely to assess your fit for relevant positions.

        For complete details on your rights under GDPR, visit [https://gdpr.eu/](https://gdpr.eu/)
    """)
    if st.button("I Agree"):
        st.session_state.gdpr_consent = True

if st.session_state.gdpr_consent:
    st.switch_page("pages/1_Chatbot.py")