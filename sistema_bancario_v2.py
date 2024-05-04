
def menu():

    menu = """

    [D] Depositar
    [S] Sacar
    [E] Extrato
    [N] Nova conta
    [U] Novo Usuário
    [C] Contas Cadastradas
    [Q] Sair
     -->  """
    return input(menu)

def depositar(saldo, valor, extrato,/):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f} realizado!\n"
    else:
        print("Falha na Operação! Valor inválido.") 
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    
    if valor > saldo:
        print("Falha na Operação! Saldo insuficiente.")

    elif valor > limite:
        print("Falha na Operação! O valor excede o limite da conta.")

    elif numero_saques >= limite_saques:
        print("Falha na Operação! Máximo de saques diário atingido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque de R$ {valor:.2f} realizado!\n"
        numero_saques += 1

    else:
        print("Falha na Operação! Valor inválido.")

    return saldo, extrato

def extrato(saldo, /, *extrato):
    print("EXTRATO".center(40,"-"))
    print("Sem Movimentações.\n" if not extrato else extrato)
    print(f"Saldo: R$ {saldo:.2f}")
    print("-" * 40)

def cria_usuario(clientes):
    cpf = input("CPF (somente número): ")
    usuario = filtrar_usuario(cpf, clientes)

    if usuario:
        print("\nCPF já cadastrado")
        return

    nome = input("Nome Completo: ")
    data_nascimento = input("Data de Nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (Logradouro, Nº - Bairro - Cidade/UF): ")

    clientes.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("Novo Cliente Cadastrado!")

def cria_conta(agencia, numero_conta, clientes):
    cpf = input("Informe o CPF do cliente: ")
    usuario = filtrar_usuario(cpf, clientes)

    if usuario:
        print("\nConta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}

    print("\nUsuário não encontrado!")
          
def lista_contas(contas):
    for conta in contas:
        contas_cadastradas = f"""\
            Agência:\n{conta['agencia']}
            C/C:\n{conta['numero_conta']}
            Titular:\n{conta['usuario']['nome']}
        """
        print("-" * 40)
        print(contas_cadastradas)

def filtrar_usuario(cpf, usuarios):
    usuarios_cadastrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_cadastrados[0] if usuarios_cadastrados else None 

def main():
    contas = []
    clientes = []
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    while True:

        opcao = menu().lower()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor de saque: "))
            saldo, extrato = sacar(saldo=saldo, valor=valor, extrato=extrato, limite=limite, numero_saques=numero_saques, limite_saques=LIMITE_SAQUES)

        elif opcao == "e":
            extrato(saldo, extrato=extrato)
        
        elif opcao == "u":
            cria_usuario(clientes)

        elif opcao == "n":
            numero_conta = len(clientes) + 1
            conta = cria_conta(AGENCIA, numero_conta, clientes)
            if conta:
                contas.append(conta)

        elif opcao == "c":
            lista_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, tente novamente.")

main()