import streamlit as st

page1 = st.Page("wordle.py", title="Wordle", icon=":material/crown")
page2 = st.Page("wordle_statistics.py", title="Statistics", icon="📈")

pg = st.navigation(pages=[page1, page2])
pg.run()
 #test funktioniert diese github