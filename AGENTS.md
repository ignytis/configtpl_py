# Project: configtpl, the configuration library

## General instructions

- The project should be compatible with Python versions 3.11 - 3.14
- `uv` + `venv` is used for local development

## Coding style

- Follow the Ruff rules defined in @.ruff.toml
- Use `./scripts/full_test.sh` to perform full testing after making changes in code

## Testing

- Tests are runnable from `venv`
- Unit tests can be executed by command `pytest ./tests/unit`
- Functional tests can be executed by command `python ./tests/functional/run.py`
- Ruff check can be executed by command `./.venv/bin/ruff check`

## Workflow of the library

- `defaults` is a dictionary which acts as a base configuration. Empty by default
- `files` is a list of files which is empty by default. `files` are read in a loop:
  - each `file` is rendered as Jinja template. Context contains:
    - results of the previous iterations
    - `context` dictionary provided by user, empty by default
- `overrides` apply at the very end of configuration building
- all components are deep-merged into nested dictionary
- the final result is a nested dictionary
