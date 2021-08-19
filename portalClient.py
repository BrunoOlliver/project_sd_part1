#portalClient.py publish -> mqtt -> client.py

#Socket
import base64
#import pickle
import socket                               # Import socket module
import paho.mqtt as mqtt
import time

s = socket.socket()                         # Create a socket object
host = socket.gethostname()                 # Get local machine name
port = 12345                                # Reserve a port for your service.
s.bind((host, port))                        # Bind to the port

banco = dict()


s.listen(5)                                 # Now wait for client connections.
while True:
   c, addr = s.accept()
   print('Got connection from', addr)
                        # Establish connection with client.
   base64_dict = c.recv(1024)
   #msgCliente = data.decode()

   my_dict_again = eval(base64.b64decode(base64_dict))
   print(my_dict_again)
   #print(base64_dict)
   my_dict_again = eval(base64.b64decode(base64_dict))
   print(my_dict_again)

   # EXEMPLO
   #my_dict = {'name': 'Rajiv Sharma', 'designation': "Technology Supervisor"}
   #encoded_dict = str(my_dict).encode('utf-8')
   #base64_dict = base64.b64encode(encoded_dict)
   #print(base64_dict)

   #my_dict_again = eval(base64.b64decode(base64_dict))
   #print(my_dict_again)


   c.close()


#server.py
#!/usr/bin/python                           # This is server.py file

#import socket                               # Import socket module

#s = socket.socket()                         # Create a socket object
#host = socket.gethostname()                 # Get local machine name
#port = 12345                                # Reserve a port for your service.
#s.bind((host, port))                        # Bind to the port

#s.listen(5)                                 # Now wait for client connections.
#while True:
#   c, addr = s.accept()                     # Establish connection with client.
#   print('Got connection from', addr)
#   c.send('Thank you for connecting'.encode())
#   c.close()                                # Close the connection
