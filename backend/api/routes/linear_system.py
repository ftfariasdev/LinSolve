from fastapi import APIRouter

router = APIRouter(prefix="/api/linear-system", tags=["linear-system"])


@router.post("/solve/")
def solve():
    return {"message": "não implementado"}
