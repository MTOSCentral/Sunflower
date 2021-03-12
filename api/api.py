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
apimodule=Blueprint("api", __name__, static_folder="static", template_folder="template")
conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
cursor = conn.cursor()
year = datetime.now().strftime('%Y')
hasher=Hashing()
links=['/','/setup']
apis={'child':['lala3','child'],'adult':['lala','adult']}
with open("branding\\branding.json") as file:
    brandinfo = json.load(file)
    productname = brandinfo["Vendor"]+" "+brandinfo["ProductName"]
    lc=brandinfo["License"]
    print(productname)
    file.close()
with open("lang\\en-us.json",encoding="utf-8") as file:
    lang = json.load(file)
    file.close()
with open(lc,encoding="utf-8") as file:
    license1=file.readlines()
    file.close()
def genapi(user,passwd):
    hasher=Hashing()
    sqlstr='select * from users'
    cur=conn.execute(sqlstr)
    rows=cur.fetchall()
    cor=False
    for row in rows:
        if hasher.check(passwd,row[1]) and user == row[0]:
            global apis
            #session["user"] = user
            #session["role"] = row[2]
            #gensession()
            cor=True
            letters = string.ascii_letters
            letters=letters+string.digits
            apikey = ''.join(random.choice(letters) for i in range(64))
            apis[apikey]=[user,row[2]]
            #{'APIKEY':[Username,Role]}
            print("[Debug Information] API KEY LIST = "+str(apis))
            return {'value':apikey}
        #else:
            #pass
    if not cor:
        return {'value':'0x00000'}
@apimodule.route('/chkuser/<username>/<password>/<role>')
def checklogin(username,password,role):
    hasher=Hashing()
    sqlstr='select * from users'
    cur=conn.execute(sqlstr)
    rows=cur.fetchall()
    cor=False
    if role.lower()=="none":
        for row in rows:
            if hasher.check(password,row[1]) and username == row[0]:
                global apis
                #session["user"] = user
                #session["role"] = row[2]
                #gensession()
                cor=True
                return {'value':True}
            #else:
                #pass
        if not cor:
            return {'value':'PWINC'}
    else:
        for row in rows:
            if hasher.check(password,row[1]) and username == row[0] and role == row[2]:
                global apis
                #session["user"] = user
                #session["role"] = row[2]
                #gensession()
                cor=True
                return {'value':True}
            elif hasher.check(password,row[1]) and username == row[0]:
                return {'value':'RINC'}
            #else:
                #pass
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

