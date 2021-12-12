import json
import os
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def get_outer_shell(path="outer_shell_default.json", **kwargs):
    path = kwargs["path"] if 'path' in kwargs else path
    JSONModel = None
    with open(os.path.join(BASE_DIR, "static")+"/defaults/"+path) as file:
        JSONModel = json.load(file)
    return JSONModel


def everyday(path="inner_shell_everyday_month_default.json", **kwargs):
    path = kwargs["path"] if 'path' in kwargs else path
    JSONModel = None
    with open(os.path.join(BASE_DIR, "static")+"/defaults/"+path) as file:
        # JSONModel = file.read()
        JSONModel = json.load(file)
    # loadedJson = json.loads(JSONModel)
    # return loadedJson
    return JSONModel


def business(path="inner_shell_business_month_default.json", **kwargs):
    path = kwargs["path"] if 'path' in kwargs else path
    JSONModel = None
    return JSONModel


def investment(path="inner_shell_investment_month_default.json", **kwargs):
    path = kwargs["path"] if 'path' in kwargs else path
    JSONModel = None
    return JSONModel
