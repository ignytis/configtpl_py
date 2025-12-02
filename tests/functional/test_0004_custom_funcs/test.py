import unittest

from configtpl.main import ConfigTpl


def str_rev(text: str) -> str:
  return "".join(list(reversed(text)))


def gen_seq(min_val: int, max_val: int) -> list:
  return [*range(min_val, max_val), max_val]


class TestCustomFuncs(unittest.TestCase):
  """
  Tests the custom function in Jinja environment
  """

  def setUp(self) -> None:
    self.maxDiff = None
    return super().setUp()

  def test_custom_funcs(self) -> None:
    builder = ConfigTpl()
    builder.set_filter("str_rev", str_rev)
    builder.set_global("gen_seq", gen_seq)
    cfg = builder.build_from_files(["config.cfg"])

    assert cfg == {
      "simple_value": "abc",
      "custom_filter": "olleh",
      "custom_function": [3, 4, 5, 6, 7, 8, 9],
    }


if __name__ == "__main__":
  unittest.main()
