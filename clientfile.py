import socket
import os
import sys
import threading
import time

#Ask for the domain name of the server as a string
serverAddr = raw_input("Enter the domain name of the server.")

#Ask for the port of the server as an int
serverPort = input("Enter the port of the server.")

print("Domain name given was: " + serverAddr + "\nServer port given was: " + str(serverPort))

#Make a TCP Socket
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Connect to the server
connSock.connect((serverAddr, serverPort))

listenport = 1320

#the number of bytes sent to the server
bytesSent = 0

#let the server connect to us
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(('', listenport))
# Start listening on the socket
welcomeSock.listen(1)
clientSock, addr = welcomeSock.accept()

        
#****************************************************************************
#upload_file first opens a file, then tells the server it plans to upload a file
#sends the file name after a 1 second delay
#first a 10 byte header is added with the file size
#whole file is sent to the server
#waits for an acknowledgement message from the server with the file size
#tries 3 times to get an acknowledgement message
#if the file size sent back is too small or 0 then upload fails
#prints out the files uploaded and downloaded
#****************************************************************************
def upload_file(file_name):
    #open and read the file
    fileObj = open(file_name, "r")
    #send message to the server that a file is being uploaded
    connSock.send("upload file")
    time.sleep(1)
    #sends name of the file
    connSock.send(file_name)
    
    #data inside the uploaded file
    upload_data = None
    
    while True:
        upload_data = fileObj.read(65536)

        if upload_data:
            dataSizeStr = str(len(upload_data))

            while (len(dataSizeStr) < 10):
                dataSizeStr = "0" + dataSizeStr

            upload_data = dataSizeStr + upload_data

            #Number of bytes we are sending to the server
            numSent = 0

            while len(upload_data) > numSent:
                numSent += connSock.send(upload_data[numSent:])
                
        else:
            #subtract 10 because 10 is the file header
            numSent -= 10
            filenum = 0
            counter = 0
            while True:               
                filenum = clientSock.recv(4096)
                print ("Size of the file is: " + str(filenum))
                if (filenum > 0):
                    break
                if (counter == 3):
                    break
                time.sleep(5)
                #request the filesize again
                connSock.send("filesize")
                counter +=1
               
            filenum = int(filenum)
            #conditions to check if the file upload was successful or not
            if (filenum == 0):
                print("File upload failed, no file sent.")
            elif (filenum == int(numSent)):
                  print("File upload successful.")
                  connSock.send("file upload success")
            else:
                print("File upload failed, not all of the file was sent.")

            print(str(numSent) + " :Bytes sent.")
            print(str(filenum) + " :Bytes recieved.")
            break
    


#****************************************************************************
#based on what the user chooses, the client will send a command to the client
#server will execute a command based on the command that the client sends
#****************************************************************************
        
choice = ""

while (choice.lower() != "quit"):
    
    print("\nEnter a command. Syntax is as follows: ")
    print("get <filename> downloads a file from the server.")
    print("put <filename> uploads a file to the server.")
    print("ls lists the files from the server")
    print("quit exits the program\n")

    choice = raw_input("ftp>")

    if (choice[:3] == "put"):
        f = choice[4:]
        print("Filename given is: " + f)           
        upload_file(f)
    
    #****************************************************************************
    #make a list to store the files from the server
    #send a message to the server to send the file list
    #recieve the number of files from the server
    #loop for the number of files that the server has
    #****************************************************************************
    if (choice == "ls"):
        #list to hold file names
        z = []
        #counts number of files for looping purposes
        fnum = 0
        #send a message to let the server know file list is requested
        connSock.send("file list")
        while True:
            #wait for server to send a file name
            filenum = clientSock.recv(4096)
            fnum = int(filenum)
            print ("Number of files is: " + str(fnum))
            #only add to the list if the number of files is greater than 0
            if fnum > 0:
                while True:
                    for i in range(fnum):
                        #get the file name
                        flist = clientSock.recv(4096)
                        #add file to the file list
                        z.append(flist)                       
                    break
            print("List of files: ")
            print(f)
            break

    if (choice[:3] == "get"):
        df = choice[4:]
        connSock.send("dl file")
        time.sleep(2)
        connSock.send(df) 

            
        
        
