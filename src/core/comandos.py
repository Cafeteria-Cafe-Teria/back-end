from abc import ABC, abstractmethod
from uuid import UUID

from .tipos_de_pagamento import TipoDePagamento
from .pedidos import Pedido
from .bebidas import Bebida
from .pedidos import PedidoEmRealizacao, PedidoEmPreparo, PedidoEntregue, PedidoPronto, PedidoRecebido, PedidoCancelado
from typing import Any, Generic, List, TypeVar
from .DAO.pedido_dao import PedidoDAO


T = TypeVar('T')

class Comando(ABC, Generic[T]):
    @abstractmethod
    def executar(self) -> T:
        pass

class CriarPedidoComando(Comando[Pedido]):

    def __init__(self, pedido_dao : PedidoDAO):
        
        self.___pedido_dao = pedido_dao

    def executar(self) -> Pedido:
        pedido = PedidoEmRealizacao("")

        self.___pedido_dao.salvar(pedido)

        return pedido

class CancelarPedidoComando(Comando[str | None]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID):
        self.__uuid = uuid 
        self.___pedido_dao = pedido_dao

    def executar(self) -> str | None:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        remover_de_persistencia = isinstance(pedido, PedidoEmRealizacao)

        try:
            pedido.para_cancelado()
        except Exception:
            return f"Impossivel cancelar pedido de status {pedido.__class__.__name__}"

        if remover_de_persistencia:
            self.___pedido_dao.remover(pedido)
        else:
            pedido = pedido.para_cancelado()
            self.___pedido_dao.salvar(pedido)
            pedido.notificar()

        return None

class AdicionarBebidaComando(Comando[str | Pedido.Item]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID, bebida : Bebida):
        self.__uuid = uuid 
        self.___pedido_dao = pedido_dao
        self.__bebida = bebida

    def executar(self) -> str | Pedido.Item:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        try:
            pedido.adicionar(self.__bebida)
        except Exception:
            return f"Impossivel adicionar bebida em pedido de status {pedido.__class__.__name__}"

        self.___pedido_dao.salvar(pedido)

        return pedido.itens[-1] 
 
class RemoverBebidaComando(Comando[str | None]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID, id_bebida : int):
        self.__uuid = uuid 
        self.___pedido_dao = pedido_dao
        self.__id_bebida = id_bebida

    def executar(self) -> str | None:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        if not pedido.remover(self.__id_bebida):
            return f"Impossivel remover bebida {self.__id_bebida} bebida em do pedido {pedido.uuid}"

        self.___pedido_dao.salvar(pedido)

        return None
  
class GerarNotaDePedidoComando(Comando[dict[str, Any] | str]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID):
        self.__uuid = uuid 
        self.___pedido_dao = pedido_dao

    def executar(self) -> str | dict[str, Any]:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        return pedido.gerar_nota()
 
class DefinirNomeDoClienteComando(Comando [ str | None]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID, nome_cliente : str):
        self.__uuid = uuid
        self.___pedido_dao = pedido_dao
        self.___nome = nome_cliente

    def executar(self) -> str | None:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        pedido.nome_cliente = self.___nome

        self.___pedido_dao.salvar(pedido)
        
        return None

class DefinirNomeDoClienteComando(Comando [ str | None]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID, nome_cliente : str):
        self.__uuid = uuid
        self.___pedido_dao = pedido_dao
        self.___nome = nome_cliente

    def executar(self) -> str | None:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        pedido.nome_cliente = self.___nome

        self.___pedido_dao.salvar(pedido)
        
        return None

class EnviarPedidoComando(Comando[str | None]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID):
        self.__uuid = uuid
        self.___pedido_dao = pedido_dao

    async def executar(self) -> str | None:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        try:
            pedido = pedido.para_recebido()        
        except Exception:
            return f"Impossivel passar {pedido.__class__.__name__} para status recebido"

        self.___pedido_dao.salvar(pedido)

        await pedido.notificar()

        return None


class SimularNotaComPagamentoComando(Comando[dict[str, Any] | str]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID, tipo_de_pagamento : type[TipoDePagamento]):
        self.__uuid = uuid
        self.___pedido_dao = pedido_dao
        self.__tipo_de_pagamento = tipo_de_pagamento

    def executar(self) -> str | dict[str, Any]:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"
        
        return self.__tipo_de_pagamento(pedido).gerar_nota()
   
class PegarTodosOsPedidosComando(Comando[List[Pedido]]):
    def __init__(self, pedido_dao : PedidoDAO):
        self.___pedido_dao = pedido_dao

    def executar(self) -> List[Pedido]:
        return self.___pedido_dao.pegar_todos()
    
class MudarStatusDePagamentoComando(Comando[None | str]):
    def __init__(self, pedido_dao : PedidoDAO, uuid : UUID, proximo_status : type[Pedido]):
        self.__uuid = uuid
        self.___pedido_dao = pedido_dao
        self.__proximo_status = proximo_status

    async def executar(self) -> str | None:
        pedido = self.___pedido_dao.pegar(self.__uuid)

        if pedido is None:
            return f"Pedido {self.__uuid} não encontrado"

        try:        

            if self.__proximo_status == PedidoEmRealizacao:
                pedido = pedido.para_em_realizacao()
            if self.__proximo_status ==  PedidoEmPreparo: 
                pedido = pedido.para_em_preparo()
            if self.__proximo_status == PedidoEntregue: 
                pedido = pedido.para_entregue()
            if self.__proximo_status == PedidoPronto: 
                pedido = pedido.para_pronto()
            if self.__proximo_status == PedidoRecebido: 
                pedido = pedido.para_recebido()
            if self.__proximo_status == PedidoCancelado:
                pedido = pedido.para_cancelado()

        except Exception:
            return f"{pedido.__class__.__name__} não pode ser trocado de status para {self.__proximo_status.__name__}"

        self.___pedido_dao.salvar(pedido)
        await pedido.notificar()

        return None 