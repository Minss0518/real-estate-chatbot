from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from dotenv import load_dotenv

load_dotenv()

print("모델 로딩 중... (시간이 걸릴 수 있어요)")
models = create_model_dict()

converter = PdfConverter(artifact_dict=models)

print("PDF 변환 중...")
result = converter("data/housing_lease.pdf")

print("\n===== 변환 결과 (앞부분) =====")
print(result.markdown[:500])