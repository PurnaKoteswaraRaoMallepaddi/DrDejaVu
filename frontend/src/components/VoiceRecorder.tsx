import { useVoiceRecorder } from "../hooks/useVoiceRecorder";

interface VoiceRecorderProps {
  onRecordingComplete: (blob: Blob) => void;
  disabled?: boolean;
}

export default function VoiceRecorder({
  onRecordingComplete,
  disabled,
}: VoiceRecorderProps) {
  const { isRecording, audioBlob, startRecording, stopRecording, clearRecording } =
    useVoiceRecorder();

  const handleStop = () => {
    stopRecording();
  };

  const handleSend = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob);
      clearRecording();
    }
  };

  return (
    <div className="voice-recorder">
      {!isRecording && !audioBlob && (
        <button
          className="btn btn-record"
          onClick={startRecording}
          disabled={disabled}
        >
          <span className="mic-icon">&#127908;</span> Hold to Speak
        </button>
      )}

      {isRecording && (
        <button className="btn btn-recording" onClick={handleStop}>
          <span className="pulse" /> Stop Recording
        </button>
      )}

      {audioBlob && !isRecording && (
        <div className="recording-preview">
          <audio src={URL.createObjectURL(audioBlob)} controls />
          <div className="recording-actions">
            <button className="btn btn-send" onClick={handleSend}>
              Send
            </button>
            <button className="btn btn-discard" onClick={clearRecording}>
              Discard
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
