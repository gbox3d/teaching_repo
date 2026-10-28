import streamlit as st

st.title("첫 Streamlit 앱")
st.write("입력한 값을 화면에 출력합니다.")
name = st.text_input("수업용 이름", value="student01")
if st.button("인사 출력"):
    st.write(f"{name}님, 안녕하세요.")
