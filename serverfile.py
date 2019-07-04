
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import time

# The port on which to listen
listenPort = 1270
ad = 1320

# Create a welcome socket. 
welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
welcomeSock.bind(('', listenPort))

# Start listening on the socket
welcomeSock.listen(1)

connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


file_list = ["hello.txt", "cool.txt", "bingbingwahoo.txt"]
# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):

	# The buffer
	recvBuff = ""
	
	# The temporary buffer
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff

print "Waiting for connection..."
# Accept connections
clientSock, addr = welcomeSock.accept()
#Connect to the client
connSock.connect(("localhost", ad))


#****************************************************************************
#based on what the user chooses, the client will send a command to the client
#server will execute a command based on the command that the client sends
#****************************************************************************
# Accept connections forever
while True: 
    print "Accepted connection from client: ", addr
    print "\n"	

    #gets the first message that the client recieves
    command = clientSock.recv(4096)
    print (command)

    if (command == "file list"):
        
        connSock.send(str(len(file_list)))
        #stop for 2 seconds
        time.sleep(2)
        
        for i in range(len(file_list)):
            connSock.send(file_list[i])
            #stop for 1 second
            time.sleep(1)
        
        print("Finished uploading files, stopping connection.")
        connSock.close()
        
    #sends the filesize of the last file recieved
    elif (command == "filesize"):
        connSock.send(str(real_fsize))

    #if the file was successfully uploaded successfully append it to the list
    elif (command == "file upload success"):
        file_list.append(filename)
        


    elif (command == "upload file"):
        
        filename = clientSock.recv(4096)
        print("Filename is: " + filename)
        # The buffer to all data received from the
        # the client.
        fileData = ""
        
        # The temporary buffer to store the received
        # data.
        recvBuff = ""
        
        # The size of the incoming file
        fileSize = 0	
        
        # The buffer containing the file size
        fileSizeBuff = ""
        
        # Receive the first 10 bytes indicating the
        # size of the file
        fileSizeBuff = recvAll(clientSock, 10)
                
        # Get the file size
        fileSize = int(fileSizeBuff)
        
        print "The file size is ", fileSize
        
        # Get the file data
        fileData = recvAll(clientSock, fileSize)
        
        print "The file data is: "
        print fileData

        #convert the contents of the file into a byte value
        real_fsize = len(fileData.encode('utf-8'))
        
        #send the number of bytes to client
        connSock.send(str(real_fsize))        

            
                
# Close our side
clientSock.close()
	
