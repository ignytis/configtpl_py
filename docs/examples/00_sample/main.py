import json

from configtpl_py_native import ConfigBuilder

cfg = ConfigBuilder()
output = cfg.render(["config.cfg"])

print(json.dumps(output, indent=4))
