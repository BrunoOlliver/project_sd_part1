from __future__ import print_function

import logging
import socket
import random

import grpc
import portal_pb2
import portal_pb2_grpc

s = socket.socket()
host = socket.gethostname()
ip_admin = socket.gethostbyname(host)
port = 12345

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = portal_pb2_grpc.GreeterStub(channel)

    response = stub.Connecting(portal_pb2.ConectRequest(message=host))
    print(response.message)

    #Requisita usuario e id do adminsitrador
    id_login = int(input('Informe seu ID: '))
    user_login = input('Informe seu Usuário Administrador: ')

    response = stub.CheckUser(portal_pb2.AdministratorRequest(id=id_login,name=user_login))
    print(response.message)

    while True:
        options = int(input('\nSelecione a opção desejada: '))
        response = stub.CheckOption(portal_pb2.OptionRequest(option = options))
        if options == 1:
            print('Opção selecionada: ' + response.message)
            client_name = input('Nome do Novo Cliente: ')
            client_id = random.randint(100,999)
            response = stub.InsertNewClient(portal_pb2.InsertClientRequest(id=client_id,name=client_name))
            print(response.message)
        elif options == 2:
            print('Opção selecionada: ' + response.message)
            src_id = int(input('Informe a ID do Cliente: '))
            src_name = input('Informe o Nome do Cliente: ')
            response = stub.SearchClient(portal_pb2.SearchClientRequest(id=src_id,name=src_name))
            print(response.message)
        elif options == 3:
            print('Opção selecionada: ' + response.message)
            response = stub.ListClients(portal_pb2.ListClientsRequest(message='Requisitada todos Clientes'))
            print(response.message)
        elif options == 4:
            print('Opção selecionada: ' + response.message)
            del_id = int(input('Informe a ID do Cliente: '))
            del_name = input('Informe o Nome do Cliente: ')
            response = stub.DeleteClient(portal_pb2.DeleteClientRequest(id=del_id,name=del_name))
            print(response.message)
        elif options == 5:
            print('Opção selecionada: ' + response.message)
            response = stub.RemoveClients(portal_pb2.RemoveClientsRequest(message='Requisita apagar todos Clientes'))
            print(response.message)
        elif options == 6:
            print('Saindo da Aplicação')
            break
        else:
            print(response.message)


if __name__ == '__main__':
    logging.basicConfig()
    run()
