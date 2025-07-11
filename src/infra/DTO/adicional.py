from pydantic import BaseModel
from enum import Enum
from typing import List

from ...core.adicionais import Adicional, LeiteDeAveia, Canela, SemAcucar


class AdicionalEnum(str,Enum):
    leite_de_aveia = "Leite de Aveia"
    canela = "Canela"
    sem_acucar = "Sem Açucar"

class AdicionalDTO(BaseModel):
    id : AdicionalEnum

    @staticmethod
    def para_enum(adicional : Adicional) ->AdicionalEnum:
        return {
            LeiteDeAveia : AdicionalEnum.leite_de_aveia,
            Canela: AdicionalEnum.canela,
            SemAcucar : AdicionalEnum.sem_acucar,
        }[type(adicional)]

    def de_enum(adicional : AdicionalEnum) -> Adicional:
        return {
            AdicionalEnum.leite_de_aveia : LeiteDeAveia,
            AdicionalEnum.canela : Canela,
            AdicionalEnum.sem_acucar : SemAcucar,
        }[adicional]

