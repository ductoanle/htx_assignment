from htx_transcriber.services.transcription_service import (
    get_all_transcriptions,
    search_transcriptions
)


def test_get_all_transcriptions_empty(db_session):
    """Test getting all transcriptions when database is empty."""
    result = get_all_transcriptions(db_session)
    assert len(result) == 0


def test_get_all_transcriptions_with_data(db_session, multiple_transcriptions):
    """Test getting all transcriptions when database has data."""
    result = get_all_transcriptions(db_session)

    assert len(result) == 3
    assert result[0]["audio_file_name"] == "audio3_ver_1.mp3"
    assert result[1]["audio_file_name"] == "audio2_ver_1.mp3"
    assert result[2]["audio_file_name"] == "audio1_ver_1.mp3"


def test_search_transcriptions_empty(db_session):
    """Test searching transcriptions when database is empty."""
    result = search_transcriptions("test", db_session)
    assert len(result) == 0


def test_search_transcriptions_no_matches(
    db_session, multiple_transcriptions
):
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
