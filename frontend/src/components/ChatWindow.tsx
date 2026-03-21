import type { ChatMessage } from "../types";
import AudioPlayer from "./AudioPlayer";

interface ChatWindowProps {
  messages: ChatMessage[];
}

export default function ChatWindow({ messages }: ChatWindowProps) {
  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="chat-empty">
          <h3>Welcome to DrDejaVu</h3>
          <p>
            Ask about your health history using voice or text. For example:
          </p>
          <ul>
            <li>"What did my doctor say about my blood pressure last year?"</li>
            <li>"How has my diet advice changed over time?"</li>
            <li>"Compare my last two consultation summaries"</li>
          </ul>
        </div>
      )}

      {messages.map((msg) => (
        <div key={msg.id} className={`chat-message chat-${msg.role}`}>
          <div className="message-header">
            <strong>{msg.role === "user" ? "You" : "DrDejaVu"}</strong>
            <span className="timestamp">
              {msg.timestamp.toLocaleTimeString()}
            </span>
          </div>
          <div className="message-body">{msg.content}</div>

          {msg.audio_url && <AudioPlayer src={msg.audio_url} />}

          {msg.sources && msg.sources.length > 0 && (
            <div className="message-sources">
              <details>
                <summary>
                  Sources ({msg.sources.length} consultation records)
                </summary>
                <ul>
                  {msg.sources.map((s, i) => (
                    <li key={i}>
                      <strong>{s.consultation_date}</strong> ({s.doc_type}):{" "}
                      {s.excerpt}
                    </li>
                  ))}
                </ul>
              </details>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
