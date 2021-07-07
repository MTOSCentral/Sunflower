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
from werkzeug.utils import secure_filename
oobeui=Blueprint("oobe", __name__, static_folder="static", template_folder="template")
conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
cursor = conn.cursor()
year = datetime.now().strftime('%Y')
hasher=Hashing()
all_steps=['License Agreement','User Accounts']
links=['/','/setup']
with open("branding\\branding.json") as file:
    brandinfo = json.load(file)
    productname = brandinfo["Vendor"]+" "+brandinfo["ProductName"]
    lc=brandinfo["License"]
    print(productname)
    file.close()
with open("lang\\zh-HK.json",encoding="utf-8") as file:
    lang = json.load(file)
    file.close()
with open(lc,encoding="utf-8") as file:
    license1=file.readlines()
    file.close()
@oobeui.route('/')
def boot():
    session["stepoobe"]=0
    return render_template("nano/welcome.html",prodname=productname,ver="2.0.0")
@oobeui.route('/license',methods=['POST','GET'])
def start():
    stmt = """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users';"""
    cursor.execute(stmt)
    result = cursor.fetchone()
    #result=[0]
    if "stepoobe" not in session:
        return redirect(url_for("oobe.boot"))
    if result[0] == 0 and session["stepoobe"] == 0:
        if request.method == "POST":
            session['stepoobe']=1
            return redirect(url_for("oobe.setup"))
        else:
            if 'stepoobe' in session:
                #session.pop('stepoobe')
                pass
            return render_template("nano/license2.html",productname=productname,year=year,license=license1,steps=all_steps,current=all_steps[0],link=links)
        #conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
        #cursor = conn.cursor()
    else:
        if request.method == 'GET':
            flash("Server is already set up.")
            return redirect(url_for("home"))
        else:
            flash("This is not possible")
            return redirect(url_for("home"))

@oobeui.route('/setup',methods=["POST","GET"])
def setup():
    if "stepoobe" in session:
        if session["stepoobe"] == 1:
            global conn
            if request.method == 'POST':
                a1n = request.form['a1n']
                a1p = request.form['a1p']
                a2n = request.form['a2n']
                a2p = request.form['a2p']
                cn = request.form['cn']
                cp = request.form['cp']
                if a1n.strip() =="" or a1p =="" or a2n.strip() == "" or a2p == "" or cn.strip() == "" or cp=="":
                    flash("You Must Enter A Username/Password")
                    return redirect(url_for("oobe.setup"))
                elif a1n == a2n or a2n == cn or a1n==cn:
                    flash("Username cannot be the same")
                    return redirect(url_for("oobe.setup"))
                elif len(a1p) < 1 or len(a2p) < 1 or len(cp) <1:
                    flash("Password must be greater than 1 characters.")
                    return redirect(url_for("oobe.setup"))
                else:
                    curs = conn.cursor()
                    sqlstr='CREATE TABLE IF NOT EXISTS users \
                    ("Name" TEXT,"Password" TEXT,"Role" TEXT,"Money" TEXT)'
                    cursor.execute(sqlstr)
                    conn.commit()
                    sqlstr='insert into users values("'+a1n+'","'+hasher.hash(a1p)+'", "'+"adult"+'", "'+'0'+'")'
                    curs.execute(sqlstr)
                    conn.commit()
                    sqlstr='insert into users values("'+a2n+'","'+hasher.hash(a2p)+'", "'+"adult"+'", "'+'0'+'")'
                    curs = conn.cursor()
                    curs.execute(sqlstr)
                    conn.commit()
                    sqlstr='insert into users values("'+cn+'","'+hasher.hash(cp)+'", "'+"child"+'", "'+'0'+'")'
                    curs = conn.cursor()
                    curs.execute(sqlstr)
                    conn.commit()
                    session["stepoobe"]=2
                    flash("Setup Success")
                    return redirect(url_for("home"))
            else:
                return render_template("nano/oobe1.html",productname=productname,year=year,steps=all_steps,current=all_steps[1],link=links)
        elif session["stepoobe"] > 1:
            flash("You cannot modify user once it is submitted.")
            return redirect(url_for("oobe.start"))
        else:
            flash("You Must Accept The License Term.")
            return redirect(url_for("oobe.start"))
    else:
        flash("You Must Accept The License Term.")
        return redirect(url_for("oobe.start"))
