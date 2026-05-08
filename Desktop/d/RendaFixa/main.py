from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from app.routers import titulos, clientes, alocacoes
from app.state import AppState
from app.loader import load_titulos


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not hasattr(app.state, "db"):
        app.state.db = AppState(titulos=load_titulos())
    yield



app = FastAPI(
    title="API de Renda Fixa",
    description="Gestão de títulos de renda fixa, cadastro de clientes e alocações.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"] ,
)

app.include_router(titulos.router, prefix="/titulos", tags=["Títulos"])
app.include_router(clientes.router, prefix="/clientes", tags=["Clientes"])
app.include_router(alocacoes.router, prefix="/alocacoes", tags=["Alocações"])



@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
