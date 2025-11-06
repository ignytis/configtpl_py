import subprocess
import unittest
from unittest.mock import MagicMock, patch

from configtpl.jinja.globals import jinja_global_cmd, jinja_global_env


class TestJinjaGlobals(unittest.TestCase):
  @patch("subprocess.run")
  def test_jinja_global_cmd(self, mock_run):
    # Mock the subprocess.run method
    mock_run.return_value = MagicMock(stdout="mocked output")

    # Test the function
    result = jinja_global_cmd("echo Hello")
    self.assertEqual(result, "mocked output")

    # Ensure subprocess.run was called with the correct arguments
    mock_run.assert_called_once_with("echo Hello", shell=True, check=True, capture_output=True, text=True)

  @patch("os.getenv")
  def test_jinja_global_env_with_value(self, mock_getenv):
    mock_getenv.return_value = "mocked_value"

    result = jinja_global_env("TEST_VAR")
    self.assertEqual(result, "mocked_value")

  @patch("os.getenv")
  def test_jinja_global_env_with_default(self, mock_getenv):
    env_vars = {"TEST_VAR": "mocked_value"}
    mock_getenv.side_effect = lambda key, default=None: env_vars.get(key, default)

    self.assertEqual("mocked_value", jinja_global_env("TEST_VAR", "default_value"))
    self.assertEqual("default_value", jinja_global_env("THIS_DOES_NOT_EXIST", "default_value"))

    self.assertEqual(mock_getenv.call_count, 2)
    mock_getenv.assert_any_call("TEST_VAR", "default_value")
    mock_getenv.assert_any_call("THIS_DOES_NOT_EXIST", "default_value")
