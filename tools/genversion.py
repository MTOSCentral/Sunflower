#Version Number Generator v1 - For Version 0.1 to 9.9
from datetime import datetime
with open("version.txt") as file:
    files=file.read()
    print(files)
    op=""
    full=""
    for n in range (0,3):
        full=full+files[n]
    full1=""
    for n in range (4,8):
        op=op+files[n]
    op=str(int(op)+1)
    for n in range (0,4-len(op)):
        op="0"+op
    print(op)
    today = datetime.now()
    d3 = today.strftime("%y%m%d-%H%M")
    branch=input('Enter Build Branch: ')
    print(full+"."+op+"."+branch+"."+d3)
    file.close()
    file2=open("version.txt","w+")
    file2.write(full+"."+op+"."+branch+"."+d3)
