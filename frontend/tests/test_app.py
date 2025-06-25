"""
TASK-004 Streamlit 프론트엔드 테스트
"""
import pytest
from unittest.mock import patch, Mock
from streamlit.testing.v1 import AppTest


def test_app_initialization():
    """앱 초기화 테스트"""
    at = AppTest.from_file("app.py").run()
    
    # 기본 요소들이 존재하는지 확인
    assert len(at.title) >= 1
    assert "AI Agent 챗봇" in at.title[0].value
    
    # 세션 상태 초기화 확인
    assert "messages" in at.session_state
    assert isinstance(at.session_state["messages"], list)


def test_chat_input_exists():
    """채팅 입력 위젯 존재 테스트"""
    at = AppTest.from_file("app.py").run()
    
    # 채팅 입력 위젯이 존재하는지 확인
    assert len(at.chat_input) >= 1


def test_initial_empty_chat():
    """초기 빈 채팅 상태 테스트"""
    at = AppTest.from_file("app.py").run()
    
    # 초기에는 메시지가 없어야 함
    assert len(at.session_state["messages"]) == 0
    assert len(at.chat_message) == 0


@patch('requests.post')
def test_user_message_input(mock_post):
    """사용자 메시지 입력 테스트"""
    # Mock API 응답 설정
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "테스트 응답입니다.",
        "timestamp": "2025-06-23T20:40:57.441436",
        "user_id": "test_user"
    }
    mock_post.return_value = mock_response
    
    at = AppTest.from_file("app.py").run()
    
    # 사용자 메시지 입력
    at.chat_input[0].set_value("아이폰 15 Pro 가격").run()
    
    # 메시지가 세션 상태에 저장되었는지 확인
    assert len(at.session_state["messages"]) >= 1
    
    # 사용자 메시지가 표시되는지 확인
    user_messages = [msg for msg in at.session_state["messages"] if msg["role"] == "user"]
    assert len(user_messages) >= 1
    assert user_messages[0]["content"] == "아이폰 15 Pro 가격"


@patch('requests.post')
def test_api_call_success(mock_post):
    """API 호출 성공 테스트"""
    # Mock API 응답 설정
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "response": "아이폰 15 Pro는 최신 모델로 약 1,200,000원부터 시작합니다.",
        "timestamp": "2025-06-23T20:40:57.441436",
        "user_id": "test_user"
    }
    mock_post.return_value = mock_response
    
    at = AppTest.from_file("app.py").run()
    
    # 사용자 메시지 입력
    at.chat_input[0].set_value("아이폰 15 Pro 가격").run()
    
    # API가 호출되었는지 확인
    mock_post.assert_called_once()
    
    # Assistant 응답이 세션 상태에 저장되었는지 확인
    assistant_messages = [msg for msg in at.session_state["messages"] if msg["role"] == "assistant"]
    assert len(assistant_messages) >= 1
    assert "아이폰 15 Pro" in assistant_messages[0]["content"]


@patch('requests.post')
def test_api_call_failure(mock_post):
    """API 호출 실패 테스트"""
    # Mock API 실패 응답 설정
    mock_post.side_effect = Exception("Connection error")
    
    at = AppTest.from_file("app.py").run()
    
    # 사용자 메시지 입력
    at.chat_input[0].set_value("테스트 메시지").run()
    
    # 에러 메시지가 표시되는지 확인
    error_messages = [msg for msg in at.session_state["messages"] if msg["role"] == "assistant" and "오류" in msg["content"]]
    assert len(error_messages) >= 1


def test_chat_history_display():
    """채팅 히스토리 표시 테스트"""
    at = AppTest.from_file("app.py").run()
    
    # 테스트 메시지를 세션 상태에 직접 추가
    at.session_state["messages"] = [
        {"role": "user", "content": "안녕하세요"},
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"}
    ]
    at.run()
    
    # 채팅 메시지가 표시되는지 확인
    assert len(at.chat_message) >= 2


def test_empty_message_handling():
    """빈 메시지 처리 테스트"""
    at = AppTest.from_file("app.py").run()
    
    # 빈 메시지 입력 시도
    at.chat_input[0].set_value("").run()
    
    # 빈 메시지는 처리되지 않아야 함
    assert len(at.session_state["messages"]) == 0 