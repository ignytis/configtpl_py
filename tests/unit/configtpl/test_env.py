import os
import unittest
from unittest.mock import patch

from configtpl.env import _parse_env_var_value, get_config_from_env


class TestEnv(unittest.TestCase):
  def test_parse_env_var_value(self) -> None:
    # Test cases for _parse_env_var_value
    assert _parse_env_var_value("") is None
    assert _parse_env_var_value("test_string") == "test_string"
    assert _parse_env_var_value("'quoted_string'") == "quoted_string"
    assert _parse_env_var_value('"another_quoted_string"') == "another_quoted_string"
    assert _parse_env_var_value("true") is True
    assert _parse_env_var_value("false") is False
    assert _parse_env_var_value("123") == 123
    assert _parse_env_var_value("-45") == -45
    assert _parse_env_var_value("1.23") == 1.23
    assert _parse_env_var_value("-0.5") == -0.5
    assert _parse_env_var_value("MixedCase"), "MixedCase"

  @patch.dict(
    os.environ,
    {
      "TEST_APP__FOO__BAR": "baz",
      "TEST_APP__FOO__QUOTED": "'quoted'",
      "TEST_APP__A_BOOL": "TRUE",
      "TEST_APP__ANOTHER_BOOL": "false",
      "TEST_APP__AN_EMPTY_VALUE": "",
      "TEST_APP__AN_INT": "123",
      "TEST_APP__A_NEG_INT": "-45",
      "TEST_APP__A_FLOAT": "1.23",
      "TEST_APP__A_NEG_FLOAT": "-0.5",
      "TEST_APP__CAMELCASE_VAR": "camelCaseValue",
      "TEST_APP__WITH_UNDERSCORE__VAR": "with_underscore_value",
      "UNRELATED_VAR": "unrelated",
    },
    clear=True,
  )
  def test_get_config_from_env(self) -> None:
    # Test with no prefix
    assert get_config_from_env(env_prefix=None) == {}

    # Test with a prefix that doesn't match any env vars
    assert get_config_from_env(env_prefix="NON_EXISTENT") == {}

    # Test with matching prefix
    expected_config = {
      "foo": {
        "bar": "baz",
        "quoted": "quoted",
      },
      "a_bool": "TRUE",
      "another_bool": False,
      "an_empty_value": None,
      "an_int": 123,
      "a_neg_int": -45,
      "a_float": 1.23,
      "a_neg_float": -0.5,
      "camelcase_var": "camelCaseValue",
      "with_underscore": {
        "var": "with_underscore_value",
      },
    }
    assert get_config_from_env(env_prefix="TEST_APP") == expected_config
