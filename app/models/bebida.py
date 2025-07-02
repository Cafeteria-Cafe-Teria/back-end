from abc import ABC, abstractmethod

class Bebida(ABC):
    @abstractmethod
    def get_descricao(self) -> str:
        pass

    @abstractmethod
    def get_custo(self) -> float:
        pass


class Cafe(Bebida):
    def get_descricao(self) -> str:
        return "Café"

    def get_custo(self) -> float:
        return 5.0


class Cha(Bebida):
    def get_descricao(self) -> str:
        return "Chá"

    def get_custo(self) -> float:
        return 4.0


class IngredienteDecorator(Bebida, ABC):
    def __init__(self, bebida: Bebida):
        self._bebida = bebida


class LeiteDeAveia(IngredienteDecorator):
    def get_descricao(self) -> str:
        return self._bebida.get_descricao() + " + Leite de Aveia"

    def get_custo(self) -> float:
        return self._bebida.get_custo() + 2.0


class Canela(IngredienteDecorator):
    def get_descricao(self) -> str:
        return self._bebida.get_descricao() + " + Canela"

    def get_custo(self) -> float:
        return self._bebida.get_custo() + 1.0


class SemAcucar(IngredienteDecorator):
    def get_descricao(self) -> str:
        return self._bebida.get_descricao() + " + Sem Açúcar"

    def get_custo(self) -> float:
        return self._bebida.get_custo()


class BebidaFactory:
    @staticmethod
    def criar_bebida(tipo: str) -> Bebida:
        if tipo.lower() == "cafe":
            return Cafe()
        elif tipo.lower() == "cha":
            return Cha()
        else:
            raise ValueError(f"Tipo de bebida desconhecido: {tipo}")
