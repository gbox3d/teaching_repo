"""State independence, atomic changes and concurrent input delivery contracts."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from pathlib import Path
import subprocess
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import simulator
from session import BoardSession, SessionClosed


class ModelTests(unittest.TestCase):
    def test_pure_transition_keeps_previous_state(self):
        original = simulator.State()
        changed, events = simulator.set_leds(original, [0, 3], 128)
        self.assertEqual(original.leds, (0, 0, 0, 0))
        self.assertEqual(changed.leds, (128, 0, 0, 128))
        self.assertEqual(events, ())
        with self.assertRaises(FrozenInstanceError):
            changed.blink = True

    def test_invalid_multi_field_update_is_atomic(self):
        session = BoardSession()
        before = session.snapshot()
        for values in ([0, 4], [True], [], [-1]):
            with self.subTest(indices=values), self.assertRaises(ValueError):
                session.set_leds(values, 255)
        for value in (True, "20", float("nan"), float("inf"), 10**1000):
            with self.subTest(value=type(value)), self.assertRaises(ValueError):
                session.set_environment(10.5, value)
        self.assertEqual(session.snapshot(), before)
        for value in (True, 1.5, -1, 256):
            with self.subTest(brightness=value), self.assertRaises(ValueError):
                session.set_leds([0], value)
        self.assertEqual(session.snapshot(), before)

    def test_concurrent_input_is_ordered_without_any_transport(self):
        session = BoardSession(history_limit=500)
        def press_many(_):
            for _ in range(50):
                session.press_input()
        with ThreadPoolExecutor(max_workers=8) as workers:
            list(workers.map(press_many, range(8)))
        snapshot = session.snapshot()
        batch = session.events_after(0)
        self.assertEqual((snapshot.input_sequence, snapshot.revision), (400, 400))
        self.assertEqual(snapshot.state.input_value, 0)
        self.assertFalse(batch.missed)
        self.assertEqual([e.sequence for e in batch.events], list(range(1, 401)))
        self.assertEqual([e.event.value for e in batch.events], [n % 2 for n in range(1, 401)])

    def test_history_overflow_and_new_consumer_boundary(self):
        session = BoardSession(history_limit=2)
        for _ in range(3):
            session.press_input()
        self.assertTrue(session.events_after(0).missed)
        self.assertEqual([r.sequence for r in session.events_after(1).events], [2, 3])
        cursor = session.snapshot().input_sequence
        self.assertEqual(session.events_after(cursor).events, ())
        session.press_input()
        self.assertEqual([e.sequence for e in session.events_after(cursor).events], [4])

    def test_reset_does_not_rewind_event_cursor(self):
        session = BoardSession()
        session.set_environment(55, 87)
        session.set_blink(True)
        session.set_leds([0, 1], 100)
        session.press_input()
        reset = session.reset()
        self.assertEqual(reset.state, simulator.State())
        self.assertEqual(reset.input_sequence, 2)
        self.assertEqual([e.event.value for e in session.events_after(0).events], [1, 0])
        session.close()
        session.close()
        with self.assertRaises(SessionClosed):
            session.press_input()
        self.assertEqual(session.snapshot(), reset)

    def test_model_and_session_import_with_io_modules_blocked(self):
        code = '''
import sys
class NoIO:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.')[0] in {'socket','tkinter','json','protocol','tcp','udp','http_api'}:
            raise ImportError('forbidden: ' + fullname)
sys.meta_path.insert(0, NoIO())
from session import BoardSession
s = BoardSession()
assert s.press_input().state.input_value == 1
assert s.set_environment(35.5, 80).state.temperature == 35.5
'''
        result = subprocess.run([sys.executable, "-S", "-B", "-c", code],
                                cwd=Path(__file__).resolve().parents[1],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
