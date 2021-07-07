#Settings For Meow Tech Codenamed Central
from flask import Blueprint,session,render_template,Response,request,flash,url_for
import random
import string
import shutil
from werkzeug.utils import redirect
from hashing import Hashing
import sqlite3
from flask import json
from datetime import datetime
import os
settingsui=Blueprint("settings", __name__, static_folder="static", template_folder="template")
year = datetime.now().strftime('%Y')
hasher=Hashing()
with open("branding"+os.sep+"branding.json") as file:
    brandinfo = json.load(file)
    productname = brandinfo["Vendor"]+" "+brandinfo["ProductName"]
    lc=brandinfo["License"]
    print(productname)
    file.close()
with open("lang"+os.sep+"zh-HK.json",encoding="utf-8") as file:
    lang = json.load(file)
    file.close()
with open(lc,encoding="utf-8") as file:
    license1=file.readlines()
    file.close()
@settingsui.route('/')
def boot():
    session["stepoobe"]=0
    return render_template("nano/welcome.html",prodname=productname,ver="2.0.0")