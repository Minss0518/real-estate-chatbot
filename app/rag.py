"""
rag.py
LlamaIndex RAG 엔진 초기화 및 쿼리 담당 (Memory 기능 포함)
"""

import os
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer
import chromadb
from langsmith import traceable

CHROMA_DIR = "vectorstore/chroma_db"
COLLECTION_NAME = "real_estate"


def build_chat_engine():
    """ChromaDB에서 인덱스를 불러와 대화 기억 엔진 반환"""
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.2)

    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        storage_context=storage_context,
    )

    memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

    chat_engine = index.as_chat_engine(
        chat_mode="condense_plus_context",
        memory=memory,
        similarity_top_k=4,
        system_prompt=(
            "당신은 부동산 법률 전문 AI 어시스턴트입니다. "
            "반드시 제공된 법률 문서에 근거하여 답변하세요. "
            "문서에 없는 내용은 답변하지 마세요. "
            "답변 시 관련 법 조항을 구체적으로 언급하세요."
        ),
    )

    return chat_engine


@traceable
def chat(engine, question: str) -> str:
    """대화 엔진에 질문을 던지고 답변 문자열 반환"""
    response = engine.chat(question)

    answer = str(response)

    sources = []
    if hasattr(response, 'source_nodes') and response.source_nodes:
        for node in response.source_nodes:
            if hasattr(node, 'metadata') and node.metadata:
                filename = node.metadata.get('file_name', '')
                if 'housing_lease' in filename:
                    sources.append("주택임대차보호법")
                elif 'real_estate_agent' in filename:
                    sources.append("공인중개사법")
                elif 'housing_act' in filename:
                    sources.append("주택법")

    sources = list(set(sources))
    if sources:
        answer += f"\n\n📚 참고 법령: {', '.join(sources)}"

    answer += "\n\n⚠️ 본 내용은 법률 정보 제공 목적이며 전문 법률 상담을 대체하지 않습니다."

    return answer