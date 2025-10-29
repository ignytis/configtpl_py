venv_cmd ?= python3 -m venv
pip_cmd ?= venv/bin/pip

sdist_file_path := ../../../target/wheels
sdist_file = $(shell find $(sdist_file_path) -name '*.tar.gz')

ifeq ($(sdist_file),)
$(error No sdist file found at $(sdist_file_path))
endif

install:
	$(venv_cmd) venv
	$(pip_cmd) install $(sdist_file)

run:
	venv/bin/python ./main.py

.PHONY: install run
