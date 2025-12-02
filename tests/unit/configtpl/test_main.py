from copy import deepcopy
from unittest import TestCase
from unittest.mock import mock_open, patch

from configtpl.main import ConfigTpl

FILE_CONFIG_CONTENTS_SIMPLE = """\
{% set name = "John" %}
params:
  user_name: {{ name }}
  greeting: "Hello, {{ name }}!"
"""

FILE_CONFIG_CONTENTS_COMPOSITE_FIRST = """\
{% set name = "John" %}
params:
  user_name: {{ name }}
  greeting: "Hello, {{ name }}!"
"""

CONFIG_COMPILED_SIMPLE = {
  "params": {
    "user_name": "John",
    "greeting": "Hello, John!",
  },
}


@patch("pathlib.Path.cwd", return_value="/test/cwd")
@patch("pathlib.Path.home", return_value="/test/home")
@patch("os.path.isfile", return_value=True)
@patch("os.path.getmtime", return_value=123)
class CompilerTest(TestCase):
  def __init__(self, method_name: str = "runTest") -> None:
    super().__init__(method_name)
    self.maxDiff = None

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_SIMPLE)
  def test_compile_simple(self, _a: object, _b: object, _c: object, _d: object, _e: object) -> None:
    assert get_instance().build_from_files("/test/sample.cfg") == CONFIG_COMPILED_SIMPLE

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_SIMPLE)
  def test_compile_simple_override(self, _a: object, _b: object, _c: object, _d: object, _e: object) -> None:
    cfg_compiled = deepcopy(CONFIG_COMPILED_SIMPLE)
    cfg_compiled["params"] = {
      **cfg_compiled["params"],
      "some_param": "some_param_val1",
      "greeting": "Overridden greeting",
    }
    assert cfg_compiled == get_instance().build_from_files(
      "/test/sample.cfg",
      overrides={
        "params": {
          "some_param": "some_param_val1",
          "greeting": "Overridden greeting",
        },
      },
    )

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_COMPOSITE_FIRST)
  def test_compile_composite(self, _a: object, _b: object, _c: object, _d: object, _e: object) -> None:
    assert get_instance().build_from_files("/test/sample.cfg") == {
      "params": {
        "user_name": "John",
        "greeting": "Hello, John!",
      },
    }


def get_instance() -> ConfigTpl:
  return ConfigTpl()
