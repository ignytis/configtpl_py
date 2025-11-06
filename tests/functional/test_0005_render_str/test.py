import unittest

from configtpl.config_builder import ConfigBuilder

CFG = """\
{% set domain = "example.com" %}
domain: {{ domain }}
subdomain: mysite.{{ domain }}
sample_filter: {{ "abc" | md5 }}
sample_global: {{ env("SAMPLE_ENV_KEY") }}
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
    builder = ConfigBuilder()
    cfg = builder.build_from_str(CFG)
    assert cfg == {
      "domain": "example.com",
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
