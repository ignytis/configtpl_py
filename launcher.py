#!/usr/bin/env python

import argparse
import os
import os.path
import subprocess
import sys
from pathlib import Path

parser = argparse.ArgumentParser(prog="configtpl_cli", description="CLI for Configtpl development environment")
parser.add_argument("command")


args = parser.parse_args()
if args.command == "tests:functional":
  print("Functional testing started.")
  root_dir = Path(Path.cwd(), "tests", "functional")
  for current_dir, _subdirs, _files in os.walk(Path(Path.cwd(), "tests", "functional"), topdown=False):
    if current_dir == str(root_dir):  # skip the root directory
      continue

    test_path = Path(current_dir, "test.py")
    test_path_relative = str(test_path).removeprefix(str(root_dir) + "/")
    print(f"Running '{test_path_relative}'...")
    try:
      result = subprocess.run(  # noqa: S603
        [sys.executable, test_path],
        env={"SAMPLE_ENV_KEY": "sample_value"},
        capture_output=True,
        text=True,
        cwd=current_dir,
        check=True,
      )
    except subprocess.CalledProcessError as e:
      print(f"Test case failed with return code {e.returncode}")
      print(f"stdout: {e.stdout}")
      print(f"stderr: {e.stderr}")
      sys.exit(-1)

  print("Testing complete.")
else:
  raise ValueError(f"Invalid command: {args.command}")  # noqa: EM102,TRY003
