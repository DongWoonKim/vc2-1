"""
TASK-004 Streamlit 프론트엔드 구현
상품 검색 챗봇 인터페이스
"""
import streamlit as st
import requests
import json
import time
from typing import Dict, Any


def init_session_state():
    """세션 상태 초기화"""
    if "messages" not in st.session_state:
        st.session_state.messages = []


def call_chat_api(message: str, user_id: str = "streamlit_user") -> Dict[str, Any]:
    """
    FastAPI 백엔드 Chat API 호출
    
    Args:
        message: 사용자 메시지
        user_id: 사용자 ID
        
    Returns:
        API 응답 데이터
        
    Raises:
        Exception: API 호출 실패 시
    """
    api_url = "http://localhost:8000/chat"
    
    payload = {
        "message": message,
        "user_id": user_id
    }
    
    try:
        response = requests.post(
            api_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"API 호출 실패: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        raise Exception(f"네트워크 오류: {str(e)}")


def display_chat_messages():
    """채팅 메시지 표시"""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(user_input: str):
    """
    사용자 입력 처리
    
    Args:
        user_input: 사용자가 입력한 메시지
    """
    if not user_input.strip():
        return
    
    # 사용자 메시지를 세션 상태에 추가
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    
    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # API 호출 및 응답 처리
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # 로딩 표시
            message_placeholder.markdown("🔍 상품을 검색하고 있습니다...")
            
            # API 호출
            response_data = call_chat_api(user_input)
            
            # 응답 표시
            assistant_response = response_data.get("response", "응답을 받을 수 없습니다.")
            message_placeholder.markdown(assistant_response)
            
            # Assistant 메시지를 세션 상태에 추가
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response
            })
            
        except Exception as e:
            error_message = f"❌ 오류가 발생했습니다: {str(e)}"
            message_placeholder.markdown(error_message)
            
            # 에러 메시지를 세션 상태에 추가
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message
            })


def main():
    """메인 앱 함수"""
    # 페이지 설정
    st.set_page_config(
        page_title="상품 검색 챗봇",
        page_icon="🛒",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # 앱 제목
    st.title("🛒 상품 검색 챗봇")
    st.markdown("궁금한 상품에 대해 질문해보세요! AI가 최신 정보를 검색해서 알려드립니다.")
    
    # 세션 상태 초기화
    init_session_state()
    
    # 기존 채팅 메시지 표시
    display_chat_messages()
    
    # 사용자 입력 처리
    if user_input := st.chat_input("상품에 대해 질문해보세요..."):
        handle_user_input(user_input)


if __name__ == "__main__":
    main() 