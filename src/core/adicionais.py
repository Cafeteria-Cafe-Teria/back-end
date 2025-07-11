from .bebidas import Bebida
from abc import ABC

class Adicional(Bebida, ABC):
    def __init__(self, nome : str, preco : float, base : Bebida):
        super().__init__(nome, preco)
        self.__base = base

    @property
    def nome(self) -> str:
        # print(super().__dict__)
        return f'{self.__base.nome}, {self._nome}' 

    @property
    def preco(self) -> float:
        return self._preco + self.__base.preco

    def pegar_base(self):
        return self.__base

    def gerar_nota(self):
        return self.__base.gerar_nota() + [{'nome' : self._nome, "preco" : self._preco}] 

class LeiteDeAveia(Adicional):
    def __init__(self, base: Bebida):
        super().__init__("com leite de aveia", 2.0 , base)
class Canela(Adicional):
    def __init__(self, base: Bebida):
        super().__init__("com canela", 0.5 , base)
class SemAcucar(Adicional):
    def __init__(self, base: Bebida):
        super().__init__("sem açucar", 0.0 , base)
