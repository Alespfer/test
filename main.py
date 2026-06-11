from greetings import say_hello, say_goodbye


def main() -> None:
    print(say_hello())
    print(say_hello("Alberto"))
    print(say_goodbye("Alberto"))


if __name__ == "__main__":
    main()
