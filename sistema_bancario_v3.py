from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print("\nVocê excedeu o número de transações permitidas para hoje!")
        
            transacao.registrar(conta)
       

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nasc, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nasc = data_nasc

class Conta:
    def __init__(self, numero_conta, cliente):
        self._saldo = 0
        self._numero_conta = numero_conta
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def nova_conta(cls, cliente, numero_conta):
        return cls(numero_conta, cliente)
    
    @property
    def numero(self):
        return self._numero_conta
    
    @property
    def agencia(self):
        return self._agencia   
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        if valor > saldo:
            print("Falha na Operação! Saldo insuficiente.")

        elif valor > 0:
            self._saldo -= valor
            print (f"Saque de R$ {valor:.2f} realizado!\n")
            return True

        else:
            print("Falha na Operação! Valor inválido.")

        return False 
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print (f"Depósito: R$ {valor:.2f} realizado!\n")
        
        else:
            print("Falha na Operação! Valor inválido.") 
            return False
        
        return True
       
class ContaCorrente(Conta):
    def __init__(self, numero_conta, cliente, limite=500, limite_saques=3):
        super().__init__(numero_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    @classmethod
    def nova_conta(cls, cliente, numero_conta, limite, limite_saques):
        return cls(numero_conta, cliente, limite, limite_saques)

    def sacar(self, valor):
        nro_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"]== "Saque"])
    
        if valor > self.limite:
            print("Falha na Operação! Limite Insuficiente")

        elif nro_saques >= self.limite_saques:
            print("Falha na Operação! Número de saques permitido foi excedido!")
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            Agência: {self.agencia}\n
            Contas Cadastradas: {self.numero_conta}\n
            Titular: {self.cliente.nome}\n
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {"tipo": transacao.__class__.__name__, 
            "valor:": transacao.valor,
            "data": datetime.now()}
        )

    def gerar_relatorio(self, tipo_transacao=None):
        for transacao in self._transacoes:
            if (tipo_transacao is None or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        data_atual = datetime.now().date()
        transacoes = []

        for transacao in self._transacoes:
            data_transacao = datetime.strptime(transacao, "%d-%m-%Y %H:%M:%S")
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        transacao_efetuada = conta.sacar(self.valor)
        if transacao_efetuada:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class ContasIterador:
    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1

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

def filtrar_cliente(cpf, clientes):
    clientes_cadastrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_cadastrados[0] if clientes_cadastrados else None 

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Conta Inexistente!")
        return

    return cliente.contas[0]

def depositar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def sacar(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    valor = float(input("Valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

def exibir_extrato(clientes):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    if not tem_transacao:
        extrato = "Não foram realizadas movimentações"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("=" * 30)

def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe cliente com esse CPF!")
        return

    nome = input("Informe o nome completo: ")
    data_nasc = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, nro - bairro - cidade/UF): "
    )

    cliente = PessoaFisica(
        nome=nome, data_nasc=data_nasc, cpf=cpf, endereco=endereco
    )

    clientes.append(cliente)

    print("\nCliente criado com sucesso!")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não encontrado!")
        return

    conta = ContaCorrente.nova_conta(
        cliente=cliente, numero_conta=numero_conta, limite=500, limite_saques=50
    )
    contas.append(conta)
    cliente.contas.append(conta)

    print("\nConta criada com sucesso!")

def listar_contas(contas):
    for conta in ContasIterador(contas):
        print("=" * 100)
        print(str(conta))

def main():
    contas = []
    clientes = []
    
    while True:
        opcao = menu().lower()

        if opcao == "d":
            depositar(clientes)
            
        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
           exibir_extrato(clientes)

        elif opcao == "u":
            criar_cliente(clientes)

        elif opcao == "n":
           numero_conta = len(contas) + 1
           criar_conta(numero_conta, clientes, contas)

        elif opcao == "c":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, tente novamente.")
main()