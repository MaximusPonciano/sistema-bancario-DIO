from abc import ABC, abstractmethod

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_de_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, numero, cliente):
        self.__saldo = 0
        self.__numero = numero
        self.__agencia = 1004
        self.__cliente = cliente
        self.__historico = Historico()

    @classmethod
    def nova_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self.__saldo

    @property
    def numero(self):
        return self.__numero

    @property
    def agencia(self):
        return self.__agencia

    @property
    def cliente(self):
        return self.__cliente

    @property
    def historico(self):
        return self.__historico

    def sacar(self, valor):
        if valor > self.__saldo:
            print("Saldo insuficiente")
            return False

        if valor <= 0:
            print("Valor inválido")
            return False

        self.__saldo -= valor
        print("Saque realizado")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("O depósito deve ser maior que zero")
            return False

        self.__saldo += valor
        print("Depósito realizado")
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_de_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_de_saques = limite_de_saques

    def sacar(self, valor):

        numero_saques = len([
            transacao for transacao in self.historico.transacoes
            if isinstance(transacao, Saque)
        ])

        if numero_saques >= self.limite_de_saques:
            print("Limite de saques atingido!")
            return False

        return super().sacar(valor)

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
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)

if __name__ == "__main__":
    cliente = PessoaFisica(
        cpf="12345678900",
        nome="João",
        data_de_nascimento="01/01/2000",
        endereco="Rua XPTO"
    )

    conta = ContaCorrente(numero=1, cliente=cliente)
    cliente.adicionar_conta(conta)

    print("\n--- TESTANDO ---")

    cliente.realizar_transacao(conta, Deposito(1000))
    cliente.realizar_transacao(conta, Saque(100))
    cliente.realizar_transacao(conta, Saque(200))
    cliente.realizar_transacao(conta, Saque(50))
    cliente.realizar_transacao(conta, Saque(10))  
