from concurrent import futures
import logging
import socket
import random

import grpc
import portal_pb2
import portal_pb2_grpc

ntask = dict()
dic_adm = {'ID':'12345','NAME':'ADMIN'}
dic_client = {'ID':'12345','NAME':'JOAO','TASK':ntask}
banco_adm = {dic_adm['ID']:dic_adm}
banco_client = {dic_client['ID']:dic_client}

def menu():
    menu ='''\n=======PORTAL DO ADMINISTRADOR=======\n
    1. Cadastrar novo Cliente
    2. Buscar Cliente existente
    3. Listar todos os cliente
    4. Excluir cliente
    5. Excluir todos os clientes
    6. Sair'''
    return menu

class Greeter(portal_pb2_grpc.GreeterServicer):

    def CheckUser(self, request, context):
        id = str(request.id)
        for id in banco_adm.keys():
            tsk_temp = banco_adm[id]
            if request.name in tsk_temp['NAME']:
                options = menu()
                print('[USER AUTENTICATION] OK! ID: %s ' %request.id + 'USER: %s' %request.name)
                return portal_pb2.AdministratorReplay(message= 'Bem vindo, %s ' % request.name + 'ID: %s ' %request.id + options )
            else:
                break
        return portal_pb2.AdministratorReplay(message= 'ID[%s] ' % request.id + 'Usuário: %s, não foi localizado' % request.name)

    def InsertNewClient(self, request, context):
        id = str(request.id)

        while True:
            if id in banco_client.keys():
                id_temp = random.randint(100,999)
                id = str(id_temp)
            else:
                dic = dict()
                tsk_temp = {'ID':id,'NAME':request.name,'TASK':dic}
                banco_client.update({id : tsk_temp})
                break
        return portal_pb2.InsertClientReplay(message='\nUsuário cadastrado com sucesso!\nID: '+id+' NAME: %s' %request.name)

    def SearchClient(self, request, context):
        id = str(request.id)
        if id in banco_client.keys() and request.name in banco_client[id]['NAME']:
            client_temp = str(banco_client[id])
            return portal_pb2.SearchClientReplay(message=client_temp)
        else:
            return portal_pb2.SearchClientReplay(message='Não foi possível localizar o ID: %s' %request.id)

    def ListClients(self, request, context):
        client_temp = str(banco_client)
        return portal_pb2.ListClientsReplay(message=client_temp)

    def DeleteClient(self, request, context):
        id = str(request.id)
        if id in banco_client.keys() and request.name in banco_client[id]['NAME']:
            print('[USER EXCLUSION] ID: %s' %request.id + ' USER: %s'%request.name)
            banco_client.pop(id)
            return portal_pb2.DeleteClientReplay(message='Excluido: ID: %s'%request.id + ' Cliente: %s'%request.name)
        else:
            print('[USER EXCLUSION FAILED] ID: %s' %request.id + ' USER: %s'%request.name)
            return portal_pb2.DeleteClientReplay(message='Não foi possível localizar o ID: %s' %request.id)

    def RemoveClients(self, request, context):
        print('[ATENCTION] %s' %request.message)
        banco_client.clear()
        return portal_pb2.RemoveClientsReplay(message='Todos os clientes foram removidos')

    def CheckOption(self, request, context):
        if request.option == 1:
            print('[OPTION SELECT: %s] Cadastrar novo Cliente' % request.option)
            return portal_pb2.OptionReplay(message='[%s] Cadastrar novo Cliente' % request.option)
        elif request.option == 2:
            print('[OPTION SELECT: %s] Buscar Cliente existente' % request.option)
            return portal_pb2.OptionReplay(message='[%s] Buscar Cliente existente' % request.option)
        elif request.option == 3:
            print('[OPTION SELECT: %s] Listar todos os cliente' % request.option)
            return portal_pb2.OptionReplay(message='[%s] Listar todos os cliente' % request.option)
        elif request.option == 4:
            print('[OPTION SELECT: %s] Excluir cliente' % request.option)
            return portal_pb2.OptionReplay(message='[%s] Excluir cliente' % request.option)
        elif request.option == 5:
            print('[OPTION SELECT: %s] Excluir todos os clientes' % request.option)
            return portal_pb2.OptionReplay(message='[%s] Excluir todos os clientes' % request.option)
        return portal_pb2.OptionReplay(message='Valor informado não corresponde as opções disponíveis')

    def Connecting(self, request, context):
        print('[CONNECTED] Host: %s' %request.message)
        return portal_pb2.ConectReply(message='Conexão Estabelecida com sucesso!')

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    portal_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
