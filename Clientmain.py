
import argparse
import socket
import ssl
import os

sockettouse = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


def parse_arguments():#set up parsing of arguments for required arguements
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs=1, type = str)
    parser.add_argument('-c', nargs=1)
    parser.add_argument('-f', nargs=1)
    parser.add_argument('-ho', nargs=1)
    parser.add_argument('-l', nargs=1)
    parser.add_argument('-n', nargs=1)
    parser.add_argument('-u', nargs=1)
    parser.add_argument('-v', nargs=2)
    args = parser.parse_args()
    return args




def connecttoserver(hostname):
    sockettouse.connect(hostname, 0)
    return sockettouse



def sendPrompt(prompt,sslsocket):
    tosend = prompt.encode('utf-8')#build prompt to be sent.
    sslsocket.send(tosend)
    data = sslsocket.recv(1024)
    if data==tosend:return True;
    else: return False

def addFile(filename, sslsocket):
    if sendPrompt('-a',sslsocket)==True: #send the prompt, check if it is received
        
    #filetosend = open(filename, 'rb') #open the file to send
    #size = os.path.getsize(filename) #determine size of the file
    #sslsocket.send('siz:'+size) #send server the expected size of the file in order for server to loop through until its received all
    #l = filetosend.read(1024) #read first chunk of bytes from file
    #while(l):#send bytes until none
    #    sslsocket.send(l)#send bytes to socket
     #   l = filetosend.read(1024)#read next part of file
    #result = sslsocket.recv(4)#receive acknowledgement from server

    return 0 #return server acknoledgement

def fetchFile(filename, sslsocket):
    sendPrompt('-f',sslsocket) #send the prompt to the server
    return 0

def listFiles(sslsocket):
    sendPrompt('-l',sslsocket) #send the prompt to the server
    return 0

def uploadCertificate(certificatename, sslsocket):
    sendPrompt('-u',sslsocket) #send the prompt to the server
    return 0

def verifyCertificate(signature, sslsocket):
    if(sendPrompt('-v',sslsocket)==true):return 0

    #send the prompt to the server
    return 0

def main():
    arguments = parse_arguments()
    if arguments.ho is None:
        print("Please Specify a host")
        return


    if arguments.a is None and arguments.f is None and arguments.l is None and arguments.u is None and arguments.v is None:
        print('Please specify an action')
        return

    sslsock = ssl.wrap_socket(sockettouse)
    sslsock.connect(('localhost', 12345))
    data = sslsock.recv(1024)
    print(data)
    if arguments.a is not None: addFile(str(arguments.a), sslsock)
    #if arguments.f is not None: fetchFile(arguments.f,sslsock)
    #if arguments.l is not None: listFiles(sslsock)
    #if arguments.u is not None: uploadCertificate(arguments.u,sslsock)
    #if arguments.v is not None: verifyCertificate(arguments.v,sslsock)
    sslsock.close()



        
if __name__ == '__main__':
    main()







