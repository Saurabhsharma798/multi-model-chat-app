import streamlit as st

st.title("Chatbot")

if "messages" not in st.session_state:
    st.session_state['messages'] = [] 


st.sidebar.title("Choose Model")


for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# chat interface
if prompt:= st.chat_input("enter your query"):
    st.session_state['messages'].append({"role":"user","content":prompt})
    with st.chat_message('user'):
        st.markdown(prompt)


    with st.chat_message('assistant'):
        response=st.write('hello')
    st.session_state['messages'].append({'role':"assistent","content":response})