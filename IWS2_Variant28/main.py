"""IWS2 Variant 28 — Hackathon Results. Text menu.

Authors: Diar (Student A / Student B — solo project)
"""

from data_structures import run_task1
from file_io import run_task6
from models import demo_oop
from optimization import debug_demo
from recursion import run_task4
from searching import run_task3
from sorting import run_task2


MENU = """
========================================
  IWS2 Variant 28 — Hackathon Results
========================================
  1. Task 1 — Tuples, Sets, Dictionaries
  2. Task 2 — Bubble Sort
  3. Task 3 — Searching
  4. Task 4 — Recursion
  5. Task 5 — OOP
  6. Task 6 — Files & Exceptions
  7. Task 7 — Debug & Optimize
  8. Run all tasks
  0. Exit
========================================
"""


def run_all():
    run_task1()
    print()
    run_task2()
    print()
    run_task3()
    print()
    run_task4()
    print()
    demo_oop()
    print()
    run_task6()
    print()
    debug_demo()


def main():
    actions = {
        "1": run_task1,
        "2": run_task2,
        "3": run_task3,
        "4": run_task4,
        "5": demo_oop,
        "6": run_task6,
        "7": debug_demo,
        "8": run_all,
    }
    while True:
        print(MENU)
        choice = input("Choose option: ").strip()
        if choice == "0":
            print("Bye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Unknown option, try again.")
            continue
        print()
        action()
        print()
        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
