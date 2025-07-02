class ClienteDAO:
    _clientes = {}

    @classmethod
    def salvar(cls, nome: str, dados: dict):
        cls._clientes[nome] = dados

    @classmethod
    def buscar(cls, nome: str):
        return cls._clientes.get(nome, None)
