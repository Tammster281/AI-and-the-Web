import streamlit as st
import pandas as pd
import numpy as np

st.header("Statistics :t-rex:")

word_difficulty = st.select_slider( 
    "choose difficulty:",
    options=["easy", "normal", "hard",],
    value="normal")

st.markdown(st.session_state["stats"])

# 
df = pd.DataFrame({
    "Stat": ["Games", "Won"],
    "Count": [
        st.session_state["stats"][word_difficulty]["games_played"],
        st.session_state["stats"][word_difficulty]["games_won"]
    ]
})

st.bar_chart(
    df,
    x="Stat",
    y="Count"
)

df = pd.DataFrame({
    "Guesses": list(st.session_state["stats"][word_difficulty]["game_guesses"].keys()),
    "Count": list(st.session_state["stats"][word_difficulty]["game_guesses"].values())
})

st.bar_chart(
    df,
    x="Guesses",
    y="Count"
)


#values = np.array(list(game_guesses.values()))      
#hist_values = np.histogram(values)
#st.bar_chart(hist_values)

#chart = np.histogram(st.session_state["stats"]["game_guesses"])
#st.bar_chart(chart)
