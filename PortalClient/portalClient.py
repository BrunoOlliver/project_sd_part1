#portalClient.py publish -> mqtt -> portalAdmin
import base64
import socket
import threading
import time
import random
import paho.mqtt as mqtt

def start():
    #atribui um endereço IP e um número de porta a
    #uma instância de soquete.
    s = socket.socket()
    host = socket.gethostname()
    port = 12345
    s.bind((host, port))
    print('[LISTENING] Seridor está aguardando comunicação com cliente')
    s.listen(5)

    #threadsub = threading.Thread(target=subscribeToTopic, args=())
    #threadsub.run()
    while True:
        c, addr = s.accept()

        thread = threading.Thread(target=customer_portal, args=(c, addr))
        thread.start()

        print('[ACTIVE CONNECTION] '+str((threading.activeCount()-1)))
    s.close()

def validaID():
    while True:
        usrid = input('Digite seu ID: ')
        if not usrid.isdigit():
            print('ID precisa ser numerico')
        else:
            break
    return usrid


def customer_portal(c, addr):
    print('[CONNECTED] Conexão estabelecida: ', addr)
    try:
        while True:
            c.send('\n\n=======PORTAL DO CLIENTE=======\n'+
                  '1. Nova Tarefa\n'+
                  '2. Alterar tarefa existente\n'+
                  '3. Listar todas as tarefas\n'+
                  '4. Excluir tarefa existente\n'+
                  '5. Excluir todas as tarefas\n'+
                  '6. Sair'.encode())
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

                newId = random.randint(1,50)
                id = str(newId)
                newTask = {'ID':id,'TITULO':titulo,'TAREFA':tarefa}

                #Esse trecho manda um dict para PortalAdmin (teste feito em Portal Cliente)
                #teste com cliente funciona
                #proximo passo: enviar via mosquito para portal Admin
                encoded_task = str(newTask).encode('utf-8')

                base64_task = base64.b64encode(encoded_task)
                c.send(base64_task)

                banco = {id:base64_task}

            elif opcao == '2':
                #2. Alterar tarefa existente
                #recebe o nro da tarefa que deseja alterar
                #portalAdmin deve receber essa tarefa e fazer a alteração
                print('[OK] Opção selecionada: '+opcao+'.Alterar tarefa existente')
                loop2 = True
                while loop2:
                    c.send('Digite a ID da Tarefa: '.encode())
                    op2 = c.recv(1024)
                    numTask = op2.decode()

                    if not numTask.isdigit():
                        print('[ERRO]: ['+numTask+'] não corresponde ao valor de uma ID.')
                        c.send('[ERRO] Favor inserir um valor numérico para a ID: '.encode())
                    else:
                        print('[OK] ID recebida com sucesso')
                        flag = 'False'
                        loop2 = False
                        c.send(flag.encode())

            elif opcao == '3':
                #3. Listar todas as tarefas
                #receber do portalAdmin um dicionario com todos as tarefas
                print('[OK] Opção selecionada: '+opcao+'.Listar todas as tarefas')
                c.send('Segue todas as tarefas abaixo: '.encode())

                op3 = c.recv(1024)
                listTask = op3.decode()
            elif opcao == '4':
                #4. Excluir tarefa existente
                print('[OK] Opção selecionada: '+opcao+'.Excluir tarefa existente')
                c.send('Informe a ID da Tarefa a ser excluida: '.encode())
                op4 = c.recv(1024)
                removeTask = op4.decode()
            elif opcao == '5':
                #5. Excluir todas as tarefas
                print('[OK] Opção selecionada: '+opcao+'.Excluir todas as tarefas')
                c.send('Deseja realmente excluit todas as tarefas?'.encode())
                op5 = c.recv(1024)
                delTask = op5.decode()
            elif opcao == '6':
                #6. Sair
                print('[OK] Opção selecionada: '+opcao+'.Sair')

    except ConnectionError:
        print('[DESCONECT] Encerrada conexão com cliente: ',addr)

start()
 # EXEMPLO
 #my_dict = {'name': 'Rajiv Sharma', 'designation': "Technology Supervisor"}
 #encoded_dict = str(my_dict).encode('utf-8')
 #base64_dict = base64.b64encode(encoded_dict)
 #print(base64_dict)

 #my_dict_again = eval(base64.b64decode(base64_dict))
 #print(my_dict_again)


#client.py

#!/usr/bin/python                      # This is client.py file

#import socket                          # Import socket module

#s = socket.socket()                    # Create a socket object
#host = socket.gethostname()            # Get local machine name
#port = 12345                           # Reserve a port for your service.

#s.connect((host, port))
#data = s.recv(1024)
#print(data.decode())
#s.close()
