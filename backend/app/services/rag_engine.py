"""RAG Engine — ChromaDB-based retrieval + Eigen AI generation.

Indexes consultation transcripts and summaries as vector embeddings,
retrieves relevant records for patient queries, and generates
comparative answers using the Eigen chat model.
"""

from app.db.vector_store import get_collection
from app.models.schemas import QueryResponse
from app.services.eigen_chat import chat_completion


async def index_consultation(
    consultation_id: str,
    patient_id: str,
    transcript: str,
    summary: str,
    consultation_date: str,
) -> None:
    """Index a consultation transcript and summary into ChromaDB."""
    collection = get_collection()

    # Index both transcript and summary as separate documents
    # with shared metadata for filtering
    documents = []
    ids = []
    metadatas = []

    # Split transcript into chunks for better retrieval
    chunks = _chunk_text(transcript, max_chars=1000)
    for i, chunk in enumerate(chunks):
        documents.append(chunk)
        ids.append(f"{consultation_id}_transcript_{i}")
        metadatas.append({
            "consultation_id": consultation_id,
            "patient_id": patient_id,
            "consultation_date": consultation_date,
            "doc_type": "transcript",
            "chunk_index": i,
        })

    # Add summary as a single document
    documents.append(summary)
    ids.append(f"{consultation_id}_summary")
    metadatas.append({
        "consultation_id": consultation_id,
        "patient_id": patient_id,
        "consultation_date": consultation_date,
        "doc_type": "summary",
        "chunk_index": 0,
    })

    collection.add(documents=documents, ids=ids, metadatas=metadatas)


async def query_consultations(patient_id: str, question: str) -> QueryResponse:
    """Query patient history using RAG: retrieve context + generate answer."""
    collection = get_collection()

    # Retrieve relevant documents for this patient
    results = collection.query(
        query_texts=[question],
        n_results=10,
        where={"patient_id": patient_id},
    )

    # Build context from retrieved documents
    sources = []
    context_parts = []

    if results["documents"] and results["documents"][0]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context_parts.append(
                f"[{meta['consultation_date']} - {meta['doc_type']}]\n{doc}"
            )
            sources.append({
                "consultation_id": meta["consultation_id"],
                "consultation_date": meta["consultation_date"],
                "doc_type": meta["doc_type"],
                "excerpt": doc[:200],
            })

    patient_context = "\n\n---\n\n".join(context_parts)

    # Generate answer using Eigen chat model with RAG context
    answer = await chat_completion(
        messages=[{"role": "user", "content": question}],
        patient_context=patient_context,
    )

    return QueryResponse(answer=answer, sources=sources)


def _chunk_text(text: str, max_chars: int = 1000) -> list[str]:
    """Split text into chunks at sentence boundaries."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    current = ""

    for sentence in text.replace("\n", " ").split(". "):
        candidate = f"{current}. {sentence}" if current else sentence
        if len(candidate) > max_chars and current:
            chunks.append(current.strip())
            current = sentence
        else:
            current = candidate

    if current.strip():
        chunks.append(current.strip())

    return chunks if chunks else [text]
