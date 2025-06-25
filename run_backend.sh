#!/bin/bash

# TASK-002 FastAPI 백엔드 서버 실행 스크립트

echo "🚀 FastAPI 백엔드 서버 시작 중..."
echo "📝 서버 주소: http://localhost:8000"
echo "📚 API 문서: http://localhost:8000/docs"
echo "🔍 헬스체크: http://localhost:8000/health"
echo ""

# 의존성 설치 확인
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 없습니다. python -m venv venv 로 생성하세요."
    exit 1
fi

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 패키지 설치 확인
echo "📦 필요한 패키지들을 설치하고 있습니다..."
pip install -r requirements.txt

# FastAPI 서버 실행
echo "🚀 서버를 시작합니다..."
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload 