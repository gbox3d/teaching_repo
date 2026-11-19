"""One state owner: atomic transitions and a bounded journal for optional consumers."""

from collections import deque
from dataclasses import dataclass
from threading import Lock

import simulator


class SessionClosed(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class Snapshot:
    state: simulator.State
    revision: int
    input_sequence: int


@dataclass(frozen=True, slots=True)
class InputRecord:
    sequence: int
    revision: int
    event: simulator.InputChanged


@dataclass(frozen=True, slots=True)
class EventBatch:
    cursor: int
    events: tuple[InputRecord, ...]
    missed: bool


class BoardSession:
    def __init__(self, history_limit=256):
        if type(history_limit) is not int or history_limit < 1:
            raise ValueError("history_limit must be positive")
        self._state = simulator.State()
        self._lock = Lock()
        self._revision = 0
        self._sequence = 0
        self._events = deque(maxlen=history_limit)
        self._closed = False

    def _snapshot(self):
        return Snapshot(self._state, self._revision, self._sequence)

    def snapshot(self):
        with self._lock:
            return self._snapshot()

    def _apply(self, transition, *args):
        # Only pure model functions run under this lock; never user callbacks or I/O.
        with self._lock:
            if self._closed:
                raise SessionClosed("simulation is stopping")
            state, events = transition(self._state, *args)
            self._state = state
            self._revision += 1
            for event in events:
                self._sequence += 1
                self._events.append(InputRecord(self._sequence, self._revision, event))
            return self._snapshot()

    def set_leds(self, indices, brightness):
        # Materialize caller-owned iterators before taking the state lock.
        return self._apply(simulator.set_leds, tuple(indices), brightness)

    def set_blink(self, enabled):
        return self._apply(simulator.set_blink, enabled)

    def set_environment(self, temperature=None, humidity=None):
        return self._apply(simulator.set_environment, temperature, humidity)

    def press_input(self):
        return self._apply(simulator.press_input)

    def reset(self):
        return self._apply(simulator.reset)

    def events_after(self, cursor):
        if type(cursor) is not int or cursor < 0:
            raise ValueError("cursor must be a nonnegative integer")
        with self._lock:
            oldest = self._events[0].sequence if self._events else self._sequence + 1
            missed = cursor < oldest - 1 or cursor > self._sequence
            events = () if missed else tuple(e for e in self._events if e.sequence > cursor)
            return EventBatch(self._sequence, events, missed)

    def close(self):
        with self._lock:
            self._closed = True
