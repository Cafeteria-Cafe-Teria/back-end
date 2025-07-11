from pydantic import BaseModel
from typing import List, Self, Tuple
from .bebida import BebidaDTO
from ...core.pedidos import Pedido, PedidoEmPreparo, PedidoCancelado, PedidoEntregue, PedidoRecebido, PedidoPronto, PedidoEmRealizacao
from uuid import UUID
from enum import Enum

class StatusDePedidoEnum(str, Enum):
    entregue = "Entregue"
    cancelado = "Cancelado"
    pronto = "Pronto"
    em_preparo = "Em prepearo"
    recebido = "Recebido"
    em_realizacao = "Em realização"    

class PedidoDTO(BaseModel):
    bebidas : List[ BebidaDTO ]
    uuid : UUID
    nome_do_cliente : str
    status : StatusDePedidoEnum

    @staticmethod
    def para_enum(pedido: Pedido):
        return {
            PedidoEmPreparo : StatusDePedidoEnum.em_preparo,
            PedidoCancelado: StatusDePedidoEnum.cancelado,
            PedidoEmRealizacao : StatusDePedidoEnum.em_realizacao,
            PedidoEntregue : StatusDePedidoEnum.entregue,
            PedidoRecebido : StatusDePedidoEnum.recebido,
            PedidoPronto : StatusDePedidoEnum.pronto
        }[type(pedido)]

    @staticmethod
    def de_enum(pedido: StatusDePedidoEnum):
        return {
            StatusDePedidoEnum.em_preparo : PedidoEmPreparo,
            StatusDePedidoEnum.cancelado : PedidoCancelado,
            StatusDePedidoEnum.em_realizacao : PedidoEmRealizacao ,
            StatusDePedidoEnum.entregue : PedidoEntregue ,
            StatusDePedidoEnum.recebido : PedidoRecebido ,
            StatusDePedidoEnum.pronto : PedidoPronto 
        }[pedido]



    @classmethod
    def de_pedido(cls, pedido : Pedido) -> Self:        
        # print(cls)
        bebidas = []

        for item in pedido.itens:
            bebidas.append(BebidaDTO.de_item(item))
        
        return cls(bebidas=bebidas, uuid= pedido.uuid, nome_do_cliente= pedido.nome_cliente, status = cls.para_enum(pedido))


    def para_dict(self) -> dict:
        return {
            'uuid' : self.uuid.__str__(),
            'nome_do_cliente' : self.nome_do_cliente,
            'status' : str(self.status),
            'bebidas' : [bebida.para_dict() for bebida in self.bebidas]
        }
