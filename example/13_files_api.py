import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Files API: 파일 업로드 및 참조] ===\n")

# 3. 파일 업로드 (Beta)
file_path = "data/book_metamorphosis.txt"
print(f"[파일 업로드]")
print(f"- 파일: {file_path}")

with open(file_path, "rb") as f:
    file = client.beta.files.upload(
        file=(os.path.basename(file_path), f, "text/plain")
    )

print(f"- File ID: {file.id}")
print(f"- 상태: 업로드 완료\n")

# 4. 업로드된 파일을 file_id로 참조하여 메시지 생성
print("[파일 분석 요청]")
response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    betas=["files-api-2025-04-14"],
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "이 소설의 줄거리와 주인공의 심리 변화를 간략히 요약해줘."
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": file.id
                    }
                }
            ]
        }
    ]
)

# 5. 응답 출력
print("\n[응답]")
print(response.content[0].text)

# 6. 토큰 사용량 확인
print("\n=== 토큰 사용량 ===")
print(f"- Input tokens: {response.usage.input_tokens}")
print(f"- Output tokens: {response.usage.output_tokens}")

# 7. 파일 목록 조회 (선택사항)
print("\n[업로드된 파일 목록]")
files_list = client.beta.files.list()
for f in files_list.data:
    print(f"- {f.id}: {f.filename}")
