from unittest.mock import AsyncMock, patch

from app.models.schemas import QueryResponse


@patch("app.routers.query.query_consultations", new_callable=AsyncMock)
def test_query_endpoint(mock_query, client):
    mock_query.return_value = QueryResponse(
        answer="Your blood pressure has improved since 2023.",
        sources=[{
            "consultation_id": "c1",
            "consultation_date": "2023-01-15",
            "doc_type": "summary",
            "excerpt": "Blood pressure elevated...",
        }],
    )

    response = client.post(
        "/api/query",
        json={"patient_id": "patient-001", "question": "How is my blood pressure?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "blood pressure" in data["answer"].lower()
    assert len(data["sources"]) == 1
