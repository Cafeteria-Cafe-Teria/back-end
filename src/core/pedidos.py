from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Self
from dataclasses import dataclass
from uuid import UUID, uuid4
from .bebidas import Bebida
from ..utils.singleton import SingletonMeta
from .bebidas import Bebida

class Observer(ABC):
    @abstractmethod
    async def atualizar(self, data : Pedido):
        pass

class ObserverHub(metaclass = SingletonMeta):
    def __init__(self):
        self.__observers  : list[Observer]= []

    def registrar(self, observer : Observer):
        self.__observers.append(observer)

    def remover(self, observer : Observer):
        self.__observers.remove(observer)

    async def notificar(self, data : Pedido):
        for observer in self.__observers:
            await observer.atualizar(data) 

class Pedido(ABC):      
    @dataclass
    class Item:
       id : int
       bebida : Bebida

    def __init__(self,  nome_cliente : str, bebidas : list[Bebida] = []):
        self.__itens = [ self.Item(id, bebida) for id, bebida in enumerate(bebidas) ]    
        self.__cont = len(bebidas)
        self.__uuid = uuid4()
        self.__nome_cliente = nome_cliente

        self.__hub = ObserverHub()

    @classmethod
    def de_lista_de_itens(cls,  nome_cliente : str, itens : list[Item] = [] ,uuid : UUID = uuid4()):
        instance = cls.__new__(cls)
        instance.__itens = itens    
        instance.__cont = max( [item.id for item in itens] + [-1] ) + 1
        instance.__uuid = uuid
        instance.__nome_cliente = nome_cliente

        instance.__hub = ObserverHub()

        return instance

    async def notificar(self):
        await self.__hub.notificar(self)

    @property
    def nome_cliente(self):
        return self.__nome_cliente
    @property
    def uuid(self):
        return self.__uuid
    @property
    def bebidas(self):
        return [ item.bebida for item in self.__itens ]
    @property
    def itens(self):
        return self.__itens

    @nome_cliente.setter
    def nome_cliente(self, valor : str):
        self.__nome_cliente = valor

    def adicionar(self, bebida : Bebida) -> int:
        id = self.__cont

        self.__itens.append(self.Item(id, bebida))
        self.__cont += 1

        return id

    def remover(self, id: int) -> bool:
        to_remove = [i for i in self.__itens if i.id == id]

        if len(to_remove) == 0:
            return False
    
        self.__itens.remove(to_remove[0])
        return True

    def tamanho(self) -> int:
        return len(self.__itens)

    def gerar_nota(self):
        bebidas = dict( (item.id , item.bebida.gerar_nota() ) for item in self.__itens )

        return {
            "id" : self.uuid,
            "nome_cliente" : self.nome_cliente,
            "bebidas" : bebidas,
            "preco_total" : sum([elemento["preco"] for bebida in bebidas.values() for elemento in bebida ])
        }

    @classmethod
    def _de_outro_pedido(cls, pedido : Self) -> Self:
        instancia = cls.de_lista_de_itens(pedido.nome_cliente, pedido.itens, pedido.uuid)

        return instancia

    def para_em_realizacao(self) -> Self:
        raise Exception(f'{self.__class__.__name__} não suporta transição para PedidoEmRealizacao')
    def para_recebido(self) -> Self:
        raise Exception(f'{self.__class__.__name__} não suporta transição para PedidoRecebido')
    def para_em_preparo(self) -> Self:        
        raise Exception(f'{self.__class__.__name__} não suporta transição para PedidoEmPreparo')
    def para_pronto(self) -> Self:
        raise Exception(f'{self.__class__.__name__} não suporta transição para PedidoPronto')
    def para_entregue(self) -> Self:
        raise Exception(f'{self.__class__.__name__} não suporta transição para PedidoEntregue')
    def para_cancelado(self) -> Self:
        raise Exception(f'{self.__class__.__name__} não suporta transição para PedidoCancelado')

    def registrar_hub(self, hub : ObserverHub):
        self.__hub = hub

class PedidoConstante(Pedido, ABC):
    def __init__(self, nome_cliente, bebidas = []):
        super().__init__(nome_cliente, bebidas)

    def adicionar(self, bebida):
        raise Exception(f"{self.__class__.__name__} não permite a adição de novas bebidas")
    def remover(self, id):
        raise Exception(f"{self.__class__.__name__} não permite a remoção de bebidas")

class PedidoEntregue(PedidoConstante):
    def __init__(self, nome_cliente, bebidas=[]):
        super().__init__(nome_cliente, bebidas)

class PedidoCancelado(PedidoConstante):
    def __init__(self, nome_cliente, bebidas=[]):
        super().__init__(nome_cliente, bebidas)

class PedidoPronto(PedidoConstante):
    def __init__(self, nome_cliente, bebidas=[]):
        super().__init__(nome_cliente, bebidas)

    def para_entregue(self):
        return PedidoEntregue._de_outro_pedido(self)

    def para_cancelado(self):
        return  PedidoCancelado._de_outro_pedido(self)

class PedidoEmPreparo(PedidoConstante):
    def __init__(self, nome_cliente, bebidas=[]):
        super().__init__(nome_cliente, bebidas)

    def para_pronto(self):
        return PedidoPronto._de_outro_pedido(self)
    def para_cancelado(self):
        return  PedidoCancelado._de_outro_pedido(self)

class PedidoRecebido(PedidoConstante):
    def __init__(self, nome_cliente, bebidas=[]):
        super().__init__(nome_cliente, bebidas)

    def para_em_preparo(self):
        return PedidoEmPreparo._de_outro_pedido(self)
    def para_cancelado(self):
        return  PedidoCancelado._de_outro_pedido(self)
    
class PedidoEmRealizacao(Pedido):
    def __init__(self, nome_cliente, bebidas = []):
        super().__init__(nome_cliente, bebidas)

    def para_recebido(self):
        return PedidoRecebido._de_outro_pedido(self)
    def para_cancelado(self):
        return  PedidoCancelado._de_outro_pedido(self)
 