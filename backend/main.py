from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.routes import health, linear_system

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(linear_system.router)


# Entrada inválida: responde 400 com uma mensagem que dá para mostrar ao
# usuário (o padrão do FastAPI seria 422 com uma lista de erros em inglês).
@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exc: RequestValidationError):
    erro = exc.errors()[0]

    if erro["type"] == "value_error":
        # Mensagem escrita por nós no schema; o Pydantic põe "Value error, " na frente.
        mensagem = erro["msg"].removeprefix("Value error, ")
    else:
        mensagem = "Formato inválido: os valores enviados não correspondem ao esperado."

    return JSONResponse(status_code=400, content={"detail": mensagem})


# Erro inesperado: responde 500 com uma mensagem genérica. O detalhe do erro
# fica só no log do servidor.
@app.exception_handler(Exception)
def handle_unexpected_error(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Erro interno. Tente novamente mais tarde."},
    )
