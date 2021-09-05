
import base64
import socket
import time
import os

def clean():
    os.system('cls')


def run():
    loop1 = True
    while loop1:
        try:
            s = socket.socket()
            host = socket.gethostname()
            port = 12345
            s.connect((host, port))
            loop2 = True
            while loop2:
                #Solicita dados para validação de Cliente
                id_login = input('Informe seu ID: ')
                s.send(id_login.encode())
                user_login = input('Informe seu Usuário Cliente: ')
                s.send(user_login.encode())

                login = s.recv(1024)

                if login.decode() == 'PERMITIDO':
                    print('Usuário Autenticado!')
                    loop2 = False
                elif login.decode() == 'NEGADO':
                    print('Usuário Não Autenticado!')
                    loop2 = True
            loop3 = True
            while loop3:
                #Recebe Menu
                menu = s.recv(1024)
                print(menu.decode())

                #Envia opção escolhida
                num = input('\nDigite a opção: ')
                opcao = str(num)
                s.send(opcao.encode())

                if opcao == '1':
                    #clean()
                    #1. Nova Tarefa
                    op1 = s.recv(1024)
                    print(op1.decode())
                    titulo = input()
                    s.send(titulo.encode())

                    op1 = s.recv(1024)
                    print(op1.decode())
                    tarefa = input()
                    s.send(tarefa.encode())

                    base64_task = s.recv(1024)
                    decode_task = eval(base64.b64decode(base64_task))

                    print('\nDados Cadastrados: ')
                    for x,y in decode_task.items():
                        print(x,y)
                    #break
                elif opcao == '2':
                    #clean()
                    #2. Alterar tarefa existente
                    loop4 = True
                    while loop4:
                        op2 = s.recv(1024)
                        print(op2.decode())
                        idTask = input()
                        numTask = str(idTask)
                        s.send(numTask.encode())

                        rsp = s.recv(1024)
                        flag = s.recv(1024)
                        if rsp.decode() == 'PERMITE':
                            loop4 = False
                            if flag.decode() =='False':

                                base64_task1 = s.recv(1024)
                                decode_task1 = eval(base64.b64decode(base64_task1))

                                print('\nDados da Tarefa Cadastrada: ')
                                for x,y in decode_task1.items():
                                    print(x,y)

                                loop5 = True
                                while loop5:
                                    altTask = input('''\nInforme o que será alterado:\n1. Título da Tarefa\n2. Descrição da Tarefa\nOpção Desejada: ''')
                                    s.send(altTask.encode())
                                    if altTask == '1':
                                        loop5 = False

                                        newTitle = input('\nDigite o novo Título: ')
                                        s.send(newTitle.encode())
                                    elif altTask == '2':
                                        loop5 = False
                                        newDesc = str(input('Digite a nova Descrição: '))
                                        s.send(newDesc.encode())
                                    elif altTask != '1' or altTask != '2':
                                        loop5 = True
                                        print('Opção inválida')

                                    base64_task2 = s.recv(1024)
                                    decode_task2 = eval(base64.b64decode(base64_task2))

                                    print(base64_task2)

                                    print('\nDados da Tarefa Cadastrada: ')
                                    for x,y in decode_task2.items():
                                        print(x,y)
                            else:
                                if flag.decode() == 'True':
                                    print(rspFlag.decode())
                        else:
                            loop4 = False
                            print('ID inválida ou não encontrada!')
                elif opcao == '3':
                    #clean()
                    loop3 = True

                    encode_tsk = s.recv(1024)
                    tsk_list = eval(base64.b64decode(encode_tsk))

                    if len(tsk_list.items()) == 0:
                        print('Não há tarefas cadastradas!')
                    else:
                        #3. Listar todas as tarefas
                        print('\nTarefa Cadastrada: ')
                        for x,y in tsk_list.items():
                            print(x,y)
                elif opcao == '4':
                    #clean()
                    loop3 = True
                    #4. Excluir tarefa existente
                    op4 = s.recv(1024)
                    print(op4.decode())
                    idTask = input()

                    s.send(idTask.encode())
                    keys = s.recv(1024)
                    tsk_keys = eval(base64.b64decode(keys))

                    if idTask in tsk_keys.keys():
                        rsp = s.recv(1024)
                        print(rsp.decode())
                    else:
                        print('ID inválida ou não existe!')
                elif opcao == '5':
                    #clean()
                    #5. Excluir todas as tarefas
                    op5 = s.recv(1024)
                    print(op5.decode())

                    op_task = input('DIGITE: [1] SIM [2] NÃO\nOPÇÃO: ')
                    s.send(op_task.encode())

                    tsk_del = s.recv(1024)
                    print(tsk_del.decode())

                elif opcao == '6':
                    #6. Sair da Tarefa
                    loop1 = False
                    break

            s.close()
        except ConnectionError:
            print('[ERRO] Conexão com o servidor não disponível')


run()
