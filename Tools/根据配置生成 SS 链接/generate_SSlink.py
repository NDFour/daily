#
#   Description: ---
#        Author: Lynn
#         Email: lgang219@gmail.com
#        Create: 2018-04-24 22:30:12
# Last Modified: 2018-04-25 18:16:53
#
import base 
import base64 

def generatSSLink(method,passwd,host,port):
    #ssRaw=method+":"+passwd+"@"+host+":"+port
    ssRaw=method+":"+passwd+"@"+host+"#"+port
    return ssRaw

def main():
    print("------------SS Link-----------");
    method=input("Method:")
    Passwd=input("Passwd:")
    Host=input("Host:")
    port=input("Port:")

    ssRaw=generatSSLink(method,Passwd,Host,port)
    # base64 object must be 'bytes'
    b64raw=base64.urlsafe_b64encode(ssRaw.encode(encoding="utf-8"))
    # decode 'bytes' to 'string'
    b64string=b64raw.decode()

    print('\n---------------------')
    print("Your SSLink:")
    print("ss://"+b64string)

main()
