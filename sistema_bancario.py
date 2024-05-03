menu = """

[D] Depositar
[S] Sacar
[E] Extrato
[Q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d" or "D":
        deposito = float(input("Informe o valor do depósito: "))

        if deposito > 0:
            saldo += deposito
            extrato += f"Depósito: R$ {deposito:.2f}\n"

        else:
            print("Falha na Operação! Valor inválido.")

    elif opcao == "s" or "S":
        saque = float(input("Informe o valor de saque: "))

        if saque > saldo:
            print("Falha na Operação! Saldo insuficiente.")

        elif saque > limite:
            print("Falha na Operação! O valor excede o limite da conta.")

        elif numero_saques >= LIMITE_SAQUES:
            print("Falha na Operação! Máximo de saques diários atingido.")

        elif saque > 0:
            saldo -= saque
            extrato += f"Saque: R$ {saque:.2f}\n"
            numero_saques += 1

        else:
            print("Falha na Operação! Valor inválido.")

    elif opcao == "e" or "E":
        print("EXTRATO".center(40,"-"))
        print("Sem Movimentações.\n" if not extrato else extrato)
        print(f"Saldo: R$ {saldo:.2f}")
        print("-" * 40)

    elif opcao == "q" or "Q":
        break

    else:
        print("Operação inválida, tente novamente.")