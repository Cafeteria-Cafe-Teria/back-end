from app.dao.pedido_dao import PedidoDAO
from app.models.pedido import Pedido
from app.models.observer import Cozinha, Cliente
from app.models.commands import FazerPedido

class PedidoBO:

    @staticmethod
    def criar_pedido(bebida, nome_cliente: str) -> Pedido:
        pedido = Pedido(bebida)

        cozinha = Cozinha()
        cliente_obs = Cliente(nome_cliente)

        pedido.adicionar_observador(cozinha)
        pedido.adicionar_observador(cliente_obs)

        PedidoDAO.salvar(pedido)

        comando = FazerPedido(pedido)
        comando.executar()

        return pedido

    @staticmethod
    def avancar_status(pedido: Pedido):
        pedido.avancar_estado()
