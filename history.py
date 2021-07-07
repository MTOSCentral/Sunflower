#MintLog For Mint/Central
import sqlite3
from datetime import datetime
import os
conn =sqlite3.connect('database'+os.sep+'history.sql', check_same_thread=False)
cursor = conn.cursor()
VER="1.0.1"
class History:
    def __init__(self):
        global conn
        sqlstr='CREATE TABLE IF NOT EXISTS history \
        ("YearMonthDate" TEXT,"Action" TEXT,"Money" TEXT,"Adult" TEXT,"Child" TEXT,"Note" TEXT,"CurrentValue" TEXT)'
        self.curs = conn.cursor()
        self.curs.execute(sqlstr)
        conn.commit()
    def makehistory(self,action,year,month,date,money,note,who,child,currentvalue):
        global conn
        sqlstr=f'insert into history values("{year}{month}{date}","{action}","{money}","{who}","{child}","{note}","{currentvalue}")'
        self.curs.execute(sqlstr)
        conn.commit()
    def version(self):
        return VER
    def list(self,startingdate,endingdate):
        global conn
        sqlstr='select * from history'
        cur=conn.execute(sqlstr)
        rows=cur.fetchall()
        biggestdate=endingdate
        smallestdate=startingdate
        lister=[]
        for row in rows:
            if int(row[0])<=biggestdate and int(row[0])>=smallestdate:
                #print(row)
                tmp=datetime.strptime(row[0], "%Y%m%d").date()
                u=[]
                u.append(row[0])
                u.append(row[1])
                u.append(row[2])
                u.append(row[3])
                u.append(row[4])
                u.append(row[5])
                u.append(row[6])
                u[0]=tmp.strftime("%Y-%m-%d")
                lister.append(u)
        #print(lister)
        return lister
    def listall(self):
        global conn
        sqlstr='select * from history'
        cur=conn.execute(sqlstr)
        rows=cur.fetchall()
        lister=[]
        for row in rows:
            #print(row)
            tmp=datetime.strptime(row[0], "%Y%m%d").date()
            u=[]
            u.append(row[0])
            u.append(row[1])
            u.append(row[2])
            u.append(row[3])
            u.append(row[4])
            u.append(row[5])
            u.append(row[6])
            u[0]=tmp.strftime("%Y-%m-%d")
            lister.append(u)
        return lister