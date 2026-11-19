"""Pure board state and transitions. No I/O, clocks, threads or wire formats."""

from dataclasses import dataclass, replace
import math


LED_COUNT = 4


@dataclass(frozen=True, slots=True)
class State:
    leds: tuple[int, ...] = (0, 0, 0, 0)
    blink: bool = False
    temperature: float = 24.5
    humidity: float = 40.0
    input_value: int = 0


@dataclass(frozen=True, slots=True)
class InputChanged:
    index: int
    value: int


def set_leds(state: State, indices, brightness: int):
    indices = tuple(indices)
    if not indices or any(type(i) is not int or not 0 <= i < LED_COUNT for i in indices):
        raise ValueError("LED indices must be integers in 0..3")
    if type(brightness) is not int or not 0 <= brightness <= 255:
        raise ValueError("brightness must be an integer in 0..255")
    values = list(state.leds)
    for index in indices:
        values[index] = brightness
    return replace(state, leds=tuple(values)), ()


def set_blink(state: State, enabled: bool):
    if type(enabled) is not bool:
        raise ValueError("enabled must be a boolean")
    return replace(state, blink=enabled), ()


def set_environment(state: State, temperature=None, humidity=None):
    def number(value, current):
        if value is None:
            return current
        if type(value) not in (int, float):
            raise ValueError("sensor values must be finite numbers")
        try:
            value = float(value)
        except OverflowError:
            raise ValueError("sensor values must be finite numbers") from None
        if not math.isfinite(value):
            raise ValueError("sensor values must be finite numbers")
        return value

    temperature = number(temperature, state.temperature)
    humidity = number(humidity, state.humidity)
    return replace(state, temperature=temperature, humidity=humidity), ()


def press_input(state: State):
    value = 1 - state.input_value
    return replace(state, input_value=value), (InputChanged(0, value),)


def reset(state: State):
    events = (InputChanged(0, 0),) if state.input_value else ()
    return State(), events
