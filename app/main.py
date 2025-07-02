from app.models.bebida import BebidaFactory, LeiteDeAveia, Canela, SemAcucar
from app.bo.pedido_bo import PedidoBO
from app.bo.pagamento_bo import PagamentoBO
from app.dao.pedido_dao import PedidoDAO


def main():
    print("=== Cafeteria ===")

    nome_cliente = "João"

    # Criação e personalização da bebida
    bebida = BebidaFactory.criar_bebida("cafe")
    bebida = LeiteDeAveia(bebida)
    bebida = Canela(bebida)
    bebida = SemAcucar(bebida)

    print(f"\nBebida escolhida: {bebida.get_descricao()} - R${bebida.get_custo():.2f}")

    # Criar pedido
    pedido = PedidoBO.criar_pedido(bebida, nome_cliente)

    # Avançar status do pedido
    print("\n--- Atualizando status do pedido ---")
    PedidoBO.avancar_status(pedido)
    PedidoBO.avancar_status(pedido)
    PedidoBO.avancar_status(pedido)

    # Pagamento
    print("\n--- Pagamento ---")
    valor_total = bebida.get_custo()
    metodo_pagamento = "fidelidade"  # Pode ser "fidelidade", "pix" ou outro (cartão)

    valor_final = PagamentoBO.calcular_valor_final(valor_total, metodo_pagamento)
    print(f"Valor total: R${valor_total:.2f}")
    print(f"Valor final com desconto ({metodo_pagamento}): R${valor_final:.2f}")

    # Listar pedidos
    print("\n--- Pedidos registrados ---")
    for p in PedidoDAO.listar_todos():
        print(f"- {p.bebida.get_descricao()} | Status: {p.estado}")


if __name__ == "__main__":
    main()
