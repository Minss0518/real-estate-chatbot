import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, StorageContext, Settings, Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
import chromadb

load_dotenv()

PDF_DIR = "data"
CHROMA_DIR = "vectorstore/chroma_db"
COLLECTION_NAME = "real_estate"

def load_pdfs_with_marker(pdf_dir):
    print("🤖 Marker 모델 로딩 중... (시간이 걸릴 수 있어요)")
    models = create_model_dict()
    converter = PdfConverter(artifact_dict=models)

    documents = []
    for filename in os.listdir(pdf_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(pdf_dir, filename)
            print(f"📄 변환 중: {filename}")
            result = converter(filepath)
            doc = Document(
                text=result.markdown,
                metadata={"file_name": filename}
            )
            documents.append(doc)
            print(f"   ✅ 완료: {len(result.markdown)}자 변환됨")
    return documents

def main():
    print("📄 PDF 로딩 중...")
    documents = load_pdfs_with_marker(PDF_DIR)
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