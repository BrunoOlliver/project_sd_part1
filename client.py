#Client.py subscribe -> mqtt -> portalClient.py
import base64
#import codecs
#import pickle
import socket                          # Import socket module

s = socket.socket()                    # Create a socket object
host = socket.gethostname()            # Get local machine name
port = 12345                           # Reserve a port for your service.

s.connect((host, port))

def menu():
    print('========MENU DO CLIENTE======\n')
    print('1. Nova Tarefa\n')
    print('2. Alterar tarefa existente\n')
    print('3. Listar todas as tarefas\n')
    print('4. Excluir tarefa existente\n')
    print('5. Excluir todas as tarefas\n')
    print('6. Sair\n')
    opcao = input('\nDigite uma das opções acima: ')
    return opcao


def validaID():
    while True:
        usrid = input('Digite seu ID: ')
        if not usrid.isdigit():
            print('ID precisa ser numerico')
        else:
            break
    return usrid


def run():

    while True:
        opcao = menu()

        #s.send(opcao.encode())

        if opcao == '1':
            usrid = validaID()
            titulo = input('Titulo da Tarefa: ')
            tarefa = input('Descrição da Tarefa: ')

            dataTask = {'ID': usrid,'TITULO': titulo,'TAREFA': tarefa}

            s.send(str(dataTask).encode('utf-8'))

            #DECODIFICANDO PARA VER SE CODIFICOU
            #base64_dict = base64.b64encode(encoded_dict)
            #print(encoded_dict)

#my_dict = {'name': 'Rajiv Sharma', 'designation': "Technology Supervisor"}
#encoded_dict = str(my_dict).encode('utf-8')
#base64_dict = base64.b64encode(encoded_dict)
#print(base64_dict)

#my_dict_again = eval(base64.b64decode(base64_dict))
#print(my_dict_again)

        else:
            break

        data = s.recv(1024)
        print("\nMensagem recebida: ",data.decode())


    print('\nFechando conexão do Cliente')
    s.close()                              # Close the socket when done

run()


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
