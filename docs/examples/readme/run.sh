#!/usr/bin/env bash

set -e

export MY_ENV_VAR=testing
export MY_APP__NESTED__VAR=hello

python ./app.py
