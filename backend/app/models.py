"""
TASK-002 Pydantic 모델 정의
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """채팅 요청 모델"""
    message: str = Field(..., min_length=1, description="사용자 메시지")
    user_id: str = Field(..., description="사용자 ID")


class ChatResponse(BaseModel):
    """채팅 응답 모델"""
    response: str = Field(..., description="AI 응답")
    timestamp: datetime = Field(..., description="응답 시간")
    user_id: str = Field(..., description="사용자 ID")


class HealthResponse(BaseModel):
    """헬스체크 응답 모델"""
    status: str = Field(..., description="서버 상태")
    message: str = Field(..., description="상태 메시지")


class ErrorResponse(BaseModel):
    """에러 응답 모델"""
    error: str = Field(..., description="에러 메시지")
    detail: Optional[str] = Field(None, description="상세 에러 정보") 