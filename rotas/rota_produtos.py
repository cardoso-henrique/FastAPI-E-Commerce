from fastapi import APIRouter
from fastapi import status
from typing import List
from fastapi import Path
from fastapi import HTTPException

from models import Produto
from models import Produto_Criar
from models import Produto_Deletar
import uuid

produtos_db = []

rota_produtos = APIRouter()

@rota_produtos.post("",
                    status_code=status.HTTP_201_CREATED,
                    response_model=Produto,
                    summary="Criar Produto",
                    response_description="Produto Criado",
                    )
async def criar_produto(produto: Produto_Criar,
                        #futura implemetação de autenticação
                        #x_autenticador: bool = Header(default=False)
                        ):
    """
    Cria um produto e atribui um id aleatório a ele.
    
    - **nome**: "Novo Produto"
    - **preco**: 99,99

    O nome do produto não pode ser maior do que 5 palavras
    """
    produto_id = uuid.uuid4()
    produto.id = produto_id
    produtos_db.append(produto.dict())
    #print(f'Autenticador: {x_autenticador}')
    return produto

@rota_produtos.get("",
                    response_model=List[Produto],
                    summary="Lista de Produtos",
                    description="Retorna uma lista de produtos disponíveis ou uma lista vazia.")
async def list_produtos():
    try:
        return produtos_db
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail='Produto não encontrado')

@rota_produtos.get("/{produto_id}", 
                    response_model=Produto,
                    summary="Lista de Produtos por ID",
                    description="Retorna o produto por seu ID.")
async def get_produto(produto_id: uuid.UUID = Path(title='ID do tipo uui', 
                                                    description='Deve ser do tipo uuid')):
    encontrou_produtos = [p for p in produtos_db if p["id"] == produto_id]
    if not encontrou_produtos:
        raise HTTPException(
            status_code=404, detail=f"Produto com ID {produto_id} não encontrado")
    return encontrou_produtos[0]

@rota_produtos.put("/{produto_id}", 
                    response_model=Produto,
                    summary="Alterar Produto por seu ID",
                    description="Altera o produtos por seu ID.")
async def update_produto(produto_id: uuid.UUID, updated_produto: Produto):
    for idx, produto in enumerate(produtos_db):
        if produto["id"] == produto_id:
            produtos_db[idx] = updated_produto.dict()
            produtos_db[idx]["id"] = produto_id  # Garante que o ID não seja alterado
            return updated_produto
    raise HTTPException(status_code=404, detail=f'Produto com ID {produto_id} não encontrado')

@rota_produtos.delete("/{produto_id}", 
                    response_model=Produto_Deletar,
                    summary="Excluir Produto por ID",
                    description="Exclui o produto por seu ID.")
async def delete_produto(produto_id: uuid.UUID = Path(title='ID do tipo uui', description='Deve ser do tipo uuid')):
    for idx, produto in enumerate(produtos_db):
        if produto["id"] == produto_id:
            deleted_produto = produtos_db.pop(idx)
            del deleted_produto
            return Produto_Deletar(msg="Produto deletado com sucesso.")
    raise HTTPException(status_code=404, detail=f"Produto com ID {produto_id} não encontrado")