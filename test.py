import openai
import streamlit as st
from streamlit_chat import message
from fakeyou import FakeYou
import winsound
from threading import Thread

if "fake" not in st.session_state:
    st.session_state.fake = FakeYou()
    st.session_state.fake.login("MustafaCAN", password="DExvc5JhJ6bsWfW")
    st.session_state.fake_file_name = "output.mp3"

if "history" not in st.session_state:
    st.session_state.history = [{"role": "system", 
                                 "content": "I want you to act as Pewdiepie. Which is a known Youtuber. I will type my sentences and you will reply with what the Pewdiepie would respond. I want you to only reply with the natural-sounding Pewdiepie comments, then continue with follow-up questions or initiatives and nothing else. Do not write explanations. Do not explain unless I instruct you to do so."}]

def change_key():
    st.session_state.openai_key = st.session_state.openai_key

def execute_openai():

    # check for openai key
    if not st.session_state.openai_key:
        st.error("Please enter an OpenAI key")
        return
    
    # check for input
    if st.session_state.input:
        st.session_state.history.append({"role": "user", "content": st.session_state.input})
    else:
        st.error("Please enter a message")
        return
    
    # embed the key & run the model
    openai.api_key = st.session_state.openai_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.history
    )

    # add the response to the history
    st.session_state.output = response.choices[0].message.content
    st.session_state.history.append({"role": "assistant", "content": f'''{response.choices[0].message.content}'''})
    Thread(target=vocalize_output, name="vocalize_thread", args=(st.session_state.fake, st.session_state.fake_file_name, st.session_state.output)).start()
    print_history()
    clear_input()

def vocalize_output(fake, file_name, output):
    save_output(fake, file_name, output)
    winsound.PlaySound(file_name, winsound.SND_FILENAME)

def save_output(fake, file_name, output):
    res = fake.make_tts_job(output, "TM:qmr1mfe2zs46")
    poll_res = fake.tts_poll(res)
    poll_res.save(file_name)

def print_history():
    # print the history if its not system & clear the input
    for i in st.session_state.history:
        if i["role"] == "system":
            continue
        elif i["role"] == "assistant":
            message(f'''{i["content"]}''', is_user=False)
        else:
            message(i["content"], is_user=True)

def clear_input():
    st.session_state.input = ""


st.text_input("Type something", key="input", on_change=execute_openai, placeholder="Hello, how are you?")
st.text_input("OpenAI Key", key="openai_key", on_change=change_key, placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
