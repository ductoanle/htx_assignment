from typing import List
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from htx_transcriber.database import get_db
from htx_transcriber.services.transcription_service import (
    validate_audio_file,
    process_audio_file,
    get_all_transcriptions,
    search_transcriptions
)

router = APIRouter()


@router.post("/transcribe")
def transcribe(
    audio_files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    results = []
    for audio_file in audio_files:
        try:
            validate_audio_file(audio_file)
            result = process_audio_file(audio_file, db)
            results.append(result)
        except Exception as e:
            results.append({
                "filename": audio_file.filename,
                "status": "error",
                "message": str(e)
            })
    return results


@router.get("/transcriptions")
def get_transcriptions(db: Session = Depends(get_db)):
    return get_all_transcriptions(db)


@router.get("/search")
def search_transcriptions_endpoint(
    query: str,
    db: Session = Depends(get_db)
):
    return search_transcriptions(query, db)
