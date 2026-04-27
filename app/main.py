"""
main.py
FastAPI 서버 및 라우터 담당
RAG 로직은 rag.py, 모델은 schemas.py 참고
"""

from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio

from app.schemas import ChatRequest, ChatResponse
from app import rag

load_dotenv()

chat_engine = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global chat_engine
    print("🚀 RAG 엔진 초기화 중...")
    try:
        chat_engine = rag.build_chat_engine()
        print("✅ RAG 엔진 준비 완료!")
    except Exception as e:
        print(f"⚠️ 오류: {e}")
    yield
    print("🛑 서버 종료")


app = FastAPI(
    title="부동산 법률 챗봇 API",
    description="부동산 관련 법률 PDF 기반 RAG 챗봇",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "부동산 법률 챗봇 API 🏠", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok", "engine_loaded": chat_engine is not None}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if chat_engine is None:
        raise HTTPException(status_code=503, detail="RAG 엔진이 준비되지 않았습니다.")
    answer = rag.chat(chat_engine, request.question)
    return ChatResponse(answer=answer)


@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    if chat_engine is None:
        raise HTTPException(status_code=503, detail="RAG 엔진이 준비되지 않았습니다.")

    async def generate():
        answer = rag.chat(chat_engine, request.question)
        for char in answer:
            yield char
            await asyncio.sleep(0.01)

    return StreamingResponse(generate(), media_type="text/plain")