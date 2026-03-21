import { useState, useRef } from "react";
import { transcribeAudio } from "../services/api";

interface UploadPanelProps {
  patientId: string;
  onUploadComplete: () => void;
}

export default function UploadPanel({
  patientId,
  onUploadComplete,
}: UploadPanelProps) {
  const [doctorName, setDoctorName] = useState("");
  const [consultDate, setConsultDate] = useState("");
  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const handleUpload = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file) return;

    setUploading(true);
    setResult(null);
    try {
      const res = await transcribeAudio(file, patientId, doctorName, consultDate);
      setResult(`Transcribed and indexed! Summary:\n${res.summary}`);
      onUploadComplete();
    } catch (err) {
      setResult("Upload failed. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-panel">
      <h3>Upload Consultation Audio</h3>
      <div className="form-group">
        <label>Audio File (wav, mp3, m4a)</label>
        <input ref={fileRef} type="file" accept=".wav,.mp3,.m4a" />
      </div>
      <div className="form-group">
        <label>Doctor Name</label>
        <input
          type="text"
          value={doctorName}
          onChange={(e) => setDoctorName(e.target.value)}
          placeholder="Dr. Smith"
        />
      </div>
      <div className="form-group">
        <label>Consultation Date</label>
        <input
          type="date"
          value={consultDate}
          onChange={(e) => setConsultDate(e.target.value)}
        />
      </div>
      <button
        className="btn btn-upload"
        onClick={handleUpload}
        disabled={uploading}
      >
        {uploading ? "Processing..." : "Upload & Transcribe"}
      </button>
      {result && <div className="upload-result">{result}</div>}
    </div>
  );
}
