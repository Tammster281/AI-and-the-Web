import streamlit as st
import random
from openai import OpenAI, AuthenticationError, OpenAIError
#import pandas as pd
#import numpy as np
import json


# JSON-Datei with real words
with open('2of12id.json', 'r') as file:
    official_words = [word for category in json.load(file).values() for word in category]

# api key input
if not "api_key" in st.session_state:
    st.session_state["api_key"] = ""
with st.sidebar:
    with st.form("api_key_form", clear_on_submit=False, enter_to_submit=False):
        api_key = st.text_input(f"Enter your API key", value=st.session_state.get("api_key", ""))
        submit_key = st.form_submit_button("Enter")

# this must stay in, otherwise it deletes the session state if it is only written on in the form when you switch pages
if submit_key:
    st.session_state["api_key"] = api_key

# if there is no API key yet, info about that
if not st.session_state["api_key"]:
    st.info("Please enter your Uni Osnabrück API key. If you don't have one, you can obtain it from https://ai-keys.uni-osnabrueck.de.")
    st.stop()

# pass the entered key
client = OpenAI(
    base_url="https://litellm.uni-osnabrueck.de/v1",
    api_key=st.session_state["api_key"]
)

if "word_generated" not in st.session_state: # these variables should already exist but not turn false everytime the website gets an input
    st.session_state["word_generated"] = False
if "solved" not in st.session_state:
    st.session_state["solved"] = False
if "used_word" not in st.session_state:
    st.session_state["used_word"] = [] #list of words later used not to generate same word twice
if "word_list" not in st.session_state:
    st.session_state["word_list"]=[]
if "hint_displayed" not in st.session_state:
    st.session_state["hint_displayed"] = False
if "no_hint_yet" not in st.session_state:
    st.session_state["no_hint_yet"] = False #no hint is ALLOWED yet if not_hint_yes is false 
st.session_state["no_hint_yet" ]= False # the "no hint yet" message should not be displayed yet before requesting a hint


col1, col2 = st.columns([8.5,1.5], vertical_alignment="bottom")
with col1:
    st.header(":red[W]:orange[o]:yellow[r]:green[d]:blue[l]:violet[e]")

with col2:
    with st.popover("Settings"):
        # make a slider to adjust the word difficulty
        word_difficulty = st.select_slider( 
            "word difficulty:",
            options=["easy", "normal", "hard",],
            value="normal")

        # word length gets chosen with a slider
        wortlaenge = st.slider("wordlength:", min_value=3, max_value=8, value=5)

# create 3 columns with their individual widths
col_, col2_, col3_ = st.columns([6.7,2.3,1], vertical_alignment="center")
with col_:
    # create a form in the first column with 2 columns of its own
    with st.form("text", clear_on_submit=False, enter_to_submit=True, border=True):
        column1, column2 = st.columns([8,2])
        # in the first of those columns, put a text input with a placeholder value
        with column1:
            word_topic = st.text_input(   
                    "wordtopic", placeholder="Enter a wordtopic...", # the text where you have to type in wordtopic displays this
                label_visibility="collapsed"  # makes layout more compact by removing the topic above field
            )
        # in the second column, put a submit button
        with column2:
            submitted1 = st.form_submit_button("Submit")


# prompt for the AI to generate a word later
prompt = (
    f"Generate ONE real, existing dictionary word with the topic '{word_topic}' with exactly {wortlaenge} letters with a {word_difficulty} difficulty to guess. "
    f"Do NOT generate any of the following previously used words: '{word_topic}', {', '.join(st.session_state['used_word'])}. Output ONLY the word and nothing else."
)
# create session state for the statistics if it doesn't exist already
if "stats" not in st.session_state:
    # we use a dictionary to track values for each different difficulty
    st.session_state["stats"] = {
        "easy":{
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
        },
        "normal":{
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
        },
        "hard":{
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
    }

# If the button gets clicked, the AI generates a word
with col2_:
    if st.button("Generate new word") :
        st.session_state["hint_displayed"] = False
        try:
            with st.spinner("Answer is being created …"): 
                resp = client.chat.completions.create(
                model="Qwen/Qwen3.8-27B-FP8",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}], # a spinner while the model is generating      
                    )

                try:
                    st.session_state["word"] = resp.choices[0].message.content.strip().upper() #so that the generated word uses capital letters and nothing else 
                    st.session_state["used_word"].append(st.session_state["word"]) #list with words that were already used so AI doesnt generate same word twice                    
                    st.toast(":green[Generated.]")
                except:
                    st.session_state["word_generated"] = False # set the flag back to false if it failed to generate
                    st.toast(":red[Failed to generate. Please try again.]")

            st.session_state["guess_counter"] = 0 # set guesses to 0 initially after word generation
            st.session_state["solved"] = False # reset "solved" for a new round
            st.session_state["stats"][word_difficulty]["games_played"] += 1 # advance the "games played" stat for that difficulty by one after word generation
            st.session_state["word_generated"] = True # mark that a word was generated
            st.session_state["current_word_diff"] = word_difficulty # mark the difficulty of the current game for stat tracking later
            st.session_state["hint_displayed"] = False # make the hint not be displayed (yet) for the new round
            st.session_state["no_hint_yet"] = False
            st.session_state["word_list"] = [] # a list gets created in which all guesses are saved later
        
        # API error handling
        except AuthenticationError:
            st.error("API was not accepted. Please check it.")

        except OpenAIError:
            st.error(
                "AI API request failed. Please check it and try again. "
            )

# make hint button in third column
with col3_:
    # Button to get a hint only works when a word is generated and not won
    if st.button("Hint") and st.session_state["solved"] == False and st.session_state["word_generated"] == True and st.session_state["hint_displayed"] == False:
        if st.session_state["guess_counter"] == 5 : # only at the last guess should you be able to get a hint
            # catch if no word is generated yet to plug into the AI prompt
            try:
                hint = f"give a riddle to guess {st.session_state['word']} without saying {st.session_state['word']}. Make sure that it actually rhymes." #AI prompt
            
            except:
                st.error("No word generated yet")

            try:
                with st.spinner(""): # a spinner while the model is generating
                    resp = client.chat.completions.create(
                    model="Qwen/Qwen3.8-27B-FP8",
                    max_tokens=8000,
                    messages=[{"role": "user", "content": hint}],    
                            )
                    st.session_state["hint"] = resp.choices[0].message.content
                    st.session_state["hint_displayed"] = True

            except AuthenticationError:
                st.error("API was not accept. Please check it.")

            except OpenAIError:
                st.error(
                    "AI API request failed. Please check it and try again. "
                )
            
        else:
            st.session_state["no_hint_yet"] = True


# this variable is used to prevent the submit button from checking an invalid input
stop = False

# check the inputs validity and make it upper case 
with st.form("textform", clear_on_submit=True, enter_to_submit=True, border=True):

    guess_ungereinigt = st.text_input(   #the guess can be submitted
         f"Enter a {wortlaenge} letter word.",
    )

    submitted = st.form_submit_button("Submit") 
    if submitted and st.session_state["solved"] == False and "word" in st.session_state: #when a word was submitted, and one was generated by ai
        guess = guess_ungereinigt.strip().upper() # removes spaces and makes everything upper letters
        if guess_ungereinigt == "42":
            st.snow()

        if (guess.lower() not in official_words or len(guess) != len(st.session_state["word"])) and (guess != st.session_state["word"]): # if the word is not an actual word or wrong length,
            st.error("Enter valid word!:confounded:")                                 # it is not supposed to keep using it so stop = True
            stop = True

# clearing/creating variables
guess_marked = []
letter_used=[]
# if the Submit button was pressed and the word wasn't guessed yet, but has been generated, compare guess with the word
if submitted and not st.session_state["solved"] and stop == False and "word" in st.session_state:

    st.session_state["guess_counter"] += 1 # increase the guess counter

    if st.session_state["guess_counter"] <= 6: # if the guess counter is 6 or less
        st.write(f"You submitted: {guess}. Guesses remaining: {6-st.session_state["guess_counter"]}") # displays the submit and the remaining guesses

        # append a 0 into a list for every letter of the guessed word
        # this variable helps us keep track of which letters in the word were already used to color a letter in our guess
        # this ensures that if our word only has one "o" for example, only one "o" in our submit is highlighted
        for i in range (len(guess)):
            letter_used.append(0)

        # comparing guessed word with wanted word letter by letter and coloring the letters accordingly
        for buchstabe in range(len(guess)):
            b1 = guess[buchstabe]
            b2 = st.session_state["word"][buchstabe]

            # count=0
            # if the letter is in the correct spot, make it green
            if b1 == b2:
                guess_marked.append(f":green[{b1}]")
                letter_used[buchstabe]=1

            # otherwise, search for the letter in the rest of the word:
            # and if it is in the word and not already used and not in the right spot, make it yellow 
            else:
                l_found = False
                for i in range(len(st.session_state["word"])):
                    # 
                    if b1 == st.session_state["word"][i] and letter_used[i]==0 and guess[i]!=st.session_state["word"][i]:
                        guess_marked.append(f":yellow[{b1}]") # make letter yellow
                        letter_used[i]=1 # mark the letter as used by making the 0 in its position a 1
                        l_found = True
                        break

                if not l_found: # letter is made red if it does not occour in our wanted word
                    guess_marked.append(f":red[{b1}]")
        # combines the colored letters of the current guess into a single string and adds it to the list of previous guesses
        st.session_state["word_list"].append(" ".join(guess_marked))

        # was the word guessed correctly?
        if guess == st.session_state['word']:
            st.success("Yeah! You did it!:partying::partying: "
                       "Generate a new word to keep playing!"
            )
            st.balloons()
            # first solve will be saved in "stats":
            if not st.session_state["solved"]:
                st.session_state["stats"][st.session_state["current_word_diff"]]["games_won"] += 1
                st.session_state["stats"][st.session_state["current_word_diff"]]["game_guesses"][st.session_state["guess_counter"]] += 1
            st.session_state["solved"] = True
            
        # guess is incorrect:
        else:
            # if all guesses were used, tell that the game ended 
            if st.session_state["guess_counter"] == 6:
                st.error("Oh no. The word is wrong.:dizzy_face:")
                #st.info(f"Debug info: The word is {st.session_state['word']}")
                st.error("You have used up all your guesses:sob:. " +f" The word was {st.session_state['word']}. " + "Please generate a new word and try again.")
    else:
        st.error("You have used up all your guesses:sob:. " +f"Debug info: The word was {st.session_state['word']}. " + "Please generate a new word and try again.")

if st.session_state["no_hint_yet"] == True: #if no hint is allowed yet
    if 6 > st.session_state["guess_counter"]:
        st.toast("Come on, try a few times first! The hint is only available for your last guess.")
    else:
        st.write("You lost this round, no hints available!")
# displays the hint. If the AI failed to generate one, inform the user
if st.session_state["hint_displayed"] == True:
    if not st.session_state["hint"] == None:
        st.write (st.session_state["hint"])
    else:
        st.toast("Hint failed to generate. :sob:")
# displays our guesses beneath one another
for a in st.session_state["word_list"]: #the wordlist should outputed in a different design
    st.markdown(
                    f"<div style='text-align: center; font-size: 32px; font-weight: bold; letter-spacing: 8px;'>\n\n{a}\n\n</div>",
                     unsafe_allow_html=True
                     )