# Contributing to ML-Scope

We welcome contributions to ML-Scope, a modular real-time reinforcement learning pipeline designed for scalability and resilience. Follow the guidelines below to set up, contribute, and maintain the quality of the project.

---

## Getting Started

1. **Fork the Repository**:

   - Click the "Fork" button on the top-right corner of the repository page on GitHub.

2. **Clone Your Fork**:

   ```bash
   git clone https://github.com/<your-username>/ml-scope.git
   cd ml-scope
   ```

3. **Set Up the Environment**:

   - Create a virtual environment and install dependencies:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows: venv\Scripts\activate
     pip install -r requirements.txt
     ```

4. **Set Up the Queue Server**:

   - Start the queue server to enable inter-process communication:
     ```bash
     python forecasting_model/queue_server.py
     ```

5. **Run Unit Tests**:
   - Ensure the existing codebase passes all tests:
     ```bash
     pytest tests/
     ```

---

## Contribution Guidelines

### Code Style

- Follow **PEP 8** standards for Python code.
- Use `flake8` to lint your code before committing:
  ```bash
  flake8 .
  ```
- Keep functions modular and well-documented with inline comments.

### Branching and Commits

1. **Create a New Branch**:

   - Always create a feature branch for your changes:
     ```bash
     git checkout -b <branch-name>
     ```
   - Use descriptive branch names like `feature-hyperparameter-tuning` or `bugfix-logging`.

2. **Write Clear Commit Messages**:

   - Example format:
     ```
     Add: Implement hyperparameter tuning in pipeline.py
     Fix: Resolve queue overflow bug in rl_training.py
     ```

3. **Push Changes**:
   - Push your changes to your fork:
     ```bash
     git push origin <branch-name>
     ```

### Testing

- Write unit tests for all new features and place them in the `tests/unit_tests/` directory.
- Use `pytest` for writing and running tests.
- For integration tests, include them in the `tests/integration_tests/` directory.

### Documentation

- Update relevant sections in:
  - `README.md` for new features or usage changes.
  - `docs/architecture.md` for structural changes or new components.
  - `docs/api_documentation.md` for API-level updates.
- Add comments to your code for clarity, especially for complex algorithms.

---

## Pull Request Process

1. **Ensure All Tests Pass**:

   ```bash
   pytest tests/
   ```

2. **Check Code Quality**:

   - Run `flake8` and resolve all issues:
     ```bash
     flake8 .
     ```

3. **Open a Pull Request**:

   - Push your branch to your fork and open a pull request on the main repository.
   - Use a descriptive title and include a summary of your changes in the description.

4. **Respond to Reviews**:
   - Be prompt in addressing comments or requested changes from reviewers.

---

## Reporting Issues

- If you encounter a bug or have a feature request, open an issue [here](https://github.com/<repository-owner>/ml-scope/issues).
- Use the following template for issues:

  ```markdown
  **Description**:
  Briefly describe the issue or feature request.

  **Steps to Reproduce** (for bugs):

  1. Step 1
  2. Step 2
  3. Step 3

  **Expected Behavior**:
  What you expected to happen.

  **Actual Behavior**:
  What actually happened.

  **Additional Context**:
  Add any relevant screenshots, logs, or context.
  ```

---

## Feedback and Discussions

For questions or discussions, open a GitHub discussion [here](https://github.com/<repository-owner>/ml-scope/discussions). Collaborate and share ideas to improve ML-Scope!

Thank you for contributing to ML-Scope! 🎉
