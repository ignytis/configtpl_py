import os
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
class ConfigTplSimpleTest(TestCase):
  def __init__(self, method_name: str = "runTest") -> None:
    super().__init__(method_name)
    self.maxDiff = None

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_SIMPLE)
  def test_compile_simple(self, _a: object, _b: object, _c: object, _d: object, _e: object) -> None:
    assert self.get_instance().build_from_files("/test/sample.cfg") == CONFIG_COMPILED_SIMPLE

  @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_SIMPLE)
  def test_compile_simple_override(self, _a: object, _b: object, _c: object, _d: object, _e: object) -> None:
    cfg_compiled = deepcopy(CONFIG_COMPILED_SIMPLE)
    cfg_compiled["params"] = {
      **cfg_compiled["params"],
      "some_param": "some_param_val1",
      "greeting": "Overridden greeting",
    }
    assert cfg_compiled == self.get_instance().build_from_files(
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
    assert self.get_instance().build_from_files("/test/sample.cfg") == {
      "params": {
        "user_name": "John",
        "greeting": "Hello, John!",
      },
    }

  def get_instance(self) -> ConfigTpl:
    return ConfigTpl()


@patch("pathlib.Path.cwd", return_value="/test/cwd")
@patch("pathlib.Path.home", return_value="/test/home")
@patch("os.path.isfile", return_value=True)
@patch("os.path.getmtime", return_value=123)
@patch.dict(
  os.environ,
  {
    "TEST_APP__PARAMS__SIMPLE_ENV_VAR": "simple_env_var_val",
    "TEST_APP_THIS__IS_INVALID": "because_no_prefix_after_app",
    "THIS_IS_JUST_IRRELEVANT": "because_no_prefix",
  },
)
class ConfigTplEnvVarsTest(TestCase):
  @patch("builtins.open", new_callable=mock_open, read_data=FILE_CONFIG_CONTENTS_COMPOSITE_FIRST)
  def test_compile_composite(self, _a: object, _b: object, _c: object, _d: object, _e: object) -> None:
    assert self.get_instance().build_from_files("/test/sample.cfg") == {
      "params": {
        "user_name": "John",
        "greeting": "Hello, John!",
        # This comes from the env vars in class decorator
        "simple_env_var": "simple_env_var_val",
      },
    }

  @patch.dict(
    os.environ,
    {
      "TEST_APP__FOO__BAR": "baz",
      "TEST_APP__FOO__QUOTED": "'quoted'",
      "TEST_APP__FOO__QUOTED_SINGLE_INSIDE_DOUBLE": '"single" inside double',
      "TEST_APP__A_BOOL_STRING": "TRUE",
      "TEST_APP__A_STRING_TRUE": "'true'",
      "TEST_APP__ANOTHER_BOOL": "false",
      "TEST_APP__AN_EMPTY_VALUE": "",
      "TEST_APP__AN_INT": "123",
      "TEST_APP__A_NEG_INT": "-45",
      "TEST_APP__A_FLOAT": "1.23",
      "TEST_APP__A_NEG_FLOAT": "-0.5",
    },
  )
  def test_compile_advanced_env_vars(self, _a: object, _b: object, _c: object, _d: object) -> None:
    assert self.get_instance().build_from_str("") == {
      "foo": {
        "bar": "baz",
        "quoted": "quoted",
        "quoted_single_inside_double": '"single" inside double',
      },
      "a_bool_string": "TRUE",
      "a_string_true": "true",
      "another_bool": False,
      "an_empty_value": None,
      "an_int": 123,
      "a_neg_int": -45,
      "a_float": 1.23,
      "a_neg_float": -0.5,
      # This comes from the env vars in class decorator
      "params": {
        "simple_env_var": "simple_env_var_val",
      },
    }

  def get_instance(self) -> ConfigTpl:
    return ConfigTpl(env_var_prefix="TEST_APP")
