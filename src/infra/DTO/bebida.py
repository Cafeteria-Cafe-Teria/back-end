from pydantic import BaseModel
from typing import List, Optional

from ...core.pedidos import Pedido

from ...core.bebidas import Bebida, Cafe, Cha
from ...core.adicionais import Adicional, LeiteDeAveia, Canela, SemAcucar
from .adicional import AdicionalEnum, AdicionalDTO
from enum import Enum

class BebidaEnum(str,Enum):   
    cafe = "Café"
    cha = "Chá"

class BebidaDTO(BaseModel):
    id : Optional[int] = None
    tipo : BebidaEnum
    adicionais : List[AdicionalEnum]

    @staticmethod
    def para_enum(bebida : Bebida):
        return {
            Cafe : BebidaEnum.cafe,
            Cha : BebidaEnum.cha
        }[type(bebida)]

    @staticmethod
    def de_enum(bebida : BebidaEnum):
        return {
            BebidaEnum.cafe : Cafe,
            BebidaEnum.cha : Cha
        }[bebida]


    @classmethod
    def de_item(cls, item : Pedido.Item):
        
        adicionais = []

        bebida = item.bebida

        while isinstance(bebida, Adicional):
            adicionais.append( AdicionalDTO.para_enum(bebida) )
            bebida = bebida.pegar_base()
        
        return cls( id = item.id, tipo = cls.para_enum(bebida), adicionais= adicionais)


    def para_item(self) -> Pedido.Item:
        base = self.de_enum(self.tipo)()

        for adicional in self.adicionais:
            base = AdicionalDTO.de_enum( adicional )(base)

        return Pedido.Item(self.id, base)
    
    def para_bebida(self) -> Bebida:
        return self.para_item().bebida

    def para_dict(self) -> dict:
        return {
            'id' : self.id,
            'tipo' : self.tipo.value,
            'adicionais' : [adicional.value for adicional in self.adicionais]
        }
