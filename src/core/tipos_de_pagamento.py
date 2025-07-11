from abc import ABC, abstractmethod
from .pedidos import Pedido

class TipoDePagamento(ABC):
    
    def __init__(self, pedido : Pedido):
        self.__pedido = pedido

    def gerar_nota(self):
        nota = self.__pedido.gerar_nota()        
        return nota
    
class TipoDePagamentoComDesconto(TipoDePagamento, ABC):    
    def __init__(self, pedido : Pedido, desconto : float): 
        if 1 < desconto or desconto < 0:
            raise Exception("O valor de desconto deve representar uma porcentagem, ou seja desconto <= 1 e desconto >=0")
        self.__desconto = desconto

        self.__pedido = pedido

        super().__init__(pedido)

    def gerar_nota(self):
        nota = self.__pedido.gerar_nota()
        nota["preco_final"] = nota["preco_total"] * (1- self.__desconto) 
        nota["desconto"] = self.__desconto

        return nota
 
class Pix(TipoDePagamentoComDesconto):
    def __init__(self, pedido : Pedido):
        super().__init__(pedido, 0.05)
class CartaoFidelidade(TipoDePagamentoComDesconto):
    def __init__(self, pedido : Pedido):
        super().__init__(pedido, 0.10)
class Cartao(TipoDePagamento):
    def __init__(self, pedido : Pedido):
        super().__init__(pedido)

# class CartaoDeDebito(TipoDePagamento):
#     def __init__(self, pedido : Pedido):
#         super().__init__(pedido)


