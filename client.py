#Client.py subscribe -> mqtt -> portalClient.py

import socket                          # Import socket module

s = socket.socket()                    # Create a socket object
host = socket.gethostname()            # Get local machine name
port = 12345                           # Reserve a port for your service.

s.connect((host, port))

print("1")
data = s.recv(1024)
print(data.decode())
print("2")
data = s.recv(1024)
print(data.decode())
s.close()                              # Close the socket when done
