from abc import ABC, abstractmethod
from ..pedidos import Pedido
from uuid import UUID

class EspecificacaoPedido(ABC):
    @abstractmethod
    def condicao(self, pedido : Pedido) -> bool:
        pass

class TipoDePedidoEspecificacao(EspecificacaoPedido):
    def __init__(self, tipo_de_pedido : type):
        self.__tipo = tipo_de_pedido

    def condicao(self, pedido : Pedido):
        return pedido is self.__tipo

class PedidoDAO(ABC):
    @abstractmethod
    def pegar_todos(self) -> list[Pedido]:
        pass

    @abstractmethod
    def pegar(self, uuid : UUID) -> Pedido | None:
        pass

    @abstractmethod
    def salvar(self, pedido : Pedido) -> bool:
        pass

    def pegar_por_especificacao(self, especificacao : EspecificacaoPedido) -> list[Pedido]:
        return [  pedido for pedido in self.pegar_todos() if especificacao.condicao(pedido) ]

    @abstractmethod
    def remover(self, pedido : Pedido):
        pass
