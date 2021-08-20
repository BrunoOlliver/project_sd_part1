#portalClient.py publish -> mqtt -> portalAdmin
import base64
import socket
import random
import paho.mqtt as mqtt

s = socket.socket()
host = socket.gethostname()
port = 12345
#atribui um endereço IP e um número de porta a
#uma instância de soquete.
s.bind((host, port))

def validaID():
    while True:
        usrid = input('Digite seu ID: ')
        if not usrid.isdigit():
            print('ID precisa ser numerico')
        else:
            break
    return usrid


def run():
    s.listen(5)
    while True:
        c, addr = s.accept()
        print('Got connection from', addr)

        #Envia Menu
        c.send('=======PORTAL DO CLIENTE=======\n1. Nova Tarefa\n2. Alterar tarefa existente\n3. Listar todas as tarefas\n4. Excluir tarefa existente\n5. Excluir todas as tarefas\n6. Sair'.encode())
        #c.send('Opcao: '.encode())
        #Recebe opção escolhida
        num = c.recv(1024)
        opcao = num.decode()

        if opcao == '1':
            #1. Nova Tarefa
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

        elif opcao == '2':
            #2. Alterar tarefa existente
            c.send('Titulo da Tarefa: '.encode())
            op2 = c.recv(1024)
            alterTask = op2.decode()
        elif opcao == '3':
            #3. Listar todas as tarefas
            c.send('Titulo da Tarefa: '.encode())
            op3 = c.recv(1024)
            listTask = op3.decode()
        elif opcao == '4':
            #4. Excluir tarefa existente
            c.send('Titulo da Tarefa: '.encode())
            op4 = c.recv(1024)
            removeTask = op4.decode()
        elif opcao == '5':
            #5. Excluir todas as tarefas
            c.send('Titulo da Tarefa: '.encode())
            op5 = c.recv(1024)
            delTask = op5.decode()
        elif opcao == '6':
            #6. Sair
            c.send('Titulo da Tarefa: '.encode())
            op6 = c.recv(1024)
            exitTask = op6.decode()
    print('\nFechando conexão do Cliente')
run()

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
