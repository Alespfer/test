"""Title-case helpers for greetings strings.

Added during the SESHAT vague 2 test wave of 2026-06-19 (iteration 1/3).
Pure stdlib, no external dependency.
"""

from greetings import say_goodbye, say_hello


def hello_title(name: str = "world") -> str:
    return say_hello(name).title()


def goodbye_title(name: str = "world") -> str:
    return say_goodbye(name).title()


if __name__ == "__main__":
    for who in ("world", "alberto", "seshat"):
        print(f"{hello_title(who)}  |  {goodbye_title(who)}")
