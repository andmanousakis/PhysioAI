## How to run the app:

1. Create virtual env: make venv
2. Activate venv: source venv/bin/activate
3. Q1 - Apply the data transformation: make transform
4. Run test on Q1: pytest tests/Q1_unit_test.py
5. Run test on Q2A: pytest tests/Q2_unit_test.py
6. Q2A - Running examples for testing:

`make get_message SESSION_GROUP="r+KlNwrwjJuFiuYXoFbY+/XSOUs="`

`make get_message SESSION_GROUP="uiCjoT07wEEYJhLxDQyJfY7Xh/A="`

`make get_message SESSION_GROUP="i9dTBS/3MSuXKSAb/Bg+OS6F7vY="`

You can find more session_group ids in session_group_ids.txt, located in the parent directory.

7. You will find the answer for Q2B in documentation folder as Q2B_documentation.pdf.

## Important

Please make sure you're not running several virtual environments at the same time, e.g. venv and base (conda env). Python will mix paths and errors will emerge.