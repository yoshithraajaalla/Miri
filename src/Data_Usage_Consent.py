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
st.markdown("## Miri")
st.markdown("The Smart Hiring Assistant by 🔶TalentScout")

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
    st.session_state.gdpr_consent = st.checkbox("I have read and agree to the terms.")

if st.session_state.gdpr_consent:
    st.switch_page("pages/1_Information_Form.py")