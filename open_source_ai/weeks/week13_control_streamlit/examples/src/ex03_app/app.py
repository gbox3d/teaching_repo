import streamlit as st
from shared import Board, MODELS_DIR, needle_predictor, trained_path

st.set_page_config(page_title="작은 모델로 LED 제어")
st.title("작은 모델로 LED 제어")
st.caption("12주차에 학습한 Needle 모델로 제어합니다. 요청마다 대화 문맥을 초기화합니다.")


@st.cache_resource
def load_predictor(path):
    return needle_predictor(path)


try:
    path = trained_path(MODELS_DIR)
except (RuntimeError, FileNotFoundError) as error:
    st.error(str(error))
    st.stop()

if st.button("시뮬레이터 연결", disabled="board" in st.session_state):
    try:
        st.session_state.board = Board()
        st.rerun()
    except Exception as error:
        st.error(f"연결 실패: {error}")

if st.button("연결 해제", disabled="board" not in st.session_state):
    st.session_state.pop("board").close()
    st.rerun()

connection_status = st.empty()
st.caption("한 PC에서는 제어 창 하나만 사용하세요. 연결·해제 시 LED 상태는 유지됩니다. 다른 연결의 제어 명령은 같은 보드에 반영됩니다.")
with st.form("control"):
    question = st.text_input("제어 요청", placeholder="2번 LED 밝기를 75로 맞춰 줘")
    submitted = st.form_submit_button("요청 실행")

if submitted:
    if "board" not in st.session_state:
        st.warning("먼저 시뮬레이터에 연결하세요.")
    elif not question.strip():
        st.warning("제어 요청을 입력하세요.")
    else:
        try:
            with st.spinner("모델 호출 중"):
                calls = load_predictor(str(path))(question.strip())
            st.write("모델이 제안한 호출")
            st.json(calls)
            if calls:
                st.write("실행 응답", st.session_state.board.execute(calls))
            else:
                st.info("실행할 호출이 없습니다.")
        except Exception as error:
            st.error(f"요청 실패: {error}")
            if st.session_state.board.closed:
                st.warning("연결 해제를 누른 뒤 다시 연결하세요.")

if "board" in st.session_state:
    try:
        st.write("현재 LED 밝기", st.session_state.board.state()["leds"])
    except Exception as error:
        st.error(f"상태 확인 실패: {error}")
connected = "board" in st.session_state and not st.session_state.board.closed
connection_status.caption("연결됨" if connected else "연결 안 됨")
st.caption("종료할 때 연결 해제를 누른 뒤 실행 터미널에서 Ctrl+C를 누르세요.")
