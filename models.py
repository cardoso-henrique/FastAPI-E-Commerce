from pydantic import BaseModel, validator
from typing import List, Optional
import uuid

class Produto(BaseModel):
    nome: str
    preco: float
    id: Optional[uuid.UUID] | None = None
    @validator('nome')
    def validador_nome(cls, value: str):
        nome = value.split(' ')
        if len(nome) > 5:
            raise ValueError('Nome do produto muito grande')
        # @validator('preco')
        # def validador_preco(cls, value: float):
        #     max_preco = 6
        #     if value > max_preco:
        #         raise ValueError(f'Preço do produto deve ser menor que {max_preco}')
        return value

class Produto_Criar(BaseModel):
    nome: str
    preco: float
    id: Optional[uuid.UUID] | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "nome": "Nome do Produto",
                    "preco": 99.99
                }
            ]
        }
    }

class Produto_Deletar(BaseModel):
    msg: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "msg": "Produto deletado com sucesso.",
                }
            ]
        }
    }

class PedidoItem(BaseModel):
    produto_id: uuid.UUID
    quantity: int

class Pedido(BaseModel):
    id: uuid.UUID
    customer_nome: str
    items: List[PedidoItem]

class Resposta(BaseModel):
    msg: str
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "msg": "FastAPI E-Commerce Online by: Henrique Cardoso Lana.",
                }
            ]
        }
    }
