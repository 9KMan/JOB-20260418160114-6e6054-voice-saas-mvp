import whisper
import numpy as np
from typing import Optional
import load_dotenv
import torch

from app.config import settings


class VoiceService:
    """Service for voice-to-text processing using Whisper AI."""

    _model = None

    @classmethod
    def get_model(cls):
        """Get or load the Whisper model (singleton pattern)."""
        if cls._model is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
            cls._model = whisper.load_model(
                settings.whisper_model,
                device=device
            )
        return cls._model

    @classmethod
    async def transcribe_audio(
        cls,
        audio_path: str,
        language: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio file to text.

        Args:
            audio_path: Path to the audio file
            language: Optional language code (e.g., 'en', 'zh')

        Returns:
            Dictionary with transcript, duration, and language
        """
        model = cls.get_model()

        # Load audio and pad/trim to handle various formats
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)

        # Make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Decode the audio
        options = whisper.DecodingOptions(language=language)
        result = whisper.decode(model, mel, options)

        # Get full audio duration
        audio_duration = len(audio) / whisper.audio.SAMPLE_RATE

        return {
            "transcript": result.text,
            "language": result.language,
            "duration": audio_duration,
            "language_probability": result.language_probability
        }

    @classmethod
    async def transcribe_from_array(
        cls,
        audio_array: np.ndarray,
        sample_rate: int,
        language: Optional[str] = None
    ) -> dict:
        """
        Transcribe audio from numpy array.

        Args:
            audio_array: NumPy array of audio data
            sample_rate: Sample rate of the audio
            language: Optional language code

        Returns:
            Dictionary with transcript and language info
        """
        model = cls.get_model()

        # Ensure audio is in the correct format
        if sample_rate != whisper.audio.SAMPLE_RATE:
            # Resample audio
            audio = whisper.pad_or_trim(audio_array)
        else:
            audio = whisper.pad_or_trim(audio_array)

        # Make log-Mel spectrogram
        mel = whisper.log_mel_spectrogram(audio).to(model.device)

        # Decode
        options = whisper.DecodingOptions(language=language)
        result = whisper.decode(model, mel, options)

        return {
            "transcript": result.text,
            "language": result.language,
            "language_probability": result.language_probability
        }