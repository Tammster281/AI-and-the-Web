import streamlit as st

st.header("Wordle")

st.markdown("""

Normal Game

## Use markdown in Streamlit.

Just use `markdown`syntax for longer texts.
""")

if st.button("Go to Statistics"):
    st.switch_page("08-page2.py")
