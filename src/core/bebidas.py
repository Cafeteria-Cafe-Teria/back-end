from abc import ABC, abstractmethod

class Bebida(ABC):
    def __init__(self, nome : str, preco : float):
        self._nome = nome
        self._preco = preco

    @property
    def nome(self) -> str:
        return self._nome

    @property
    def preco(self) -> float:
        return self._preco

    def gerar_nota(self):
        return [{'nome' : self._nome, "preco" : self.preco}]
    
class Cafe(Bebida):
    def __init__(self):
        super().__init__("Café", 5.0)

class Cha(Bebida):
    def __init__(self):
        super().__init__("Chá", 4.0)
 

class BebidaFabrica(ABC):
    @abstractmethod    
    def criar(self) -> Bebida:
        pass
class CafeFabrica(BebidaFabrica):
    def criar(self):
        return Cafe()
class ChaFabrica(BebidaFabrica):
    def criar(self):
        return Cha()
