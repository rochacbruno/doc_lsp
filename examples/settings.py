"""This is a python configuration file,each variable is detailed with extensive details on settings.py.md"""
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