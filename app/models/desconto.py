from abc import ABC, abstractmethod

class DescontoStrategy(ABC):
    @abstractmethod
    def aplicar_desconto(self, valor: float) -> float:
        pass


class DescontoFidelidade(DescontoStrategy):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.9


class DescontoPix(DescontoStrategy):
    def aplicar_desconto(self, valor: float) -> float:
        return valor * 0.95


class SemDesconto(DescontoStrategy):
    def aplicar_desconto(self, valor: float) -> float:
        return valor
