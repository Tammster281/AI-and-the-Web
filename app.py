import streamlit as st

page1 = st.Page("first_test.py", title="Wordle!", icon="🤔")
page2 = st.Page("stats.py", title="Stats page", icon="📈")

pg = st.navigation(pages=[page1, page2])
pg.run()