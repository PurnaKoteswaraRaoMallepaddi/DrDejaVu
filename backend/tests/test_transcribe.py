from unittest.mock import AsyncMock, patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.routers.transcribe.transcribe_audio", new_callable=AsyncMock)
@patch("app.routers.transcribe.summarize_transcript", new_callable=AsyncMock)
@patch("app.routers.transcribe.index_consultation", new_callable=AsyncMock)
@patch("app.routers.transcribe.save_consultation", new_callable=AsyncMock)
def test_transcribe_endpoint(
    mock_save, mock_index, mock_summarize, mock_transcribe, client
):
    mock_transcribe.return_value = "Doctor said reduce salt intake."
    mock_summarize.return_value = "**Lifestyle Advice**: Reduce salt intake."

    response = client.post(
        "/api/transcribe",
        files={"audio": ("test.wav", b"fake-audio-bytes", "audio/wav")},
        data={"patient_id": "patient-001", "doctor_name": "Dr. Smith"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["transcript"] == "Doctor said reduce salt intake."
    assert "consultation_id" in data
    mock_transcribe.assert_called_once()
    mock_index.assert_called_once()
