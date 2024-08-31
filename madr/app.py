from fastapi import FastAPI

from madr.routers import auth, autores, contas, livros

app = FastAPI()

app.include_router(auth.router)
app.include_router(contas.router)
app.include_router(autores.router)
app.include_router(livros.router)
