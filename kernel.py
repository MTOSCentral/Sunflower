#Mint Kernel Dummy v1.1
#Always Return False and Error, please download full version.
VERSION="DUMMY"
class Kernel:
    def __init__(self):
        print("Please Download The Kernel https://github.com/MTOSCentral/MintKernel")
    def version(self):
        global VERSION
        return VERSION
    def checkuser(self,username,password):
        print("Please Download The Kernel https://github.com/MTOSCentral/MintKernel")
        return [False]
    def chkrole(self,user,role):
        print("Please Download The Kernel https://github.com/MTOSCentral/MintKernel")
        return False
    def addmoney(self,childname,addper,role,adder,note):
        print("Please Download The Kernel https://github.com/MTOSCentral/MintKernel")
        return "0x0001"
    def removemoney(self,childname,addult,role,adder,notes):
        print("Please Download The Kernel https://github.com/MTOSCentral/MintKernel")
        return "0x0003"
    def getmoney(self,user):
        print("Please Download The Kernel https://github.com/MTOSCentral/MintKernel")
        return "D"