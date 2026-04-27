---
name: write-tests
description: Generate pytest test stubs and edge cases for a Python function or module
domain: coding
requires_script: false
---

## Usage

Invoke with `/write-tests` then provide:
- The Python code (function, class, or module) to test
- Any known constraints or tricky edge cases
- Whether integration tests are needed (yes/no)

## Output

A complete `test_<module>.py` file with:
- Happy-path tests
- Edge case tests (empty input, None, boundary values, type mismatches)
- Exception tests
- Mock setup for external dependencies (ADO, HTTP, file system)

## Test Standards

- Framework: `pytest`
- Naming: `test_<function>_<scenario>` (e.g., `test_create_item_missing_title_raises`)
- Each test has a one-sentence docstring
- External deps mocked with `unittest.mock.patch` or `pytest-mock`
- File I/O uses `tmp_path` pytest fixture
- Deterministic: no random or time-dependent values without monkeypatching

## Steps

1. Read the provided code
2. List all public functions/methods
3. For each: enumerate happy path, edge cases, and error scenarios
4. Write the test file
5. Flag anything that's hard to unit test and suggest an integration test approach
