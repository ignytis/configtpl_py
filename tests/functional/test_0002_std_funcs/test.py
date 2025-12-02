import unittest

from configtpl.main import ConfigTpl


class TestStdFunccs(unittest.TestCase):
  """
  Tests standard Jinja functions.
  "Standard" means "standard for this library" or "default" functions
  """

  def setUp(self) -> None:
    self.maxDiff = None
    return super().setUp()

  def test_std_funcs(self) -> None:
    cfg = ConfigTpl().build_from_files(["config.cfg"])

    assert cfg == {
      # file_contents are fetched using 'file' global.
      # In this test it's relative path, but it could be also global path
      "file_contents": {
        "additional_level": {
          "var_a": 123,
          "var_b": False,
        },
      },
      # "greetings" is based on output of a system command splitted by line break
      # TODO: does it works on Windows! Perhaps another test is needed. As an option - OS check
      "greetings": [
        "Hello, First!",
        "Hello, Second!",
        "Hello, Third!",
      ],
      # Frequently used hash and encoding functions
      "globals": {
        "base64": "SGVsbG8sIFdvcmxk",
        "base64_decode": "Lorem Ipsum",
        "md5": "82bb413746aee42f89dea2b59614f9ef",
        "sha512": "03675ac53ff9cd1535ccc7dfcdfa2c458c5218371f418dc136f2d19ac1fbe8a5",
      },
      "server": {
        "host": "example.com",
        "port": 1234,
      },
      "urls": {
        "base": "example.com",
        "subdomain": "sample_value.example.com",
      },
    }


if __name__ == "__main__":
  unittest.main()
