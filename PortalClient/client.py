#client.py subscribe -> socket -> portalClient.py

import base64
import socket
import time
import os

def clean():
    os.system('cls')

loop1 = True
while loop1:
    try:
        s = socket.socket()
        host = socket.gethostname()
        port = 12345
        s.connect((host, port))

        banco = dict()
        contador = 0

        loop2 = True
        while loop2:

            #print('volta ',contador)
            #Recebe Menu
            menu = s.recv(1024)
            print(menu.decode())

            #Envia opção escolhida
            num = input('\nDigite a opção: ')
            opcao = str(num)
            s.send(opcao.encode())

            if opcao == '1':
                clean()
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

                print(base64_task)

                print('\nDados Cadastrados: ')
                for x,y in decode_task.items():
                    print(x,y)
                #break
            elif opcao == '2':
                clean()
                #2. Alterar tarefa existente

                loop3 = True
                while loop3:
                    op2 = s.recv(1024)
                    print(op2.decode())
                    idTask = input()
                    numTask = str(idTask)
                    s.send(numTask.encode())

                    rspFlag = s.recv(1024)
                    flag = rspFlag.decode()

                    if flag =='False':
                        loop3 = False
                    else:
                        print(rspFlag.decode())
                #break
            elif opcao == '3':
                clean()
                #3. Listar todas as tarefas
                op3 = s.recv(1024)
                print(op3.decode())
                listTask = input()
                break
            elif opcao == '4':
                clean()
                #4. Excluir tarefa existente
                op4 = s.recv(1024)
                print(op4.decode())
                removeTask = input()

                s.send(removeTask.encode())
                break
            elif opcao == '5':
                clean()
                #5. Excluir todas as tarefas
                op5 = s.recv(1024)
                print(op5.decode())
                delTask = input()
                break
            elif opcao == '6':
                #6. Sair da Tarefa
                loop1 = False
                break

        s.close()
    except ConnectionError:
        print('[ERRO] Conexão com o servidor não disponível')


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
