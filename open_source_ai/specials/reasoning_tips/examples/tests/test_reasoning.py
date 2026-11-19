import sys
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from io import StringIO
from unittest.mock import Mock, patch

from langchain_core.messages import AIMessage, AIMessageChunk

import ex01_baseline
import ex02_observe
import ex03_recover
import shared
from shared import recovery


EXAMPLES = (ex01_baseline, ex02_observe, ex03_recover)


class ReasoningStreamTests(unittest.TestCase):
    def setUp(self):
        self.enterContext(patch("shared.REASONING", True))
        self.enterContext(patch("shared.TYPE_DELAY", 0))
        self.console = sys.stdout
        self.output = self.enterContext(redirect_stdout(StringIO()))
        self.model = Mock()
        self.messages = [
            ("system", shared.CHAT_PROMPT),
            ("human", "딸기가 7개 있습니다."),
            ("ai", "알겠습니다."),
            ("human", "2개를 먹으면 몇 개 남나요?"),
        ]
        self.closed = 0

    def chunks(self, *parts):
        try:
            yield from parts
        finally:
            self.closed += 1

    def answer(self, limit=2048):
        return recovery.answer_with_recovery(self.model, self.messages, limit=limit)

    def test_complete_answer_preserves_whitespace_without_retrying(self):
        self.model.stream.return_value = self.chunks(
            AIMessageChunk(content="\n"), AIMessageChunk(content="  5개입니다."), AIMessageChunk(content="\n"),
        )
        self.assertEqual(self.answer(), "\n  5개입니다.\n")
        self.model.stream.assert_called_once_with(self.messages)
        self.assertIn("\n  5개입니다.\n", self.output.getvalue())
        self.assertNotIn("추론>", self.output.getvalue())
        self.assertEqual(self.closed, 1)

    def test_answer_in_the_limit_chunk_takes_priority_over_reasoning(self):
        self.model.stream.return_value = self.chunks(
            AIMessageChunk(content="", additional_kwargs={"reasoning_content": "a" * 8}),
            AIMessageChunk(content="7 - 2 = ", additional_kwargs={"reasoning_content": "x" * 32}),
            AIMessageChunk(content="5개입니다."),
        )
        self.assertEqual(self.answer(limit=16), "7 - 2 = 5개입니다.")
        self.model.stream.assert_called_once()
        self.assertIn("추론> " + "a" * 8 + "x" * 8 + "\nAI> 7 - 2 = 5개입니다.", self.output.getvalue())
        self.assertEqual(self.output.getvalue().count("추론> "), 1)
        self.assertNotIn("이어 씁니다", self.output.getvalue())
        self.assertEqual(self.closed, 1)

    def test_limit_closes_before_continuation_and_leaves_history_unchanged(self):
        original = deepcopy(self.messages)
        thought = "Count the strawberries before subtracting."

        def first_stream():
            try:
                yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": thought})
                self.fail("추론 한도에 도달한 뒤 다음 청크를 요청했습니다.")
            finally:
                self.closed += 1

        def requests(messages):
            if messages is self.messages:
                return first_stream()
            self.assertEqual(self.closed, 1)
            return self.chunks(AIMessageChunk(content="5개입니다."))

        self.model.stream.side_effect = requests
        self.assertEqual(self.answer(limit=16), "5개입니다.")
        self.assertEqual(self.messages, original)
        continuation = self.model.stream.call_args.args[0]
        self.assertEqual(continuation[:-1], original)
        self.assertIsInstance(continuation[-1], AIMessage)
        self.assertEqual(continuation[-1].content, "\n")
        self.assertEqual(continuation[-1].additional_kwargs["reasoning_content"], thought[:16])
        self.assertTrue(all(not call.kwargs for call in self.model.stream.call_args_list))
        self.assertIn("한도", self.output.getvalue())
        self.assertIn("추론> " + thought[:16] + "\n", self.output.getvalue())
        self.assertEqual(self.output.getvalue().count("추론> "), 1)
        self.assertRegex(
            self.output.getvalue(),
            r"(?s)추론> [^\n]+\n.*수집한 추론 16자에서 답변을 이어 씁니다\.\nAI> 5개입니다\.",
        )
        self.assertEqual(self.closed, 2)

    def test_repetition_requires_three_completed_normalized_sentences_of_twenty_characters(self):
        sentence = "Count all the fruit!"  # 19 letters and spaces before the delimiter
        self.assertFalse(recovery.repeats_sentence(sentence * 3))
        twenty = "Count all the fruits"
        self.assertEqual(len(twenty), 20)
        unfinished = twenty + ". " + twenty.upper() + "! " + "count   all the fruits"
        self.assertFalse(recovery.repeats_sentence(unfinished))
        self.assertTrue(recovery.repeats_sentence(unfinished + "."))

    def test_sentence_repeated_across_chunks_stops_on_the_third_occurrence(self):
        sentence = "I should count the fruit in chronological order.\n"

        def repeated():
            try:
                for _ in range(3):
                    yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": sentence[:15]})
                    yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": sentence[15:]})
                self.fail("같은 문장의 네 번째 반복을 요청했습니다.")
            finally:
                self.closed += 1

        self.model.stream.side_effect = [repeated(), self.chunks(AIMessageChunk(content="5개입니다."))]
        self.assertEqual(self.answer(), "5개입니다.")
        prefix = self.model.stream.call_args.args[0][-1]
        self.assertEqual(prefix.additional_kwargs["reasoning_content"], sentence * 3)
        self.assertIn("세 번", self.output.getvalue())
        self.assertEqual(self.closed, 2)

    def test_continuation_uses_only_the_remaining_reasoning_budget(self):
        def continuation():
            try:
                yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": "xyz"})
                yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": "uvw"})
                self.fail("두 요청의 추론 글자 수 합계가 한도를 넘었습니다.")
            finally:
                self.closed += 1

        self.model.stream.side_effect = [
            self.chunks(AIMessageChunk(content="", additional_kwargs={"reasoning_content": "abcd"})),
            continuation(),
        ]
        self.assertEqual(self.answer(limit=10), "")
        self.assertEqual(self.model.stream.call_count, 2)
        self.assertIn("추론> abcd\n", self.output.getvalue())
        self.assertIn("추론> xyzuvw\n", self.output.getvalue())
        self.assertEqual(self.output.getvalue().count("추론> "), 2)
        self.assertEqual(self.closed, 2)

    def test_two_empty_attempts_end_without_a_blank_answer_or_history_change(self):
        original = deepcopy(self.messages)
        self.model.stream.side_effect = [
            self.chunks(AIMessageChunk(content="")),
            self.chunks(AIMessageChunk(content=" \n\t")),
        ]
        self.assertEqual(self.answer(), "")
        self.assertEqual(self.model.stream.call_count, 2)
        self.assertIn("한 번 더", self.output.getvalue())
        self.assertNotIn("추론>", self.output.getvalue())
        self.assertEqual([call.args[0] for call in self.model.stream.call_args_list], [original, original])
        self.assertEqual(self.messages, original)
        self.assertEqual(self.closed, 2)

    def test_stream_failure_closes_and_does_not_replay_the_partial_answer(self):
        def interrupted():
            try:
                yield AIMessageChunk(content="부분 답변")
                raise ConnectionError("stream interrupted")
            finally:
                self.closed += 1

        self.model.stream.return_value = interrupted()
        with patch("shared.type_text", wraps=shared.type_text) as display:
            with self.assertRaises(ConnectionError):
                self.answer()
        display.assert_called_once_with("부분 답변")
        self.model.stream.assert_called_once()
        self.assertEqual(self.closed, 1)

    def test_output_failure_or_keyboard_interrupt_closes_without_retrying(self):
        for error in (BrokenPipeError("output closed"), KeyboardInterrupt()):
            with self.subTest(error=type(error).__name__):
                self.closed = 0
                self.model.stream.reset_mock()
                self.model.stream.return_value = self.chunks(
                    AIMessageChunk(content="첫 조각"), AIMessageChunk(content="다음 조각"),
                )
                with patch("shared.type_text", side_effect=error) as display:
                    with self.assertRaises(type(error)):
                        self.answer()
                display.assert_called_once_with("첫 조각")
                self.model.stream.assert_called_once()
                self.assertEqual(self.closed, 1)

    def test_received_chunks_are_displayed_before_requesting_the_next_chunk(self):
        events = []

        def arriving():
            try:
                for text in ("첫 조각", "다음 조각"):
                    events.append(("receive", text))
                    yield AIMessageChunk(content=text)
            finally:
                events.append(("close", None))

        self.model.stream.return_value = arriving()
        with patch("shared.type_text", side_effect=lambda text: events.append(("display", text))):
            self.assertEqual(self.answer(), "첫 조각다음 조각")
        self.assertEqual(events, [
            ("receive", "첫 조각"), ("display", "첫 조각"),
            ("receive", "다음 조각"), ("display", "다음 조각"), ("close", None),
        ])

    def test_reasoning_chunks_are_flushed_immediately_without_typing_delay(self):
        thought = ["먼저 수를\n", "확인한다."]

        def arriving():
            try:
                yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": thought[0]})
                self.assertEqual(self.output.getvalue(), "추론> " + thought[0])
                self.assertGreater(flush.call_count, 0)
                first_flushes = flush.call_count
                type_text.assert_not_called()
                sleep.assert_not_called()
                yield AIMessageChunk(content="", additional_kwargs={"reasoning_content": thought[1]})
                self.assertEqual(self.output.getvalue(), "추론> " + "".join(thought))
                self.assertGreater(flush.call_count, first_flushes)
                type_text.assert_not_called()
                sleep.assert_not_called()
                yield AIMessageChunk(content="5개입니다.")
            finally:
                self.closed += 1

        self.model.stream.return_value = arriving()
        with (
            patch.object(self.output, "flush", wraps=self.output.flush) as flush,
            patch("shared.type_text", wraps=shared.type_text) as type_text,
            patch("shared.sleep") as sleep,
        ):
            self.assertEqual(self.answer(), "5개입니다.")
        type_text.assert_called_once_with("5개입니다.")
        self.assertIn("추론> " + "".join(thought) + "\nAI> 5개입니다.", self.output.getvalue())
        self.assertEqual(self.output.getvalue().count("추론> "), 1)
        self.assertEqual(self.closed, 1)

    def test_reasoning_disabled_requests_only_once_even_for_an_empty_answer(self):
        self.model.stream.return_value = self.chunks(AIMessageChunk(content=" \n"))
        with patch("shared.REASONING", False):
            self.assertEqual(self.answer(), "")
        self.model.stream.assert_called_once_with(self.messages)
        self.assertNotIn("한 번 더", self.output.getvalue())
        self.assertEqual(self.closed, 1)

    def test_create_model_sets_reasoning_and_generation_budget(self):
        for enabled in (True, False):
            with (
                self.subTest(reasoning=enabled),
                patch("shared.REASONING", enabled),
                patch("shared.ChatOllama", return_value=self.model) as constructor,
            ):
                self.assertIs(shared.create_model(), self.model)
                constructor.assert_called_once()
                self.assertIs(constructor.call_args.kwargs["reasoning"], enabled)
                self.assertEqual(constructor.call_args.kwargs["num_predict"], 128)
                self.assertEqual(constructor.call_args.kwargs["temperature"], 0)

    def test_terminal_keeps_completed_answers_and_clear_starts_a_new_history(self):
        thought = "7개를 기억한다.\n다음 질문에서 수량을 확인한다."
        self.model.stream.side_effect = [
            self.chunks(
                AIMessageChunk(content="알겠", additional_kwargs={"reasoning_content": thought}),
                AIMessageChunk(content="습니다."),
            ),
            self.chunks(AIMessageChunk(content="5개입니다.")),
            self.chunks(AIMessageChunk(content="새 대화입니다.")),
        ]
        questions = ["딸기가 7개 있습니다.", "2개를 먹으면 몇 개 남나요?", "새 질문입니다."]
        with (
            patch("shared.ChatOllama", return_value=self.model),
            patch("builtins.input", side_effect=["  ", *questions[:2], "/clear", questions[2], "/bye"]),
        ):
            ex03_recover.main()

        self.assertEqual(self.model.stream.call_count, 3)
        self.assertIn("추론> " + thought + "\nAI> 알겠습니다.", self.output.getvalue())
        first, second, fresh = [call.args[0] for call in self.model.stream.call_args_list]
        for sent in (first, second, fresh):
            self.assertEqual(sent[0], ("system", shared.CHAT_PROMPT))
        self.assertEqual(second[1:], [
            ("human", questions[0]), ("ai", "알겠습니다."), ("human", questions[1]),
        ])
        self.assertEqual(fresh[1:], [("human", questions[2])])
        self.assertEqual(self.closed, 3)

    def test_terminal_does_not_save_empty_answers_and_accepts_followup_questions(self):
        self.model.stream.side_effect = [
            self.chunks(AIMessageChunk(content="")),
            self.chunks(AIMessageChunk(content=" \n")),
            self.chunks(AIMessageChunk(content="정상 답변입니다.")),
            self.chunks(AIMessageChunk(content="후속 답변입니다.")),
        ]
        with (
            patch("shared.ChatOllama", return_value=self.model),
            patch("builtins.input", side_effect=["첫 질문", "다음 질문", "후속 질문", "/bye"]),
        ):
            ex03_recover.main()

        self.assertEqual(self.model.stream.call_count, 4)
        self.assertIn("답변 본문을 보내지 않았습니다", self.output.getvalue())
        after_empty = self.model.stream.call_args_list[2].args[0]
        self.assertEqual(after_empty[1:], [("human", "첫 질문"), ("human", "다음 질문")])
        followup = self.model.stream.call_args_list[3].args[0]
        self.assertEqual(followup[1:], [
            *after_empty[1:], ("ai", "정상 답변입니다."), ("human", "후속 질문"),
        ])
        self.assertEqual(self.closed, 4)

    def test_terminal_exits_at_eof_without_requesting_a_model_response(self):
        for example in EXAMPLES:
            with (
                self.subTest(example=example.__name__),
                patch("shared.ChatOllama", return_value=self.model),
                patch("builtins.input", side_effect=EOFError),
            ):
                example.main()
                self.model.invoke.assert_not_called()
                self.model.stream.assert_not_called()

    def test_invoke_examples_send_only_the_current_question_and_skip_reserved_input(self):
        for example in (ex01_baseline, ex02_observe):
            with self.subTest(example=example.__name__):
                self.model = Mock()
                self.model.invoke.side_effect = [AIMessage(content="첫 답변"), AIMessage(content="다음 답변")]
                with (
                    patch("shared.ChatOllama", return_value=self.model),
                    patch("builtins.input", side_effect=[" ", "첫 질문", "/clear", "다음 질문", "/bye"]),
                ):
                    example.main()
                self.assertEqual([call.args[0] for call in self.model.invoke.call_args_list], [
                    [("system", shared.CHAT_PROMPT), ("human", "첫 질문")],
                    [("system", shared.CHAT_PROMPT), ("human", "다음 질문")],
                ])
                self.assertTrue(all(not call.kwargs for call in self.model.invoke.call_args_list))
                self.model.stream.assert_not_called()
                self.assertIn("첫 답변", self.output.getvalue())
                self.assertIn("다음 답변", self.output.getvalue())
                self.assertNotIn("추론>", self.output.getvalue())

    def test_observation_reports_aggregated_counts_and_done_reason_after_one_invoke(self):
        thought = "먼저 수를 계산한다.\n7 - 2를 확인한다.\n"
        body = "\n5개입니다."
        for done_reason in ("stop", None):
            with self.subTest(done_reason=done_reason):
                self.output.seek(0)
                self.output.truncate(0)
                self.model.invoke.reset_mock()
                self.model.invoke.return_value = AIMessage(
                    content=body, additional_kwargs={"reasoning_content": thought},
                    response_metadata={"done_reason": done_reason} if done_reason else {},
                )
                with patch("shared.ChatOllama", return_value=self.model), patch(
                    "builtins.input", side_effect=["질문입니다.", "/bye"],
                ):
                    ex02_observe.main()
                printed = self.output.getvalue()
                summary = f"추론 {len(thought)}자 · 본문 {len(body)}자 · 종료 사유: {done_reason or '미제공'}"
                self.assertIn("추론> " + thought, printed)
                self.assertIn(summary, printed)
                self.assertIn(body, printed)
                self.assertLess(printed.index("추론> " + thought), printed.index(summary))
                self.assertLess(printed.index(summary), printed.index("AI>"))
                self.assertEqual(printed.count("추론> "), 1)
                self.model.invoke.assert_called_once_with([
                    ("system", shared.CHAT_PROMPT), ("human", "질문입니다."),
                ])
                self.model.stream.assert_not_called()

    def test_same_reasoning_only_response_compares_all_three_steps(self):
        thought = "딸기가 7개이고 2개를 먹었으므로 남은 수를 계산한다."
        for example in EXAMPLES:
            with self.subTest(example=example.__name__):
                self.closed = 0
                self.model = Mock()
                self.output.seek(0)
                self.output.truncate(0)
                response = {
                    "content": "", "additional_kwargs": {"reasoning_content": thought},
                    "response_metadata": {"done_reason": "length"},
                }
                original = deepcopy(self.messages)
                if example is ex03_recover:
                    self.model.stream.side_effect = [
                        self.chunks(AIMessageChunk(**response)),
                        self.chunks(AIMessageChunk(content="7 - 2 = 5개입니다.")),
                    ]
                    answer = self.answer()
                    self.assertEqual(answer, "7 - 2 = 5개입니다.")
                    self.assertIn(answer, self.output.getvalue())
                    prefix = self.model.stream.call_args.args[0][-1]
                    self.assertEqual(prefix.additional_kwargs["reasoning_content"], thought)
                    self.assertEqual(prefix.content, "\n")
                    self.assertEqual(self.model.stream.call_count, 2)
                    self.model.invoke.assert_not_called()
                    self.assertEqual(self.closed, 2)
                    printed = self.output.getvalue()
                    self.assertIn("추론> " + thought + "\n", printed)
                    self.assertIn("\nAI> " + answer, printed)
                    self.assertLess(printed.index("추론> "), printed.index("이어 씁니다."))
                    self.assertLess(printed.index("이어 씁니다."), printed.index("AI> "))
                    self.assertEqual(printed.count("추론> "), 1)
                else:
                    self.model.invoke.return_value = AIMessage(**response)
                    with patch("shared.ChatOllama", return_value=self.model), patch(
                        "builtins.input", side_effect=["2개를 먹으면 몇 개 남나요?", "/bye"],
                    ):
                        example.main()
                    self.model.invoke.assert_called_once()
                    self.model.stream.assert_not_called()
                    self.assertIn("답변 본문을 보내지 않았습니다", self.output.getvalue())
                printed = self.output.getvalue()
                if example is ex02_observe:
                    summary = f"추론 {len(thought)}자 · 본문 0자 · 종료 사유: length"
                    self.assertIn("추론> " + thought + "\n", printed)
                    self.assertIn(summary, printed)
                    self.assertLess(printed.index("추론> "), printed.index(summary))
                    self.assertLess(printed.index(summary), printed.index("AI>"))
                elif example is ex01_baseline:
                    self.assertNotIn("추론>", printed)
                    self.assertNotIn(thought, printed)
                self.assertEqual(self.messages, original)
                print(f"\n[{example.__name__}: 동일 모의 응답의 실제 출력]\n{printed}", file=self.console)


class TypeTextTests(unittest.TestCase):
    def test_tty_types_korean_characters_with_flush_and_delay_in_order(self):
        self.assertEqual(shared.TYPE_DELAY, 0.03)
        text = "한글 여러자"
        events = []
        terminal = Mock()
        terminal.isatty.return_value = True
        terminal.write.side_effect = lambda value: events.append(("write", value)) if value else None
        terminal.flush.side_effect = lambda: events.append(("flush", None))
        with (
            patch("sys.stdout", terminal),
            patch("shared.sleep", side_effect=lambda delay: events.append(("sleep", delay))),
        ):
            shared.type_text(text)
        expected = []
        for character in text:
            expected.extend([("write", character), ("flush", None), ("sleep", 0.03)])
        self.assertEqual(events, expected)

    def test_non_tty_or_zero_delay_writes_a_whole_chunk_without_sleeping(self):
        for is_tty, delay in ((False, 0.03), (True, 0)):
            with self.subTest(is_tty=is_tty, delay=delay):
                output = Mock()
                output.isatty.return_value = is_tty
                with patch("sys.stdout", output), patch("shared.TYPE_DELAY", delay), patch("shared.sleep") as sleep:
                    shared.type_text("한글 여러자")
                writes = [call.args[0] for call in output.write.call_args_list if call.args[0]]
                self.assertEqual(writes, ["한글 여러자"])
                sleep.assert_not_called()

    def test_empty_text_does_not_delay_the_terminal(self):
        terminal = Mock()
        terminal.isatty.return_value = True
        with patch("sys.stdout", terminal), patch("shared.TYPE_DELAY", 0.03), patch("shared.sleep") as sleep:
            shared.type_text("")
        self.assertFalse(any(call.args[0] for call in terminal.write.call_args_list))
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
