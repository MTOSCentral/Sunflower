#Mint Kernel File v1.1
import sqlite3
from hashing import Hashing
from history import History
from datetime import datetime
VERSION="1.0.5_hist"
class Kernel:
    def __init__(self):
        #print("Mint Engine")
        self.conn =sqlite3.connect('database\\users.sql', check_same_thread=False)
        self.cursor = self.conn.cursor()
    def version(self):
        global VERSION
        return VERSION
    def checkuser(self,username,password):
        hasher=Hashing()
        sqlstr='select * from users'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        cor=False
        for row in rows:
            if hasher.check(password,row[1]) and username == row[0]:
                cor=True
                return [True,row]
            #else:
                #pass
        if not cor:
            return [False]
    def chkrole(self,user,role):
        hasher=Hashing()
        sqlstr='select * from users'
        self.cur=self.conn.execute(sqlstr)
        rows=self.cur.fetchall()
        cor=False
        for row in rows:
            if user == row[0] and role == row[2]:
                cor=True
                return True
        if not cor:
            return False

    def addmoney(self,childname,addper,role,adder,note):
        #FORCE CHECK
        year = datetime.now().strftime('%Y')
        month = datetime.now().strftime('%m')
        date = datetime.now().strftime('%d')
        ro=self.chkrole(addper,'adult')
        #r1=self.checkuser(adder,adultpassword)
        if ro:# and r1:
            role = True
        else:
            role=False
        a = True
        if a:
            if role:
                child=childname
                sqlstr='select * from users'
                cur=self.conn.execute(sqlstr)
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
                    return "0x0002"
                else:
                    child=childname
                    cm=nowdollar
                    #return redirect(url_for("add_now"))
                    #Add Money
                    cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)+int(adder))+'" WHERE Name="'+child+'"'
                    curs = self.conn.cursor()
                    curs.execute(cmd)
                    self.conn.commit()
                    history=History()
                    history.makehistory("+",year,month,date,str(int(adder)),note,addper,child,str(int(nowdollar)+int(adder)))
            else:
                return "0x0001"
#0x0001 = Adult Username ,PW or Role Incorrect #0x0002=Child Username,Role Incorrect
    def removemoney(self,childname,addult,role,adder,notes):
        role=self.chkrole(addult,'adult')
        #r1=self.checkuser(adder,adderpw)
        #r2=self.checkuser(childname,childpw)
        year = datetime.now().strftime('%Y')
        month = datetime.now().strftime('%m')
        date = datetime.now().strftime('%d')
        if role: #and r1 and r2:
            role=True
        else:
            role=False
        add = True
        if add:
            if role:
                child=childname
                sqlstr='select * from users'
                cur=self.conn.execute(sqlstr)
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
                    return "0x0002"
                else:
                    #addmoney1=money
                    #add=int(addmoney1)
                    child=childname
                    cm=nowdollar
                    #return redirect(url_for("add_now"))
                    #Add Money
                    cmd='UPDATE users SET "Money" = "'+str(int(nowdollar)-int(adder))+'" WHERE Name="'+child+'"'
                    curs = self.conn.cursor()
                    curs.execute(cmd)
                    self.conn.commit()
                    history=History()
                    history.makehistory("-",year,month,date,str(int(adder)),notes,addult,child,str(int(nowdollar)-int(adder)))
                    return "OK"
            else:
                return "0x0003"
#0x0003=IS NOT ADULT
    def getmoney(self,user):
        nowdollar="D"
        child=user
        sqlstr='select * from users'
        cur=self.conn.execute(sqlstr)
        rows=cur.fetchall()
        for row in rows:
            # print('RAN USER='+session['user'])
            if row[0] == child and row[2]=="child":
                #print(row[3])
                #print("--------")
                nowdollar=row[3]
                #print(nowdollar)
        if nowdollar == "D":
            return "D"
        else:
            return nowdollar
"""
Meow Tech Mint - Kernel For The Central System
Central System Has Been Modified To Use The Mint Core.
"""