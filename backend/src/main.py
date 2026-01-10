from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, user, disciplina, tema, revisao, painel
from .database import Base, engine
from sqlalchemy import text
from contextlib import asynccontextmanager
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

@app.middleware("http")
async def method_override_middleware(request: Request, call_next):
    if request.method == "POST":
        method_override = request.headers.get("X-HTTP-Method-Override", "").upper()
        if method_override == "PUT":
            request.scope["method"] = method_override
            
    return await call_next(request)


origins = [
    "https://5174-firebase--lip-sisestudogit-1764198916068.cluster-c72u3gwiofapkvxrcwjq5zllcu.cloudworkstations.dev",
    "https://8000-firebase--lip-sisestudogit-1764198916068.cluster-c72u3gwiofapkvxrcwjq5zllcu.cloudworkstations.dev",
    "http://localhost:5174",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(disciplina.router)
app.include_router(tema.disciplina_tema_router)
app.include_router(tema.tema_router)
app.include_router(revisao.router)
app.include_router(painel.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


if __name__ == "__main__":
    # Definindo a porta e o host para o servidor
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
