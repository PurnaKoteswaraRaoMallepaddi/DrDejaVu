import axios from "axios";
import type {
  Consultation,
  TranscribeResult,
  QueryResult,
  ChatResult,
} from "../types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "",
});

export async function transcribeAudio(
  file: File | Blob,
  patientId: string,
  doctorName?: string,
  consultationDate?: string
): Promise<TranscribeResult> {
  const form = new FormData();
  form.append("audio", file);
  form.append("patient_id", patientId);
  if (doctorName) form.append("doctor_name", doctorName);
  if (consultationDate) form.append("consultation_date", consultationDate);

  const { data } = await api.post<TranscribeResult>("/api/transcribe", form);
  return data;
}

export async function queryHistory(
  patientId: string,
  question: string
): Promise<QueryResult> {
  const { data } = await api.post<QueryResult>("/api/query", {
    patient_id: patientId,
    question,
  });
  return data;
}

export async function chatText(
  patientId: string,
  question: string,
  voiceResponse = true
): Promise<ChatResult> {
  const { data } = await api.post<ChatResult>("/api/chat/text", {
    patient_id: patientId,
    question,
    voice_response: voiceResponse,
  });
  return data;
}

export async function chatVoice(
  audioBlob: Blob,
  patientId: string
): Promise<ChatResult> {
  const form = new FormData();
  form.append("audio", audioBlob, "recording.wav");
  form.append("patient_id", patientId);

  const { data } = await api.post<ChatResult>("/api/chat/voice", form);
  return data;
}

export async function getConsultations(
  patientId: string
): Promise<Consultation[]> {
  const { data } = await api.get<Consultation[]>(
    `/api/consultations/${patientId}`
  );
  return data;
}

export default api;
