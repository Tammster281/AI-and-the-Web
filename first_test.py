import streamlit as st
import random
from openai import OpenAI, AuthenticationError, OpenAIError
#import pandas as pd
#import numpy as np
import json

# JSON-Datei laden
with open('2of12id.json', 'r') as file:
    nouns = json.load(file)['N']

# api key
# TODO: have user input the key themselves later!
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
if "word_generated" not in st.session_state: # these variables should allready exist but not turn false everytime the website gets an input
    st.session_state["word_generated"] = False
if "solved" not in st.session_state:
    st.session_state["solved"] = False
st.header("Wordle")

# make a slider to adjust the word difficulty
# TODO: think about different input method, slider is clunky
word_difficulty = st.select_slider( 
    "choose word difficulty:",
    options=["easy", "normal", "hard",],
    value="normal")

# word length gets chosen with a slider
wortlaenge = st.slider("Wortlänge:", min_value=3, max_value=8, value=5)
with st.form("text", clear_on_submit=False, enter_to_submit=True, border=True):
    word_topic = st.text_input(   
        f"Enter a wordtopic"

    )
    submitted = st.form_submit_button("Submit")

# prompt for the AI to generate a word later
prompt = (f"Generate ONE real, existing dictionary word with the topic {word_topic} with exactly {wortlaenge} letters {word_difficulty} to guess. Output ONLY the word and nothing else.")

# create session state for the statistics if it doesn't exist already
if "stats" not in st.session_state:
    st.session_state["stats"] = {
        "games_played": 0,
        "games_won": 0,
        "game_guesses": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        }  
    }

# (If there is no word yet or) the button gets clicked, the AI generates a word
# remove the comment and the ":" in between in the "if"-line to generate the word immediately
# TODO: handle problems arising from not generating the word immediately IF we keep it commented out. Maybe set default word for testing
if st.button("Generate new Word") : # or "word" not in st.session_state: 
    try:
        with st.spinner("Answer is being created …"): 
            resp = client.chat.completions.create(
            model="Qwen/Qwen3.8-27B-FP8",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}], # a spinner while the model is generating      
                )

            try:
                st.session_state["word"] = resp.choices[0].message.content.strip().upper()
            
            except:
                st.error("The AI couldn't generate a word. Please try again.")

        st.session_state["guess_counter"] = 0
        st.session_state["solved"] = False
        st.session_state["stats"]["games_played"] += 1
        st.session_state["word_generated"] = True
        try:
            st.write (st.session_state["word"])
        except:
            st.error("No word was chosen. Please try again.")
            st.session_state["word_generated"] = False # set the flag back to false if it failed to generate
        st.session_state["word_list"] = [] # a list gets created in which all guesses are saved later
    except AuthenticationError:
        st.error("API was not accept. Please check it.")

    except OpenAIError:
        st.error(
            "AI API request failed. Please check it and try again. "
        )

# Button to get a hint
if st.button("Hint") and st.session_state["solved"] == False and st.session_state["word_generated"] == True:
    if st.session_state["guess_counter"] > 3: # only after a few guess should you be able to get a hint
        hint = f"give a riddle to guess {st.session_state['word']} without saying {st.session_state['word']}"
        try:
            with st.spinner("Answer is being created …"): # a spinner while the model is generating
                resp = client.chat.completions.create(
                model="Qwen/Qwen3.8-27B-FP8",
                max_tokens=1000,
                messages=[{"role": "user", "content": hint}],    
                        )
                st.session_state["hint"] = resp.choices[0].message.content
                st.write (st.session_state["hint"])

                        
        except AuthenticationError:
            st.error("API was not accept. Please check it.")

        except OpenAIError:
            st.error(
                "AI API request failed. Please check it and try again. "
            )
    else:
        st.write("Come on, try a few times first!")
    for a in st.session_state["word_list"]: #the list of allready tiped words should still be shows
        st.markdown(a)

stop = False

# TODO: add comments
with st.form("textform", clear_on_submit=True, enter_to_submit=True, border=True):
    
    guess_ungereinigt = st.text_input(   
        f"Enter a {wortlaenge} letter word",

    )
    submitted = st.form_submit_button("Submit") # TODO: same variable as above, overrides the input
    if submitted and st.session_state["solved"] == False:
        guess = guess_ungereinigt.strip().upper() # removes spaces and makes everything upper letters

        if guess.lower() not in nouns or len(guess) != len(st.session_state["word"]): # if the word is not an actual word or wrong length,
            st.error("Enter valid word!")     # it is not supposed to keep using it so stop = True
            stop = True
            for a in st.session_state["word_list"]: # the list of already typed words should still be shown
                st.markdown(a)


guess_marked = []
letter_used=[]
# if the Submit button was pressed and the word wasn't guessed yet,
if submitted and not st.session_state["solved"] and stop == False:
    
    st.session_state["guess_counter"] += 1 # increase the guess counter

    if st.session_state["guess_counter"] <= 6: # if the guess counter is 6 or less
        st.write(f"You submitted: {guess}") # write the submitted guessed word

        # append a 0 into a list for every letter of the guessed word
        for i in range (len(guess)):
            letter_used.append(0)

        # Abgleichen des guesses mit dem gesuchten wort, entsprechendes färben der buchstaben
        for buchstabe in range(len(guess)):
            b1 = guess[buchstabe]
            b2 = st.session_state["word"][buchstabe]

            # count=0
            # if the letter is in the correct spot, make it green
            if b1 == b2:
                guess_marked.append(f":green[{b1}]")
                letter_used[buchstabe]=1

            # otherwise, search for the letter in the word and if it is in the word and not already used and not in the right spot, make it yellow 
            else:
                l_found = False
                for i in range(len(st.session_state["word"])):
                    if b1 == st.session_state["word"][i] and letter_used[i]==0 and guess[i]!=st.session_state["word"][i]:
                        guess_marked.append(f":yellow[{b1}]")
                        letter_used[i]=1 # mark the letter as used by making the 0 in its position a 1
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
            if not st.session_state["solved"]:
                st.session_state["stats"]["games_won"] += 1
                st.session_state["stats"]["game_guesses"][st.session_state["guess_counter"]] += 1
            st.session_state["solved"] = True
            
        # del st.session_state['word']
        else:
            st.error("Oh no. The word is wrong.")
            st.info(f"Debug info: The word is {st.session_state['word']}")
    else:
        st.error("You have used up all your guesses." +f"Debug info: The word was {st.session_state['word']}" + "Please generate a new word and try again.")