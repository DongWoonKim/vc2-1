"""
TASK-002 FastAPI 백엔드 기본 구조 테스트
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """헬스체크 엔드포인트 테스트"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "FastAPI server is running"}


def test_root_redirect():
    """루트 엔드포인트 테스트 (헬스체크로 리다이렉트)"""
    response = client.get("/")
    assert response.status_code == 200
    assert "status" in response.json()


def test_chat_endpoint_success():
    """Chat API 엔드포인트 성공 테스트"""
    chat_request = {
        "message": "안녕하세요",
        "user_id": "test_user"
    }
    response = client.post("/chat", json=chat_request)
    assert response.status_code == 200
    assert "response" in response.json()
    assert "timestamp" in response.json()


def test_chat_endpoint_empty_message():
    """Chat API 빈 메시지 테스트"""
    chat_request = {
        "message": "",
        "user_id": "test_user"
    }
    response = client.post("/chat", json=chat_request)
    assert response.status_code == 422  # Pydantic validation error
    assert "detail" in response.json()


def test_chat_endpoint_missing_fields():
    """Chat API 필수 필드 누락 테스트"""
    chat_request = {
        "message": "안녕하세요"
        # user_id 누락
    }
    response = client.post("/chat", json=chat_request)
    assert response.status_code == 422  # Validation error


def test_invalid_endpoint():
    """존재하지 않는 엔드포인트 테스트"""
    response = client.get("/invalid")
    assert response.status_code == 404 