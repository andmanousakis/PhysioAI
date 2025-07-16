# PhysioAI

PhysioAI is an intelligent assistant designed for physiotherapists to streamline session data analysis, automate feature extraction, and facilitate data-driven patient insights. The system transforms raw exercise data into session-level metrics and provides tools for reviewing, testing, and exploring patient sessions.

---

## Getting Started

Follow these steps to set up and run PhysioAI:

1. **Clone the branch to the directory of your choice:**

    ```bash
    git clone --branch production --single-branch git@github.com:andmanousakis/PhysioAI.git
    ```

2. **Create virtual environment:**
   ```bash
   make venv
   ```

3. **Activate virtual environment:**
    ```bash
   source venv/bin/activate
   ```

4. **Q1 – Apply the data transformation:**
    ```bash
    make transform
    ```

5. **Run unit test on Q1**
    ```bash
    pytest tests/Q1_unit_test.py
    ```

6. **Run unit test on Q2A:**
    ```bash
    pytest tests/Q2_unit_test.py
    ```

7. **Q2A – Running examples for testing:**
    ```bash
    make get_message SESSION_GROUP="r+KlNwrwjJuFiuYXoFbY+/XSOUs="
    make get_message SESSION_GROUP="uiCjoT07wEEYJhLxDQyJfY7Xh/A="
    make get_message SESSION_GROUP="i9dTBS/3MSuXKSAb/Bg+OS6F7vY="
    ```

## Important Notes

1. Avoid running multiple Python environments (e.g., both venv and conda's base) simultaneously. This can cause Python to mix paths, resulting in unexpected errors.

2. You need an OpenAI API key.