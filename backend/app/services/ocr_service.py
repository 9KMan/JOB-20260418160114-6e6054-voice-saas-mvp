import easyocr
import numpy as np
from PIL import Image
from typing import List, Optional

from app.config import settings


class OCRService:
    """Service for document/text extraction using EasyOCR."""

    _reader = None

    @classmethod
    def get_reader(cls):
        """Get or initialize the EasyOCR reader (singleton pattern)."""
        if cls._reader is None:
            languages = settings.ocr_languages.split(",")
            cls._reader = easyocr.Reader(
                languages,
                gpu=True,
                model_storage_directory=None,
                download_enabled=True
            )
        return cls._reader

    @classmethod
    async def extract_text_from_image(cls, image_path: str) -> dict:
        """
        Extract text from an image file.

        Args:
            image_path: Path to the image file

        Returns:
            Dictionary with extracted text, bounding boxes, and confidence
        """
        reader = cls.get_reader()

        # Read text from image
        results = reader.readtext(image_path)

        # Process results
        extracted_data = cls._process_results(results)

        return extracted_data

    @classmethod
    async def extract_text_from_array(cls, image_array: np.ndarray) -> dict:
        """
        Extract text from a numpy image array.

        Args:
            image_array: NumPy array representing an image

        Returns:
            Dictionary with extracted text and confidence
        """
        reader = cls.get_reader()

        # Read text from numpy array
        results = reader.readtext(image_array)

        # Process results
        extracted_data = cls._process_results(results)

        return extracted_data

    @classmethod
    def _process_results(cls, results: List) -> dict:
        """
        Process EasyOCR results into structured format.

        Args:
            results: List of EasyOCR result tuples

        Returns:
            Structured dictionary with text, confidence, and bounding boxes
        """
        extracted_texts = []
        bounding_boxes = []
        confidences = []

        for bbox, text, confidence in results:
            if text.strip():  # Only include non-empty text
                extracted_texts.append(text)
                bounding_boxes.append(bbox)
                confidences.append(confidence)

        # Calculate average confidence
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        return {
            "text": "\n".join(extracted_texts),
            "full_text": " ".join(extracted_texts),
            "bounding_boxes": bounding_boxes,
            "confidence": avg_confidence,
            "num_text_regions": len(extracted_texts)
        }

    @classmethod
    async def extract_text_from_pil_image(cls, image: Image.Image) -> dict:
        """
        Extract text from a PIL Image.

        Args:
            image: PIL Image object

        Returns:
            Dictionary with extracted text and confidence
        """
        # Convert PIL image to numpy array
        image_array = np.array(image)
        return await cls.extract_text_from_array(image_array)