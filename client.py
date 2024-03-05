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
  clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  clientIP = socket.gethostbyname(clientName)
  try:
    clientSocket.connect(serverIP, serverPort)
    print("{} running on {}".format(clientName, clientIP))
  except:
    print("Error: Connection to server failed.")
    TERMINATE(1)

  while (True):
    userInput = input(">")
    if(userInput == "/id"):
      print("User ID:", clientName)
    elif (userInput == "/register"):
      registerRequest = "REGISTER\n\rclientID: {}\n\rIP: {}\n\rPort: {}\n\r\n\r".format(clientName, clientIP, clientPort)
      clientSocket.send(registerRequest.encode())
      clientData = (clientSocket.recv(1024)).decode
      print(clientData.decode)
    elif (userInput == "/bridge"):
      bridgeRequest = "BRIDGE\n\rclientID: {}\n\rBRIDGE\n\r".format(clientName)
      clientSocket.send(bridgeRequest.encode())
      bridgeData = (clientSocket.recv(1024)).decode()
      print("Response from server:", bridgeData)
    elif (KeyboardInterrupt):
      TERMINATE(130)
    else:
      print("Error: Invalid argument.")
    
# end INITIALIZE()

def WAIT():
  pass
# end WAIT()

def CHAT():
  pass
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