import unittest
from pathlib import Path
from unittest.mock import patch

from langchain_core.messages import AIMessageChunk
from streamlit.testing.v1 import AppTest

import shared


EXAMPLES = Path(__file__).resolve().parents[1]


class ChatAppTests(unittest.TestCase):
    def setUp(self):
        model = self.enterContext(patch("langchain_ollama.ChatOllama"))
        self.stream = model.return_value.stream
        self.matches = [(2, 0.91, "도서관은 평일 오전 9시에 문을 연다.")]
        self.search = self.enterContext(patch("shared.retrieve", return_value=self.matches))

    def open_app(self, name):
        app = AppTest.from_file(str(EXAMPLES / "src" / name / "app.py")).run()
        self.assertFalse(app.exception)
        return app

    def ask(self, app, question):
        app.chat_input[0].set_value(question).run()
        self.assertFalse(app.exception)

    def test_chat_sends_three_turns_in_order_and_clears_history(self):
        self.stream.side_effect = [
            [
                AIMessageChunk(content="알겠", additional_kwargs={"reasoning_content": "숨긴 추론"}),
                AIMessageChunk(content="습니다."),
            ],
            [AIMessageChunk(content="두 사람이 총 4개를 먹었습니다.")],
            [AIMessageChunk(content="7 - 2 - 2 = "), AIMessageChunk(content="3개입니다.")],
            [AIMessageChunk(content="새 대화를 시작합니다.")],
        ]
        app = self.open_app("ex02_chat")
        questions = ["딸기가 7개 있습니다.", "저와 친구가 2개씩 먹었습니다.", "몇 개 남았나요?"]
        for question in questions:
            self.ask(app, question)

        sent = self.stream.call_args_list[2].args[0]
        self.assertEqual(sent[0]["role"], "system")
        self.assertEqual(sent[1:], [
            {"role": "user", "content": questions[0]},
            {"role": "assistant", "content": "알겠습니다."},
            {"role": "user", "content": questions[1]},
            {"role": "assistant", "content": "두 사람이 총 4개를 먹었습니다."},
            {"role": "user", "content": questions[2]},
        ])
        self.assertEqual(app.session_state["messages"][-1], {
            "role": "assistant", "content": "7 - 2 - 2 = 3개입니다.",
        })
        self.assertEqual(app.chat_message[-1].markdown[-1].value, "7 - 2 - 2 = 3개입니다.")

        app.sidebar.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["messages"], [])
        self.assertEqual(len(app.chat_message), 0)
        self.assertEqual(self.stream.call_count, 3)
        self.ask(app, "새 질문입니다.")
        self.assertEqual(self.stream.call_args.args[0][1:], [
            {"role": "user", "content": "새 질문입니다."},
        ])

    def test_empty_answers_warn_without_saving_and_allow_the_next_question(self):
        responses = {
            "no chunks": [],
            "empty content": [AIMessageChunk(content="")],
            "whitespace": [AIMessageChunk(content=" \n\t")],
            "reasoning only": [AIMessageChunk(
                content="", additional_kwargs={"reasoning_content": "아직 추론 중입니다."},
            )],
        }
        for name in ("ex02_chat", "ex03_rag"):
            for label, response in responses.items():
                with self.subTest(app=name, response=label):
                    self.stream.reset_mock()
                    self.stream.side_effect = [response, [AIMessageChunk(content="정상 답변입니다.")]]
                    app = self.open_app(name)
                    self.ask(app, "첫 질문입니다.")
                    self.assertTrue(app.warning)
                    self.assertIn("답변", app.warning[0].value)
                    self.assertEqual(app.session_state["messages"], [
                        {"role": "user", "content": "첫 질문입니다."},
                    ])
                    self.assertNotIn("아직 추론 중입니다.", "\n".join(m.value for m in app.markdown))

                    self.ask(app, "다음 질문입니다.")
                    self.assertFalse(app.warning)
                    self.assertEqual(app.session_state["messages"], [
                        {"role": "user", "content": "첫 질문입니다."},
                        {"role": "user", "content": "다음 질문입니다."},
                        {"role": "assistant", "content": "정상 답변입니다."},
                    ])
                    self.assertEqual(self.stream.call_count, 2)

    def test_rag_displays_and_sends_retrieved_evidence(self):
        self.stream.return_value = [AIMessageChunk(content="평일 오전 9시입니다. [문단 2]")]
        app = self.open_app("ex03_rag")
        self.ask(app, "도서관은 언제 문을 여나요?")

        self.search.assert_called_once_with(
            shared.DOCUMENT.read_text(encoding="utf-8"), "도서관은 언제 문을 여나요?",
        )
        sent = self.stream.call_args.args[0]
        self.assertIn("[문단 2] " + self.matches[0][2], sent[0]["content"])
        evidence = next(e for e in app.expander if e.label == "검색한 문단")
        displayed = "\n".join(m.value for m in evidence.markdown)
        self.assertIn("문단 2, 유사도 0.910", displayed)
        self.assertIn(self.matches[0][2], displayed)
        self.assertFalse(app.warning)
        self.assertEqual(app.session_state["messages"][-1]["content"], "평일 오전 9시입니다. [문단 2]")

    def test_rag_saves_a_nonempty_answer_when_no_evidence_matches(self):
        self.search.return_value = []
        answer = "자료에서 해당 정보를 찾을 수 없습니다."
        self.stream.return_value = [AIMessageChunk(content=answer)]
        app = self.open_app("ex03_rag")
        self.ask(app, "자료에 없는 정보도 알려 주세요.")

        self.assertFalse(app.warning)
        self.assertEqual(app.session_state["messages"][-1], {"role": "assistant", "content": answer})
        self.assertEqual(app.chat_message[-1].markdown[-1].value, answer)


if __name__ == "__main__":
    unittest.main()
