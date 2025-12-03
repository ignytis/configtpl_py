#!/usr/bin/env python

import logging
import os
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
log = logging.getLogger(__name__)

log.info("Functional testing started.")
root_dir = Path(Path.cwd(), "tests", "functional")
for current_dir, _subdirs, _files in os.walk(Path(Path.cwd(), "tests", "functional"), topdown=False):
  if current_dir == str(root_dir):  # skip the root directory
    continue

  test_path = Path(current_dir, "test.py")
  test_path_relative = str(test_path).removeprefix(str(root_dir) + "/")
  log.info("Running '%s'...", test_path_relative)
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
    log.info("Test case failed with return code {%s}", e.returncode)
    log.info("stdout: {%s}", e.stdout)
    log.info("stderr: {%s}", e.stderr)
    sys.exit(-1)

log.info("Testing complete.")
