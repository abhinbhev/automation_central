---
name: write-tests
description: "Generate unit and integration test stubs for a function or module"
mode: ask
---

Generate test cases for the following code.

For each function or class method, produce:
1. A happy-path test
2. At least two edge cases (empty input, boundary values, None, type mismatches)
3. An error/exception test if the function raises

Use `pytest` style. Add docstrings explaining what each test checks.

Also list any cases that are hard to unit test and suggest integration test approaches for them.

If the code has external dependencies (DB, API, file system), show how to mock them with `unittest.mock.patch`.

Always ask the user if they want an HTML version of the test report. If yes, generate a detailed HTML report covering: every test case name and description, inputs used, expected vs actual outputs, pass/fail status, any mocking setup applied, and a summary section with total counts and any flagged untestable paths.
