import streamlit as st
import random


# If you want Streamlit's built-in colored text rendering:
st.header("P:red[y]t:blue[ho]n")

# create a new random number if we don't have one yet
if "word" not in st.session_state:
    words = ["python", "coding", "skater", "header"]
    st.session_state["word"] =random.choice(words)
    print(st.info("New word generated!"))
st.write (st.session_state["word"])

with st.form("text_form"):
    guess = st.text_input(
        "Enter a 6 letter word",

    )
    submitted = st.form_submit_button("Submit")

guess_marked = []
letter_used=[]
if submitted:
    st.write(f"You submitted: {guess}")
    
    for i in range (len(guess)):
        letter_used.append(0)

    # Abgleichen des guesses mit dem gesuchten wort, entsprechendes färben der buchstaben
    for buchstabe in range(len(guess)):
        b1 = guess[buchstabe]
        b2 = st.session_state["word"][buchstabe]

        #count=0
        if b1 == b2:
            guess_marked.append(f":green[{b1}]")
            letter_used[buchstabe]=1

        else:
            l_found = False
            for i in range(len(st.session_state["word"])):
                if b1 == st.session_state["word"][i] and letter_used[i]==0 and guess[i]!=st.session_state["word"][i]:
                    guess_marked.append(f":yellow[{b1}]")
                    letter_used[i]=1
                    l_found = True
                    break

            if not l_found:
                guess_marked.append(f":red[{b1}]")

    st.markdown(" ".join(guess_marked))
    if guess == st.session_state['word']:
        st.success("Yeah! You did it")
       # del st.session_state['word']
    else:
        st.error("Oh no. The word is wrong.")
        st.info(f"Debug info: The word is {st.session_state['word']}")