import sys


def get_input(prompt="> ") -> str:
    sys.stdout.write(prompt)
    sys.stdout.flush()
    try:
        return input().strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

# def get_input(prompt="> "):
#     try:
#         return input(prompt).strip()
#     except (KeyboardInterrupt, EOFError):
#         print("\nВыход из игры.")
#         return "quit"