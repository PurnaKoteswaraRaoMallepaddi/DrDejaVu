export interface Consultation {
  id: string;
  patient_id: string;
  doctor_name: string;
  consultation_date: string;
  transcript: string;
  summary: string;
  notes: string;
  created_at: string;
}

export interface TranscribeResult {
  consultation_id: string;
  transcript: string;
  summary: string;
  duration_seconds?: number;
}

export interface QueryResult {
  answer: string;
  sources: Source[];
}

export interface ChatResult {
  answer: string;
  audio_url?: string;
  sources: Source[];
}

export interface Source {
  consultation_id: string;
  consultation_date: string;
  doc_type: string;
  excerpt: string;
}

export interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  audio_url?: string;
  sources?: Source[];
  timestamp: Date;
}
