from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from . import db


app = FastAPI()


class ItemIn(BaseModel):
    name: str


@app.on_event("startup")
def startup() -> None:
    db.init_db()


@app.get("/")
async def read_root():
    return {"message": "Hello from app!"}


@app.get("/items")
def list_items():
    return list(db.iter_items())


@app.post("/items", status_code=201)
def create_item(item: ItemIn):
    if not item.name.strip():
        raise HTTPException(status_code=400, detail="name is required")
    return db.add_item(item.name)
