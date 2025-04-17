from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from htx_transcriber.database import get_db

router = APIRouter()


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "OK"}
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={"status": "ERROR", "error": str(e)}
        )
