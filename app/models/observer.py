from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def atualizar(self, mensagem: str):
        pass


class Cozinha(Observer):
    def atualizar(self, mensagem: str):
        print(f"[Cozinha] {mensagem}")


class Cliente(Observer):
    def __init__(self, nome: str):
        self.nome = nome

    def atualizar(self, mensagem: str):
        print(f"[Cliente {self.nome}] {mensagem}")
