"""
Stage 2 of the pipeline: splitting documents into chunks.

Milestone 3 chunking strategy for the campus_life corpus.

The campus_life corpus contains short posts that usually focus on one main
topic. During Milestone 1, I observed that useful information is normally
contained in one sentence, one paragraph, or within the short post as a whole.

The starter chunker used fixed 800-character windows. Because almost all of
the campus_life documents are shorter than 800 characters, the baseline
produced 88 documents and 88 chunks.

For my Milestone 3 strategy, I intentionally keep each campus_life document
together as one chunk. This avoids splitting related information across
multiple chunks and allows each retrieved chunk to stand on its own.

The original fallback_split function is kept below for comparison.
"""

from dataclasses import dataclass

import config
from ingest import Document

@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"

def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker.

    This uses fixed-size character windows with overlap. It is kept so the
    Milestone 3 strategy can be compared with the original starter behavior.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []

    for doc in documents:
        start = 0
        index = 0

        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()

            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1

            start += chunk_size - overlap

    return chunks

def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split campus_life documents using one complete post per chunk.

    I chose this strategy because the campus_life documents are short posts
    that normally focus on one topic. Keeping each document together preserves
    the context of the post and avoids splitting useful sentences or
    paragraphs across different chunks.

    There is no overlap because each document is already a separate,
    self-contained post.
    """
    chunks: list[Chunk] = []

    for doc in documents:
        text = doc.text.strip()

        if not text:
            continue

        chunks.append(
            Chunk(
                text=text,
                source=doc.source,
                index=0,
                produced_by="chunker.py::split_documents",
            )
        )

    return chunks

def describe(chunks: list[Chunk]) -> str:
    """Return a one-line summary of the chunks produced."""

    if not chunks:
        return "0 chunks"

    lengths = [len(c.text) for c in chunks]

    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )

if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))