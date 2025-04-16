import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from htx_transcriber.database import Base
from htx_transcriber.models.transcription import TranscriptionModel


# Create a test database engine
@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    # Use an in-memory SQLite database for testing
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


# Create tables in the test database
@pytest.fixture(scope="session")
def tables(engine):
    """Create all tables in the test database."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


# Create a session factory
@pytest.fixture(scope="session")
def session_factory(engine):
    """Create a session factory for the test database."""
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create a database session for each test
@pytest.fixture
def db_session(session_factory, tables):
    """Create a database session for a test."""
    session = session_factory()
    try:
        yield session
    finally:
        # Clean up all records to ensure test isolation
        session.query(TranscriptionModel).delete()
        session.commit()
        session.rollback()
        session.close()


# Create a fixture for a sample transcription
@pytest.fixture
def sample_transcription(db_session):
    """Create a sample transcription in the database."""
    from datetime import datetime
    transcription = TranscriptionModel(
        audio_file_name="sample_audio_ver_1.mp3",
        transcribed_text="This is a sample transcription",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db_session.add(transcription)
    db_session.commit()
    return transcription


# Create a fixture for multiple transcriptions
@pytest.fixture
def multiple_transcriptions(db_session):
    """Create multiple transcriptions in the database."""
    from datetime import datetime
    transcriptions = [
        TranscriptionModel(
            audio_file_name="audio1_ver_1.mp3",
            transcribed_text="First transcription",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        TranscriptionModel(
            audio_file_name="audio2_ver_1.mp3",
            transcribed_text="Second transcription",
            created_at=datetime.now(),
            updated_at=datetime.now()
        ),
        TranscriptionModel(
            audio_file_name="audio3_ver_1.mp3",
            transcribed_text="Third transcription",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
    ]

    for transcription in transcriptions:
        db_session.add(transcription)
    db_session.commit()
    return transcriptions
