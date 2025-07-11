from fastapi import APIRouter, HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect, WebSocketState
from uuid import UUID
from typing import Any, List
from .DTO.bebida import BebidaDTO
from .DTO.metodo_de_pagamento import MetodoDePagamentoEnum, MetodoDePagamentoDTO
from .DTO.pedido import StatusDePedidoEnum, PedidoDTO
from ..core.comandos import AdicionarBebidaComando, CancelarPedidoComando, CriarPedidoComando, DefinirNomeDoClienteComando, EnviarPedidoComando, GerarNotaDePedidoComando, MudarStatusDePagamentoComando, PegarTodosOsPedidosComando, RemoverBebidaComando, SimularNotaComPagamentoComando
from .bd.pedido_sqlite_dao import PedidoDAOSqlite
from ..core.pedidos import Observer, Pedido, ObserverHub
import asyncio

import json

class ClienteObserver(Observer):
    def __init__(self, socket : WebSocket, uuid : UUID):
        self.__socket = socket
        self.__uuid = uuid

    async def atualizar(self, data:Pedido):
        if self.__uuid == data.uuid:
            try:
                await self.__socket.send_text( json.dumps( PedidoDTO.de_pedido(data).para_dict() ) )
            except WebSocketDisconnect:
                ObserverHub().remover(self)


def endpoints_cliente() -> APIRouter:
    router = APIRouter()

    @router.post("/cliente/pedido/")
    def criar_pedido() -> PedidoDTO:
        return  PedidoDTO.de_pedido( CriarPedidoComando(PedidoDAOSqlite()).executar() )        

    @router.delete("/cliente/pedido/{uuid}")
    def cancelar_pedido(uuid : UUID) -> str:
        log = CancelarPedidoComando(PedidoDAOSqlite(), uuid).executar()

        if log is None:
            return "Ok"
        
        raise HTTPException(status_code=400, detail=log)

    @router.post("/cliente/pedido/{uuid}/bebida")
    def adicionar_bebida_em_pedido( uuid : UUID, bebida : BebidaDTO) -> BebidaDTO:
        log_ou_item = AdicionarBebidaComando(PedidoDAOSqlite(), uuid, bebida.para_bebida()).executar()

        if type(log_ou_item) == Pedido.Item:
            return BebidaDTO.de_item(log_ou_item)
        
        raise HTTPException(status_code=400, detail=log_ou_item)

    @router.delete("/cliente/pedido/{uuid}/bebida/{id_bebida}")
    def remover_bebida_de_pedido( uuid : UUID, id_bebida : int ) -> str: 
        log = RemoverBebidaComando(PedidoDAOSqlite(), uuid, id_bebida).executar()

        if log is None:
            return "Ok"
        
        raise HTTPException(status_code=400, detail=log)
    
    @router.get("/cliente/pedido/{uuid}/nota/")
    def gerar_nota_de_pedido(uuid : UUID) -> dict[str, Any]:
        nota = GerarNotaDePedidoComando(PedidoDAOSqlite(), uuid).executar()
        if type(nota) is str:
            raise HTTPException(status_code=400, detail=nota)

        return nota

    @router.put('/cliente/pedido/{uuid}/nome/{nome_cliente}')
    def definir_nome_do_cliente_no_pedido(uuid : UUID, nome_cliente : str) -> str: 
        log = DefinirNomeDoClienteComando(PedidoDAOSqlite(), uuid, nome_cliente).executar()

        if log is None:
            return "Ok"
        
        raise HTTPException(status_code=400, detail=log)

    @router.post("/cliente/pedido/{uuid}/")
    async def enviar_pedido(uuid : UUID) -> str:
        log = await EnviarPedidoComando(PedidoDAOSqlite(), uuid).executar()

        if log is None:
            return "Ok"
        
        raise HTTPException(status_code=400, detail=log)


    @router.get("/cliente/pedido/{uuid}/nota/metodo/{metodo_de_pagamento}")
    def simular_nota_com_pagamento(uuid : UUID, metodo_de_pagamento : MetodoDePagamentoEnum) -> dict[str, Any]: 
        nota = SimularNotaComPagamentoComando(PedidoDAOSqlite(), uuid, MetodoDePagamentoDTO.para_tipo_de_pagamento( metodo_de_pagamento)).executar()
        if type(nota) is str:
            raise HTTPException(status_code=400, detail=nota)

        return nota
    
    # Socket cliente
    # Nesse socket o cliente vai enviar um uuid e vai somente se importar com alterações neste id

    @router.websocket_route("/ws/{uuid}")
    async def cliente_socket(websocket : WebSocket, uuid : UUID):
        await websocket.accept()

        observer = ClienteObserver(websocket, uuid)
        ObserverHub().registrar(observer)

        while websocket.state != WebSocketState.DISCONNECTED:
            await asyncio.sleep(1)


    return router


class CozinhaObserver(Observer):
    def __init__(self, socket : WebSocket):
        self.__socket = socket

    async def atualizar(self, data : Pedido):
        try:
            await self.__socket.send_text( json.dumps( PedidoDTO.de_pedido(data).para_dict() ) )
        except WebSocketDisconnect:
            ObserverHub().remover(self)

def endpoints_cozinha() -> APIRouter:
    router = APIRouter()

    @router.get("/cozinha/pedido")
    def pegar_todos_os_pedidos() -> List[dict]:
        pedidos = PegarTodosOsPedidosComando(PedidoDAOSqlite()).executar()

        return [PedidoDTO.de_pedido(pedido).para_dict() for pedido in pedidos]

    @router.put("/cozinha/pedido/{uuid}/status/{status_de_pedido}")
    async def mudar_status_de_pedido(uuid : UUID, status_de_pedido : StatusDePedidoEnum) -> str:
        log = await MudarStatusDePagamentoComando(PedidoDAOSqlite(), uuid,  PedidoDTO.de_enum( status_de_pedido) ).executar()

        if log is None:
            return "Ok"
        
        raise HTTPException(status_code=400, detail=log)

    # Nesse socket o cozinha vai se importar com alterações em TODOS os pedidos



    @router.websocket_route("/ws")
    async def cozinha_socket(websocket : WebSocket):
        await websocket.accept()

        observer = CozinhaObserver(websocket)
        ObserverHub().registrar(observer)

        while websocket.state != [WebSocketState.DISCONNECTED]:
            await asyncio.sleep(1)


    return router

