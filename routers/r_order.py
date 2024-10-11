from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from models.order_items import OrderItem
from models.orders import Order
from models.products import Product
from schemas.order import OrderCreate, OrderResponse, OrderListResponse, OrderUpdate
from config.db import async_session_maker
from schemas.order_item import OrderItemCreate

router = APIRouter()

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

@router.post("/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncSession = Depends(get_db)):
    try:
        db_order = Order(status=order.status)
        db.add(db_order)

        # Проверка и создание заказов
        for item in order.order_items:
            product = await db.get(Product, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")

            if product.quantity_in_stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Not enough stock for product {product.name}")

            db_order_item = OrderItem(order_id=db_order.id, product_id=item.product_id, quantity=item.quantity)
            db.add(db_order_item)
            product.quantity_in_stock -= item.quantity  # Обновляем количество товара

        await db.commit()  # Один общий коммит для добавления заказа и обновления товара

        return OrderResponse(
            id=db_order.id,
            created_at=db_order.created_at,
            status=db_order.status,
            order_items=[OrderItemCreate(product_id=item.product_id, quantity=item.quantity) for item in order.order_items]
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/", response_model=OrderListResponse)
async def get_orders(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Order).options(selectinload(Order.order_items)))
    orders = result.scalars().all()

    orders_with_items = [
        OrderResponse(
            id=order.id,
            created_at=order.created_at,
            status=order.status,
            order_items=[
                OrderItemCreate(product_id=item.product_id, quantity=item.quantity)
                for item in order.order_items
            ]
        )
        for order in orders
    ]

    return OrderListResponse(orders=orders_with_items)


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order_items = await db.execute(select(OrderItem).where(OrderItem.order_id == order_id))
    order_items = order_items.scalars().all()

    return OrderResponse(
        id=order.id,
        created_at=order.created_at,
        status=order.status,
        order_items=[OrderItemCreate(product_id=item.product_id, quantity=item.quantity) for item in order_items]
    )


@router.put("/{order_id}")
async def update_order(order_id: int, order_data: OrderUpdate, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id, options=[selectinload(Order.order_items)])
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = order_data.status

    current_items = {item.product_id: item for item in order.order_items}

    for item_data in order_data.order_items:
        if item_data.product_id in current_items:
            current_item = current_items[item_data.product_id]
            current_item.quantity = item_data.quantity
        else:
            new_item = OrderItem(order_id=order_id, product_id=item_data.product_id, quantity=item_data.quantity)
            db.add(new_item)

    await db.commit()

    return {"detail": "Order updated"}


@router.delete("/{order_id}")
async def delete_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    await db.delete(order)
    await db.commit()

    return {"detail": "Order deleted"}