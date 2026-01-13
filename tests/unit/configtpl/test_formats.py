import sys
from typing import Any
from unittest import TestCase
from unittest.mock import mock_open, patch

import pytest

from configtpl.main import ConfigFormat, ConfigTpl

FILE_JSON_CONTENT = '{"key": "value", "int": 123}'
FILE_TOML_CONTENT = 'key = "value"\nint = 123'
FILE_YAML_CONTENT = "key: value\nint: 123"

EXPECTED_RESULT = {"key": "value", "int": 123}


@patch("pathlib.Path.cwd", return_value="/test/cwd")
@patch("pathlib.Path.home", return_value="/test/home")
@patch("os.path.isfile", return_value=True)
@patch("os.path.getmtime", return_value=123)
class ConfigTplFormatsTest(TestCase):
  def get_instance(self) -> ConfigTpl:
    return ConfigTpl()

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_JSON_CONTENT)
  def test_from_file_json_auto(self, *_args: Any) -> None:  # noqa: ANN401
    assert self.get_instance().build_from_files(["/test/config.json"]) == EXPECTED_RESULT

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_TOML_CONTENT)
  def test_from_file_toml_auto(self, *_args: Any) -> None:  # noqa: ANN401
    assert self.get_instance().build_from_files(["/test/config.toml"]) == EXPECTED_RESULT

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_YAML_CONTENT)
  def test_from_file_yaml_auto(self, *_args: Any) -> None:  # noqa: ANN401
    with patch.dict(sys.modules, {"yaml": sys.modules.get("yaml")}):  # ensure it is visible?
      assert self.get_instance().build_from_files(["/test/config.yaml"]) == EXPECTED_RESULT

  def test_from_str_json_default(self, *_args: Any) -> None:  # noqa: ANN401
    # Default should be JSON
    assert self.get_instance().build_from_str(FILE_JSON_CONTENT) == EXPECTED_RESULT

  def test_from_str_toml_explicit(self, *_args: Any) -> None:  # noqa: ANN401
    assert self.get_instance().build_from_str(FILE_TOML_CONTENT, file_type="toml") == EXPECTED_RESULT
    assert self.get_instance().build_from_str(FILE_TOML_CONTENT, file_type=ConfigFormat.TOML) == EXPECTED_RESULT

  def test_from_str_yaml_explicit(self, *_args: Any) -> None:  # noqa: ANN401
    assert self.get_instance().build_from_str(FILE_YAML_CONTENT, file_type="yaml") == EXPECTED_RESULT

  def test_missing_yaml_raises_error(self, *_args: Any) -> None:  # noqa: ANN401
    # Simulate missing yaml
    with patch("configtpl.main.yaml", None), pytest.raises(ImportError, match="PyYAML is not installed"):
      self.get_instance().build_from_str(FILE_YAML_CONTENT, file_type="yaml")
