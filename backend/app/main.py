"""
TASK-002 FastAPI 백엔드 기본 구조 구현
"""
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Dict, Any

from .models import ChatRequest, ChatResponse, HealthResponse, ErrorResponse

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="Vibe Coding W2-1 Backend",
    description="FastAPI 백엔드 서버 - 채팅 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit 포트
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def read_root():
    """루트 엔드포인트 - 헬스체크로 리다이렉트"""
    return HealthResponse(
        status="healthy",
        message="FastAPI server is running"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """헬스체크 엔드포인트"""
    return HealthResponse(
        status="healthy",
        message="FastAPI server is running"
    )


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """채팅 API 엔드포인트 - LangGraph Agent 연동"""
    
    # 빈 메시지 검증
    if not request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "메시지가 비어있습니다"}
        )
    
    try:
        # LangGraph Agent를 통한 상품 검색
        from .agent import search_products
        
        response_text = search_products(request.message)
        
        return ChatResponse(
            response=response_text,
            timestamp=datetime.now(),
            user_id=request.user_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": f"채팅 처리 중 오류가 발생했습니다: {str(e)}"}
        )


@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """값 에러 핸들러"""
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={"error": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """일반 예외 핸들러"""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={"error": "내부 서버 오류가 발생했습니다"}
    )


@app.get("/test")
async def test_endpoint():
    """PR 테스트용 엔드포인트"""
    return {
        "message": "PR 테스트가 성공적으로 작동합니다!",
        "test": "GitHub Actions 자동화 테스트",
        "branch": "pr_test"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 