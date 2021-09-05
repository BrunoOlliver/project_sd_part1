#portalClient.py publish -> mqtt -> portalAdmin
import base64
import socket
import threading
import time
import random
import paho.mqtt as mqtt

ntask = {'100':{'ID':'100','TITLE':'TESTE','DESC':'EXEMPLO'},'200':{'ID':'200','TITLE':'TESTE','DESC':'EXEMPLO'}}
dic_client = {'ID':'12345','NAME':'JOAO','TASK':ntask}
global banco_client
banco_client = {dic_client['ID']:dic_client}

def start():
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    print('[LISTENING] Servidor está aguardando comunicação com cliente')
    s.listen(5)

    while True:
        c, addr = s.accept()
        thread = threading.Thread(target=customer_portal, args=(c, addr))
        thread.start()

        print('[ACTIVE CONNECTION] '+str((threading.activeCount()-1)))
    s.close()

def CheckUser(id, user, banco_client):
    if id in banco_client.keys() and user in banco_client[id]['NAME']:
        return True
    else:
        return False


def validaID():
    while True:
        usrid = input('Digite seu ID: ')
        if not usrid.isdigit():
            print('ID precisa ser numerico')
        else:
            break
    return usrid

def menu():
    menu ='''\n\n=======PORTAL DO CLIENTE=======\n
    1. Nova Tarefa
    2. Alterar tarefa existente
    3. Listar todas as tarefas
    4. Excluir tarefa existente
    5. Excluir todas as tarefas
    6. Sair'''
    return menu

def customer_portal(c, addr):
    try:
        loop1 = True
        while loop1:

            id_client = c.recv(1024)
            user_client = c.recv(1024)

            idClient = id_client.decode()
            userClient = user_client.decode()

            if CheckUser(idClient,userClient,banco_client):
                loop1 = False
                print('[USER AUTENTICATION] OK! ID: '+id_client.decode()+' USER: '+user_client.decode())
                c.send('PERMITIDO'.encode())
            else:
                loop1 = True
                print('[ERROR] ID e USER não localizados.')
                c.send('NEGADO'.encode())

        print('[CONNECTED] Conexão estabelecida: ', addr)

        while True:
            portal_menu = menu()
            c.send(portal_menu.encode())
            num = c.recv(1024)
            opcao = num.decode()

            if opcao == '1':
                #1. Nova Tarefa
                print('[OK] Opção selecionada: '+opcao+'.Nova Tarefa')
                c.send('Titulo da Tarefa: '.encode())
                op1 = c.recv(1024)
                titulo = op1.decode()

                c.send('Descrição da Tarefa: '.encode())
                op1 = c.recv(1024)
                tarefa = op1.decode()

                newId = random.randint(1,50) #gera uma ID para Tarefa
                id = str(newId)
                newTask = {'ID':id,'TITLE':titulo,'DESC':tarefa}
                banco_client[idClient]['TASK'].update({id:newTask})
                encoded_task = str(newTask).encode('utf-8')
                base64_task = base64.b64encode(encoded_task)
                c.send(base64_task)
                banco = {id:base64_task}

            elif opcao == '2':
                #2. Alterar tarefa existente
                print('[OK] Opção selecionada: '+opcao+'.Alterar tarefa existente')
                loop2 = True
                while loop2:
                    c.send('Digite a ID da Tarefa: '.encode())
                    op2 = c.recv(1024)
                    idTask = op2.decode()

                    if idTask.isdigit() == False:
                        print('[ERRO]: ['+idTask+'] não corresponde ao valor de uma ID.')
                        c.send('[ERRO] Favor inserir um valor numérico para a ID: '.encode())
                    else:
                        if idTask in banco_client[idClient]['TASK'].keys():
                            print('[OK] ID recebida com sucesso')
                            loop2 = False
                            c.send('PERMITE'.encode())
                            c.send('False'.encode())

                            newTask2 = banco_client[idClient]['TASK'].get(idTask)
                            encoded_task1 = str(newTask2).encode('utf-8')
                            base64_task1 = base64.b64encode(encoded_task1)
                            c.send(base64_task1)
                            opTask = c.recv(1024)
                            if opTask.decode() == '1':
                                newTitle = c.recv(1024)
                                t_title = newTitle.decode()
                                banco_client[idClient]['TASK'][idTask]['TITLE'] = t_title
                                print('[UPDATE] Tarefa do Cliente ID: '+idTask+' sofreu alteração no Título')
                                newTask2 = banco_client[idClient]['TASK'].get(idTask)
                            elif opTask.decode() == '2':
                                newDesc = c.recv(1024)
                                t_desc = newDesc.decode()
                                banco_client[idClient]['TASK'][idTask]['DESC'] = t_desc
                                print('[UPDATE] Tarefa do Cliente ID: '+idTask+' sofreu alteração na Descrição')
                                newTask2 = banco_client[idClient]['TASK'].get(idTask)
                            encoded_task2 = str(newTask2).encode('utf-8')
                            base64_task2 = base64.b64encode(encoded_task2)
                            print(base64_task2)
                            c.send(base64_task2)
                        else:
                            loop2 = False
                            print('[ID TASK INVALID] Não há tarefas com a ID informada!')
                            c.send('NEGADO'.encode())
                            c.send('True'.encode())

            elif opcao == '3':
                #3. Listar todas as tarefas
                print('[OK] Opção selecionada: '+opcao+'.Listar todas as tarefas')
                newTask3 = banco_client[idClient].get('TASK')
                t_tsk = str(newTask3)
                encode_tsk = t_tsk.encode('utf-8')
                base64_tsk = base64.b64encode(encode_tsk)
                c.send(base64_tsk)

            elif opcao == '4':
                #4. Excluir tarefa existente
                print('[OK] Opção selecionada: '+opcao+'.Excluir tarefa existente')
                c.send('Informe a ID da Tarefa a ser excluida: '.encode())
                op4 = c.recv(1024)
                idTask = op4.decode()

                tsk_keys = banco_client[idClient]['TASK']
                encode_tsk_keys = str(tsk_keys).encode('utf-8')
                base64_tsk_keys = base64.b64encode(encode_tsk_keys)
                c.send(base64_tsk_keys)

                if idTask in tsk_keys.keys():
                    banco_client[idClient]['TASK'].pop(idTask)

                    print('[REMOVE] Uma tarefa foi excluida do cliente ID: ',idClient)
                    c.send('Tarefa removida com sucesso!'.encode())

                else:
                    print('[ERROR] Chave informada não existe')

            elif opcao == '5':
                #5. Excluir todas as tarefas
                print('[OK] Opção selecionada: '+opcao+'.Excluir todas as tarefas')
                c.send('Deseja realmente excluir todas as tarefas?'.encode())
                op_task = c.recv(1024)

                if op_task.decode() == '1':
                    print('[DELETE ALL TASKS] Todas as tarefas foram removidas do cliente ID: ',idClient)
                    banco_client[idClient]['TASK'].clear()
                    c.send('Ação efetuada com sucesso!'.encode())
                elif op_task.decode() == '2':
                    print('[CANCEL TASK DELETION] Cancelada a exclusão das tarefas do cliente ID: ',idClient)
                    c.send('Ação cancelada, nenhuma tarefa excluida!'.encode())
                elif op_task.decode() != '1' or op_task.decode() != '2':
                    print('[INVALID] Opção inválida')
                    c.send('Ação cancelada, nenhuma tarefa excluida!'.encode())
            elif opcao == '6':
                #6. Sair
                print('[OK] Opção selecionada: '+opcao+'.Sair')
    except ConnectionError:
        print('[DESCONECT] Encerrada conexão com cliente: ',addr)

start()
