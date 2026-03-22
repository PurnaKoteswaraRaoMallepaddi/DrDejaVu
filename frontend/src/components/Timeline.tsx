import type { Consultation } from "../types";

interface TimelineProps {
  consultations: Consultation[];
}

export default function Timeline({ consultations }: TimelineProps) {
  if (consultations.length === 0) return null;

  return (
    <div className="timeline">
      <h3>Health Timeline</h3>
      <div className="timeline-track">
        {consultations.map((c, i) => (
          <div key={c.id} className="timeline-item">
            <div className="timeline-dot" />
            <div className="timeline-content">
              <div className="timeline-date">{c.consultation_date}</div>
              <div className="timeline-doctor">{c.doctor_name}</div>
              <p className="timeline-summary">
                {c.summary.slice(0, 150)}
                {c.summary.length > 150 ? "..." : ""}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
