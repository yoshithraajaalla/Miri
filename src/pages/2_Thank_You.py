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

st.balloons()

st.markdown("""<h1><p style="text-align:center;"><b>THANK YOU!</b></p></h1>""",
    unsafe_allow_html=True,
)

st.markdown("""<h3><p style="text-align:center;">We'll get back to you via email.</p></h3>""",
    unsafe_allow_html=True,
)

st.markdown("---")
st.markdown("""<p style="text-align:center;">You can close the tab now...</p>""",
    unsafe_allow_html=True,
)