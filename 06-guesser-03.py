import streamlit as st
import random

<<<<<<< HEAD
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
if submitted:
    st.write(f"You submitted: {guess}")
    # Run your calculation or other action here.
    for buchstabe in range(len(guess)):
        b1 = guess[buchstabe]
        b2 = st.session_state["word"][buchstabe]
        count=0
        if b1 == b2:
         #   st.write(f":green[{b1}]")
            guess_marked.append(f":green[{b1}]")
            
        else:
            for buchstabe in range(len(guess)):
                if b1 == st.session_state["word"][buchstabe]:
                    #st.write(f":blue[{b1}]")
                    #break
                    count = count + 1
            if count > 0:   
             #   st.write(f":blue[{b1}]")
                guess_marked.append(b1)
                count = 0
            else:   
             #   st.write(f":red[{b1}]")
                guess_marked.append(f":red[{b1}]")
                count = 0
    st.markdown(" ".join(guess_marked))
    if guess == st.session_state['word']:
        st.success("Yeah! You did it")
       # del st.session_state['word']
    else:
        st.error("Oh no. The word is wrong.")
        st.info(f"Debug info: The word is {st.session_state['word']}")
=======
st.header("Hello, world!")

# create a new random number if we don't have one yet
if "number" not in st.session_state:
    st.session_state["number"] = random.randint(1,100)
    st.info("New number generated!")

with st.form("number_form"):
    guess = st.number_input(
        "Enter a number",
        min_value=0,
        max_value=100,
        value=10,
        step=1,
    )
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"You submitted: {guess}")
    # Run your calculation or other action here.
    if guess == st.session_state['number']:
        st.success("Yeah! You did it")
        del st.session_state['number']
    else:
        st.error("Oh no. The number is wrong.")
        st.info(f"Debug info: The number is {st.session_state['number']}")
>>>>>>> 4bf76417d533794d7defd1647433929c7c76d10e
