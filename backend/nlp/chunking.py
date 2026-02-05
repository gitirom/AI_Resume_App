from chonkie import TextChunker
from typing import List, Dict, Optional
import re
import logging


logger = logging.getLogger(__name__)

class ChunkingService:
    def __init__(
            self,
            chunk_size: int = 400,
            chunk_overlap: int = 80,
            split_method: str = "sentence",
            min_chunk_length: int = 50,
            remove_duplicates: bool = True
        ):
        """
        Initialize Chunking Service

        Parameters
        ----------
        chunk_size : int
            Target token size per chunk ==> chunk_size = 12 tokens (≈ 12 words)  
                Ex: Chunk 1:
                    5G networks consume significant energy. Machine learning helps optimize power usage.

        chunk_overlap : int
            Overlap between chunks to preserve context ==> in the new chunk repeat the last 80 words from the prev chunk 
            
        split_method : str
            Splitting logic ("sentence" recommended)  ==> keep full sentences.

        min_chunk_length : int
            Remove very small chunks 

        remove_duplicates : bool
            Prevents storing repeated chunks.
        """

        self.min_chunk_length = min_chunk_length
        self.remove_duplicates = remove_duplicates

        self.chunker = TextChunker(
            chnuk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            split_method=split_method
        )

        def _clean_text(text: str) -> str:
            if not text:
                return ""
            
            text = re.sub(r"\s+", " ", text)   # Remove excessive whitespace

            text = re.sub(r"[•●▪►]+", " ", text)  # Remove common bullet characters

            text = text.replace("\uf0b7", " ")  # Remove weird unicode bullets
            return text.strip()
        
        def _chunk_text(self, text: str, source_type: str) -> List[dict]:
            if not text or not text.strip():
                logger.warning(f"Empty text received for {source_type}")
                return []
            
            cleaned_text = self._clean_text(text)

            raw_chunks = self.chunker.chunk_text(cleaned_text)

            processed_chunks = []
            seen_chunks = set()

            for idx, chunk in enumerate(raw_chunks):
                chunk = chunk.strip()
                if len(chunk) < self.min_chunk_length:
                    continue                         #Stop executing the current iteration immediately Jump to the next loop iteration
                if self.remove_duplicates:
                    if chunk in seen_chunks:
                        continue
                    seen_chunks.add(chunk)
                
                processed_chunks.append({
                    "chunk_text": chunk,
                    "chunk_index": idx,
                    "source": source_type
                })

            logger.info(f"{source_type.upper()} chunked into {len(processed_chunks)} chunks")
            return processed_chunks
        
        def chunk_resume(self, resume_text: str) -> List[Dict]:
            return self._chunk_text(resume_text, source_type="resume")
        
        def chunk_job_description(self, job_description: str) -> List[Dict]:
            return self._chunk_text(job_description, source_type="job")















"""
List[Dict] :
            [
                {
                    "chunk_text": "...",
                    "chunk_index": 0,
                    "source": "resume" | "job"
                }
            ]
"""
