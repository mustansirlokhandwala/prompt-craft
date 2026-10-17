---
name: usecase-tests
description: Writes and verifies tests that check what the code is supposed to do (the use case), not what it currently happens to do, proves the tests can catch a bug, and reports code coverage. Use whenever code is about to be submitted, committed or opened as a pull request; when the user asks to add, write, fix or review tests; when they ask for test or code coverage; or when a test was changed just to make it pass.
---

# Use-Case Tests

A test that was written by reading the code will pass even when the code is wrong. Tests come from the **use case**: what a user or caller needs to happen. The code is what's being checked.

## Step 1: List the use cases before reading the code

From the request, spec, issue, docs or function name — **not the implementation** — list the behaviors:

```
Use case: <who> <does what> → <expected result>
- Happy path: <normal input> → <result>
- Edge: <empty, zero, one, maximum, boundary value, unicode, duplicates> → <result>
- Error: <invalid or missing input, failure of a dependency> → <error or fallback>
```

Work out each **expected value independently**: by hand, from the spec, or from a known real-world example. Never run the code and copy its output into the assertion.

If the expected behavior is unclear, ask the user one question with your best guess. Don't guess silently by reading the code.

## Step 2: Write the tests

- Each test is named after a behavior: `test_rejects_expired_coupon`, not `test_apply_2`.
- Test through the public interface: inputs in, results and side effects out.
- Assert on **results** — the return value, saved data, visible output — rather than on internal calls. Mock only what you don't own or can't run (network, clock, payments).
- Put one behavior in each test, with an exact expected value. Avoid loose assertions like `assert result` or `is not None`.
- Use the project's existing test framework, folder and style.

## Step 3: Run them and read the failures honestly

When a test fails, decide by checking the use case, never the code:

- **The code is wrong** → fix the code.
- **The test misunderstood the use case** → fix the test, and say why in one line.
- **It's unclear** → ask the user.

Never do these to get to green:
- weaken an assertion
- copy the actual output into the expectation
- skip, comment out or delete a failing test
- add code paths that exist only for tests

## Step 4: Prove the tests can catch a bug

A test that can't fail is worthless. For each important behavior, make **one deliberate small break** in the code and confirm a test fails. Then undo it. Example breaks:

- flip a condition (`>` to `>=`, `and` to `or`)
- an off-by-one error
- return early or return a default value
- delete the line that saves or validates

If nothing fails, the test is missing or too weak: add or strengthen it. Always restore the code, and re-run the tests to confirm they are green.

## Step 5: Measure coverage

Use the project's existing coverage tool. If it has none, use the standard one for the language:

| Language | Command |
|---|---|
| Python | `pytest --cov=<package> --cov-branch --cov-report=term-missing`, or `coverage run --branch -m unittest && coverage report -m` |
| JavaScript/TypeScript | `npx vitest run --coverage` or `npx jest --coverage` |
| Go | `go test -cover ./...` |
| Rust | `cargo llvm-cov` |
| Java/Kotlin | JaCoCo through Gradle or Maven |

Report **line and branch coverage for the changed files**. Coverage shows what never ran; it doesn't prove correctness. Turn every uncovered line into a question: "Which use case runs this line?" Then either test that use case or delete the dead code.

The default target is **80% branch coverage on changed code**, unless the project sets its own. Don't write tests that run lines without checking anything, just to raise the number.

If no coverage tool is installed, say so and give the install command. Don't add a dependency without asking the user.

## Step 6: Report

```
**Use cases tested**
| Use case | Test | Result |
|---|---|---|
| <behavior> | <test name> | ✅ / ❌ |

**Bug check:** <n> deliberate breaks, <n> caught. <any that weren't, and the fix>
**Coverage (changed files):** lines <x>%, branches <y>%. Untested: <use cases, not line numbers>
**Changed to pass:** <code fixes made, test fixes and why, or "none">
```

Keep it to this table and three lines. Show raw test output only if something failed.
