import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
import chromadb
from pypdf import PdfReader

load_dotenv()

PDF_DIR = "data"
CHROMA_DIR = "vectorstore/chroma_db"
COLLECTION_NAME = "real_estate"

def load_pdfs(pdf_dir):
    documents = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_dir, filename)
            print(f"읽는 중: {filename}")
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            doc = Document(text=text, metadata={"file_name": filename})
            documents.append(doc)
    return documents

def main():
    print("📄 PDF 로딩 중...")
    documents = load_pdfs(PDF_DIR)
    print(f"   총 {len(documents)}개 문서 로드 완료")

    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
    Settings.transformations = [SentenceSplitter(chunk_size=1024, chunk_overlap=200)]

    print("🔢 ChromaDB 설정 중...")
    os.makedirs(CHROMA_DIR, exist_ok=True)
    chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)
    chroma_collection = chroma_client.get_or_create_collection(COLLECTION_NAME)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    print("💾 인덱스 생성 중... (시간이 걸릴 수 있어요)")
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
    )
    print("✅ ChromaDB 저장 완료!")
    print("\n🎉 완료! 서버를 실행하세요: uvicorn app.main:app --reload")

if __name__ == "__main__":
    main()