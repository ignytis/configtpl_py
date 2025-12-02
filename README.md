# configtpl

This library builds configuration in two stages:

1. Renders the provided configuration as Jinja templates
1. Parses the rendered data as YAML file

# Features

- Uses Jinja2 and Yaml capabilities to build a dynamic configuration
- Multiple configuration files might be passed. The library merges all of them into single config.
- Basic confuration includes Jinja functions and filters for general-purpose tasks:
  - Reading the environment variables
  - Execution of system commands
  - Hashing

# Standard features

## Filters

In addition to [Jinja buildin filters](https://tedboy.github.io/jinja2/templ14.html#list-of-builtin-filters), the library provides the following ones:


| Filter        | Description                                               |
|---------------|-----------------------------------------------------------|
| base64        | Base64 encoding                                           |
| base64_decode | Base64 decoding                                           |
| md5           | MD5 hash                                                  |
| sha256        | SHA-256 hash                                              |
| sha512        | SHA-512 hash                                              |
| split_space   | Splits a string with space separator into list of strings |

## Functions

See also [List of Global Functions](https://tedboy.github.io/jinja2/templ16.html#list-of-global-functions) on Jinja page

| Function                      | Description                                                    |
|-------------------------------|----------------------------------------------------------------|
| cmd(cmd: str)                 | Executes a system command and returns the standard output      |
| cwd()                         | Returns the current working directory                          |
| env(name: str, default: str)  | Returns the value of enviroment variable `name` if it exists,  |
|                               | or falls back to `default` value otherwise                     |
| file(path: str)               | Reads the file and returns the contents                        |
| uuid                          | Generates a UUID e.g `1f6c868d-f9b7-4d3f-b7c9-48048b065019`    |

# Examples

You can check the [functional tests folder](tests/functional) for more examples.

A very simple example of usage is provided below:

```yaml
# my_first_config.cfg

{% set my_val = "abc" %}
app:
  param_env: "{{ env('MY_ENV_VAR', 'default') }}"
  param1: "{{ my_val }}"
```

```yaml
# my_second_config.cfg

app:
  param2: def
  param3: "{{ app.param1 }}123"
hash: "{{ app.param1 | md5 }}"
```


```python
# app.py

import json
from configtpl.config_builder import ConfigBuilder

builder = ConfigBuilder()
cfg = builder.build_from_files(["my_first_config.cfg","my_second_config.cfg"])
print(json.dumps(cfg, indent=2))

```

```bash
# Execution

MY_ENV_VAR=testing python ./app.py

# output
{
  "app": {
    "param_env": "testing",
    "param1": "abc",
    "param2": "def",
    "param3": "abc123"
  },
  "hash": "900150983cd24fb0d6963f7d28e17f72"
}
```
