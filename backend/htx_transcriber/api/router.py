from fastapi import APIRouter
from htx_transcriber.api import (
    health_check,
    transcribe,
)

router = APIRouter()

for route in [
    health_check.router,
    transcribe.router,
]:
    router.include_router(route)
