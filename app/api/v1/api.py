from fastapi import APIRouter
from .endpoints import smax, topdesk

router = APIRouter()

router.include_router(smax.router, prefix="/smax", tags=["smax"])
router.include_router(topdesk.router, prefix="/topdesk", tags=["topdesk"])