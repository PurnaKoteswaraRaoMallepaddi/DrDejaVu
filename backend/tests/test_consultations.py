from unittest.mock import AsyncMock, patch

from app.models.schemas import ConsultationResponse


@patch("app.routers.consultations.get_consultations", new_callable=AsyncMock)
def test_list_consultations(mock_get, client):
    mock_get.return_value = [
        ConsultationResponse(
            id="c1",
            patient_id="patient-001",
            doctor_name="Dr. Smith",
            consultation_date="2024-01-15",
            transcript="Sample transcript",
            summary="Sample summary",
            notes="",
            created_at="2024-01-15T10:00:00",
        )
    ]

    response = client.get("/api/consultations/patient-001")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["patient_id"] == "patient-001"
