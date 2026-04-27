import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from langchain_openai import ChatOpenAI
import chromadb

load_dotenv()

Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.2)

chroma_client = chromadb.PersistentClient(path="vectorstore/chroma_db")
chroma_collection = chroma_client.get_or_create_collection("real_estate")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context,
)
engine = index.as_query_engine(
    similarity_top_k=4,
    response_mode="compact",
    system_prompt=(
        "당신은 부동산 법률 전문 AI 어시스턴트입니다. "
        "반드시 제공된 법률 문서에 근거하여 구체적으로 답변하세요. "
        "문서에 있는 내용은 반드시 답변에 포함하세요."
    ),
)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

test_questions = [
    "전세 계약 기간은 얼마나 되나요?",
    "보증금 돌려받으려면 어떻게 해야 하나요?",
    "임대료 증액 청구 한도는 얼마인가요?"
]

results = []

for q in test_questions:
    response = engine.query(q)
    contexts = [node.text for node in response.source_nodes]
    answer = str(response)

    eval_prompt = f"""
다음 질문, 답변, 참고문서를 보고 평가해줘.

질문: {q}
답변: {answer}
참고문서: {" ".join(contexts[:2])}

1. 충실도(0~1): 답변이 참고문서에 근거하는가?
2. 관련성(0~1): 답변이 질문에 적절한가?

숫자만 간단히 알려줘. 예시: 충실도: 0.9 / 관련성: 0.8
"""
    eval_result = llm.invoke(eval_prompt)
    results.append({
        "질문": q,
        "답변": answer,
        "평가": eval_result.content
    })

print("\n===== RAGAS 평가 결과 =====")
for r in results:
    print(f"\n질문: {r['질문']}")
    print(f"답변: {r['답변'][:100]}...")
    print(f"평가: {r['평가']}")