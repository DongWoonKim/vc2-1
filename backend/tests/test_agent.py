"""
TASK-003 LangGraph Agent 테스트
"""
import pytest
import os
from unittest.mock import Mock, patch
from app.agent import create_agent, search_products

def test_create_agent():
    """Agent 생성 테스트"""
    # 환경변수 모킹
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
        agent = create_agent()
        assert agent is not None
        assert hasattr(agent, 'invoke')

def test_search_products_success():
    """상품 검색 성공 테스트"""
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
        # Agent 응답 모킹
        mock_response = {
            "messages": [
                {
                    "role": "assistant", 
                    "content": "아이폰 15 Pro는 최신 모델로 다음과 같은 특징이 있습니다:\n\n1. **A17 Pro 칩셋**: 최고 성능\n2. **티타늄 디자인**: 가볍고 견고함\n3. **48MP 카메라**: 프로급 사진 촬영\n\n가격: 약 1,200,000원부터"
                }
            ]
        }
        
        with patch('app.agent.create_agent') as mock_create_agent:
            mock_agent = Mock()
            mock_agent.invoke.return_value = mock_response
            mock_create_agent.return_value = mock_agent
            
            result = search_products("아이폰 15 Pro 가격과 특징")
            
            assert result is not None
            assert "아이폰 15 Pro" in result
            assert "A17 Pro" in result
            assert "가격" in result

def test_search_products_empty_query():
    """빈 검색어 테스트"""
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
        result = search_products("")
        assert "검색어를 입력해주세요" in result

def test_search_products_agent_error():
    """Agent 에러 처리 테스트"""
    with patch.dict(os.environ, {'GOOGLE_API_KEY': 'test_key'}):
        with patch('app.agent.create_agent') as mock_create_agent:
            mock_agent = Mock()
            mock_agent.invoke.side_effect = Exception("API Error")
            mock_create_agent.return_value = mock_agent
            
            result = search_products("테스트 상품")
            
            assert "검색 중 오류가 발생했습니다" in result

def test_environment_variable_missing():
    """환경변수 누락 테스트"""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError, match="GOOGLE_API_KEY"):
            create_agent() 