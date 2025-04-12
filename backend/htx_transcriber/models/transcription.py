from sqlalchemy import Column, Integer, String, UnicodeText, DateTime
from htx_transcriber.database import Base


class TranscriptionModel(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    audio_file_name = Column(String(100), nullable=False, unique=True)
    transcribed_text = Column(UnicodeText)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def as_JSON(self):
        """Convert the model to a JSON-compatible dictionary."""
        return {
            "id": self.id,
            "audio_file_name": self.audio_file_name,
            "transcribed_text": self.transcribed_text,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
