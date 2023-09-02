from contextlib import asynccontextmanager

from fastapi import FastAPI, Body

from pharmacy.database.core import Base, engine
from pharmacy.routers import users, inventories, admins


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(inventories.router)
app.include_router(users.router)
app.include_router(admins.router)


@app.get("/ping")
def ping_pong() -> dict[str, str]:
    return {"message": "pong"}


@app.get("/name/{first_name}")
def get_first_name(first_name: str) -> dict[str, str]:
    return {"name": first_name}


@app.post("/name")
def get_surname(surname: str = Body(embed=True)) -> dict[str, str]:
    return {"surname": surname}
