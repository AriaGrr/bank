import datetime

# Funções auxiliares

def clear_screen():
    # Função para limpar a tela do terminal
    print('\033[H\033[J')

def load_data():
    # Função para carregar os dados do arquivo de dados
    try:
        with open('data.txt', 'r') as file:
            data = eval(file.read())
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    # Função para salvar os dados no arquivo de dados
    with open('data.txt', 'w') as file:
        file.write(str(data))

def load_transactions():
    # Função para carregar as transações do arquivo de transações
    try:
        with open('transactions.txt', 'r') as file:
            transactions = eval(file.read())
    except FileNotFoundError:
        transactions = {}
    return transactions

def save_transactions(transactions):
    # Função para salvar as transações no arquivo de transações
    with open('transactions.txt', 'w') as file:
        file.write(str(transactions))

# Carregar os dados e transações existentes
data = load_data()
transactions = load_transactions()

def create_account():
    # Função para criar um novo cliente
    name = input('Digite o nome do cliente: ')
    while not name.isalpha():
        print("Nome invalido.")
        name = input('Digite o nome do cliente: ')
    # Verifica se o CPF já está cadastrado
    cpf = input('Digite o CPF do cliente: ')
    while cpf in data:
        print('CPF já cadastrado.')
        cpf = input('Digite o CPF do cliente: ')
    # Verifica se o CPF é válido
    while not cpf.isdigit() or len(cpf) != 11:
        print("CPF invalido.")
        cpf = input('Digite o CPF do cliente: ')
    # Verifica se o tipo de conta é válido
    account_type = input('Digite o tipo de conta (1 - Comum, 2 - Plus): ')
    while account_type not in ['1', '2']:
        print('Tipo de conta inválido. Digite 1 para conta comum ou 2 para conta plus.')
        account_type = input('Digite o tipo de conta (1 - Comum, 2 - Plus): ')
    account_type = int(account_type)
    if account_type == 1:
        account_type = 'comum'
    elif account_type == 2:
        account_type = 'plus'
    # Verifica se o saldo inicial é válido
    initial_balance = input('Digite o valor inicial da conta: ')
    while not initial_balance.isdigit():
        print("Valor invalido.")
        initial_balance = input('Digite o valor inicial da conta: ')
    initial_balance = float(initial_balance)
    if initial_balance < 0:
        print('Saldo inicial inválido. O saldo inicial não pode ser negativo.')
        return
    # Verifica se o saldo inicial da poupança é válido
    initial_saving = input('Digite o valor inicial da conta poupança: ')
    while not initial_saving.isdigit():
        print("Valor invalido.")
        initial_saving = input('Digite o valor inicial da conta: ')
    initial_saving = float(initial_saving)
    if initial_saving < 0:
        print('Saldo inicial inválido. O saldo inicial não pode ser negativo.')
        return
    # Verifica se a senha é válida
    password = input('Digite a senha de quatro digitos do cliente: ')
    while not password.isdigit() or len(password) != 4:
        print("Senha invalida.")
        password = input('Digite a senha de quatro digitos do cliente: ')

    if not name or not cpf or not account_type or not initial_balance or not initial_saving or not password:
        print('Dados inválidos. Preencha todos os campos.')
        return
    # Cria o cliente
    data[cpf] = {
        'name': name,
        'account_type': account_type,
        'balance': initial_balance,
        'password': password,
        'saving': initial_saving,
        'created_at': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    save_data(data)
    print('Cliente criado com sucesso!')

def delete_account():
    # Função para apagar um cliente pelo CPF
    cpf = input('Digite o CPF do cliente: ')
    # Verifica se o CPF é válido
    if not cpf:
        print('CPF inválido. Digite um CPF válido.')
        return
    # Verifica se o CPF está cadastrado
    if cpf in data:
        del data[cpf]
        save_data(data)
        if cpf in transactions:
            del transactions[cpf]
            save_transactions(transactions)
        print('Cliente removido com sucesso!')
    else:
        print('CPF não encontrado. Cliente não removido.')

def list_accounts():
    # Função para listar os clientes
    if not data:
        print('Nenhum cliente cadastrado.')
    else:
        print('Lista de Clientes:')
        for cpf, account in data.items():
            print('---')
            print(f"Nome: {account['name']}")
            print(f"CPF: {cpf}")
            print(f"Tipo de conta: {account['account_type']}")
            print(f"Saldo Corrente: R$ {account['balance']:.2f}")
            print(f"Saldo Poupança: R$ {account['saving']:.2f}")
        print('---')

def debit():
    # Função para debitar um valor da conta do cliente
    cpf = input('Digite o CPF do cliente: ')
    password = input('Digite a senha do cliente: ')
    value = input('Digite o valor a ser debitado: ')
    # Verifica se o CPF é válido
    if not cpf or not password or not value:
        print('Dados inválidos. Preencha todos os campos.')
        return
    # Verifica se o CPF está cadastrado
    if cpf in data and data[cpf]['password'] == password:
        try:
            value = float(value)
        except ValueError:
            print('Valor inválido. Digite um número.')
            return
        
        account_type = data[cpf]['account_type']
        balance = data[cpf]['balance']
        # Verifica se o saldo é suficiente para o débito e o tipo de conta, e então debita o valor
        if account_type == 'comum':
            if balance - value >= -1000:
                data[cpf]['balance'] -= value
                fee = value * 0.05
                data[cpf]['balance'] -= fee
                add_transaction(cpf, -value, 'Débito', fee)
                save_data(data)
                print('Débito realizado com sucesso!')
            else:
                print('Saldo insuficiente para realizar o débito.')
        elif account_type == 'plus':
            if balance - value >= -5000:
                data[cpf]['balance'] -= value
                fee = value * 0.03
                data[cpf]['balance'] -= fee
                add_transaction(cpf, -value, 'Débito', fee)
                save_data(data)
                print('Débito realizado com sucesso!')
            else:
                print('Saldo insuficiente para realizar o débito.')
    else:
        print('CPF ou senha incorretos.')

def deposit():
    # Função para depositar um valor na conta do cliente
    cpf = input('Digite o CPF do cliente: ')
    value = input('Digite o valor a ser depositado: ')
    # Verifica se o CPF é válido
    if not cpf or not value:
        print('Dados inválidos. Preencha todos os campos.')
        return
    # Verifica se o CPF está cadastrado
    if cpf in data:
        try:
            value = float(value)
        except ValueError:
            print('Valor inválido. Digite um número.')
            return
        # Deposita o valor
        data[cpf]['balance'] += value
        add_transaction(cpf, value, 'Depósito')
        save_data(data)
        print('Depósito realizado com sucesso!')
    else:
        print('CPF não encontrado.')

def add_transaction(cpf, value, origin, fee = 0.00):
    # Função para adicionar uma transação à lista de transações
    if cpf in transactions:
        balance = data[cpf]['balance']
        saving = data[cpf]['saving']
        account = data[cpf]['account_type']
        # # Verifica o tipo de conta e calcula a taxa se for débito
        # if origin == ('Débito' or 'Débito Automatico' or 'Débito Poupança') and account == 'comum':
        #     fee = value * 0.05 
        # elif origin == ('Débito' or 'Débito Automatico' or 'Débito Poupança') and account == 'plus':
        #     fee = value * 0.03
        # else:
        #     fee = 0.0
        transactions[cpf].append({
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': value,
            'origin': origin,
            'balance': balance,
            'saving': saving,
            'fee': fee
        })
    else:
        transactions[cpf] = [{
            'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'value': value,
            'origin': origin,
            'balance': data[cpf]['balance'],
            'saving': data[cpf]['saving'],
            'fee': fee
        }]
    save_transactions(transactions)

def statement():
    # Função para exibir o extrato do cliente
    cpf = input('Digite o CPF do cliente: ')
    password = input('Digite a senha do cliente: ')

    if not cpf or not password:
        print('Dados inválidos. Preencha todos os campos.')
        return

    if cpf in data and data[cpf]['password'] == password:
        print('Extrato de transações:')
        for transaction in transactions[cpf]:
            print('---')
            print(f"Data: {transaction['date']}")
            print(f"Origem: {transaction['origin']}")
            print(f"Valor: R$ {transaction['value']:.2f}")
            if transaction['fee'] > 0.00:
                print(f"Tarifa: R$ {transaction['fee']:.2f}")
            print(f"Saldo Corrente: R$ {transaction['balance']:.2f}")
            print(f"Saldo Poupança: R$ {transaction['saving']:.2f}")
        print('---')

        # Exibe o saldo atual da conta incluindo poupança
        print('Saldo atual:')
        print(f"Saldo Corrente: R$ {data[cpf]['balance']:.2f}")
        print(f"Saldo Poupança: R$ {data[cpf]['saving']:.2f}")
    else:
        print('CPF ou senha incorretos.')

def transfer():
    # Função para realizar a transferência entre contas
    cpf_origin = input('Digite o CPF da conta de origem: ')
    password_origin = input('Digite a senha da conta de origem: ')
    cpf_destination = input('Digite o CPF da conta de destino: ')
    value = input('Digite o valor a ser transferido: ')

    if not cpf_origin or not password_origin or not cpf_destination or not value:
        print('Dados inválidos. Preencha todos os campos.')
        return

    if cpf_origin in data and data[cpf_origin]['password'] == password_origin and cpf_destination in data and cpf_origin != cpf_destination:
        try:
            value = float(value)
        except ValueError:
            print('Valor inválido. Digite um número.')
            return

        if data[cpf_origin]['balance'] >= value:
            data[cpf_origin]['balance'] -= value
            data[cpf_destination]['balance'] += value
            add_transaction(cpf_origin, -value, f'Transferido para {get_name(cpf_destination)}')
            add_transaction(cpf_destination, value, f'Transferência recebida de {get_name(cpf_origin)}')
            save_data(data)
            print('Transferência realizada com sucesso!')
        else:
            print('Saldo insuficiente para realizar a transferência.')
    else:
        print('CPF ou senha incorretos ou conta de destino não encontrada.')

def get_name(cpf):
    # Função para obter o nome correspondente a um CPF
    if cpf in data:
        return data[cpf]['name']
    return "Desconhecido"

# def register_automatic_debit():
#     # Função para registrar um débito automático
#     cpf = input('Digite o CPF do cliente: ')
#     password = input('Digite a senha do cliente: ')

#     if not cpf or not password:
#         print('Dados inválidos. Preencha todos os campos.')
#         return

#     if cpf in data and data[cpf]['password'] == password:
#         value = input('Digite o valor a ser debitado: ')
#         debit_type = input('Digite o tipo de débito: ')
#         recurrence = input('Digite a recorrência (1 - Diária, 2 - Semanal, 3 - Mensal): ')

        
                
#         if recurrence == '1':
#             recurrence = 'Diária'
#         elif recurrence == '2':
#             recurrence = 'Semanal'
#         elif recurrence == '3':
#             recurrence = 'Mensal'
#         else:
#             print('Recorrência inválida. Escolha entre 1, 2 ou 3 para Diária, Semanal ou Mensal, respectivamente.')
#             return
#         # Verifica se os dados foram preenchidos
#         if not value or not debit_type or not recurrence:
#             print('Dados inválidos. Preencha todos os campos.')
#             return
#         # Verifica se o valor é um número
#         try:
#             value = float(value)
#         except ValueError:
#             print('Valor inválido. Digite um número.')
#             return

#         if recurrence not in ['Diária', 'Semanal', 'Mensal']:
#             print('Recorrência inválida. Escolha entre Diária, Semanal ou Mensal.')
#             return

#         # Armazene os dados do débito automático como uma transação
#         transaction = {
#             'date': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'value': -value,
#             'origin': f'Débito Automático - {debit_type} ({recurrence})',
#             'type': 'auto-debit',
#             'recurrence': {recurrence}
#         }       
        
#         data[cpf]['balance'] -= value
#         fee = value * 0.05
#         data[cpf]['balance'] -= fee
       
#         save_data(data)
       
#         # Armazene os dados do débito automático como uma transação
#         if cpf in transactions:
#             transactions[cpf].append(transaction)
#         else:
#             transactions[cpf] = [transaction]

#         save_transactions(transactions)        

#         print('Débito automático cadastrado com sucesso!')
#     else:
#         print('CPF ou senha incorretos.')

# def list_automatic_debits():
#     data = load_data()
#     transactions = load_transactions()
#     # Função para listar os débitos automáticos de um cliente
#     cpf = input('Digite o CPF do cliente: ')
#     password = input('Digite a senha do cliente: ')

#     if not cpf or not password:
#         print('Dados inválidos. Preencha todos os campos.')
#         return
#     # Verifica se o cliente existe e se a senha está correta
#     if cpf in data and data[cpf]['password'] == password:
#         if cpf in transactions:
#             automatic_debits = [transaction for transaction in transactions[cpf] if 'Débito Automático' in transaction['origin']]
#             if automatic_debits:
#                 print('Débitos Automáticos:')
#                 print('Data\t\t\tValor\tOrigem')
#                 for transaction in automatic_debits:
#                     print(f"{transaction['date']}\t{transaction['value']}\t{transaction['origin']}")
#                 print('---')
#             else:
#                 print('Nenhum débito automático cadastrado para este cliente.')
#         else:
#             print('Nenhum débito automático cadastrado para este cliente.')
#     else:
#         print('CPF ou senha incorretos.')

# def delete_automatic_debit():
#     # Função para excluir um débito automático cadastrado
#     cpf = input('Digite o CPF do cliente: ')
#     password = input('Digite a senha do cliente: ')
#     # Verifica se os dados foram preenchidos
#     if not cpf or not password:
#         print('Dados inválidos. Preencha todos os campos.')
#         return
#     # Verifica se o cliente existe e se a senha está correta
#     if cpf in data and data[cpf]['password'] == password:
#         if cpf in transactions:
#             automatic_debits = [transaction for transaction in transactions[cpf] if 'Débito Automático' in transaction['origin']]
#             if automatic_debits:
#                 print('Débitos Automáticos:')
#                 print('Índice\tData\t\t\tValor\tOrigem')
#                 for i, transaction in enumerate(automatic_debits):
#                     print(f"{i}\t{transaction['date']}\t{transaction['value']}\t{transaction['origin']}")
#                 print('---')
#                 index = input('Digite o índice do débito automático a ser excluído: ')
#                 if index.isdigit() and int(index) < len(automatic_debits):
#                     del transactions[cpf][transactions[cpf].index(automatic_debits[int(index)])]
#                     save_transactions(transactions)
#                     print('Débito automático excluído com sucesso!')
#                 else:
#                     print('Índice inválido.')
#             else:
#                 print('Nenhum débito automático cadastrado para este cliente.')
#         else:
#             print('Nenhum débito automático cadastrado para este cliente.')
#     else:
#         print('CPF ou senha incorretos.')

def savings_debit():
    # Função para debitar um valor da conta do cliente
    cpf = input('Digite o CPF do cliente: ')
    password = input('Digite a senha do cliente: ')
    value = input('Digite o valor a ser debitado: ')

    if not cpf or not password or not value:
        print('Dados inválidos. Preencha todos os campos.')
        return
    # Verifica se o cliente existe e se a senha está correta
    if cpf in data and data[cpf]['password'] == password:
        try:
            value = float(value)
        except ValueError:
            print('Valor inválido. Digite um número.')
            return

        account_type = data[cpf]['account_type']
        saving = data[cpf]['saving']

        if account_type == 'comum':
            if saving - value >= -1000:
                data[cpf]['saving'] -= value
                fee = value * 0.05
                data[cpf]['saving'] -= fee
                add_transaction(cpf, -value, 'Débito Poupança', fee)
                save_data(data)
                print('Débito realizado com sucesso!')
            else:
                print('Saldo insuficiente para realizar o débito.')
        elif account_type == 'plus':
            if saving - value >= -5000:
                data[cpf]['saving'] -= value
                fee = value * 0.03
                data[cpf]['saving'] -= fee
                add_transaction(cpf, -value, 'Débito Poupança', fee)
                save_data(data)
                print('Débito realizado com sucesso!')
            else:
                print('Saldo insuficiente para realizar o débito.')
    else:
        print('CPF ou senha incorretos.')

def savings_transfer():
    # Função para transferir um valor da conta do cliente para a conta corrente
    cpf_origin = input('Digite o CPF da conta de origem: ')
    password_origin = input('Digite a senha da conta de origem: ')
    cpf_destination = input('Digite o CPF da conta de destino: ')
    value = input('Digite o valor a ser transferido: ')

    if not cpf_origin or not password_origin or not cpf_destination or not value:
        print('Dados inválidos. Preencha todos os campos.')
        return

    if cpf_origin in data and data[cpf_origin]['password'] == password_origin and cpf_destination in data:
        try:
            value = float(value)
        except ValueError:
            print('Valor inválido. Digite um número.')
            return

        if data[cpf_origin]['saving'] >= value:
            data[cpf_origin]['saving'] -= value
            data[cpf_destination]['balance'] += value
            add_transaction(cpf_origin, -value, f'Transferido para {get_name(cpf_destination)}')
            add_transaction(cpf_destination, value, f'Transferência recebida de {get_name(cpf_origin)}')
            save_data(data)
            print('Transferência realizada com sucesso!')
        else:
            print('Saldo insuficiente para realizar a transferência.')
    else:
        print('CPF ou senha incorretos ou conta de destino não encontrada.')

def savings_deposit():
    # Função para depositar um valor na conta do cliente
    cpf = input('Digite o CPF do cliente: ')
    password = input('Digite a senha do cliente: ')
    value = input('Digite o valor a ser depositado: ')

    if not cpf or not password or not value:
        print('Dados inválidos. Preencha todos os campos.')
        return

    if cpf in data and data[cpf]['password'] == password:
        try:
            value = float(value)
        except ValueError:
            print('Valor inválido. Digite um número.')
            return

        data[cpf]['saving'] += value
        add_transaction(cpf, value, 'Depósito Poupança')
        save_data(data)
        print('Depósito realizado com sucesso!')
    else:
        print('CPF ou senha incorretos.')

def advance_bank_time():
    # Função para avançar o tempo do banco
    days = input('Digite quantos dias deseja avançar: ')

    if not days:
        print('Dados inválidos. Preencha todos os campos.')
        return

    try:
        days = int(days)
    except ValueError:
        print('Valor inválido. Digite um número inteiro.')
        return

    if days > 0:
        for _ in range(days):
            for cpf in data:
                saving = data[cpf]['saving']
                if data[cpf]['account_type'] == 'plus':
                    value = saving * 0.00004
                    data[cpf]['saving'] *= 1.00004
                    add_transaction(cpf, value, f'Rendimento diário da poupança') 
                elif data[cpf]['account_type'] == 'comum':
                    value = saving * 0.00002
                    data[cpf]['saving'] *= 1.00002 
                    add_transaction(cpf, value, f'Rendimento diário da poupança')                 
        save_data(data)
        print(f'Tempo avançado em {days} dias.')
    else:
        print('Valor inválido. Digite um número inteiro positivo.')

# def automatic_debits_menu():
#     # Menu de débitos automáticos
#     while True:
#         clear_screen()
#         print('=== Menu de Débitos Automáticos ===')
#         print('1. Cadastrar débito automático')
#         print('2. Listar débitos automáticos')
#         print('3. Excluir débito automático')
#         print('0. Voltar')

#         option = input('Selecione uma opção: ')

#         if option == '1':
#             register_automatic_debit()
#         elif option == '2':
#             list_automatic_debits()
#         elif option == '3':
#             delete_automatic_debit()
#         elif option == '0':
#             break
#         else:
#             print('Opção inválida. Tente novamente.')

#         input('Pressione Enter para continuar...')

def saving_menu():
    # Menu da poupança
    while True:
        clear_screen()
        print('=== Menu da Poupança ===')
        print('1. Depositar')
        print('2. Débito')
        print('3. Transferir')
        print('0. Voltar')

        option = input('Selecione uma opção: ')

        if option == '1':
            savings_deposit()
        elif option == '2':
            savings_debit()
        elif option == '3':
            savings_transfer()
        elif option == '0':
            break
        else:
            print('Opção inválida. Tente novamente.')

        input('Pressione Enter para continuar...')
 
# Menu principal
while True:
    clear_screen()
    print('=== Banco Quem Poupa Tem ===')
    print('1. Novo cliente')
    print('2. Apaga cliente')
    print('3. Listar clientes')
    print('4. Débito')
    print('5. Depósito')
    print('6. Extrato')
    print('7. Transferência entre contas')
    print('8. Operações da poupança')
    print('9. Tempo (Teste)')
    # print('10. Débitos Automáticos (Inativa)')
    print('0. Sair')

    option = input('Escolha uma opção: ')

    if option == '1':
        create_account()
    elif option == '2':
        delete_account()
    elif option == '3':
        list_accounts()
    elif option == '4':
        debit()
    elif option == '5':
        deposit()
    elif option == '6':
        statement()
    elif option == '7':
        transfer()
    elif option == '8':
        saving_menu()
    elif option == '9':
        advance_bank_time()
    # elif option == '10':
    #     automatic_debits_menu()
    elif option == '0':
        break
    else:
        print('Opção inválida. Escolha uma opção válida.')

    input('Pressione Enter para continuar...')

print('Obrigado por utilizar o Sistema de Banco!')