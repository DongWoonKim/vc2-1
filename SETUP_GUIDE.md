# TASK-003 & TASK-004 통합 설정 가이드

## 🚀 Google Gemini API 키 설정 (필수)

### 1. Google AI Studio에서 API 키 발급

1. **[Google AI Studio](https://aistudio.google.com/app/apikey) 접속**
2. **Google 계정으로 로그인**
3. **"Create API Key" 버튼 클릭**
4. **"Create API key in new project" 선택**
5. **생성된 API 키 복사** (예: `AIzaSyC...`)

### 2. 환경 변수 설정

#### macOS/Linux:
```bash
# 터미널에서 실행
export GOOGLE_API_KEY="AIzaSyC여기에실제키입력"

# 또는 ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export GOOGLE_API_KEY="AIzaSyC여기에실제키입력"' >> ~/.zshrc
source ~/.zshrc
```

#### Windows:
```cmd
# 명령 프롬프트에서 실행
set GOOGLE_API_KEY=AIzaSyC여기에실제키입력
```

### 3. API 키 확인
```bash
echo $GOOGLE_API_KEY
```

## 🖥️ 서버 실행 방법

### 백엔드 서버 실행:
```bash
# API 키 설정 후 실행
export GOOGLE_API_KEY="AIzaSyC여기에실제키입력"
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 프론트엔드 서버 실행:
```bash
# 새 터미널에서 실행
streamlit run frontend/app.py --server.port 8501
```

## 🧪 테스트 방법

### 1. 백엔드 API 테스트:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "아이폰 15 Pro 가격", "user_id": "test_user"}'
```

### 2. 프론트엔드 접속:
- **Streamlit UI**: http://localhost:8501

## 📋 예상 응답 예시

### 성공적인 API 응답:
```json
{
  "response": "아이폰 15 Pro는 최신 모델로 다음과 같은 특징이 있습니다:\n\n1. **A17 Pro 칩셋**: 최고 성능\n2. **티타늄 디자인**: 가볍고 견고함\n3. **48MP 카메라**: 프로급 사진 촬영\n\n**가격 정보:**\n- 128GB: 약 1,550,000원\n- 256GB: 약 1,790,000원\n- 512GB: 약 2,260,000원\n- 1TB: 약 2,730,000원\n\n온라인 쇼핑몰이나 애플 스토어에서 구매 가능합니다.",
  "timestamp": "2025-06-23T21:15:30.123456",
  "user_id": "test_user"
}
```

## ❌ 문제 해결

### API 키 오류가 발생하는 경우:
```
Invalid argument provided to Gemini: 400 API key not valid
```

**해결 방법:**
1. Google AI Studio에서 새로운 API 키 생성
2. 환경 변수 올바르게 설정 확인
3. 서버 재시작

### 네트워크 오류가 발생하는 경우:
- 백엔드 서버가 실행 중인지 확인 (http://localhost:8000/health)
- 방화벽 설정 확인

## 🔧 개발 환경 정보

- **백엔드**: FastAPI (포트 8000)
- **프론트엔드**: Streamlit (포트 8501)
- **AI 모델**: Google Gemini-2.0-flash-exp
- **검색 도구**: DuckDuckGo Search
- **Agent 프레임워크**: LangGraph

## 🎯 사용 예시

### 상품 검색 질문 예시:
- "아이폰 15 Pro 가격"
- "삼성 갤럭시 S24 Ultra 리뷰"
- "맥북 프로 M3 사양"
- "에어팟 프로 3세대 출시일"
- "플레이스테이션 5 재고"

AI Agent가 실시간으로 최신 상품 정보를 검색해서 정확한 답변을 제공합니다!

## 🚨 주의사항

1. **API 키 필수**: Google Gemini API 키가 반드시 필요합니다
2. **인터넷 연결**: DuckDuckGo 검색을 위해 인터넷 연결이 필요합니다
3. **사용량 제한**: Google API 사용량 제한을 확인하세요

## 📚 참고 문서

- [Google Gemini API 문서](https://ai.google.dev/docs)
- [LangGraph 문서](https://langchain-ai.github.io/langgraph/)
- [DuckDuckGo Search Tool](https://python.langchain.com/docs/integrations/tools/ddg) 