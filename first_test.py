import streamlit as st
import random
from openai import OpenAI, AuthenticationError, OpenAIError

with st.sidebar:
    api_key = "sk-W_byX2pDUK-eKqf5XjMerg"


if not api_key:
    st.info("Please enter your Uni Osnabrück API key. If you don't have one, you can obtain it from https://ai-keys.uni-osnabrueck.de.")
    st.stop()

# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=api_key
)

#Wortlänge wird mit slider festgelegt
wortlaenge = st.slider("Wortlänge:", min_value=3, max_value=8, value=5)
st.subheader("Wortlänge")
st.write(f"Wortlänge is {wortlaenge}")
#AI soll Wort nach dem Prompt später generieren
prompt = (f"Generate ONE real, existing dictionary word with exactly {wortlaenge} letters in all lowercase. Output ONLY the word and nothing else.")


if st.button("Generate Word") :#Wenn auf Button geklickt wird, Generiert AI ein Wort nach dem Prompt
    try:
        with st.spinner("Answer is being created …"):
            response = client.chat.completions.create(
                model="google/gemma-4-E4B-it",
                messages=[
                    {"role": "user", "content": prompt},
                ],
            )
        st.session_state["word"] = response.choices[0].message.content.strip()
       # st.session_state["word_generated"] = True
        st.write (st.session_state["word"])
        st.session_state["word_list"] = [] # es wird eine liste angelegt in der später alle guesses gespeichert werden
    except AuthenticationError:
        st.error("API was not accept. Please check it.")

    except OpenAIError:
        st.error(
            "AI API request failed. Please check it and try again. "
        )


st.header("P:red[y]t:blue[ho]n")


with st.form("text_form"):
    guess = st.text_input(
        f"Enter a {wortlaenge} letter word",

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
    st.session_state["word_list"].append(" ".join(guess_marked))
    for a in st.session_state["word_list"]:
        st.markdown(a)
    if guess == st.session_state['word']:
        st.success("Yeah! You did it")
        st.balloons()
       # del st.session_state['word']
    else:
        st.error("Oh no. The word is wrong.")
        st.info(f"Debug info: The word is {st.session_state['word']}")
if st.button("new_word"):
    st.info("New word has been generated!")
    st.balloons()
    st.session_state["word"] =random.choice(words)
