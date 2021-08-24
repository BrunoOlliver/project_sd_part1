
from __future__ import print_function
import logging

import grpc

import buffer_pb2
import buffer_pb2_grpc

def validateUserIDType():
  while True:
    userid = input("Digite o id: ")

    if not userid.isdigit():
      print('**ID must be an integer**')
    else:
      break
  return int(userid)

def run():
  channel = grpc.insecure_channel('localhost:50051')
  stub = buffer_pb2_grpc.GreeterStub(channel)

  while True:
    op = menu()

    if op == 1 or op == 2:
      userid = validateUserIDType()
      username = input("Digite o nome de usuario: ")

      if op == 1:
        response = stub.insertNewClient(buffer_pb2.InsertRequest(id=userid,name=username))
        print("\nGreeter client received: " + response.message)
      else:
        response = stub.updateClient(buffer_pb2.ModifyRequest(id=userid,name=username))
        print("\nGreeter client received: " + response.message)
    elif op == 3 or op == 4:
      userid = validateUserIDType()

      if op == 3:
        response = stub.findClient(buffer_pb2.FindRequest(id=userid))
        print("Greeter client received: " + response.message)
      else:
        response = stub.deleteClient(buffer_pb2.DeleteRequest(id=userid))
        print("Greeter client received: " + response.message)
    else:
      print("Desconectando Administrador...")
      break


def menu():
  print("\n-------------MENU-------------")
  print("1 - Inserir novo Cliente")
  print("2 - Modificar um Cliente")
  print("3 - Procurar Cliente")
  print("4 - Apagar Cliente")
  print("5 - Sair")
  op = int(input("Escolha a operação desejada:"))
  return op

if __name__ == '__main__':
    logging.basicConfig()
    run()
