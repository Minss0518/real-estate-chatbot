import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from pypdf import PdfReader

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

engine = index.as_query_engine(similarity_top_k=3)
response = engine.query("전세 계약 기간은 얼마나 되나요?")
print("답변:", str(response))
print("\n출처 문서:")
for node in response.source_nodes:
    print(node.text[:200])
    print("---")

reader = PdfReader("data/housing_lease.pdf")
for i, page in enumerate(reader.pages[:3]):
    text = page.extract_text()
    print(f"=== 페이지 {i+1} ===")
    print(text[:300])
    print()