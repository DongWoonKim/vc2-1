"""
TASK-003 LangGraph Agent 구현
"""
import os
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchResults
from langgraph.prebuilt import create_react_agent

def create_agent():
    """
    LangGraph React Agent 생성
    
    Returns:
        Agent: 생성된 React Agent
        
    Raises:
        ValueError: GOOGLE_API_KEY 환경변수가 없을 때
    """
    # 환경변수 검증
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
    
    # Gemini LLM 초기화
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash-exp",
        google_api_key=api_key,
        temperature=0.1
    )
    
    # DuckDuckGo Search Tool 설정
    search_tool = DuckDuckGoSearchResults(
        name="product_search",
        description="상품 정보를 검색할 때 사용하는 도구입니다. 가격, 특징, 리뷰 등을 찾을 수 있습니다."
    )
    
    tools = [search_tool]
    
    # 시스템 프롬프트 설정
    system_prompt = """당신은 상품 검색 전문가입니다. 사용자가 요청한 상품에 대해 다음과 같이 도움을 제공하세요:

1. **상품 검색**: DuckDuckGo를 통해 최신 상품 정보를 검색합니다.
2. **정보 정리**: 검색 결과를 바탕으로 다음 정보를 정리해주세요:
   - 상품명과 브랜드
   - 주요 특징 및 스펙
   - 가격 정보 (가능한 경우)
   - 사용자 리뷰나 평점 (가능한 경우)
   - 구매처 정보 (가능한 경우)

3. **응답 형식**: 
   - 명확하고 구조화된 형태로 정보를 제공하세요
   - 불확실한 정보는 "추정" 또는 "대략"이라고 명시하세요
   - 검색 결과가 부족한 경우 그 사실을 알려주세요

4. **한국어 응답**: 모든 응답은 한국어로 작성하세요.

검색 도구를 적극적으로 활용하여 최신이고 정확한 정보를 제공하세요."""
    
    # React Agent 생성
    agent = create_react_agent(
        llm, 
        tools, 
        prompt=system_prompt
    )
    
    return agent

def search_products(query: str) -> str:
    """
    상품 검색 함수
    
    Args:
        query (str): 검색어
        
    Returns:
        str: 검색 결과
    """
    # 빈 검색어 처리
    if not query or not query.strip():
        return "검색어를 입력해주세요."
    
    try:
        # Agent 생성 및 실행
        agent = create_agent()
        
        # Single Turn 방식으로 실행
        response = agent.invoke({
            "messages": [("user", query)]
        })
        
        # 응답 추출
        if "messages" in response and response["messages"]:
            last_message = response["messages"][-1]
            if hasattr(last_message, 'content'):
                return last_message.content
            elif isinstance(last_message, dict) and 'content' in last_message:
                return last_message['content']
            else:
                return str(last_message)
        
        return "검색 결과를 가져올 수 없습니다."
        
    except Exception as e:
        return f"검색 중 오류가 발생했습니다: {str(e)}" 