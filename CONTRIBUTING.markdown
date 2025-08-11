# Contributing to Imara Chat Bot

Thank you for considering contributing to the *Imara Chat Bot* project! We welcome contributions to improve the Imara Chat Bot.

## How to Contribute
1. **Fork the Repository**:
   ```bash
   git clone https://github.com/nocholla/imara_chat_bot.git
   cd imara_chat_bot
   git checkout -b feature/YourFeature
   ```
2. **Set Up the Environment**:
   ```bash
   python3.13 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Make Changes**:
   - Follow the project structure (`src/`, `ui/`, `tests/`).
   - Add or update tests in `tests/`.
   - Use logging (`logging` module) instead of print statements.
   - Ensure code passes linting (`pylint`) and tests (`pytest -v`).
4. **Commit Changes**:
   ```bash
   git commit -m "Add YourFeature"
   ```
5. **Push and Create a Pull Request**:
   ```bash
   git push origin feature/YourFeature
   ```
   Open a Pull Request on GitHub with a clear description.
6. **Code Review**:
   - Ensure tests pass in CI/CD (GitHub Actions).
   - Address feedback from reviewers.

## Coding Standards
- Use Python 3.13.
- Follow PEP 8 style guidelines.
- Add docstrings to all functions.
- Use `config.yaml` for configurable parameters.
- Log errors and info using the `logging` module.

## Testing
- Add unit tests in `tests/` for new functionality.
- Run tests with:
  ```bash
  pytest -v
  ```
- Ensure 100% test coverage for new code.

## Issues
- Check existing issues before creating a new one.
- Provide detailed descriptions and reproduction steps for bugs.

## License
Contributions are licensed under the MIT License. See `LICENSE` for details.