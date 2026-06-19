"""Case-conversion helpers for greetings strings.

Added during the SESHAT vague 2 test wave of 2026-06-19 (iteration 2/3).
Pure stdlib, no external dependency.
"""

from greetings import say_goodbye, say_hello


def shout(text: str) -> str:
    return text.upper()


def whisper(text: str) -> str:
    return text.lower()


def shouted_hello(name: str = "world") -> str:
    return shout(say_hello(name))


def whispered_goodbye(name: str = "world") -> str:
    return whisper(say_goodbye(name))


if __name__ == "__main__":
    for who in ("world", "alberto", "seshat"):
        print(f"{shouted_hello(who):<30}  {whispered_goodbye(who)}")
