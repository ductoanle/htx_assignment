import whisper
from pathlib import Path


class TranscriptionError(Exception):
    pass


class WhisperProcessor:
    def __init__(self, model_name: str = "tiny"):
        try:
            self.model = whisper.load_model(model_name)
        except Exception as e:
            raise TranscriptionError(f"Failed to load Whisper model: {str(e)}")

    def transcribe_audio(self, audio_path: str | Path) -> str:
        try:
            # Load and pre-process the audio
            audio = whisper.load_audio(str(audio_path))
            audio = whisper.pad_or_trim(audio)

            # Create mel spectrogram
            mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

            # Transcribe
            options = whisper.DecodingOptions(fp16=False)
            result = whisper.decode(self.model, mel, options)
            # Access the text attribute of the first result
            return result[0].text if isinstance(result, list) else result.text
        except Exception as e:
            raise TranscriptionError(f"Transcription failed: {str(e)}")


processor = WhisperProcessor()


def transcribe_audio(audio_path: str | Path) -> str:
    """Transcribe audio file using Whisper model.
    Args:
        audio_path: Path to audio file
    Returns:
        Transcribed text as a string
    Raises:
        TranscriptionError: If transcription fails
    """
    return processor.transcribe_audio(audio_path)
