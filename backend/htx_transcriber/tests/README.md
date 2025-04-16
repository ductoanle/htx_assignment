# Testing the HTX Transcriber

This directory contains unit tests for the HTX Transcriber application.

## Running the Tests

To run the tests, you need to have pytest installed. You can install it using pip:

```bash
pip install pytest
```

Then, from the root directory of the project, run:

```bash
pytest
```

This will run all the tests in the `tests` directory.

## Test Structure

- `conftest.py`: Contains common test fixtures used across multiple test files
- `test_transcription_service.py`: Tests for the transcription service

## Writing New Tests

When writing new tests, follow these guidelines:

1. Use the fixtures defined in `conftest.py` when possible
2. Mock external dependencies (database, file system, etc.)
3. Test both success and error cases
4. Keep tests focused and isolated

## Test Coverage

To check test coverage, you can use pytest-cov:

```bash
pip install pytest-cov
pytest --cov=htx_transcriber
```

This will show you the test coverage for the HTX Transcriber package. 