from app.models.pedido import Pedido

class PedidoDAO:
    _pedidos = []

    @classmethod
    def salvar(cls, pedido: Pedido):
        cls._pedidos.append(pedido)

    @classmethod
    def listar_todos(cls):
        return cls._pedidos

    @classmethod
    def excluir(cls, pedido: Pedido):
        cls._pedidos.remove(pedido)
