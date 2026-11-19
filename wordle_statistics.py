import streamlit as st
import pandas as pd
import numpy as np

st.header("Statistics :t-rex:")

#check wether the stat variable has been made
if "stats" in st.session_state:
    st.markdown("You can see all your stats for the different difficulty levels here! Just adjust the slider and see how you did in the selected difficulty:grin:")

    # slider to choose the difficulty
    word_difficulty = st.select_slider( 
        "choose difficulty:",
        options=["easy", "normal", "hard",],
        value="normal")


    #st.markdown(st.session_state["stats"])

    # only display graphs if there is data to display:
    if st.session_state["stats"][word_difficulty]["games_played"] != 0:
        # save stats data for graph generation
        df = pd.DataFrame({
            "Games won": ["Games", "Won"],
            "Count": [
                st.session_state["stats"][word_difficulty]["games_played"],
                st.session_state["stats"][word_difficulty]["games_won"]
            ]
        })
        # show graph
        st.bar_chart(
            df,
            x="Games won",
            y="Count"
        )

        # again only display graph and avg if there is data to display
        if st.session_state["stats"][word_difficulty]["games_won"] != 0:

            df = pd.DataFrame({
                "Guesses": list(st.session_state["stats"][word_difficulty]["game_guesses"].keys()),
                "Count": list(st.session_state["stats"][word_difficulty]["game_guesses"].values())
            })

            # calculate and display average guesses needed
            avg = (df["Guesses"] * df["Count"]).sum() / df["Count"].sum()
            st.info(f"You take on average {avg} guesses!:smiling_face_with_three_hearts:")


            st.bar_chart(
                df,
                x="Guesses",
                y="Count"
            )


else:
    st.text("No data to display yet!")

