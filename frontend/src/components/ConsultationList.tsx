import { useEffect, useState } from "react";
import type { Consultation } from "../types";
import { getConsultations } from "../services/api";

interface ConsultationListProps {
  patientId: string;
  refreshKey?: number;
}

export default function ConsultationList({
  patientId,
  refreshKey,
}: ConsultationListProps) {
  const [consultations, setConsultations] = useState<Consultation[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!patientId) return;
    setLoading(true);
    getConsultations(patientId)
      .then(setConsultations)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [patientId, refreshKey]);

  if (loading) return <div className="sidebar-loading">Loading...</div>;

  return (
    <div className="consultation-list">
      <h3>Past Consultations</h3>
      {consultations.length === 0 && (
        <p className="no-data">No consultations yet. Upload one to get started.</p>
      )}
      {consultations.map((c) => (
        <div key={c.id} className="consultation-card">
          <div className="card-date">{c.consultation_date}</div>
          <div className="card-doctor">{c.doctor_name || "Unknown Doctor"}</div>
          <details>
            <summary>Summary</summary>
            <p>{c.summary}</p>
          </details>
        </div>
      ))}
    </div>
  );
}
