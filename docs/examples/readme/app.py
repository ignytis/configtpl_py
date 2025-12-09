import json

from configtpl.main import ConfigTpl


def filter_str_rev(value: str) -> str:
  return value[::-1]


def function_str_duplicate(value: str, n_times: int) -> str:
  return value * n_times


builder = ConfigTpl(
  defaults={"default": "default_value"},
  env_var_prefix="MY_APP",
  jinja_globals={
    "str_duplicate": function_str_duplicate,
  },
  jinja_filters={
    "str_rev": filter_str_rev,
  },
)
cfg = builder.build_from_files(
  paths=["my_first_config.cfg", "my_second_config.cfg"],
  overrides={"override": "overridden"},
)
print(json.dumps(cfg, indent=2))  # noqa: T201
