import unittest

from configtpl.main import ConfigTpl


class TestSimple(unittest.TestCase):
  def setUp(self) -> None:
    self.maxDiff = None
    return super().setUp()

  def test_simple(self) -> None:
    cfg = ConfigTpl().build_from_files(["config.cfg"])

    assert cfg == {
      "urls": {
        "base": "example.com",
        "mail": "mail.example.com",
      },
      "server": {
        "host": "example.com",
        "port": 1234,
      },
    }


if __name__ == "__main__":
  unittest.main()
