import streamlit as st

# create a page running first_test.py and another using wordle_statistics.py
page1 = st.Page("first_test.py", title="Wordle!", icon=":material/crown:")
page2 = st.Page("wordle_statistics.py", title="Stats page", icon="📈")

# create a navigation sidebar
pg = st.navigation(pages=[page1, page2])
pg.run()