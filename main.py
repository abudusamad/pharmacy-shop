
from fastapi import FastAPI, Body
from contextlib import asynccontextmanager

from pharmacy_shop.database.core import Base, engine
from routers.users import users
from routers.admins import admins
from routers.inventories import inventories


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/name/")
def get_full_name(full_name: str = Body(embed=True)) -> list[dict]:
    return [{k: v for k, v in enumerate(full_name.split(), start=1)}]


app.include_router(users)
app.include_router(admins)
app.include_router(inventories)
