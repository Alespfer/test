"""Repeat helpers for greetings strings.

Added during the SESHAT vague 2 test wave of 2026-06-19 (iteration 3/3).
Pure stdlib, no external dependency.
"""

from greetings import say_goodbye, say_hello


def repeat_hello(name: str = "world", n: int = 1) -> str:
    return " ".join(say_hello(name) for _ in range(n))


def repeat_goodbye(name: str = "world", n: int = 1) -> str:
    return " ".join(say_goodbye(name) for _ in range(n))


if __name__ == "__main__":
    print(repeat_hello("Alberto", 3))
    print(repeat_goodbye("SESHAT", 2))
