from .state_pedido import Recebido, EstadoPedido
from .observer import Observer
from .bebida import Bebida

class Pedido:
    def __init__(self, bebida: Bebida):
        self.bebida = bebida
        self.observadores = []
        self.estado: EstadoPedido = Recebido()

    def adicionar_observador(self, obs: Observer):
        self.observadores.append(obs)

    def notificar_observadores(self):
        msg = f"Pedido '{self.bebida.get_descricao()}' está no estado: {self.estado}"
        for obs in self.observadores:
            obs.atualizar(msg)

    def avancar_estado(self):
        self.estado.proximo_estado(self)
        self.notificar_observadores()

    def set_estado(self, novo_estado: EstadoPedido):
        self.estado = novo_estado
