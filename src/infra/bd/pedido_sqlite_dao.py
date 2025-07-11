import json, sqlite3
from uuid import UUID, uuid4
from ...utils.singleton import SingletonMeta
from ...core.DAO.pedido_dao import PedidoDAO
from ...core.bebidas import Bebida, Cafe, Cha 
from ...core.adicionais import Adicional, LeiteDeAveia, Canela, SemAcucar
from ...core.pedidos import Pedido, PedidoCancelado, PedidoEmPreparo, PedidoEmRealizacao, PedidoEntregue, PedidoPronto, PedidoRecebido
import logging


class PedidoDAOSqlite(PedidoDAO, metaclass = SingletonMeta):
    def __para_bebida(self, valores):
        pedido, id, tipo, numero_de_sequencia = valores

        if tipo == 0:
            return Cafe
        return Cha
    
    def __para_adicional(self, valores):
        tipo = valores[1]
        if tipo == 0:
            return LeiteDeAveia
        if tipo == 1:
            return Canela
        return SemAcucar
    
    def __para_pedido(self, valores):
        id, nome_cliente, status = valores

        if status == 0:
            return PedidoEntregue
        if status == 1:
            return PedidoCancelado
        if status == 2:
            return PedidoPronto
        if status == 3:
            return PedidoEmPreparo
        if status == 4:
            return PedidoRecebido
        return PedidoEmRealizacao

    def __e_adicional(self, bebida : Bebida):
        return type(bebida) in [LeiteDeAveia, Canela, SemAcucar]

    def __de_adicional(self, adicional : Adicional):
        return {
            LeiteDeAveia : 0,
            Canela : 1,
            SemAcucar : 2
        }[type(adicional)]

    def __de_bebida(self, bebida : Bebida):
        return {
            Cafe : 0,
            Cha : 1
        }[type(bebida)]

    def __de_pedido(self, pedido : Pedido):
        return {
            PedidoEntregue : 0,
            PedidoCancelado : 1,
            PedidoPronto : 2,
            PedidoEmPreparo : 3,
            PedidoRecebido : 4,
            PedidoEmRealizacao : 5
        }[type(pedido)]

    def setup(self):
        cursor = self.__connection.cursor()
        for s in self.queries["setup"]:
            cursor.execute(s)
        cursor.close()
        self.__connection.commit()

    def __init__(self, config = {
        "caminho" : 'db.db',
        "caminho_queries" : 'sqlite_queries.json'
    }):
        sqlite3.threadsafety = 3
        self.__connection = sqlite3.connect(config["caminho"], check_same_thread=False )
        with open(config['caminho_queries'], 'r') as f:
            self.queries = json.load(f)
        self.setup()

    def pegar_todos(self) -> list[Pedido]:
        cursor = self.__connection.cursor()

        pedidos = cursor.execute(self.queries["select"]["pedido"]).fetchall()
        bebidas = cursor.execute(self.queries["select"]["bebida"]).fetchall()
        adicionais = cursor.execute(self.queries["select"]["adicional"]).fetchall()

        bebidas = [[valores[0], valores[1], self.__para_bebida(valores)(), valores[-1]] for valores in bebidas ]        


        for bebida in bebidas:
            adicionais_da_bebida = [adicional for  adicional in adicionais if adicional[0] == bebida[1] ] 
            for adicional in adicionais_da_bebida:
                bebida[2] = self.__para_adicional(adicional)(bebida[2])                

        response = []


        for pedido in pedidos:
            itens_do_pedido = [Pedido.Item(bebida[-1], bebida[2]) for bebida in bebidas if bebida[0] == pedido[0]]

            response.append(self.__para_pedido(pedido).de_lista_de_itens(pedido[1], itens_do_pedido, pedido[0]))

        cursor.close()
        return response

    def __inserir(self, pedido : Pedido):
        bebidas = []

        for item in pedido.itens:
            bebida = item.bebida
            numero_de_sequencia = item.id
            b = bebida
            adicionais = []

            while self.__e_adicional(b):
                adicionais.append(self.__de_adicional(b))                             
                b = b.pegar_base()
            
            b = self.__de_bebida(b)
            bebidas.append((b, uuid4(), adicionais, numero_de_sequencia))
        
        cursor = self.__connection.cursor()

        cursor.execute(
                self.queries["insert"]["pedido"] + 
                f" ('{pedido.uuid}', '{pedido.nome_cliente}', {self.__de_pedido(pedido)} ) "
            )  
        
        valores_bebidas = [ f" ('{pedido.uuid}', '{id}', {bebida}, {numero_de_sequencia}) "  for bebida, id, _, numero_de_sequencia in bebidas] 

        if len(valores_bebidas) > 0:
            cursor.execute( self.queries['insert']['bebida'] + ', '.join(valores_bebidas) )

        valores_adicionais = [ f" ('{id}', {adicional}) "  for _, id, adicionais, _ in bebidas for adicional in adicionais]

        if len(valores_adicionais) > 0:
            cursor.execute(
                    self.queries['insert']['adicional'] + 
                    ', '.join(valores_adicionais)
                )

        cursor.close()
        self.__connection.commit()

    def pegar(self, uuid : UUID):
        cursor = self.__connection.cursor()
        pedido = cursor.execute(self.queries['select']['pedido'] + f" WHERE uuid='{uuid}'").fetchone()

        if pedido is None:
            return None
        
        uuid, nome_cliente, status = pedido

        bebidas = cursor.execute(self.queries['select']['bebida'] + f" WHERE uuid_pedido='{uuid}'").fetchall()
        
        query = self.queries['select']['adicional'] + " WHERE uuid_bebida IN (" +', '.join([f"'{bebida[1]}'" for bebida in bebidas]) + ')'


        adicionais = cursor.execute(query).fetchall()

        bebidas = [ [valores[0], valores[1], self.__para_bebida(valores)(), valores[-1]] for valores in bebidas ]        

        for bebida in bebidas:
            adicionais_da_bebida = [adicional for  adicional in adicionais if adicional[0] == bebida[1] ] 
            for adicional in adicionais_da_bebida:
                bebida[2] = self.__para_adicional(adicional)(bebida[2])          

        itens_do_pedido = [Pedido.Item(bebida[-1], bebida[2]) for bebida in bebidas]
        pedido = self.__para_pedido(pedido).de_lista_de_itens(pedido[1], itens_do_pedido, pedido[0])

        cursor.close()
        return pedido

    def __remover_nao_seguro(self, uuid : UUID):
        cursor = self.__connection.cursor()

        cursor.execute( self.queries['delete']['pedido'] + f"'{uuid}'" )

        cursor.close()        
        self.__connection.commit()
        

    def remover(self, pedido : Pedido):
        if type(pedido) == PedidoEmRealizacao:
            self.__remover_nao_seguro(pedido.uuid)
            return
        raise Exception(f"Impossivel remover pedido de tipo {pedido.__class__.__name__}")

    def __atualizar(self, pedido : Pedido):
        self.__remover_nao_seguro(pedido.uuid)
        return self.__inserir(pedido)

    def salvar(self, pedido : Pedido):
        pedido_antigo = self.pegar(pedido.uuid)        

        if pedido_antigo is None:
            return self.__inserir(pedido)
        return self.__atualizar(pedido)
 
