from abc import ABC, abstractmethod
from .pedido import Pedido

class Comando(ABC):
    @abstractmethod
    def executar(self):
        pass


class FazerPedido(Comando):
    def __init__(self, pedido: Pedido):
        self.pedido = pedido

    def executar(self):
        print(f"Pedido realizado: {self.pedido.bebida.get_descricao()} - R${self.pedido.bebida.get_custo():.2f}")
        self.pedido.notificar_observadores()
