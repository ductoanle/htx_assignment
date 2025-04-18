from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from htx_transcriber.services.transcribe_processor import transcribe_audio
from htx_transcriber.utils import add_file_version, split_file_name
from htx_transcriber.settings import UPLOAD_DIR
from htx_transcriber.models.transcription import TranscriptionModel
from sqlalchemy.sql import select

# Allowed audio file types
ALLOWED_AUDIO_TYPES = [
    "audio/mpeg",        # .mp3
    "audio/wav",         # .wav
    "audio/x-wav",       # .wav alternative
    "audio/ogg",         # .ogg
    "audio/x-m4a",       # .m4a
    "audio/aac",         # .aac
    "audio/flac"         # .flac
]

STATUS_SUCCESS = "success"
STATUS_ERROR = "error"


def validate_audio_file(audio_file: UploadFile) -> None:
    """Validate audio file type."""
    if audio_file.content_type not in ALLOWED_AUDIO_TYPES:
        error_msg = f"File type {audio_file.content_type} not allowed. "
        error_msg += f"Must be one of: {', '.join(ALLOWED_AUDIO_TYPES)}"
        raise HTTPException(status_code=400, detail=error_msg)


def process_audio_file(audio_file: UploadFile, db: Session) -> Dict[str, Any]:
    """Process a single audio file for transcription."""
    try:
        if not audio_file.filename:
            return {
                "filename": "unknown",
                "status": STATUS_ERROR,
                "message": "Filename is missing"
            }
        # Check if file already exists
        first_version = add_file_version(audio_file.filename)
        if db.query(TranscriptionModel).filter(
            TranscriptionModel.audio_file_name == first_version
        ).first():
            # Search for latest file with similar name
            query = db.query(
                TranscriptionModel.audio_file_name
            ).filter(
                TranscriptionModel.audio_file_name.like(
                    f"{split_file_name(audio_file.filename)[0]}%"
                )
            ).order_by(TranscriptionModel.created_at.desc())
            last_similar_file = query.first()
            # Update audio file name
            if last_similar_file:
                audio_file.filename = add_file_version(
                    last_similar_file.audio_file_name
                )
        else:
            audio_file.filename = first_version
        # Save file to disk
        upload_dir = str(UPLOAD_DIR)
        file_path = Path(upload_dir) / audio_file.filename
        if not file_path.exists():
            with open(file_path, "wb") as f:
                f.write(audio_file.file.read())
        # Transcribe the audio
        transcribed_text = transcribe_audio(file_path)
        # Save transcription to database
        transcription = TranscriptionModel(
            audio_file_name=audio_file.filename,
            transcribed_text=transcribed_text,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(transcription)
        db.commit()
        return {
            "filename": audio_file.filename,
            "status": STATUS_SUCCESS,
            "transcription": transcription.as_JSON()
        }
    except Exception as e:
        return {
            "filename": audio_file.filename,
            "status": STATUS_ERROR,
            "message": str(e)
        }
    finally:
        audio_file.file.close()


def get_all_transcriptions(db: Session) -> List[Dict[str, Any]]:
    """Get all transcriptions ordered by creation date."""
    transcriptions = db.query(TranscriptionModel).order_by(
        TranscriptionModel.created_at.desc()
    ).all()
    return [transcription.as_JSON() for transcription in transcriptions]


def search_transcriptions(query: str, db: Session) -> List[Dict[str, Any]]:
    """Search transcriptions by filename."""
    transcriptions = db.query(TranscriptionModel).filter(
        TranscriptionModel.audio_file_name.ilike(f"%{query.lower()}%")
    ).order_by(
        TranscriptionModel.audio_file_name.desc(),
        TranscriptionModel.created_at.desc()
    ).all()
    return [transcription.as_JSON() for transcription in transcriptions]


def get_next_version(audio_file: UploadFile, db: Session) -> str:
    """Get the next version number for a file."""
    # Check if file already exists
    base_name = (
        audio_file.filename.split("_ver_")[0]
        if "_ver_" in audio_file.filename
        else audio_file.filename
    )
    base_name = base_name.rsplit(".", 1)[0]  # Remove extension

    # Query for existing versions
    query = select(TranscriptionModel).where(
        TranscriptionModel.audio_file_name.like(f"{base_name}_ver_%")
    ).order_by(TranscriptionModel.audio_file_name.desc())

    # Get the first result (most recent version)
    first_version = db.execute(query).first()

    if first_version:
        # Extract version number and increment
        version_str = (
            first_version[0].audio_file_name
            .split("_ver_")[1].split(".")[0]
        )
        next_version = int(version_str) + 1
    else:
        # No existing version, start with 1
        next_version = 1

    # Construct new filename
    file_ext = audio_file.filename.split(".")[-1]
    return f"{base_name}_ver_{next_version}.{file_ext}"


def find_similar_file(
    audio_file: UploadFile,
    db: Session
) -> Optional[TranscriptionModel]:
    """Find a similar file in the database."""
    # Extract base name without version
    base_name = (
        audio_file.filename.split("_ver_")[0]
        if "_ver_" in audio_file.filename
        else audio_file.filename
    )
    base_name = base_name.rsplit(".", 1)[0]  # Remove extension

    # Query for similar files
    query = select(TranscriptionModel).where(
        TranscriptionModel.audio_file_name.like(f"{base_name}%")
    ).order_by(TranscriptionModel.audio_file_name.desc())

    # Get the first result
    last_similar_file = db.execute(query).first()

    if last_similar_file:
        return last_similar_file[0]
    return None
