import gnupg
import shutil
import os
from fnmatch import fnmatch, filter
#fetch update from here and download the encrypted zip.
#Note that we will not provide key
class Update:
    def __init__(self):
        pass
    def update(self,file):
        updcode=file
        gpg = gnupg.GPG()
        with open('decryption.key') as f:
            privkey_data = f.read()
            #privkey_data=""
        # decrypt file
        key=privkey_data
        import_result = gpg.import_keys(key)
        for k in import_result.results:
            print(k)
        with open(updcode+".cudp", 'rb') as f:
            status = gpg.decrypt_file(
                file=f,
                passphrase='MeowTechOfficallySignedUpdate',
                output=updcode+'D.cupd',
                #CUPD=Central Update Decrypted
                #CUDP=Central Update Package
            )
            print(status.stderr)
        import zipfile
        with zipfile.ZipFile(updcode+"D.cupd", 'r') as zip_ref:
            zip_ref.extractall('tmp/upd/')
        shutil.copytree('tmp/upd', '.', dirs_exist_ok=True,ignore=shutil.ignore_patterns('ver.cfg'))
        a=open('tmp/upd/ver.cfg')
        u=a.read()
        a.close()
        shutil.rmtree('tmp', ignore_errors=False, onerror=None)
        os.remove(updcode+'D.cupd')
        os.remove(updcode+'.cudp')
        return u
