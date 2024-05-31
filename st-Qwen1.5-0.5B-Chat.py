import streamlit as st
import time
import sys
from openai import OpenAI
# Internal usage
import os
from time import sleep

if "hf_model" not in st.session_state:
    st.session_state.hf_model = "Qwen1.5-0.5B-Chat"
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def create_client():   
    client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")
    return client

# FUNCTION TO LOG ALL CHAT MESSAGES INTO chathistory.txt
def writehistory(text):
    with open('chathistorywen05b.txt', 'a', encoding='utf-8') as f:
        f.write(text)
        f.write('\n')
    f.close()

#AVATARS
av_us = '🧑‍💻'  # './man.png'  #"🦖"  #A single emoji, e.g. "🧑‍💻", "🤖", "🦖". Shortcodes are not supported.
av_ass = "🤖"   #'./robot.png'

### START STREAMLIT UI
st.image('./banner.png', )
st.markdown('---')

client = create_client()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message(message["role"],avatar=av_us):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"],avatar=av_ass):
            st.markdown(message["content"])
# Accept user input
if myprompt := st.chat_input("What is an AI model?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": myprompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=av_us):
        st.markdown(myprompt)
        usertext = f"user: {myprompt}"
        writehistory(usertext)
        # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        res = client.chat.completions.create(
            model="local-model", # this field is currently unused
            messages=st.session_state.messages,
            temperature=0.45,
            stream=True,
        )

        new_message = {"role": "assistant", "content": ""}
        
        for chunk in res:
            if chunk.choices[0].delta.content:
                full_response+=chunk.choices[0].delta.content
                message_placeholder.markdown(full_response+ "▌")

        message_placeholder.markdown(full_response)
        asstext = f"assistant: {full_response}"
        writehistory(asstext)       
        st.session_state.messages.append({"role": "assistant", "content": full_response})