from fastapi import APIRouter, Depends
from app.utils import verify_header


router = APIRouter(prefix="/test", tags=["default"], dependencies=[Depends(verify_header)])


@router.get("/auth")
async def test_auth():
    return "test success"