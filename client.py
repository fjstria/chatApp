# client.py
# Implementation of the client-side behavior of the chat app.

import socket, sys, argparse

# CLIENT FINITE STATE MACHINE ---------------------------------------
def INITIALIZE():
  """
  Initializes the client program.
  """
  # get command line options
  parser = argparse.ArgumentParser()
  parser.add_argument("--id", action='store') 
  parser.add_argument("--port", action='store') 
  parser.add_argument("--server", action='store') 
  args = parser.parse_args()

  # assign options to variables
  clientName = args.id
  clientPort = args.port
  serverIP, serverPort = (args.server).split(":")

  # attempt server connection
  clientIP = '127.0.0.1'
  try:
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((serverIP, int(serverPort)))
    print("{} running on {}".format(clientName, clientIP))
  except:
    print("Error: Connection failed.", file=sys.stderr)
    TERMINATE(1)  # exit code for error
  # end try-except

  # get client input for next action!
  try:
    while True:
        userInput = input(">")
        if userInput == "/id":
            print("User ID:", clientName)
        elif userInput == "/register":
            registerRequest = "REGISTER\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort)
            clientSocket.send(registerRequest.encode())
            clientData = (clientSocket.recv(1024)).decode()
            try:
                assert clientData == ("REGACK\r\nclientID: {}\r\nIP: {}\r\nPort: {}\r\n\r\n".format(clientName, clientIP, clientPort))
            except:
                print("Error: Invalid REGACK.", file=sys.stderr)
                TERMINATE(1)
            clientSocket.close()  # close the socket after registration
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # reopen socket
            clientSocket.connect((serverIP, int(serverPort))) 
        elif userInput == "/bridge":
            bridgeRequest = "BRIDGE\r\nclientID: {}\r\n\r\n".format(clientName)
            clientSocket.send(bridgeRequest.encode())
            bridgeData = (clientSocket.recv(1024)).decode()
            print("Response from server:", bridgeData)  # end point for part 1
            if bridgeData == "BRIDGEACK\r\nclientID: \r\nIP: \r\nPort: \r\n":
                WAIT()
            else:
                CHAT()
            # end if
        # end if
    # end while
  except KeyboardInterrupt:
    TERMINATE(130)  # exit code for ctrl+c
  except Exception as e:
    print("Error:", e, file=sys.stderr)
    TERMINATE(1)
  # end try-except
  # end INITIALIZE()

def WAIT():
  print("Entered WAIT State.")
  TERMINATE(0)  # exit code for success
# end WAIT()

def CHAT():
  print("Entered CHAT State.")
  TERMINATE(0)
# end CHAT()

def TERMINATE(exitCode):
  """
  Terminates the client program.
  """
  clientSocket.close()
  sys.exit(exitCode)
# end TERMINATE()
# -------------------------------------------------------------------

def main():
  global clientSocket, clientName, clientIP, clientPort, serverIP, serverPort
  INITIALIZE()
# end main()

if __name__ == "__main__":
  main()
# end if
