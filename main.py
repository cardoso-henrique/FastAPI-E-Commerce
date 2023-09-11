# FastAPI by Henrique Cardoso Lana

from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="FastAPI E-Commerce",
              description="Desenvolvido por: Henrique Cardoso Lana "
                          "[linkedin](https://www.linkedin.com/in/proj-henrique/)")


class Product(BaseModel):
    id: uuid.UUID
    name: str
    price: float

class OrderItem(BaseModel):
    product_id: uuid.UUID
    quantity: int

class Order(BaseModel):
    id: uuid.UUID
    customer_name: str
    items: List[OrderItem]

@app.get("/", summary="Teste Online",
              description="Retorna uma mensagem se a API estiver online.")
def home():
    message = "FastAPI E-Commerce Online by: Henrique Cardoso Lana."
    return message

products_db = []
orders_db = []

router_products = APIRouter()

@router_products.post("/", response_model=Product,
                     summary="Criar Produto",
                     description="Cria um produto e atribui um id a ele.")
def create_product(product: Product):
    product_id = uuid.uuid4()
    product.id = product_id
    products_db.append(product.dict())
    return product

@router_products.get("/", response_model=List[Product],
                     summary="Lista de Produtos",
                     description="Retorna uma lista de produtos disponíveis.")
def list_products():
    return products_db

@router_products.get("/{product_id}", response_model=Product,
                     summary="Lista de Produtos por ID",
                     description="Retorna o produto por seu ID.")
def get_product(product_id: uuid.UUID):
    matching_products = [p for p in products_db if p["id"] == product_id]
    if not matching_products:
        raise HTTPException(status_code=404, detail="Product not found")
    return matching_products[0]

@router_products.put("/{product_id}", response_model=Product,
                     summary="Alterar Produto por ID",
                     description="Altera o produtos por seu ID.")
def update_product(product_id: uuid.UUID, updated_product: Product):
    for idx, product in enumerate(products_db):
        if product["id"] == product_id:
            products_db[idx] = updated_product.dict()
            products_db[idx]["id"] = product_id  # Garanta que o ID não seja alterado
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@router_products.delete("/{product_id}", response_model=Product,
                     summary="Excluir Produto por ID",
                     description="Exclui o produto por seu ID.")
def delete_product(product_id: uuid.UUID):
    for idx, product in enumerate(products_db):
        if product["id"] == product_id:
            deleted_product = products_db.pop(idx)
            return deleted_product
    raise HTTPException(status_code=404, detail="Product not found")

router_orders = APIRouter()

@router_orders.post("/", response_model=Order,
                     summary="Criar Pedido",
                     description="Cria pedido com os produtos.")
def create_order(order: Order):
    order_total = 0
    order_items = []
    for item in order.items:
        product_id = item.product_id
        quantity = item.quantity
        matching_products = [p for p in products_db if p["id"] == product_id]
        if not matching_products:
            raise HTTPException(status_code=400, detail="Product ID is invalid")

        product = matching_products[0]
        product_price = product["price"]
        order_total += product_price * quantity
        order_items.append(item)

    order_id = uuid.uuid4()
    order.id = order_id
    order.items = order_items
    orders_db.append(order.dict())
    return order

@router_orders.get("/", response_model=List[Order],
                     summary="Consultar Pedidos",
                     description="Retorna uma lista de pedidos disponíveis.")
def list_orders():
    return orders_db

@router_orders.get("/{order_id}", response_model=Order,
                     summary="Consultar Pedido por ID",
                     description="Retorna um pedido por seu ID.")
def get_order(order_id: uuid.UUID):
    matching_orders = [o for o in orders_db if o["id"] == order_id]
    if not matching_orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return matching_orders[0]

@router_orders.delete("/{order_id}", response_model=Order,
                     summary="Excluir Pedido",
                     description="Exclui um pedido por seu ID.")
def delete_order(order_id: uuid.UUID):
    for idx, order in enumerate(orders_db):
        if order["id"] == order_id:
            deleted_order = orders_db.pop(idx)
            return deleted_order
    raise HTTPException(status_code=404, detail="Order not found")

app.include_router(router_products, prefix="/products", tags=["Produtos"])
app.include_router(router_orders, prefix="/orders", tags=["Pedidos"])


