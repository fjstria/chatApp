# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

def main():
    """
    Handles the initialization, running behavior, and termination of the client.
    """
    def INITIALIZE():
        global clientSocket
        """
        Initializes client-server connection.
        """
            # attempt client-server connection
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverIP, int(serverPort)))
            print("{} running on {}".format(clientName, clientIP))
        except KeyboardInterrupt:
            #print("Error: Client interrupt caught. Ending program.\n", file=sys.stderr)
            sys.exit(0)
        except:
            #print("Error: Connection not established. Ending program.\n", file=sys.stderr)
            sys.exit(1)
        # end try-except

        # get client input for next action
        try:
            while True:
                bridgeData = ''
                userInput = input(">")
                # id
                if userInput == "/id":
                    print("ID:", clientName)
                # register
                elif userInput == "/register":
                    registerRequest = "REGISTER\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort)
                    clientSocket.send(registerRequest.encode())
                    clientData = (clientSocket.recv(4096)).decode()
                    try:
                        assert clientData == ("REGACK\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort))
                    except:
                        #print("Error: Invalid REGACK.\n", file=sys.stderr)
                        TERMINATE()
                    clientSocket.close()  # close the socket after registration
                    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # reopen socket
                    clientSocket.connect((serverIP, int(serverPort))) 
                # bridge
                elif userInput == "/bridge":
                    bridgeRequest = "BRIDGE\r\nclientID: {}\r\n\r\n".format(clientName)
                    clientSocket.send(bridgeRequest.encode())
                    bridgeData = (clientSocket.recv(4096)).decode()
                    #print("Response from server:\n",bridgeData)
                    if "clientID: \r\nIP: \r\nPort: \r\n" in bridgeData:
                        WAIT()
                    #end if
                #chat      
                elif userInput == "/chat":
                    CHAT()
                # quit
                elif userInput == "/quit":
                    TERMINATE()
                # unknown command
                else:
                    print("Error: Unknown command.\n")  
                # end if
            # end while
        except KeyboardInterrupt:
            #print("Error: Client interrupt caught. Closing connection.\n", file=sys.stderr)
            TERMINATE()
        except:
            #print("Error: Connection failed.\n", file=sys.stderr)
            TERMINATE()
        # end try-except
    # end INITIALIZE()
            
    def WAIT():
        global clientSocket
        """
        Pauses client input while awaiting second client connection.
        """
        try:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.bind((clientIP, int(clientPort)))
            clientSocket.listen()   # stop-and-wait function, returns when connection received
            connection, address = clientSocket.accept()
            #print("Connection established with", address)
            clientSocket.close()
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            clientSocket.connect(address)
            CHAT()
        except KeyboardInterrupt:
            #print("Error: Client interrupt caught. Closing connection.\n", file=sys.stderr)
            TERMINATE()
        except Exception as e:
            #print("Error:", e, file=sys.stderr)
            TERMINATE()
    # end WAIT()
    
    def CHAT():
        global clientSocket
        """
        Operates chat activity between both clients. 
        """
        try:
            #clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #clientSocket.bind((clientIP, int(clientPort)))
            #clientSocket.listen()   # stop-and-wait function, returns when connection received
            #clientSocket.accept()
            while True:
                userInput = input(">")
                chatMessage = "CHAT\r\nclientID: {}\r\nMessage: {}\r\n\r\n".format(clientName, userInput)
                clientSocket.send(chatMessage.encode())
                chatData = (clientSocket.recv(4096)).decode()
                print(":", chatData)
            #print("Connection established with", address)
            #clientSocket.close()
        except KeyboardInterrupt:
            #print("Error: Client interrupt caught. Closing connection.\n", file=sys.stderr)
            TERMINATE()
        except Exception as e:
            #print("Error:", e, file=sys.stderr)
            TERMINATE()

    def TERMINATE():
        global clientSocket
        """
        Terminates the client program.
        """
        clientSocket.close()
        sys.exit(0)
    # end TERMINATE()

    # read client options
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", action='store') 
    parser.add_argument("--port", action='store') 
    parser.add_argument("--server", action='store') 
    args = parser.parse_args()

    # save client and server details
    clientName = args.id
    clientPort = args.port
    serverIP, serverPort = (args.server).split(":")
    clientIP = '127.0.0.1'

    INITIALIZE()
# end main()

if __name__ == "__main__":
    main()
# end if
