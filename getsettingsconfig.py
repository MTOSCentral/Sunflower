import json
with open("settings.cfg") as f:
    settings = json.load(f)
def translate(a):
    if a == "0":
        return False
    elif a == "1":
        return True
    else:
        return a
def default_language():
    return settings["DefaultLanguage"]
def default_currency():
    return settings["DefaultCurrency"]
def showRemainderInAdUI():
    return settings["RemainInAdultUI"]