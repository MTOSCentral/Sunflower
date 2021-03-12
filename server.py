#Meow Tech Codenamed 'Central' (SE) Web Edition v1
#Meow Tech Codenamed Central Beta 1.5
#Project Name:Central
#State:Beta 1.5 -> Release Canidate
import json
from flask import Flask, redirect, url_for, render_template, request,session,flash
import sqlite3
from datetime import datetime
from api.api import apimodule
from werkzeug.utils import append_slash_redirect
from hashing import Hashing
import random
import string
import base64
from passwordencryption import EncryptPass
from datetime import datetime
from datetime import timedelta
from oobe.oobe import oobeui
from werkzeug.utils import secure_filename
brandinfo={}
conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
cursor = conn.cursor()
#Session Id Layout{"Public ID":"Private ID"}
sessionid={}
DEBUG=False
with open("branding\\branding.json") as file:
    brandinfo = json.load(file)
    productname = brandinfo["Vendor"]+" "+brandinfo["ProductName"]
    lc=brandinfo["License"]
    print(productname)
    file.close()
with open("lang\\en-US.json",encoding="utf-8") as file:
    lang = json.load(file)
    file.close()
with open(lc,encoding="utf-8") as file:
    license1=file.readlines()
    file.close()
app = Flask(__name__)
app.register_blueprint(apimodule, url_prefix="/api")
app.register_blueprint(oobeui, url_prefix="/oobe")
app.secret_key="ThEMoSTSeCuRePassWORdINThEWorLD"
year = datetime.now().strftime('%Y')
app.permanent_session_lifetime = timedelta(days=10)
build="0110"
branch="centralbeta1_5.210906"
fullbuildname=build+"."+branch
hasher=Hashing()
@app.route('/license')
def license():
    return render_template("nano/license.html",productname=productname,year=year,license=license1)
def gensession():
    global session
    global sessionid
    letters = string.ascii_letters
    letters=letters+string.digits
    pri = ''.join(random.choice(letters) for i in range(128))
    pub = ''.join(random.choice(letters) for i in range(128))
    sessionid[pub]=pri
    session["sessionid"]=pub
def regen():
    letters = string.ascii_letters
    letters=letters+string.digits
    #print("1st"+str(sessionid))
    pri = ''.join(random.choice(letters) for i in range(128))
    sessionid[session["sessionid"]]=pri
    #print("2nd"+str(sessionid))
def chklogin(user,pw):
    global conn
    cor=False
    if "a" == "a":
        hasher=Hashing()
        session.permanent = True
        user = user
        passwd = pw
        sqlstr='select * from users'
        cur=conn.execute(sqlstr)
        rows=cur.fetchall()
        #print(rows)
        #print(rows[5][0])
        for row in rows:
            #print('!')
            if hasher.check(passwd,row[1]) and user == row[0]:
                #session["user"] = user
                #session["role"] = row[2]
                #gensession()
                cor=True
                return [True,user,row[2]]
            #else:
                #pass
        if not cor:
            return [False,0]

@app.route("/login", methods=["POST", "GET"])
def login():
    global conn
    stmt = """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users';"""
    cur=conn.execute(stmt)
    result = cur.fetchone()
    if 1+1 !=2:
        pass
    #if result[0] == 0:
        #flash("Your Server Haven't Been Setup Yet.")
        #return redirect(url_for("oobe.start"))
    else:
        #print(chklogin("a","a"))
        cor=False
        if request.method == "POST":
            hasher=Hashing()
            session.permanent = True
            user = request.form["nm"]
            passwd = request.form["pass"]
            sqlstr='select * from users'
            tmp=conn.execute(sqlstr)
            #print(tmp)
            rows=tmp.fetchall()
            #print(rows)
            #print(rows[5][0])
            for row in rows:
                #print('!')
                if hasher.check(passwd,row[1]) and user == row[0]:
                    if user == "" or passwd=="":
                        flash(lang["msg12"])
                        return redirect(url_for("login"))
                    else:
                        session["user"] = user
                        session["role"] = row[2]
                        gensession()
                        cor=True
                        flash(lang["msg2"])
                        return redirect(url_for("home"))
                #else:
                    #pass
            if not cor:
                flash(lang["msg1"])
                return redirect(url_for("login"))

        else:
            if "role" in session:
                user = session["user"]
                flash(lang["msg3"])
                return redirect(url_for("home")) 
            else:
                return render_template("nano/login.html",productname=productname,year=year)
@app.route('/')
def home():
    if "user" in session:
        return render_template("nano/home.html",buildno=fullbuildname,productname=productname,year=year)
    else:
        flash(lang['msg5'])
        return(redirect(url_for("login")))

@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user")
        session.pop("role")
        if "sessionid" in session:
            session.pop("sessionid")
        if "step" in session:
            session.pop("step")
        if "add" in session:
            session.pop("add")
        if "child" in session:
            session.pop("child")
        if "cm" in session:
            session.pop("cm")
        flash(lang["msg4"])
        return redirect(url_for("login"))
    else:
        flash(lang["msg5"])
        return redirect(url_for("login"))

def chkroleloggedin(role):
    if 'sessionid' not in session:
        return '!!'
    elif session['sessionid'] not in sessionid:
        return "!!"
    elif 'role' not in session:
        return "!!"
    elif role==None:
        return True
    elif session['role'] == role:
        return True
    else:
        return False

###RTM REMOVE THIS!!!!
@app.route('/dbg')
def debugmode():
    global DEBUG
    if DEBUG:
        if chkroleloggedin(None) == "!!":
            return redirect(url_for("logout"))
        else:
            return sessionid[session["sessionid"]]
    else:
        flash("Error!You T")
        return redirect(url_for("home"))

def popadds():
    if "add" in session:
        session.pop("add")
    if "child" in session:
        session.pop("child")
    if "step" in session:
        session.pop("step")
    if "cm" in session:
        session.pop("cm")
@app.route('/addmoney', methods=["POST", "GET"])
def addmoney():
    role=chkroleloggedin('adult')
    if request.method=="POST":
        if role != "!!":
            if role:
                child=request.form["child"]
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
                    flash("The child account you entered either is not an valid account or is not a child.")
                    return redirect(url_for("addmoney"))
                else:
                    enckey=EncryptPass()
                    addmoney1=request.form["dollars"]
                    session["add"]=enckey.encrypt(sessionid[session["sessionid"]],str(addmoney1))
                    session["child"]=enckey.encrypt(sessionid[session["sessionid"]],child)
                    session["cm"]=enckey.encrypt(sessionid[session["sessionid"]],nowdollar)
                    #print(session["add"])
                    #flash("Success!")
                    return redirect(url_for("add_now"))
            else:
                flash(lang["msg6"])
                return redirect(url_for("home"))
        else:
            return redirect(url_for("logout"))
    else:
        if role != "!!":
            return render_template("nano/add.html",productname=productname,year=year)
        else:
            flash(lang["msg7"])
            return redirect(url_for("logout"))
            
@app.route('/add_now',methods=["POST", "GET"])
def add_now():
    #Add Now!
    if request.method == "POST":
        if "add" in session and "child" in session and "cm" in session:
            #session["add"]
            if chkroleloggedin(None) == "!!":
                return redirect(url_for("logout"))
            else:
                chklogin1=chklogin(request.form['nm'],request.form['pass'])
                if chklogin1[0]:
                    if chklogin1[2] == "adult":
                        #PREP THE COMMAND
                        enckey=EncryptPass()
                        child=enckey.decrypt(sessionid[session["sessionid"]],session["child"])
                        adder=enckey.decrypt(sessionid[session["sessionid"]],session["add"])
                        nowdollar=enckey.decrypt(sessionid[session["sessionid"]],session["cm"])
                        session.pop("child")
                        session.pop("add")
                        session.pop("cm")
                        cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)+int(adder))+'" WHERE Name="'+child+'"'
                        curs = conn.cursor()
                        curs.execute(cmd)
                        conn.commit()
                        #Remake KEY

                        #History Module
                        #Coming Soon :>
                        regen()
                        flash(lang["success"])
                        return redirect(url_for("home"))
                else:
                    popadds()
                    flash(lang["msg1"]+"/"+lang["msg8"])
                    return redirect(url_for("home"))
        else:
            return redirect(url_for("addmoney"))
    else:
        #Get
        if "add" in session and "child" in session and "cm" in session:
            flash(lang["msg9"])
            return render_template("nano/login.html",productname=productname,year=year)
        else:
            flash(lang["msg10"])
            return redirect(url_for("logout"))
@app.route('/removemoney', methods=["POST", "GET"])
def removemoney():
    role=chkroleloggedin('adult')
    if request.method=="POST":
        if role != "!!":
            if role:
                child=request.form["child"]
                sqlstr='select * from users'
                cur=conn.execute(sqlstr)
                rows=cur.fetchall()
                nowdollar="D"
                for row in rows:
                    #print('RAN USER='+session['user'])
                    if row[0] == child and row[2]=="child":
                        print(row[3])
                        nowdollar=row[3]
                if nowdollar == "D":
                    flash("The child account you entered either is not an valid account or is not a child.")
                    return redirect(url_for("addmoney"))
                else:
                    enckey=EncryptPass()
                    addmoney1=request.form["dollars"]
                    session["add"]=enckey.encrypt(sessionid[session["sessionid"]],str(addmoney1))
                    session["child"]=enckey.encrypt(sessionid[session["sessionid"]],child)
                    session["cm"]=enckey.encrypt(sessionid[session["sessionid"]],str(nowdollar))
                    session["step"]=enckey.encrypt(sessionid[session["sessionid"]],'1')
                    print(session["add"])
                    #return 'Added Money Now!'
                    flash(lang["success"])
                    return redirect(url_for("remove_now"))
            else:
                flash(lang["msg6"])
                return redirect(url_for("home"))
        else:
            return redirect(url_for("logout"))
    else:
        if role != "!!":
            return render_template("nano/add.html",productname=productname,year=year)
        else:
            flash(lang["msg7"])
            return redirect(url_for("logout"))
@app.route('/remove_now',methods=["POST", "GET"])
def remove_now():
    #Remove Now!
    if request.method == "POST":
        if "add" in session and "child" in session and "cm" in session and "step" in session:
            #session["add"]
            if chkroleloggedin(None) == "!!":
                flash(lang["msg5"])
                return redirect(url_for("logout"))
            enckey=EncryptPass()
            if enckey.decrypt(sessionid[session["sessionid"]],session["step"]) !="1":
                return redirect(url_for('removemoney'))
            else:
                chklogin1=chklogin(request.form['nm'],request.form['pass'])
                if chklogin1[0]:
                    if chklogin1[2] == "adult":
                        #PREP THE COMMAND
                        session["step"]=enckey.encrypt(sessionid[session["sessionid"]],'2')
                        #child=enckey.decrypt(sessionid[session["sessionid"]],session["child"])
                        #adder=enckey.decrypt(sessionid[session["sessionid"]],session["add"])
                        #nowdollar=enckey.decrypt(sessionid[session["sessionid"]],session["cm"])
                        #session.pop("child")
                        #session.pop("add")
                        #session.pop("cm")
                        #Remake KEY

                        #History Module
                        #Coming Soon :>
                        return redirect(url_for("remove_now2"))
                        #return "Hurray:>:>:<:>:<:>:<>"
                else:
                   flash(lang["msg6"])
                   return redirect(url_for("home"))
        else:
            return redirect(url_for("removemoney"))
    else:
        if "add" in session and "child" in session and "cm" in session and "step" in session:
            flash(lang["msg9"])
            return render_template("nano/login.html",productname=productname,year=year)
        else:
            flash(lang["msg10"])
            return redirect(url_for("logout"))
@app.route('/remove_now2',methods=["POST", "GET"])
def remove_now2():
    #Remove Now!
    if request.method == "POST":
        if "add" in session and "child" in session and "cm" in session:
            #session["add"]
            if chkroleloggedin(None) == "!!":
                return redirect(url_for("logout"))
            enckey=EncryptPass()
            if enckey.decrypt(sessionid[session["sessionid"]],session["step"]) !="2":
                return redirect(url_for('removemoney'))
            else:
                chklogin1=chklogin(request.form['nm'],request.form['pass'])
                if chklogin1[0]:
                    if chklogin1[2] == "child" and request.form['nm'] == enckey.decrypt(sessionid[session["sessionid"]],session["child"]):
                        #PREP THE COMMAND
                        #enckey=EncryptPass()
                        child=enckey.decrypt(sessionid[session["sessionid"]],session["child"])
                        adder=enckey.decrypt(sessionid[session["sessionid"]],session["add"])
                        nowdollar=enckey.decrypt(sessionid[session["sessionid"]],session["cm"])
                        popadds()
                        #Remake KEY
                        regen()
                        cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)-int(adder))+'" WHERE Name="'+child+'"'
                        curs = conn.cursor()
                        curs.execute(cmd)
                        conn.commit()
                        #History Module
                        #Coming Soon :>
                        flash(lang["success"])
                        return redirect(url_for("home"))
                else:
                    flash(lang["msg1"]+"/"+lang["msg8"]+"/ Your User is not the specified user.")
                    popadds()
                    return redirect(url_for("home"))
        else:
            flash("Unknown Error.")
            popadds()
            return redirect(url_for("removemoney"))
    else:
        if "add" in session and "child" in session and "cm" in session and "step" in session:
            flash(lang["msg11"])
            return render_template("nano/login.html",productname=productname,year=year)
        else:
            flash(lang["msg10"])
            popadds()
            return redirect(url_for("logout"))
#Load Modular Components
if __name__ == "__main__":
	app.run(port=8888, debug=True,host="0.0.0.0")

# End Of Code - Meow Tech Codenamed Central
# Thanks For Using Meow Tech Codenamed Central
#Remarks:

"""
This Project Is Licensed Under The EPL (Eclipse Public License)
A copy of the license (license.txt) is included with the source code.
Copyright (c) Meow Tech Open Source 2020-2021, all rights reserved
DISCLAMER:DO NOT MODIFIY THE COPYRIGHT NOTICE IN THIS PART OF THE SOURCE CODE.
Note:Bootstrap Is Licensed Under MIT license.
"""

#Release Canidate Is Coming Soon.......