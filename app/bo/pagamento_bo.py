from app.models.desconto import DescontoStrategy, DescontoFidelidade, DescontoPix, SemDesconto

class PagamentoBO:

    @staticmethod
    def calcular_valor_final(valor: float, metodo: str) -> float:
        if metodo == "fidelidade":
            strategy: DescontoStrategy = DescontoFidelidade()
        elif metodo == "pix":
            strategy: DescontoStrategy = DescontoPix()
        else:
            strategy: DescontoStrategy = SemDesconto()

        return strategy.aplicar_desconto(valor)
