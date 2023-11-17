import os
import time
import streamlit as st
from openai import OpenAI

# Helpful functions
def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id = thread.id,
            run_id = run.id,
        )
        time.sleep(1.5)
    return run

def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order='asc')

def pretty_print(messages):
    for m in messages:
        if m.role == "assistant":
          return f"{m.content[0].text.value}"

# Streamlit interface
title, logo = st.columns([3,1])
with title:
    st.title(':100: BaeGPT')
    st.header(':rocket: 인생의 궁금한 뭐든지 물어보세요! 영어, 한글 모두 가능해요')
with logo:
    st.image('img/YGB20231116C.png')

#Authenticate
open_ai_key = os.environ["OPEN_AI_KEY"]

client = OpenAI(api_key = open_ai_key)

#Retrieve Assistant: RiskGPT
assistant_id = 'asst_ItjOa3iOaYSOoUKCAvy0cGkc'
assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)

# Take User Input
user_message = st.text_input("Your question/질문해 보세요:", "")

# Create a new Thread
thread = client.beta.threads.create()

if st.button("Advise Me"):
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_message
    )

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )

    run = wait_on_run(run,thread)

    st.write("Here is our advice: ", pretty_print(get_response(thread)))