"""Utilities for measuring greetings strings.

Added during the SESHAT test wave of 2026-06-18 (iteration 1/3).
Pure stdlib, no external dependency.
"""

from greetings import say_goodbye, say_hello


def greeting_length(name: str = "world") -> int:
    return len(say_hello(name))


def farewell_length(name: str = "world") -> int:
    return len(say_goodbye(name))


def both_lengths(name: str = "world") -> tuple[int, int]:
    return greeting_length(name), farewell_length(name)


if __name__ == "__main__":
    for who in ("world", "Alberto", "SESHAT"):
        hi, bye = both_lengths(who)
        print(f"{who:>10}  hello={hi}  goodbye={bye}")
