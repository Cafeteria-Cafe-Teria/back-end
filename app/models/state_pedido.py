from abc import ABC, abstractmethod

class EstadoPedido(ABC):
    @abstractmethod
    def proximo_estado(self, pedido):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Recebido(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.set_estado(EmPreparo())

    def __str__(self):
        return "Recebido"


class EmPreparo(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.set_estado(Pronto())

    def __str__(self):
        return "Em Preparo"


class Pronto(EstadoPedido):
    def proximo_estado(self, pedido):
        pedido.set_estado(Entregue())

    def __str__(self):
        return "Pronto"


class Entregue(EstadoPedido):
    def proximo_estado(self, pedido):
        print("Pedido já foi entregue!")

    def __str__(self):
        return "Entregue"
