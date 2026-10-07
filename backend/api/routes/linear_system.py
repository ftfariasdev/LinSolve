from fastapi import APIRouter

from schemas.linear_system import SolveRequest, SolveResponse
from services.linear_system import resolver_sistema_linear

router = APIRouter(prefix="/api/linear-system", tags=["linear-system"])


@router.post("/solve/", response_model=SolveResponse)
def solve(request: SolveRequest):
    return resolver_sistema_linear(request.coeficientes, request.termos_independentes)
