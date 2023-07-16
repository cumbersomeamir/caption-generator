import openai
import streamlit as st
from streamlit_chat import message
import re
import os

count = 0
openai.api_key = os.getenv('OPENAI_API_KEY')

#Code to hide the made with streamlit text
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)







def generate_response(prompt, num_lines, writer, emotion, target, lit_device, language):

    context = prompt
    
    content = f"This is the initial caption {context}. Give me a {language} caption which is {num_lines} lines long, expressing {emotion} emotions, written in the style of {writer}, using {lit_device} as the literary device, targeting the following audience: {target}"

    
    print(content)
    
    response = openai.ChatCompletion.create(
                                        model="gpt-3.5-turbo",
                                        messages=[{"role": "user", "content": content}]
                                            )
    
    message = response['choices'][0]['message']['content']
    return message

# EXECUTION OF THE PROGRAM STARTS HERE

st.title("Captioner - Write the best captions")
st.info(":arrow_left: Mobile Users please tap > to view filters")

# Add sliders, text inputs, and button to the right sidebar
with st.sidebar:
    num_lines = st.slider('Lines to Generate', min_value=1, max_value=5, value=1)
    writer = st.text_input("Writing Style (Ex. Elon Musk, Charles Bukowski)","")
    emotion = st.select_slider('Emotion', options=['happy', 'nostalgic', 'humorous','mysterious','romantic','calm','sarcastic', 'sad'])
    target = st.select_slider('Target Audience', options=['adults', 'teenagers', 'kids'])
    lit_device = st.selectbox('Literary Device', options=['Rhyming', 'Simile', 'Alliteration', 'Metaphor', 'Personification', 'Hyperbole', 'Onomatopoeia', 'Oxymoron', 'Pun'])
    language = st.selectbox('Language', options=['English', 'Hindi', 'Malay', 'Mandarin', 'Spanish', 'French'])

# Storing the chat

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text

prompt = get_text()

if prompt:
    output = generate_response(prompt, num_lines, writer, emotion, target, lit_device, language)
    # Save the output
    st.session_state.past.append(prompt)
    st.session_state.generated.append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1,-1,-1):
        message(st.session_state['generated'][i], key = str(i))
        message(st.session_state['past'][i], is_user =True, key=str(i)+ '_user')
