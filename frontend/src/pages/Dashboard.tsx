import { useState, useCallback } from "react";
import ChatWindow from "../components/ChatWindow";
import VoiceRecorder from "../components/VoiceRecorder";
import ConsultationList from "../components/ConsultationList";
import { chatText, chatVoice } from "../services/api";
import type { ChatMessage } from "../types";

const PATIENT_ID = "demo-patient-001";

export default function Dashboard() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [textInput, setTextInput] = useState("");
  const [loading, setLoading] = useState(false);

  const addMessage = (msg: Omit<ChatMessage, "id" | "timestamp">) => {
    setMessages((prev) => [
      ...prev,
      { ...msg, id: crypto.randomUUID(), timestamp: new Date() },
    ]);
  };

  const handleTextSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (!textInput.trim() || loading) return;

      const question = textInput.trim();
      setTextInput("");
      addMessage({ role: "user", content: question });
      setLoading(true);

      try {
        const result = await chatText(PATIENT_ID, question);
        addMessage({
          role: "assistant",
          content: result.answer,
          audio_url: result.audio_url ?? undefined,
          sources: result.sources,
        });
      } catch {
        addMessage({
          role: "assistant",
          content: "Sorry, I encountered an error. Please try again.",
        });
      } finally {
        setLoading(false);
      }
    },
    [textInput, loading]
  );

  const handleVoiceSubmit = useCallback(
    async (blob: Blob) => {
      addMessage({ role: "user", content: "[Voice message sent]" });
      setLoading(true);

      try {
        console.log("[Dashboard] Sending voice to chat API...");
        const result = await chatVoice(blob, PATIENT_ID);
        console.log("[Dashboard] Chat response received:", {
          answerLength: result.answer.length,
          hasAudioUrl: !!result.audio_url,
          audioUrl: result.audio_url,
          sourcesCount: result.sources.length,
        });
        addMessage({
          role: "assistant",
          content: result.answer,
          audio_url: result.audio_url ?? undefined,
          sources: result.sources,
        });
      } catch (error) {
        console.error("[Dashboard] Voice chat failed:", error);
        addMessage({
          role: "assistant",
          content: "Sorry, I couldn't process your voice message.",
        });
      } finally {
        setLoading(false);
      }
    },
    [loading]
  );

  return (
    <div className="dashboard">
      <aside className="sidebar">
        <ConsultationList patientId={PATIENT_ID} />
      </aside>

      <main className="main-chat">
        <ChatWindow messages={messages} />

        <div className="input-area">
          <form onSubmit={handleTextSubmit} className="text-input-form">
            <input
              type="text"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder="Ask about your health history..."
              disabled={loading}
            />
            <button type="submit" className="btn btn-send" disabled={loading}>
              {loading ? "..." : "Send"}
            </button>
          </form>
          <VoiceRecorder onRecordingComplete={handleVoiceSubmit} disabled={loading} />
        </div>
      </main>
    </div>
  );
}
