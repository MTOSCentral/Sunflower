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
        apis[apikey]=[user,row[2]]
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
@apimodule.route('/addmoney/<apikey>/<int:var1>/<var2>')
def addmoney(apikey,var1,var2):
    global apis
    if apikey in apis:
        if apis[apikey][1] == "adult":
            child=var2
            money=var1
            sqlstr='select * from users'
            cur=conn.execute(sqlstr)
            rows=cur.fetchall()
            nowdollar="D"
            for row in rows:
                # print('RAN USER='+session['user'])
                if row[0] == child and row[2]=="child":
                    #print(row[3])
                    #print("--------")
                    nowdollar=row[3]
                    #print(nowdollar)
                
            if nowdollar == "D":
                return jsonify({"value":"0x00003"})
            else:
                cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)+int(money))+'" WHERE Name="'+child+'"'
                curs = conn.cursor()
                curs.execute(cmd)
                conn.commit()
                return jsonify({"value":"Completed"})
        else:
            return jsonify({"value":"0x00001"})
            #apis.pop(apikey)
    else:
        return jsonify({'value':'0x00002'})

@apimodule.route('/minus/<apikey>/<int:var1>/<var2>')
def minus(apikey,var1,var2):
    global apis
    if apikey in apis:
        if apis[apikey][1] == "adult":
            child=var2
            money=var1
            sqlstr='select * from users'
            cur=conn.execute(sqlstr)
            rows=cur.fetchall()
            nowdollar="D"
            for row in rows:
                # print('RAN USER='+session['user'])
                if row[0] == child and row[2]=="child":
                    #print(row[3])
                    #print("--------")
                    nowdollar=row[3]
                    #print(nowdollar)
                
            if nowdollar == "D":
                return jsonify({"value":"0x00003"})
            else:
                cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)-int(money))+'" WHERE Name="'+child+'"'
                curs = conn.cursor()
                curs.execute(cmd)
                conn.commit()
                return jsonify({"value":"Completed"})
        else:
            return jsonify({"value":"0x00001"})
            #apis.pop(apikey)
    else:
        return jsonify({'value':'0x00002'})

