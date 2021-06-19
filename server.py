#Meow Tech Codenamed 'Central' (SE) Web Edition v1.1
#Meow Tech Codenamed Central v1.1 Redstone
#Project Name:Central Redstone
#Mint Engine Implemented(kernel.py)
#State:Beta/Prerelease -> Release Canidate
import json
import glob
from otp import OTP
from tabulate import tabulate
from flask import Flask, redirect, url_for, render_template, request,session,flash,send_file
import sqlite3
from datetime import datetime
from api.api import apimodule
from werkzeug.utils import append_slash_redirect
from hashing import Hashing
from flask_qrcode import QRcode
import random
import string
import base64
from passwordencryption import EncryptPass
from datetime import datetime
from datetime import timedelta
from oobe.oobe import oobeui
from werkzeug.utils import secure_filename
from kernel import Kernel
from history import History
import os
glob.glob('*.txt', recursive=True)
brandinfo={}
conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
cursor = conn.cursor()
#Session Id Layout{"Public ID":"Private ID"}
sessionid={}
DEBUG=False
glob.glob('*.txt', recursive=True)
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
#Implement CFGs - Coming v1.6
#Language Pack Support
#Assuming Setup Using OOBE.
#End Of Language Pack Support
app = Flask(__name__)
QRcode(app)
app.register_blueprint(apimodule, url_prefix="/api")
app.register_blueprint(oobeui, url_prefix="/oobe")
app.secret_key="ThEMoSTSeCuRePassWORdINThEWorLD"
app.static_folder = 'static'
year = datetime.now().strftime('%Y')
app.permanent_session_lifetime = timedelta(days=10)
build="0300"
branch="rs_rc1.210211"
fullbuildname=build+"."+branch
FRIENDLYVERSION="1.5.0_PRERELEASE"
hasher=Hashing()
#DO NOT HARDCODE
langname="zh-HK.langpck"
def langpack_rd():
    global productname
    with open(f"langpck\\{langname}\\strings.sf.json","r", encoding='utf-8') as f:
        jl=json.loads(f.read())
        ovr=jl["overrideproductname"]
        if ovr == "1":
            productname=jl["0"]
langpack_rd()
def langpack(strcode):
    global langname
    with open(f"langpck\\{langname}\\strings.sf.json","r", encoding='utf-8') as f:
        strings=json.loads(f.read())[str(strcode)]
    return strings
app.jinja_env.globals.update(strings=langpack)
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
        kernel=Kernel()
        tmp=kernel.checkuser(user, pw)
        if tmp[0] == False:
            return [False,0]
        else:
            return [tmp[0],tmp[1][0],tmp[1][2]]

@app.route("/login", methods=["POST", "GET"])
def login():
    global conn
    stmt = """SELECT count(*) FROM sqlite_master WHERE type='table' AND name='users';"""
    cur=conn.execute(stmt)
    result = cur.fetchone()
    if result[0] == 0:
        flash("Your Server Haven't Been Setup Yet.")
        return redirect(url_for("oobe.start"))
    else:
        #print(chklogin("a","a"))
        #Kernel Module Implemented
        cor=False
        if request.method == "POST":
            #hasher=Hashing()
            #session.permanent = True
            user = request.form["nm"]
            passwd = request.form["pass"]
            kernel=Kernel()
            if user == "" or passwd=="":
                flash(lang["msg12"])
                return redirect(url_for("login"))
            if kernel.checkuser(user,passwd)[0]==True:
                session["user"] = user
                session["role"] = kernel.checkuser(user,passwd)[1][2]
                gensession()
                flash(lang["msg2"])
                return redirect(url_for("home"))
            #sqlstr='select * from users'
            #tmp=conn.execute(sqlstr)
            #print(tmp)
            #rows=tmp.fetchall()
            #print(rows)
            #print(rows[5][0])
            #for row in rows:
                #print('!')
                #if hasher.check(passwd,row[1]) and user == row[0]:
                    #else:
                        #session["user"] = user
                        #session["role"] = row[2]
                        #gensession()
                        #cor=True
                        #flash(lang["msg2"])
                        #return redirect(url_for("home"))
                #else:
                    #pass
            else:
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
        glob.glob('*.txt', recursive=True)
        kernel=Kernel()
        tmp=kernel.getmoney(session["user"])
        if tmp == "D":
            tmp="0"
        if session["role"]=="adult":
            rolerole=False
        else:
            rolerole=True
        return render_template("nano/home.html",buildno=fullbuildname,productname=productname,year=year,flag=True,remaining=tmp,rolerole=rolerole)
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
        if "notes" in session:
            session.pop("notes")
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
    if "notes" in session:
        session.pop("notes")
@app.route('/addmoney', methods=["POST", "GET"])
def addmoney():
    kernel=Kernel()
    role=chkroleloggedin('adult')
    if request.method=="POST":
        if role != "!!":
            if role:
                child=request.form["child"]
                sqlstr='select * from users'
                cur=conn.execute(sqlstr)
                rows=cur.fetchall()
                nowdollar=kernel.getmoney(child)
                if nowdollar == "D":
                    flash("The child account you entered either is not an valid account or is not a child.")
                    return redirect(url_for("addmoney"))
                else:
                    enckey=EncryptPass()
                    addmoney1=request.form["dollars"]
                    session["add"]=enckey.encrypt(sessionid[session["sessionid"]],str(addmoney1))
                    session["child"]=enckey.encrypt(sessionid[session["sessionid"]],child)
                    session["cm"]=enckey.encrypt(sessionid[session["sessionid"]],nowdollar)
                    session["notes"]=enckey.encrypt(sessionid[session["sessionid"]],request.form["notes"])
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
            return render_template("nano/add.html",productname=productname,year=year,action="Add")
        else:
            flash(lang["msg7"])
            return redirect(url_for("logout"))
            
@app.route('/add_now',methods=["POST", "GET"])
def add_now():
    #Add Now!
    kernel=Kernel()
    if request.method == "POST":
        if "add" in session and "child" in session and "cm" in session and "notes" in session:
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
                        notes=enckey.decrypt(sessionid[session["sessionid"]],session["notes"])
                        popadds()
                        #cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)+int(adder))+'" WHERE Name="'+child+'"'
                        #curs = conn.cursor()
                        #curs.execute(cmd)
                        #conn.commit()
                        kernel.addmoney(child,session["user"],session["role"],adder,notes)
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
            popadds()
            return redirect(url_for("addmoney"))
    else:
        #Get
        if "add" in session and "child" in session and "cm" in session and "notes" in session:
            flash(lang["msg9"])
            return render_template("nano/login.html",productname=productname,year=year)
        else:
            flash(lang["msg10"])
            return redirect(url_for("logout"))
@app.route('/removemoney', methods=["POST", "GET"])
def removemoney():
    role=chkroleloggedin('adult')
    kernel=Kernel()
    if request.method=="POST":
        if role != "!!":
            if role:
                child=request.form["child"]
                #sqlstr='select * from users'
                #cur=conn.execute(sqlstr)
                #rows=cur.fetchall()
                nowdollar=kernel.getmoney(child)
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
                    session["notes"]=enckey.encrypt(sessionid[session["sessionid"]],request.form["notes"])
                    print(session["add"])
                    #return 'Added Money Now!'
                    #flash(lang["success"])
                    return redirect(url_for("remove_now"))
            else:
                flash(lang["msg6"])
                return redirect(url_for("home"))
        else:
            return redirect(url_for("logout"))
    else:
        if role != "!!":
            return render_template("nano/add.html",productname=productname,year=year,action="Remove")
        else:
            flash(lang["msg7"])
            return redirect(url_for("logout"))
@app.route('/remove_now',methods=["POST", "GET"])
def remove_now():
    #Remove Now!
    kernel=Kernel()
    if request.method == "POST":
        if "add" in session and "child" in session and "cm" in session and "step" in session and "notes" in session:
            #session["add"]
            if chkroleloggedin(None) == "!!":
                flash(lang["msg5"])
                return redirect(url_for("logout"))
            enckey=EncryptPass()
            if enckey.decrypt(sessionid[session["sessionid"]],session["step"]) !="1":
                return redirect(url_for('removemoney'))
            else:
                chklogin1=kernel.checkuser(request.form['nm'],request.form['pass'])
                if chklogin1[0]:
                    if chklogin1[1][2] == "adult":
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
        if "add" in session and "child" in session and "cm" in session and "step" in session and "notes" in session:
            flash(lang["msg9"])
            return render_template("nano/login.html",productname=productname,year=year)
        else:
            flash(lang["msg10"])
            return redirect(url_for("logout"))
@app.route('/remove_now2',methods=["POST", "GET"])
def remove_now2():
    #Remove Now!
    kernel=Kernel()
    if request.method == "POST":
        if "add" in session and "child" in session and "cm" in session and "notes" in session:
            #session["add"]
            if chkroleloggedin(None) == "!!":
                return redirect(url_for("logout"))
            enckey=EncryptPass()
            if enckey.decrypt(sessionid[session["sessionid"]],session["step"]) !="2":
                return redirect(url_for('removemoney'))
            else:
                chklogin1=kernel.checkuser(request.form['nm'],request.form['pass'])
                if chklogin1[0]:
                    if chklogin1[1][2] == "child" and request.form['nm'] == enckey.decrypt(sessionid[session["sessionid"]],session["child"]):
                        #PREP THE COMMAND
                        #enckey=EncryptPass()
                        child=enckey.decrypt(sessionid[session["sessionid"]],session["child"])
                        adder=enckey.decrypt(sessionid[session["sessionid"]],session["add"])
                        nowdollar=enckey.decrypt(sessionid[session["sessionid"]],session["cm"])
                        notes=enckey.decrypt(sessionid[session["sessionid"]],session["notes"])
                        popadds()
                        #Remake KEY
                        regen()
                        #cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)-int(adder))+'" WHERE Name="'+child+'"'
                        #curs = conn.cursor()
                        #curs.execute(cmd)
                        #conn.commit()
                        #History Module
                        #Coming Soon :>
                        kernel.removemoney(child,session["user"],session["role"],adder,notes)
                        flash(lang["success"])
                        return redirect(url_for("home"))
                    else:
                        popadds()
                        flash(lang["msg1"]+"/"+lang["msg8"]+"/ Your User is not the specified user.")
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
@app.route('/centver')
@app.route('/about')
@app.route('/version')
def about():
    kernel=Kernel()
    history=History()
    return "Mint Kernel Version: "+kernel.version()+"<br>Central frontend version: "+FRIENDLYVERSION+"<br> MintLog Version: "+history.version()
@app.route('/list',methods=["POST","GET"])
def list():
    glob.glob('*.txt', recursive=True)
    if "user" in session:
        if request.method == "GET":
            return render_template("nano/hist.html",productname=productname,year=year)
        else:
            history=History()
            try:
                startingdate=datetime.strptime(request.form["start"], "%Y-%m-%d").date().strftime("%Y%m%d")
                endingdate=datetime.strptime(request.form["end"], "%Y-%m-%d").date().strftime("%Y%m%d")
                return render_template("nano/list.html",lists=history.list(int(startingdate),int(endingdate)),productname=productname,year=year,startingdate=startingdate,endingdate=endingdate)
            except Exception as e:
                flash(e)
                return render_template("nano/hist.html",productname=productname,year=year)
    else:
        flash(lang["msg5"])
        return redirect(url_for("login"))
@app.route('/listall')
def listall():
    glob.glob('*.txt', recursive=True)
    if "user" in session:
        history=History()
        return render_template("nano/list.html",lists=history.listall(),productname=productname,year=year)
    else:
        flash(lang["msg5"])
        return redirect(url_for("login"))
@app.route('/export/<int:start>/<int:end>')
def export(start,end):
    glob.glob('*.txt', recursive=True)
    if "user" in session:
        filename=datetime.now().strftime("%Y%m%d%H%M%S")+".txt"
        with open(filename, 'w') as file:
            history=History()
            ex=history.list(start,end)
            txt=tabulate(ex, headers=["Date","Action", "Money", "Adult", "Child", "Note", "Remaining Value"])
            file.write(txt)
        try:
            return send_file(filename, attachment_filename=filename)
        except Exception as e:
            return str(e)
    else:
        flash(lang["msg5"])
        return redirect(url_for("login"))
@app.route('/export/')
def export2():
    glob.glob('*.txt', recursive=True)
    if "user" in session:
        filename=datetime.now().strftime("%Y%m%d%H%M%S")+".txt"
        with open(filename, 'w') as file:
            history=History()
            ex=history.listall()
            txt=tabulate(ex, headers=["Date","Action", "Money", "Adult", "Child", "Note", "Remaining Value"])
            file.write(txt)
        try:
            return send_file(filename, attachment_filename=filename)
        except Exception as e:
            return str(e)
    else:
        flash(lang["msg5"])
        return redirect(url_for("login"))
@app.route('/genotp')
def otpgen():
    if "user" in session:
        otp=OTP(productname)
        tmp=otp.genOTP()
        enckey=EncryptPass()
        return render_template("nano/2fa_gen.html",productname=productname,toqr=tmp[1],year=year)
    else:
        return redirect(url_for("login"))
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