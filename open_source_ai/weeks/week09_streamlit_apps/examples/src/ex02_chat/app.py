import streamlit as st

from shared import stream_text

st.title("로컬 AI 대화")
if "messages" not in st.session_state:
    st.session_state.messages = []
if st.sidebar.button("대화 지우기"):
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("질문을 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    messages = [{"role": "system", "content": "한국어로 짧게 답한다."}, *st.session_state.messages]
    with st.chat_message("assistant"):
        answer = st.write_stream(stream_text(messages))
    st.session_state.messages.append({"role": "assistant", "content": answer})
