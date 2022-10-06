from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List, List
from database import SessionLocal
import models


app = FastAPI()


class Item (BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode = True


db = SessionLocal()

@app.get("/")
async def root():
    return {"message": "welcome FastAPI"}



@app.get('/items',response_model=List[Item],status_code=status.HTTP_200_OK)
def get_all_items():
    items=db.query(models.Item).all()

    return items


@app.post('/items', response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item: Item):

    new_item = models.Item(
        name=item.name,
        price=item.price,
        description=item.description,
        on_offer=item.on_offer
    )

    db.add(new_item)
    db.commit()

    return item


@app.put('/item', response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, item: Item):
    item_to_update = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.price = item.price
    item_to_update.description = item.description
    item_to_update.on_offer = item.on_offer

    db.commit()

    return item


@app.delete('/item/{item_id}')
def delete_item(item_id: int):
    item_to_delete = db.query(models.Item).filter(
        models.Item.id == item_id).first()

    db.delete(item_to_delete)
    db.commit()

    return {"Delete Item Succesful"}
