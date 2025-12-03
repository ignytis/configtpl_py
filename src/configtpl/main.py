import os
import os.path
from collections.abc import Callable
from copy import deepcopy
from pathlib import Path

import yaml
from jinja2 import Template

from .jinja.env_factory import JinjaEnvFactory
from .utils.dicts import dict_deep_merge


class ConfigTpl:
  def __init__(
    self,
    *,
    defaults: dict | None = None,
    env_var_prefix: str | None = None,
    jinja_constructor_args: dict | None = None,
    jinja_filters: dict | None = None,
    jinja_globals: dict | None = None,
  ):
    """
    A constructor for Config Builder.

    Args:
        defaults (dict | None): Default values for configuration
        env_var_prefix (str | None): if specified, environment variables with
          this prefix will be injected into config
        jinja_constructor_args (dict | None): argument for Jinja environment constructor
        jinja_globals (dict | None): globals for Jinja environment constructor
        jinja_filters (dict | None): filters for Jinja environment constructor
    """
    self.jinja_env_factory: JinjaEnvFactory = JinjaEnvFactory(
      constructor_args=jinja_constructor_args,
      globs=jinja_globals,
      filters=jinja_filters,
    )
    if defaults is None:
      defaults = {}
    self.defaults = defaults
    self.env_var_prefix = env_var_prefix

  def set_global(self, k: str, v: Callable) -> None:
    """
    Sets a global for children Jinja environments
    """
    self.jinja_env_factory.set_global(k, v)

  def set_filter(self, k: str, v: Callable) -> None:
    """
    Sets a filter for children Jinja environments
    """
    self.jinja_env_factory.set_filter(k, v)

  def build_from_files(
    self,
    paths: list[str],
    overrides: dict | None = None,
    ctx: dict | None = None,
  ) -> dict:
    """
    Renders files from provided paths.

    Args:
        ctx (dict | None): additional rendering context which is NOT injected into configuration
        overrides (dict | None): Overrides are applied at the very end stage after all templates are rendered
        paths (list[str]): Paths to configuration files. Examples:
            ['/opt/myapp/myconfig_first.cfg', '/opt/myapp/myconfig_second.cfg']
    Returns:
        dict: The rendered configuration
    """
    output_cfg, ctx, overrides = self._init_render_params(ctx, overrides)

    for cfg_path_raw in paths:
      cfg_path = os.path.realpath(cfg_path_raw)
      ctx = {**output_cfg, **ctx}
      cfg_iter: dict = self._render_cfg_from_file(cfg_path, ctx)

      output_cfg = dict_deep_merge(output_cfg, cfg_iter)

    # Append overrides
    return dict_deep_merge(output_cfg, overrides)

  def build_from_str(
    self,
    s: str,
    work_dir: str | None = None,
    overrides: dict | None = None,
    ctx: dict | None = None,
  ) -> dict:
    """
    Renders config from string.

    Args:
        s (str): a Jinja template string which can be rendered into YAML format
        work_dir (str): a working directory.
            Include statements in Jinja template will be resolved relatively to this path
        ctx (dict | None): additional rendering context which is NOT injected into configuration
        overrides (dict | None): Overrides are applied at the very end stage after all templates are rendered
    Returns:
        dict: The rendered configuration
    """
    output_cfg, ctx, overrides = self._init_render_params(ctx, overrides)
    if work_dir is None:
      work_dir = str(Path.cwd())

    cfg = self._render_cfg_from_str(s, ctx, work_dir)
    output_cfg = dict_deep_merge(output_cfg, cfg)

    return dict_deep_merge(output_cfg, overrides)

  def _render_cfg_from_file(self, path: str, ctx: dict) -> dict:
    """
    Renders a template file into config dictionary in two steps:
    1. Renders a file as Jinja template
    2. Parses the rendered file as YAML template
    """
    p = Path(path)
    jinja_env = self.jinja_env_factory.get_fs_jinja_environment(p.parent)
    tpl = jinja_env.get_template(p.name)
    return _render_tpl(tpl, ctx)

  def _render_cfg_from_str(self, s: str, ctx: dict, work_dir: str) -> dict:
    jinja_env = self.jinja_env_factory.get_fs_jinja_environment(work_dir)
    tpl = jinja_env.from_string(s)
    return _render_tpl(tpl, ctx)

  def _init_render_params(
    self,
    ctx: dict | None,
    overrides: dict | None,
  ) -> tuple[dict, dict, dict]:
    """
    Initializes rendering parameters.
    """
    output_cfg = deepcopy(self.defaults)
    output_cfg = dict_deep_merge(output_cfg, _get_cfg_from_env(self.env_var_prefix))

    if ctx is None:
      ctx = {}
    if overrides is None:
      overrides = {}

    return output_cfg, ctx, overrides


def _render_tpl(tpl: Template, ctx: dict) -> dict:
  tpl_rendered = tpl.render(ctx)
  result = yaml.safe_load(tpl_rendered)
  if result is None:
    return {}

  return result


def _parse_env_var_value(value: str) -> object:  # noqa: PLR0911 too  many return statements
  """
  Parses a string value from an environment variable into a typed value.
  """
  if not value:
    return None

  # Values wrapped in single or double quotes are always strings
  if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
    return value[1:-1]

  # `TRUE` and `FALSE` are converted to corresponding Boolean values.
  val_upper = value.upper()
  if val_upper == "TRUE":
    return True
  if val_upper == "FALSE":
    return False

  # If value matches to format of integer of floating point number (consider negative values),
  # convert to corresponding numbers.
  try:
    return int(value)
  except ValueError:
    pass

  try:
    return float(value)
  except ValueError:
    pass

  return value


def _get_cfg_from_env(env_prefix: str | None = None) -> dict:
  """
  Parses environment variables into a dictionary.
  If prefix is not provided, an empty dictionary is returned.
  """
  if env_prefix is None:
    return {}

  env_vars = {}
  prefix = f"{env_prefix}__"
  for key, value in os.environ.items():
    if key.startswith(prefix):
      path = key[len(prefix) :].lower().split("__")

      current_level = env_vars
      for part in path[:-1]:
        current_level = current_level.setdefault(part, {})
      current_level[path[-1]] = _parse_env_var_value(value)
  return env_vars
