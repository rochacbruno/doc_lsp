"""Python configuration file,
each variable is detailed with extensive details on
settings.py.md
"""

SERVER = "localhost"
PORT = 1234
DEBUG = True
ALLOW_RESOURCE_MANAGEMENT = True
DEFAULT_ORG = "Acme"

DATABASES = {
  "default": {
    "NAME": "foo",
    "OPTIONS": {
        "TLS_VERIFICATION": True,
        "TIMEOUT": 30
    }
  }
}


"""

hover this date:

2025-01-01

this LSP will do the same but instead of showing the date, this
will show the documentation for the variable.

The documentation will be read from the settings.py.md file.

"""