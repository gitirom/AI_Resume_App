from chonkie import SentenceChunker
from typing import List, Dict
import re
import logging

logger = logging.getLogger(__name__)


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = 400,
        chunk_overlap: int = 80,
        min_chunk_length: int = 50,
        remove_duplicates: bool = True
    ):

        self.min_chunk_length = min_chunk_length
        self.remove_duplicates = remove_duplicates

        self.chunker = SentenceChunker(
            chunk_size=chunk_size,  
            chunk_overlap=chunk_overlap,
        )

    def _clean_text(self, text: str) -> str:
        if not text:
            return ""

        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"[•●▪►]+", " ", text)
        text = text.replace("\uf0b7", " ")

        return text.strip()

    def _chunk_text(self, text: str, source_type: str) -> List[Dict]:

        if not text or not text.strip():
            logger.warning(f"Empty text received for {source_type}")
            return []

        cleaned_text = self._clean_text(text)

        raw_chunks = self.chunker.chunk(cleaned_text)

        processed_chunks = []
        seen_chunks = set()

        for idx, chunk in enumerate(raw_chunks):

            chunk_text = chunk.text.strip()

            if len(chunk_text) < self.min_chunk_length:
                continue

            if self.remove_duplicates:
                if chunk_text in seen_chunks:
                    continue
                seen_chunks.add(chunk_text)

            processed_chunks.append({
                "chunk_text": chunk_text,
                "chunk_index": idx,
                "source": source_type
            })

        logger.info(f"{source_type.upper()} chunked into {len(processed_chunks)} chunks")

        return processed_chunks


    def chunk_resume(self, resume_text: str) -> List[Dict]:
        return self._chunk_text(resume_text, "resume")

    def chunk_job_description(self, job_description: str) -> List[Dict]:
        return self._chunk_text(job_description, "job")
