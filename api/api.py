#OOBE For Meow Tech Codenamed Central
from flask import Blueprint,session,render_template,Response,request,flash,url_for
import random
import string
import shutil
from werkzeug.utils import redirect
from hashing import Hashing
import sqlite3
from flask import json
from datetime import datetime
from flask import jsonify
from kernel import Kernel
apimodule=Blueprint("api", __name__, static_folder="static", template_folder="template")
conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
cursor = conn.cursor()
year = datetime.now().strftime('%Y')
hasher=Hashing()
links=['/','/setup']
apis={}
def genapi(user,passwd):
    kernel=Kernel()
    cor=kernel.checkuser(user,passwd)[0]
    if cor:
        row=kernel.checkuser(user,passwd)[1]
    if cor:
        global apis
        cor=True
        letters = string.ascii_letters
        letters=letters+string.digits
        apikey = ''.join(random.choice(letters) for i in range(64))
        apis[apikey]=user
        #{'APIKEY':[Username,Role]}
        print("[Debug Information] API KEY LIST = "+str(apis))
        return {'value':apikey}
    if not cor:
        return {'value':'0x00000'}

@apimodule.route('/chkuser/<username>/<password>/<role>')
def checklogin(username,password,role):
    cor=False
    kernel=Kernel()
    if role.lower()=="none":
        cor=kernel.checkuser(username,password)[0]
        if cor:
            global apis
            cor=True
            return {'value':True}
        if not cor:
            return {'value':'PWINC'}
    else:
        cor=kernel.checkuser(username,password)[0]
        if cor:
            rcor=kernel.chkrole(username,role)
        if cor and rcor:
            global apis
            return {'value':True}
        elif cor and not rcor:
            return {'value':'RINC'}
        if not cor:
            return {'value':'PWINC'}

@apimodule.route('/getkey/<usrname>/<passwd>')
def genapikey(usrname,passwd):
    return jsonify(genapi(usrname,passwd))
# /addmoney/adult/Add/Child
@apimodule.route('/addmoney/<apikey>/<int:var1>/<var2>/<var3>')
def addmoney(apikey,var1,var2,var3):
    global apis
    kernel=Kernel()
    if apikey in apis:
        if kernel.chkrole(apis[apikey],"adult"):
            child=var2
            money=var1
            notes=var3
            tmp=kernel.addmoney(child,apis[apikey],"adult",money,notes)
            print(tmp)
            if tmp=="0x0002":
                return jsonify({"value":"0x00003"})
            elif tmp==None:
                return jsonify({"value":"Completed"})
                apis.pop(apikey)
        else:
            return jsonify({"value":"0x00001"})
            #apis.pop(apikey)
    else:
        return jsonify({'value':'0x00002'})

@apimodule.route('/removemoney/<apikey>/<int:var1>/<var2>/<var3>')
def minus(apikey,var1,var2,var3):
    global apis
    kernel=Kernel()
    if apikey in apis:
        if kernel.chkrole(apis[apikey],"adult"):
            child=var2
            money=var1
            notes=var3
            tmp=kernel.removemoney(child,apis[apikey],"adult",money,notes)
            print(tmp)
            if tmp=="0x0002":
                return jsonify({"value":"0x00003"})
            elif tmp==None:
                return jsonify({"value":"Completed"})
                apis.pop(apikey)
        else:
            return jsonify({"value":"0x00001"})
            #apis.pop(apikey)
    else:
        return jsonify({'value':'0x00002'})
