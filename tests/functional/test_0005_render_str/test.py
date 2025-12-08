import unittest

from configtpl.main import ConfigTpl

CFG = """\
{% set domain = "example.com" %}
domain: {{ domain }}
subdomain: mysite.{{ domain }}
sample_filter: {{ "abc" | md5 }}
sample_global: {{ env("SAMPLE_ENV_KEY") }}
test: this will be overridden by MY_APP__TEST
file_content:
    {{ file("file_cfg.yaml") | indent(2) }}
file_content_2:
    {% include "file_cfg.yaml" %}\
"""


class TestRenderStr(unittest.TestCase):
  """
  Tests rendering config from string
  """

  def setUp(self) -> None:
    self.maxDiff = None
    return super().setUp()

  def test_custom_funcs(self) -> None:
    builder = ConfigTpl(env_var_prefix="MY_APP")
    cfg = builder.build_from_str(CFG)
    assert cfg == {
      "domain": "example.com",
      "test": "test_val",
      "subdomain": "mysite.example.com",
      "sample_filter": "900150983cd24fb0d6963f7d28e17f72",
      "sample_global": "sample_value",
      "file_content": {
        "file_key": "file_value",
      },
      "file_content_2": {
        "file_key": "file_value",
      },
    }


if __name__ == "__main__":
  unittest.main()
