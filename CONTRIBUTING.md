# Contributing to Linkwarden Telegram Bot

Thank you for considering contributing to the Linkwarden Telegram Bot project! We appreciate your time and effort in helping us improve the project. Please follow the guidelines below to ensure a smooth and efficient contribution process.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Submitting Pull Requests](#submitting-pull-requests)

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations for behavior and how to report unacceptable behavior.

## How to Contribute

1. **Fork the repository**: Click the "Fork" button at the top right corner of the repository page to create a copy of the repository in your GitHub account.

2. **Clone your fork**: Clone your forked repository to your local machine using the following command:
   ```bash
   git clone https://github.com/yourusername/linkwarden-telegram-bot.git
   cd linkwarden-telegram-bot
   ```

3. **Create a new branch**: Create a new branch for your contribution. Use a descriptive name for your branch to indicate the purpose of your changes.
   ```bash
   git checkout -b my-feature-branch
   ```

4. **Make your changes**: Implement your changes in the new branch. Ensure that your code follows the [Code Style](#code-style) guidelines and includes appropriate tests.

5. **Commit your changes**: Commit your changes with a clear and concise commit message.
   ```bash
   git add .
   git commit -m "Add feature: description of your feature"
   ```

6. **Push your changes**: Push your changes to your forked repository.
   ```bash
   git push origin my-feature-branch
   ```

7. **Create a pull request**: Open a pull request (PR) from your forked repository to the main repository. Provide a detailed description of your changes and any relevant information.

## Code Style

Please follow the code style guidelines below to ensure consistency and readability:

- Use 4 spaces for indentation.
- Follow the PEP 8 style guide for Python code.
- Write clear and concise comments to explain the purpose of your code.
- Use meaningful variable and function names.
- Keep lines of code within 79 characters.

## Testing

We use `pytest` for testing. Please ensure that your changes include appropriate tests and that all tests pass before submitting a pull request.

1. **Install dependencies**: Install the required dependencies for testing.
   ```bash
   pip install -r requirements.txt
   pip install pytest
   ```

2. **Run tests**: Run the tests to ensure that your changes do not introduce any regressions.
   ```bash
   pytest
   ```

## Submitting Pull Requests

When submitting a pull request, please follow these guidelines:

1. **Provide a clear description**: Clearly describe the purpose and scope of your changes. Include any relevant information, such as related issues or references.

2. **Follow the pull request template**: Use the provided pull request template to ensure that all necessary information is included.

3. **Address feedback**: Be responsive to feedback and make any necessary changes to your pull request based on the review comments.

4. **Keep your branch up to date**: Regularly update your branch with the latest changes from the main repository to avoid merge conflicts.

Thank you for your contributions! We appreciate your help in making the Linkwarden Telegram Bot project better.
