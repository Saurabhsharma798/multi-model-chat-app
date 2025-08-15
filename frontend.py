import streamlit as st
import requests
import os



API_URL=os.environ.get("API_URL")

st.set_page_config(page_title="MultiModel ChatBot")
st.title("AI CHATBOT")
st.write("create and interact with ai agents!")

st.sidebar.title("navigation")
system_prompt=st.sidebar.text_area("Define your AI Agent",height=70,placeholder="type your system prompt here")

MODEL_GEMINI=["gemini-2.5-pro","gemini-2.5-flash","gemini-2.0-flash"]
MODEL_GROQ=["llama-3.1-8b-instant","llama-3.3-70b-versatile","openai/gpt-oss-120b"]

provider=st.sidebar.radio("select Provider",("GROQ","GEMINI"))

if provider=="GROQ":
    selected_model=st.sidebar.selectbox("SELECT GROQ MODEL",MODEL_GROQ)

elif provider=="GEMINI":
    selected_model=st.sidebar.selectbox("SELECT GEMINI MODEL",MODEL_GEMINI)


allow_web_search=st.sidebar.checkbox("ALLOW WEB SEARCH")


# user_query=st.text_area("enter your query",height=170,placeholder="ask your question")


if "messages" not in st.session_state:
    st.session_state['messages']=[]

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

user_query=st.chat_input("enter your query")


# if st.button("ASK AGENT"):
if user_query:
    if user_query==None:
        with st.chat_message("assistant"):
            st.write("please write something")
    st.session_state['messages'].append({'role':"user","content":user_query})
    with st.chat_message('user'):
        st.markdown(user_query)
    payload={
        "model_name":selected_model,
        "model_provider":provider,
        "system_prompt":system_prompt,
        "messages":[user_query],
        "allow_search":allow_web_search
    }

    response=requests.post(API_URL,json=payload)
    if response.status_code==200:
        response_data=response.json()
        if "error" in response_data:
            st.error(response_data["error"])
    
        with st.chat_message("assistant"):
            st.markdown(response_data)
        st.session_state['messages'].append({'role':"assistent","content":response_data})