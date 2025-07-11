from enum import Enum
from ...core.tipos_de_pagamento import Pix, Cartao, CartaoFidelidade

class MetodoDePagamentoEnum(str, Enum):
    pix = "Pix"
    cartao = "Cartão"
    cartao_fidelidade = "Cartão Fidelidade"

class MetodoDePagamentoDTO:
    metodo : MetodoDePagamentoEnum

    @staticmethod
    def para_tipo_de_pagamento(metodo : MetodoDePagamentoEnum):
        return {
            MetodoDePagamentoEnum.pix : Pix,
            MetodoDePagamentoEnum.cartao : Cartao,
            MetodoDePagamentoEnum.cartao_fidelidade : CartaoFidelidade
        }[metodo]


