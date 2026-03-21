import { useState } from "react";
import UploadPanel from "../components/UploadPanel";
import ConsultationList from "../components/ConsultationList";

const PATIENT_ID = "demo-patient-001";

export default function Upload() {
  const [refreshKey, setRefreshKey] = useState(0);

  return (
    <div className="upload-page">
      <div className="upload-container">
        <UploadPanel
          patientId={PATIENT_ID}
          onUploadComplete={() => setRefreshKey((k) => k + 1)}
        />
      </div>
      <aside className="sidebar">
        <ConsultationList patientId={PATIENT_ID} refreshKey={refreshKey} />
      </aside>
    </div>
  );
}
