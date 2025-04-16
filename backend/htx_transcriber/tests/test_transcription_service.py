import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from fastapi import HTTPException

from htx_transcriber.services.transcription_service import (
    process_audio_file,
    validate_audio_file,
    get_all_transcriptions,
    search_transcriptions,
    STATUS_SUCCESS,
    STATUS_ERROR,
    ALLOWED_AUDIO_TYPES
)
from htx_transcriber.services.transcribe_processor import TranscriptionError
from htx_transcriber.models.transcription import TranscriptionModel


@pytest.fixture
def mock_upload_file():
    """Create a mock upload file."""
    file = MagicMock()
    file.filename = "sample_audio.mp3"
    file.content_type = "audio/mpeg"
    file.file = MagicMock()
    return file


# Validation tests
def test_validate_audio_file_valid(mock_upload_file):
    """Test that valid audio files are accepted."""
    # Should not raise an exception
    validate_audio_file(mock_upload_file)


def test_validate_audio_file_invalid_type():
    """Test that invalid file types are rejected."""
    file = MagicMock()
    file.filename = "test_document.pdf"
    file.content_type = "application/pdf"

    with pytest.raises(HTTPException) as excinfo:
        validate_audio_file(file)

    assert excinfo.value.status_code == 400
    assert "File type application/pdf not allowed" in excinfo.value.detail


def test_validate_audio_file_all_allowed_types():
    """Test that all allowed audio types are accepted."""
    for content_type in ALLOWED_AUDIO_TYPES:
        file = MagicMock()
        file.filename = f"test_audio.{content_type.split('/')[-1]}"
        file.content_type = content_type

        # Should not raise an exception
        validate_audio_file(file)


def test_validate_audio_file_missing_content_type():
    """Test that files with missing content type are rejected."""
    file = MagicMock()
    file.filename = "test_audio.mp3"
    file.content_type = None

    with pytest.raises(HTTPException) as excinfo:
        validate_audio_file(file)

    assert excinfo.value.status_code == 400
    assert "File type None not allowed" in excinfo.value.detail


# Processing tests
@patch('htx_transcriber.services.transcription_service.transcribe_audio')
@patch('htx_transcriber.services.transcription_service.UPLOAD_DIR', 
       Path('/tmp/uploads'))
@patch('os.path.exists')
@patch('builtins.open', new_callable=mock_open)
def test_process_audio_file_success(
    mock_file, mock_exists, mock_transcribe,
    db_session, mock_upload_file
):
    """Test successful processing of an audio file."""
    # Setup mocks
    mock_exists.return_value = False
    mock_transcribe.return_value = "Transcribed text"

    # Call the function
    result = process_audio_file(mock_upload_file, db_session)

    # Verify results
    assert result["status"] == STATUS_SUCCESS
    assert result["filename"] == "sample_audio_ver_1.mp3"
    assert "transcription" in result

    # Verify mocks were called correctly
    mock_file.assert_called_once()
    mock_transcribe.assert_called_once()

    # Verify database was updated
    transcription = db_session.query(TranscriptionModel).first()
    assert transcription is not None
    assert transcription.audio_file_name == "sample_audio_ver_1.mp3"
    assert transcription.transcribed_text == "Transcribed text"


@patch('htx_transcriber.services.transcription_service.transcribe_audio')
def test_process_audio_file_transcription_error(
    mock_transcribe, db_session, mock_upload_file
):
    """Test handling of transcription errors."""
    # Setup mocks
    mock_transcribe.side_effect = TranscriptionError("Transcription failed")

    # Call the function
    result = process_audio_file(mock_upload_file, db_session)

    # Verify results
    assert result["status"] == STATUS_ERROR
    assert "Transcription failed" in result["message"]

    # Verify database was not updated
    transcription = db_session.query(TranscriptionModel).first()
    assert transcription is None


@patch('htx_transcriber.services.transcription_service.transcribe_audio')
def test_process_audio_file_existing_file(
    mock_transcribe, db_session, mock_upload_file, sample_transcription
):
    """Test handling of existing files."""
    # Setup mocks
    mock_upload_file.filename = "sample_audio.mp3"
    mock_transcribe.return_value = "New transcribed text"

    # Call the function
    result = process_audio_file(mock_upload_file, db_session)

    # Verify results
    assert result["status"] == STATUS_SUCCESS
    assert result["filename"] == "sample_audio_ver_2.mp3"

    # Verify database was updated with new version
    transcriptions = db_session.query(TranscriptionModel).all()
    assert len(transcriptions) == 2


def test_process_audio_file_missing_filename(db_session):
    """Test handling of files with missing filenames."""
    # Create a file without a filename
    file = MagicMock()
    file.filename = None
    file.content_type = "audio/mpeg"
    file.file = MagicMock()

    # Call the function
    result = process_audio_file(file, db_session)

    # Verify results
    assert result["status"] == STATUS_ERROR
    assert "Filename is missing" in result["message"]

    # Verify database was not updated
    transcription = db_session.query(TranscriptionModel).first()
    assert transcription is None


# Query tests
def test_get_all_transcriptions_empty(db_session):
    """Test getting all transcriptions when database is empty."""
    result = get_all_transcriptions(db_session)
    assert len(result) == 0


def test_get_all_transcriptions_with_data(db_session, multiple_transcriptions):
    """Test getting all transcriptions when database has data."""
    result = get_all_transcriptions(db_session)

    assert len(result) == 3

    # Extract filenames from results
    filenames = [item["audio_file_name"] for item in result]

    # Check that all expected filenames are present, regardless of order
    expected_filenames = [
        "audio1_ver_1.mp3",
        "audio2_ver_1.mp3",
        "audio3_ver_1.mp3"
    ]
    assert sorted(filenames) == sorted(expected_filenames)


def test_search_transcriptions_empty(db_session):
    """Test searching transcriptions when database is empty."""
    result = search_transcriptions("test", db_session)
    assert len(result) == 0


def test_search_transcriptions_no_matches(db_session, multiple_transcriptions):
    """Test searching transcriptions with no matches."""
    result = search_transcriptions("nonexistent", db_session)
    assert len(result) == 0


def test_search_transcriptions_with_matches(
    db_session, multiple_transcriptions
):
    """Test searching transcriptions with matches."""
    result = search_transcriptions("audio1", db_session)

    assert len(result) == 1
    assert result[0]["audio_file_name"] == "audio1_ver_1.mp3"
    assert result[0]["transcribed_text"] == "First transcription"


def test_search_transcriptions_case_insensitive(
    db_session, multiple_transcriptions
):
    """Test that search is case insensitive."""
    result = search_transcriptions("AUDIO2", db_session)

    assert len(result) == 1
    assert result[0]["audio_file_name"] == "audio2_ver_1.mp3"
