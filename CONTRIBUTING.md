# Contributing

Thanks for helping improve this educational course.

## Principles

1. **Beginner-first.** Prefer plain English and short, copy-pasteable commands.
2. **Loopback only.** Labs must bind to `127.0.0.1` (or refuse to start).
3. **Prove it.** Prefer checks (`curl`, tests) over claims.
4. **Episode folders stay self-contained.** Do not break prior episode paths without a redirect note in that episode’s README.

## How to propose a change

1. Open an issue describing the learning gap or bug.
2. Fork, branch from `main`, keep commits focused.
3. Run the full suite from the repo root:

   ```bash
   make test
   ```

   Or a single episode: `make test-01` … `make test-04`.

4. Update the episode README / objectives if learner-facing behavior changes.
5. Shared runtime lives in `shared/` (episodes 02–04). Episode 01 stays self-contained unless you intentionally migrate it.
6. Open a pull request with a clear summary of **what learners gain**.

## Naming

| Kind | Pattern | Example |
| --- | --- | --- |
| Episode folder | `NN-short-kebab-title` | `01-your-first-local-lab` |
| Episode docs | `README.md`, `OBJECTIVES.md`, `requirements.md` | — |
| Follow-along notes | `deck/episode-NN.md` | `deck/episode-01.md` |
| Tests | `tests/test_*.py` | `tests/test_lab.py` |

## Commit messages

Write short, educational commit messages (what changed for learners). Do not include tool or editor brand names in commit subjects or bodies.

## Code of conduct (short)

Be respectful. This is a teaching space for beginners. Harassment or unsafe attack guidance will be rejected.
