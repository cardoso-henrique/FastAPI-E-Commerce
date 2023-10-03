from fastapi import APIRouter
from fastapi import status
from typing import List
from fastapi import Path
from fastapi import HTTPException
from models import Pedido
import uuid
from rotas import rota_produtos

pedidos_db = []

rota_pedidos = APIRouter()

@rota_pedidos.post("/", 
                    status_code=status.HTTP_201_CREATED,
                    response_model=Pedido,
                    summary="Criar Pedido",
                    description="Cria pedido com os produtos.")
async def criar_pedido(pedido: Pedido):
    pedido_total = 0
    pedido_items = []
    for item in pedido.items:
        produto_id = item.produto_id
        quantity = item.quantity
        matching_produtos = [p for p in rota_produtos.produtos_db if p["id"] == produto_id]
        if not matching_produtos:
            raise HTTPException(status_code=400, detail=f"Produto ID {produto_id} não existe")
        produto = matching_produtos[0]
        produto_preco = produto["preco"]
        pedido_total += produto_preco * quantity
        pedido_items.append(item)
    pedido_id = uuid.uuid4()
    pedido.id = pedido_id
    pedido.items = pedido_items
    pedidos_db.append(pedido.dict())
    return pedido

@rota_pedidos.get("/",
                    response_model=List[Pedido],
                    summary="Consultar Pedidos",
                    description="Retorna uma lista de pedidos disponíveis ou uma lista vazia.")
async def list_pedidos():
    return pedidos_db

@rota_pedidos.get("/{pedido_id}", 
                    response_model=Pedido,
                    summary="Consultar Pedido por ID",
                    description="Retorna um pedido por seu ID.")
async def get_pedido(pedido_id: uuid.UUID = Path(title='ID do tipo uui', description='Deve ser do tipo uuid')):
    matching_pedidos = [o for o in pedidos_db if o["id"] == pedido_id]
    if not matching_pedidos:
        raise HTTPException(status_code=404, detail=f"Pedido com ID {pedido_id} não encontrado")
    return matching_pedidos[0]

@rota_pedidos.delete("/{pedido_id}", 
                    response_model=Pedido,
                    summary="Excluir Pedido",
                    description="Exclui um pedido por seu ID.")
async def delete_pedido(pedido_id: uuid.UUID):
    for idx, pedido in enumerate(pedidos_db):
        if pedido["id"] == pedido_id:
            deleted_pedido = pedidos_db.pop(idx)
            return deleted_pedido
    raise HTTPException(status_code=404, detail=f"Pedido com ID {pedido_id} não encontrado")