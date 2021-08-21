#client.py subscribe -> socket -> portalClient.py

import base64
import socket
import time

s = socket.socket()
host = socket.gethostname()
port = 12345
#conecta um soquete de cliente baseado em TCP a
#um soquete de servidor baseado em TCP.
s.connect((host, port))

banco = dict()


while True:
    #Recebe Menu
    menu = s.recv(1024)
    print(menu.decode())

    #Envia opção escolhida
    num = input('\nDigite a opção: ')
    opcao = str(num)
    s.send(opcao.encode())

    if opcao == '1':
        #1. Nova Tarefa
        op1 = s.recv(1024)
        print(op1.decode())
        titulo = input()
        s.send(titulo.encode())

        op1 = s.recv(1024)
        print(op1.decode())
        tarefa = input()
        s.send(tarefa.encode())

        #Apenas um exemplo pra teste o trecho abaixo vai para o portalAdmin
        base64_task = s.recv(1024)
        decode_task = eval(base64.b64decode(base64_task))

        print('Dados Cadastrados: ', decode_task)
        break
    elif opcao == '2':
        #2. Alterar tarefa existente
        op2 = s.recv(1024)
        print(op2.decode())
        loop = True
        while loop:
            alterTask = input('ID da Tarefa: ')
            numTask = str(alterTask)
            s.send(numTask.encode())
            rspFlag = s.recv(1024)
            flag = rspFlag.decode()
            if flag =='False':
                loop = False
            else:
                print(rspFlag.decode())
        break
    elif opcao == '3':
        #3. Listar todas as tarefas
        op3 = s.recv(1024)
        print(op3.decode())
        listTask = input()
        break
    elif opcao == '4':
        #4. Excluir tarefa existente
        op4 = s.recv(1024)
        print(op4.decode())
        removeTask = input()

        s.send(removeTask.encode())
        break
    elif opcao == '5':
        #5. Excluir todas as tarefas
        op5 = s.recv(1024)
        print(op5.decode())
        delTask = input()
        break
    elif opcao == '6':
        #6. Sair
        op6 = s.recv(1024)
        print(op6.decode())
        exitTask = input()
        s.close()

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
