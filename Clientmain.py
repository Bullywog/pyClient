#Client Program for CITS3002 Networks and Security
#Created by Nathan Graves, Viktor Fidanovski and Daniel Cocks
#
#For use with old trusty client program and specified certificate
#
#SSL Encrypted connection to server for uploading and downloading files.
#
#
#

import argparse
import socket
import ssl
import os
import time
import OpenSSL
from ipaddress import ip_address

sockettouse = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

securityrequirements = 0;
namerequirements = None;
oldtrustyservername = 'cits3002.com'



def parse_arguments():#set up parsing of arguments for required arguements
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', nargs=1, type =str )
    parser.add_argument('-c', nargs=1)
    parser.add_argument('-f', nargs=1)
    parser.add_argument('-ho', nargs=1)
    parser.add_argument('-l', action='store_true')#updated so list works correctly
    parser.add_argument('-n', nargs=1)
    parser.add_argument('-u', nargs=1)
    parser.add_argument('-v', nargs=2)
    args = parser.parse_args()
    return args




def connecttoserver(hostname,port):
    sockettouse.connect(hostname, port)
    return sockettouse



def sendPrompt(prompt,sslsocket):
    tosend = prompt.encode('utf-8')#build prompt to be sent.
    sslsocket.send(tosend)#send prompt over ssl

    data = sslsocket.recv(1024)#receive response

    while(data==[]):
        data = sslsocket.recv(1024)

    if data==tosend:
        return True;#if prompt accepted then mirror of prompt returned
    if data.decode('utf-8','strict') == 'ok': return True
    else: return False


def addFile(filename, sslsocket):
    print("Uploading:"+filename)
    if os.path.isfile(filename)==False: 
        return print("File not uploaded. File not found, make sure it is in Clientmain directory")
    
    if sendPrompt('-a '+filename,sslsocket)==False:  #send the prompt, check if it is received
        return print("File not uploaded. Prompt not received correctly")
    size = os.path.getsize(filename) #determine size of the file
    if sendPrompt(str(size),sslsocket)==False:#send a file size prompt to the server
       return print("File not uploaded. Size Prompt not received correctly")

                   
    filetosend = open(filename, 'rb') #open the file to send
    sendbuffer = filetosend.read(1024) #read file into buffer
    while(sendbuffer):#while something gets read
        sent = sslsocket.send(sendbuffer)#send over sslsocket
        #print('Bytes Sent' + str(sent))#report bytes sent
        sendbuffer = filetosend.read(1024)#read the next part of file to send

    #here should wait for a server acknowledgement that transfer is complete

    data = sslsocket.recv(1024)#receive response

    while(data==[]):
        data = sslsocket.recv(1024)
    if data.decode('utf-8','ignore') == 'ok': return print("File Successfully Uploaded")

        

    return print('File not uploaded successfully')

def fetchFile(filename,trustlength,trustedperson, sslsocket):
    if sendPrompt('-f '+filename,sslsocket)==False: 
        return print("File not downloaded, prompt not received or file not found")#send the prompt to the server
    if sendPrompt(str(trustlength), sslsocket)==False:#sending the length of chain required to trust a file
        return print("Trust length prompt not received")
    if sendPrompt(trustedperson, sslsocket)==False:#sending the required person to be present in the chain
        return("Trusted person prompt not found or file not trusted.")

    sizeprompt = sslsocket.recv(1024)   #receive size of file that will be received
    print(sizeprompt.decode('utf-8','replace'))
    size = (int(sizeprompt.decode('utf-8','replace')))
    recievedfile = open(filename, 'wb') #create file on in root folder with specified name, prepared to be written to
    amountreceived = 0  #Variable for tracking how much has been received through the socket.
    receiveddata = sslsocket.recv(1024) #Receive first chunck of data from socket
    while amountreceived < size: #While all expected data of file has not been received keep looking for more
        recievedfile.write(receiveddata)
        amountreceived+=len(receiveddata)
        print(amountreceived)
        print(size)
        if(size-amountreceived!=0):receiveddata=sslsocket.recv(1024)


    print("File Transfered")
    sendPrompt('complete',sslsocket)
    return 0



def listFiles(sslsocket):
    if sendPrompt('-l',sslsocket)==True: return 1 #send the prompt to the server
    sizeprompt = sslsocket.recv(1024)   #receive size of string that will be received
    print(sizeprompt.decode('utf-8','replace'))
    size = (int(sizeprompt.decode('utf-8','replace')))
    
    amountreceived = 0 #Track amount received from socket
    receiveddata = sslsocket.recv(1024) #Receive first part of data
    while amountreceived < size: #Receive until all expected data it received
        receivedstring.append(receiveddata) #Add received bytes to array
        amountreceived+=len(receiveddata) #Update amount received
        if(size-amountreceived!=0):receiveddata = sslsocket.recv(1024)

    sendprompt('complete', sslsocket) #Inform server that process is complete
    listoffiles=receivedstring.decode('utf-8', 'ignore') #Decode the received btye array into a usable string
    listitems = listoffiles.split(':') #Split string into list of different server files
    print('List of Items on Server with Protection') 
    for listitem in listitems:
        print(listitem) #Print list of items
    return 0

def uploadCertificate(certificatename, sslsocket):

    print("Uploading:"+certificatename)
    if os.path.isfile(certificatename)==False: 
        return print("Certificate not uploaded. File not found, make sure it is in Clientmain directory")
    
    if sendPrompt('-u '+certificatename,sslsocket)==False:  #send the prompt, check if it is received
        return print("Certificate not uploaded. Prompt not received correctly")

    size = os.path.getsize(certificatename) #determine size of the file
    if sendPrompt(str(size),sslsocket)==False:#send a file size prompt to the server
       return print("Certificate not uploaded. Size not received correctly")

    certificatetosend = open(certificatename, 'rb') #open the certificate to send
    sendbuffer = certificatetosend.read(1024) #read file into buffer
    while(sendbuffer):#while something gets read
        sent = sslsocket.send(sendbuffer)#send over sslsocket
        sendbuffer = certificatetosend.read(1024)#read the next part of certificate to send


    data = sslsocket.recv(1024)#receive response

    while(data==[]):
        data = sslsocket.recv(1024)

    if data.decode('utf-8','ignore') == 'ok': return print("File Successfully Uploaded")

        

    return print('File not uploaded successfully')

def verifyFile(filename, certfile, sslsocket):
    if sendPrompt('-v '+filename+' '+signature,sslsocket)==True: return 1
    else: print('File or certicate not found unable to verify')

    #send the prompt to the server
    return 0

def main():
    arguments = parse_arguments()
    if arguments.ho is None:
        print("Please Specify a host")
        return
    #Stack overflow code for parsing a ipaddress and host from string
    #source of code http://stackoverflow.com/questions/21908454/handling-ip-and-port-in-python-and-bash
    ip, separator, port = arguments.ho[0].rpartition(':')
    assert separator # separator (`:`) must be present
    port = int(port) # convert to integer
    ip = ip_address(ip.strip("[]")) 
    print(ip)
    print(port)

    securityrequirements = 0;#setting default security requirements
    namerequirements = 'None';#default name requirements

    if arguments.c!=None:securityrequirements=arguments.c[0]#if arguments are given then change the default to one supplied
    if arguments.n!=None:namerequirements=arguments.n[0]

    print(securityrequirements)
    print(namerequirements)

    #Error checking to make sure arguments are given
    if arguments.a is None and arguments.f is None and arguments.l is None and arguments.u is None and arguments.v is None:
        print('Please specify an action')
        return

    sslsock = ssl.wrap_socket(sockettouse)#wrap created socket in ssl for encryption
    cert = ssl.get_server_certificate((str(ip), port))#requests certificate from specified location
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)#loads received certificate
    connectedserver =x509.get_subject().commonName#checks certificate name against hardcoded value of oldtrusty
    if (connectedserver!=oldtrustyservername):return print("Not old trusty")#if not old trusty does not connect
    sslsock.connect((str(ip), port))#Connect to old trusty 
    data = sslsock.recv(1024)#Recv welcome message
    print(data)
    if arguments.a is not None: addFile(arguments.a[0], sslsock)
    if arguments.f is not None: fetchFile(arguments.f[0],securityrequirements,namerequirements,sslsock)
    if arguments.l is True: listFiles(sslsock)
    if arguments.u is not None: uploadCertificate(arguments.u[0],sslsock)
    if arguments.v is not None: verifyFile(arguments.v[0],arguments.v[1],sslsock)
    sendPrompt('exit',sslsock)
    sslsock.close()



        
if __name__ == '__main__':
    main()







