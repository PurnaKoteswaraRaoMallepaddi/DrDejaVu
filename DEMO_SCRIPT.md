# DrDejaVu — Hackathon Demo Script

**Total Time: ~7 minutes**
**Presenters: [Your Names]**
**Tip: Pre-load consultations 1–4 (Dr. Sharma) + 6 (Cardiologist) + 7 (Nutritionist) before demo. Upload consultation 5 and consultation 8 live.**

---

## ACT 1 — THE HOOK (30 seconds)

> **[SPEAKER 1 — Start with the screen OFF or on a blank slide]**
>
> "Raise your hand if you've ever walked out of a doctor's office and forgotten half of what they said."
>
> *[Pause — let hands go up]*
>
> "Now imagine you're Ramesh — 52, just diagnosed with Type 2 Diabetes, three new medications, and a head full of fear because his father was on insulin for decades. Six months later, his doctor says his numbers improved. A year later, a medication gets reduced. But Ramesh can't remember — *was my glucose 152 or 189? Did the doctor say cut salt or cut sugar? Am I actually getting better?*"
>
> "And it gets worse — Ramesh doesn't just see one doctor. He has an internist, a cardiologist, a nutritionist, an eye doctor. Each one gives him critical advice, but **none of them know what the others said**. And Ramesh definitely can't remember it all."
>
> "Patients lose their medical memory between visits. And that memory gap kills compliance, kills confidence, and kills outcomes."
>
> "We built **DrDejaVu** — your AI doctor's memory that listens, remembers, and *speaks back in your doctor's own voice*."

---

## ACT 2 — THE LIVE DEMO (3 minutes)

### Scene 1: Show Pre-loaded Consultations — Multiple Doctors (30 sec)

> **[Switch to the app — Dashboard page]**
>
> "Ramesh has been seeing **multiple doctors** over three years. Look at this sidebar — we have consultations from **Dr. Ananya Sharma** his internist, **Dr. Vikram Mehta** his cardiologist, and **Dr. Priya Nair** his nutritionist. Six visits, three specialists, all in one place."
>
> **[Click through the consultation sidebar — point out different doctor names and dates spanning Jan 2023 to Nov 2024]**
>
> "Each consultation was recorded as audio. Our system used **Eigen's Higgs ASR V3.0** — which has a 9.12% word error rate — to transcribe every word. Then **gpt-oss-120b** automatically extracted diagnoses, medications, lifestyle advice, and key health metrics into structured summaries. And it doesn't matter which doctor it came from — it all goes into Ramesh's unified health memory."

### Scene 2: Upload a NEW Consultation — LIVE (45 sec)

> **[Navigate to /upload]**
>
> "Today is February 2026. Ramesh just had his latest appointment. Let's upload it — live."
>
> **[Select consultation_5_remission audio file. Enter: Doctor = Dr. Ananya Sharma, Date = Feb 17, 2026. Click Upload.]**
>
> "Watch what happens. The audio hits our FastAPI backend. Higgs ASR V3.0 transcribes it in seconds. Then gpt-oss-120b generates a structured medical summary. And finally, the transcript is chunked into semantic segments and indexed into **ChromaDB** as vector embeddings for instant retrieval."
>
> **[Show the transcript + summary appearing on screen]**
>
> "In one click, three years of medical context are now searchable by voice."

### Scene 3: Voice Q&A — The Magic Moment (60 sec)

> **[Navigate back to Dashboard. Click the microphone button.]**
>
> **[Speak into mic]:** *"How has my blood sugar improved since I was first diagnosed?"*
>
> **[Wait for response]**
>
> "Here's where our **RAG pipeline** shines. The question gets transcribed by Higgs ASR. Then it's embedded and matched against Ramesh's consultation history using **cosine similarity search** across ChromaDB — pulling the top 10 most relevant chunks from ALL five consultations."
>
> **[Point to the AI response on screen showing the comparative answer]**
>
> "Look at this answer — it's not generic. It references *specific numbers* from *specific dates*: 'Your HbA1c dropped from 8.4% in January 2023 to 5.4% in February 2026. Your fasting glucose went from 189 to 94.' And look — it cites the source consultations."
>
> **[Click the audio play button on the response]**
>
> "And now listen — that answer is spoken back using **Eigen's Higgs Audio V2.5** with **voice cloning**. We captured Dr. Sharma's voice profile from the consultation recordings, and the AI response is delivered in *her* voice. Ramesh doesn't hear a robot — he hears his doctor reassuring him."
>
> *[Let the voice play for a few seconds — this is the wow moment]*

### Scene 4: Cross-Doctor Query — The Killer Feature (45 sec)

> **[Type in the chat box]:** *"What did my cardiologist say about my cholesterol, and did my nutritionist's diet plan help?"*
>
> **[Wait for response]**
>
> "This is the moment. Watch — the RAG engine pulls from **three different doctors** to build one coherent answer."
>
> **[Point to the response]**
>
> "It says: 'Dr. Mehta, your cardiologist, flagged your LDL at 158 with an unfavorable HDL ratio in April 2023 and ordered a coronary calcium score. Dr. Nair, your nutritionist, put you on the plate method — vegetables first, swap white rice for millets, twelve-hour overnight fast. By March 2024, Dr. Sharma confirmed your LDL dropped to 94 and HDL jumped to 47. The diet plan clearly worked.'"
>
> "Three doctors. Three specialties. One unified answer. **No patient can do this from memory.** And no single doctor has this complete picture either — but DrDejaVu does."

### Scene 5: Ask About Medications — Text (30 sec)

> **[Type in the chat box]:** *"What medications have I stopped taking?"*
>
> **[Show the response]**
>
> "Instantly, the system cross-references multiple consultations: 'You were originally on Metformin, Lisinopril, and Atorvastatin. Dr. Mehta also added low-dose Aspirin. Lisinopril was stopped in March 2024 when your blood pressure normalized. Metformin was discontinued in February 2026 after your diabetes entered remission. You currently take Atorvastatin and Aspirin.'"
>
> "Three years of medication history across multiple specialists — recalled in two seconds."

### Scene 6: Upload from a NEW Specialist — LIVE (45 sec)

> **[Navigate to /upload]**
>
> "But Ramesh doesn't just see one type of doctor. He just had his annual diabetic eye screening with **Dr. Sunita Reddy, an ophthalmologist**. Let's upload that right now."
>
> **[Select consultation_8_ophthalmologist audio file. Enter: Doctor = Dr. Sunita Reddy, Date = May 15, 2024. Click Upload.]**
>
> "Same pipeline — ASR transcribes, LLM summarizes, ChromaDB indexes — but now from a completely different specialist. Cardiology, nutrition, internal medicine, ophthalmology — all flowing into one patient memory."
>
> **[Show the transcript + summary appearing on screen]**
>
> **[Navigate back to Dashboard. Type]:** *"Did my eye doctor find any problems related to diabetes?"*
>
> **[Show the response]**
>
> "Instantly: 'Dr. Reddy found no signs of diabetic retinopathy in your May 2024 exam. Your retinal blood vessels are healthy with no microaneurysms or macular edema. She recommends annual screening regardless of your remission status.' Ramesh can now recall ANY doctor's advice — not just his primary physician."

### Scene 7: History Timeline (15 sec)

> **[Navigate to /history]**
>
> "And for the full picture — the History page shows Ramesh's entire health journey as a timeline. Every consultation, every doctor, every summary — expandable with full transcripts. Dr. Sharma, Dr. Mehta, Dr. Nair, Dr. Reddy — all on one unified timeline. A multi-specialist longitudinal health record, built entirely from voice."

---

## ACT 3 — THE TECH (60 seconds)

> **[Show architecture slide or speak over the app]**
>
> "Let me break down what's under the hood — because we're using **four Eigen AI models** working in concert:"
>
> | Model | What It Does |
> |-------|-------------|
> | **Higgs ASR V3.0** | Transcribes doctor-patient conversations with medical-grade accuracy |
> | **Higgs Audio V2.5** | Generates voice responses **cloned to sound like the patient's doctor** — ~150ms first-token latency |
> | **Higgs Audio Understanding V3.5** | Analyzes the patient's tone and emotional state from their voice — enabling questions like *"Am I less anxious than last year?"* |
> | **gpt-oss-120b** | Powers summarization AND the RAG chat — extracting structured medical data and generating contextual, comparative answers |
>
> "Our stack is **React + TypeScript** on the frontend, **FastAPI** on the backend, **ChromaDB** for vector storage with cosine similarity search, and **SQLite** for metadata. The whole thing runs in **Docker Compose** — one command to deploy."
>
> "The RAG pipeline uses a **dual-indexing strategy** — we chunk transcripts into ~1000-character semantic segments AND index full summaries. This means the system can answer both granular questions like *'What was my exact LDL last March?'* and broad questions like *'Am I getting healthier?'*"

---

## ACT 4 — THE VISION & IMPACT (30 seconds)

> "DrDejaVu isn't just a chatbot. It's a **longitudinal health memory** that grows with every visit."
>
> **Use cases beyond the demo:**
> - **Chronic disease management** — Diabetes, hypertension, cancer follow-ups
> - **Elderly patients** — Who genuinely forget what their doctor said
> - **Caregiver coordination** — A daughter caring for aging parents can ask: *"What did Mom's oncologist say about her last scan?"*
> - **Multi-specialist tracking** — Cardiologist says one thing, endocrinologist says another — DrDejaVu remembers both
> - **Mental health** — Voice sentiment analysis tracks emotional wellbeing over time
>
> "Every year, **80% of medical information** given to patients is forgotten immediately. Half of what's remembered is remembered incorrectly. DrDejaVu fixes that — with voice in, voice out, and perfect memory in between."

---

## ACT 5 — THE CLOSE (15 seconds)

> "We built DrDejaVu in [X hours] using four Eigen AI models, ~1,300 lines of code, and one simple belief: **your doctor's advice shouldn't expire when you walk out the door.**"
>
> "Thank you."

---

## PRE-DEMO CHECKLIST

- [ ] Backend running (`docker-compose up`)
- [ ] Frontend accessible at `http://localhost:5173`
- [ ] 6 consultations pre-uploaded (1–4 Dr. Sharma, 6 Cardiologist, 7 Nutritionist)
- [ ] Consultation 5 (remission) audio file ready on desktop for live upload
- [ ] Consultation 8 (ophthalmologist) audio file ready on desktop for live upload
- [ ] Microphone tested and working in browser
- [ ] Browser audio permissions granted
- [ ] Eigen API key set in `.env` and working
- [ ] Screen resolution set for audience visibility (zoom browser to 125%)
- [ ] Practice the voice question 2x before going live

## BACKUP PLAN

If live voice recording fails during demo:
1. Switch to typing the question in text chat — the RAG answer is identical
2. Say: *"Let me type this one — same pipeline, same answer, the mic just needs a moment"*
3. Still play the audio response from the text answer (voice_response=true)

If API is slow:
1. Have a pre-cached response screenshot ready
2. Say: *"While that processes — let me show you what the answer looks like"*
3. Show the screenshot, then switch back when the live response arrives

---

## JUDGE-WINNING TALKING POINTS

If judges ask questions, weave in these points:

**"Why voice?"**
> "Because healthcare happens in conversation, not in text boxes. 65% of adults over 50 prefer speaking to typing. And voice captures nuance — tone, hesitation, emotion — that text never will."

**"How is this different from just recording appointments?"**
> "Recordings are passive. You still have to listen to a 30-minute audio to find one answer. DrDejaVu is *active memory* — it indexes, cross-references, and synthesizes across years of visits and across multiple doctors. Ask one question that spans your cardiologist, nutritionist, and internist — get one precise answer in seconds. No single doctor can do that."

**"What about privacy/HIPAA?"**
> "All data stays local — SQLite + ChromaDB on your own infrastructure. No patient data leaves the system except for API calls to Eigen's models, which can be deployed on-premise. The architecture is designed for self-hosted deployment."

**"Why voice cloning?"**
> "Trust. Patients trust their doctor's voice. When a follow-up answer comes in Dr. Sharma's voice, Ramesh doesn't feel like he's talking to a machine — he feels like he's getting a callback from his doctor. That familiarity drives compliance."

**"What about the Eigen models specifically?"**
> "We evaluated the tradeoffs carefully. Higgs ASR V3.0 gives us medical-grade transcription accuracy. Higgs Audio V2.5's 150-millisecond first-token latency makes voice responses feel conversational, not robotic. The Understanding model lets us track emotional health longitudinally. And gpt-oss-120b handles both summarization and chat in a single model, reducing complexity. The four models together create a complete voice-AI loop that no single model could achieve alone."

**"How does multi-doctor work?"**
> "Every consultation is stored with the doctor's name and specialty. When Ramesh asks a question, the RAG engine doesn't care which doctor it came from — it searches ALL consultations semantically. So when he asks 'Did the diet plan help my cholesterol?', it pulls the nutritionist's diet advice AND the cardiologist's cholesterol concern AND the internist's lab results — connecting dots that no single doctor could connect alone. It's like having a medical coordinator that never forgets."

**"What's next?"**
> "Three things: First, integrating with EHR systems like Epic and Cerner so consultations are captured automatically. Second, multi-language support — Higgs V2.5 already supports Spanish, German, French, and Italian. Third, a mobile app so patients can ask questions from home, not just the browser."
