# DrDejaVu
# 🏥 Voice-First Longitudinal Health Memory

> A voice-powered RAG system for tracking and comparing long-term patient progress across multiple consultations, built on the **Boson AI** and **Eigen AI** stack.

---

## 📐 High-Level Architecture

This solution follows a **Voice-RAG (Retrieval-Augmented Generation)** pattern where past consultations are transcribed, indexed, and retrieved as context for a conversational AI.
```
Audio Input → Transcription → Vector DB → Query & Compare → Voice Response
```

| Step | Description |
|------|-------------|
| **1. Data Ingestion** | Audio from every consultation is processed into structured text |
| **2. Knowledge Indexing** | Transcriptions are stored in a vector database for context-aware retrieval |
| **3. Query & Comparison** | Patient asks a question; system retrieves relevant snippets across time to provide a comparative answer |

---

## 🛠️ Implementation

### A. Transcription Engine — `Higgs Audio ASR V3.0`

Every doctor-patient consultation is recorded and transcribed into a searchable history.

- **Accuracy:** 9.12% WER with low latency
- **Input formats:** `wav`, `mp3`, `m4a`
- **Pipeline:** Transcribe consultation → summarize key takeaways (Diagnoses, Medications, Lifestyle Advice) using a secondary LLM (e.g. Llama 3.3 or Qwen 3)

---

### B. Understanding & Comparison — `Higgs Audio Understanding V3.5`

Powers deep analysis when a patient asks *"How is my progress compared to 2 years ago?"*

- Designed for advanced audio understanding and captioning
- Analyzes **tone and sentiment** of the patient's voice across years to detect well-being improvements not captured in text alone

---

### C. Conversational Interface — `Higgs Audio V2.5`

The primary interaction layer — the patient can both speak and listen.

| Feature | Detail |
|---------|--------|
| ⚡ Low Latency | ~150ms first-token latency for natural, real-time conversation |
| 🌍 Multilingual | English, Spanish, German, French, Italian |
| 🎙️ Voice Cloning | Clone the doctor's voice (with permission) using a short reference clip for a familiar, trustworthy experience |

---

## 🔄 Patient Query Workflow
```
1. Patient sends voice note:
   "What did the doctor say about my diet two years ago, and have I improved?"
         │
         ▼
2. Higgs ASR V3.0 transcribes the query
         │
         ▼
3. Vector DB retrieves relevant consultation transcripts
   (from 2 years ago + most recent)
         │
         ▼
4. Context is constructed:
   Old advice: "Reduce salt intake"
   New data:   "Blood pressure is lower"
         │
         ▼
5. Higgs Audio V2.5 generates & speaks the response:
   "Two years ago, your doctor advised reducing salt to manage your
    hypertension. Your latest notes show your levels have stabilized,
    suggesting your new eating habits are working."
```

---

## 🏆 Why This Fits the Hackathon

This project directly addresses the **"Voice-chat with RAG/info retrieval"** track, leveraging the core strengths of the Boson/Eigen stack:

- ✅ High-speed inference
- ✅ Low-latency audio generation
- ✅ Sophisticated semantic understanding

---

## 📦 Tech Stack

| Component | Tool |
|-----------|------|
| Speech-to-Text | Higgs Audio ASR V3.0 |
| Audio Understanding | Higgs Audio Understanding V3.5 |
| Conversational AI | Higgs Audio V2.5 |
| Vector Database | *(your choice — e.g. Pinecone, Weaviate, Chroma)* |
| Summarization LLM | Llama 3.3 / Qwen 3 |
