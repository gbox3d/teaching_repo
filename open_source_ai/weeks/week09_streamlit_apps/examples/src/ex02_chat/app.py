import streamlit as st

from shared import CHAT_PROMPT, stream_text

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
    messages = [{"role": "system", "content": CHAT_PROMPT}, *st.session_state.messages]
    with st.chat_message("assistant"):
        answer = st.write_stream(stream_text(messages))
        if answer and answer.strip():
            st.session_state.messages.append({"role": "assistant", "content": answer})
        else:
            st.warning("모델이 답변 본문을 보내지 않았습니다. 질문을 다시 입력하세요.")
