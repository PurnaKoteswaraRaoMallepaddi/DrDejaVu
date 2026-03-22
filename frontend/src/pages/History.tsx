import { useEffect, useState } from "react";
import Timeline from "../components/Timeline";
import { getConsultations } from "../services/api";
import type { Consultation } from "../types";

const PATIENT_ID = "demo-patient-001";

export default function History() {
  const [consultations, setConsultations] = useState<Consultation[]>([]);

  useEffect(() => {
    getConsultations(PATIENT_ID)
      .then(setConsultations)
      .catch(console.error);
  }, []);

  return (
    <div className="history-page">
      <h2>Consultation History</h2>
      <Timeline consultations={consultations} />

      <div className="consultation-details">
        {consultations.map((c) => (
          <div key={c.id} className="detail-card">
            <h3>
              {c.consultation_date} — {c.doctor_name || "Unknown Doctor"}
            </h3>
            <div className="detail-section">
              <h4>Summary</h4>
              <p>{c.summary}</p>
            </div>
            <details>
              <summary>Full Transcript</summary>
              <p className="transcript-text">{c.transcript}</p>
            </details>
          </div>
        ))}
      </div>
    </div>
  );
}
