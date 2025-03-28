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

if "user_data" not in st.session_state:
    st.session_state.user_data = {}
if "user_data_submitted" not in st.session_state:
    st.session_state.user_data_submitted = False

st.title("Enter Your Information")

with st.form("user_info_form"):
    col1, col2 = st.columns(2)
    full_name = col1.text_input("Full Name")
    email = col2.text_input("E-mail")
    country_code = col1.text_input("Country Code", value = "+91")
    mobile_number = col2.text_input("Mobile Number")
    years_exp = col1.number_input("Year(s) of Experience", min_value=0, step=1)
    desired_positions = col2.text_input("Desired Postion(s)")
    current_location = st.text_input("Current Location")
    tech_stack = st.text_area("Enter the Tech Stack you have experience with (Programming Languages, Frameworks etc)")

    submitted = st.form_submit_button("Submit Information")

    if submitted:
        errors = []
        if not full_name:
            errors.append("Full Name cannot be empty.")
        if not email or "@" not in email or "." not in email:
            errors.append("Please enter a valid E-mail address.")
        if not country_code:
            errors.append("Country Code cannot be empty.")
        if not mobile_number or len(''.join(filter(str.isdigit, mobile_number))) != 10:
            errors.append("Mobile Number must be exactly 10 digits.")
        if not desired_positions:
            errors.append("Desired Position(s) cannot be empty.")
        if not current_location:
            errors.append("Current Location cannot be empty.")
        if not tech_stack:
            errors.append("Tech Stack cannot be empty.")

        if errors:
            for error in errors:
                st.error(error)
        else:
            st.session_state.user_data = {
                "Full Name": full_name,
                "Email Address": email,
                "Country Code": country_code,
                "Mobile Number": mobile_number,
                "Years of Experience": years_exp,
                "Desired Position(s)": desired_positions,
                "Current Location": current_location,
                "Tech Stack": tech_stack,
            }
            st.session_state.user_data_submitted = True
            st.success("Information submitted successfully!")
            st.switch_page("pages/2_Chatbot.py")