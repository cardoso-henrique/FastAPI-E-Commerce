# FastAPI by Henrique Cardoso Lana

from typing import Any
from fastapi import FastAPI
from fastapi import Depends
from time import sleep
from rotas import rota_produtos
from rotas import rota_pedidos
from models import Resposta

app = FastAPI(
    title="FastAPI E-Commerce",
    description=("Desenvolvido por: Henrique Cardoso Lana\n"
                "  --  [Linkedin](https://www.linkedin.com/in/proj-henrique/)  --  "
                "[GitHub](https://github.com/cardoso-henrique)\n"
                "\nFastAPI E-Commerce, API desenvolvida para testes locais de CRUD e utilizada para estudos.\n"
                "\nDocumentação: [GitHub FastAPI E-Commerce](https://github.com/cardoso-henrique/FastAPI-E-Commerce)\n"
                "\n"
                ),                      
    version='0.0.2')

#inicio da construção do banco de dados
def fake_db():
    try:
        print('Abrindo conexão com banco de dados...')
        sleep(1)
    finally:
        print('Fechando conexão com banco de dados...')
        sleep(1)

@app.get("/", 
        summary = "Teste Online",
        description = "Envie uma requisição para http://127.0.0.1:8000 e retorna uma mensagem se a API estiver online.",
        response_model = Resposta,
        response_description="API Funcionando"
        )
async def home(db: Any = Depends(fake_db)):
    # message = "FastAPI E-Commerce Online by: Henrique Cardoso Lana."
    # return message
    return Resposta(msg="FastAPI E-Commerce Online by: Henrique Cardoso Lana.")

app.include_router(rota_produtos.rota_produtos, prefix="/produtos", tags=["Produtos"])
app.include_router(rota_pedidos.rota_pedidos, prefix="/pedidos", tags=["Pedidos"])

#otimização no comando de rodar a API e suas configs
if __name__ == '__main__':
    import uvicorn
    uvicorn.run("FastAPI-E-Commerce:app", host="127.0.0.1", port=8000,
                log_level="info", reload=True)