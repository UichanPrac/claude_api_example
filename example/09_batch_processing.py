import os
import time
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Batch Processing: 배치 처리] ===\n")

# 3. 배치 요청 생성
# 여러 요청을 한 번에 제출하여 비동기로 처리
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": "request-1",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "한국의 수도는 어디인가요?"}
                ]
            }
        },
        {
            "custom_id": "request-2",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "일본의 수도는 어디인가요?"}
                ]
            }
        },
        {
            "custom_id": "request-3",
            "params": {
                "model": "claude-sonnet-4-5-20250929",
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": "중국의 수도는 어디인가요?"}
                ]
            }
        }
    ]
)

print(f"[배치 생성 완료]")
print(f"- Batch ID: {batch.id}")
print(f"- 상태: {batch.processing_status}")
print(f"- 요청 수: {batch.request_counts}")

# 4. 배치 처리 완료 대기
print("\n[처리 대기 중...]")
while True:
    batch_status = client.messages.batches.retrieve(batch.id)
    print(f"- 상태: {batch_status.processing_status} | {batch_status.request_counts}")

    if batch_status.processing_status == "ended":
        break

    time.sleep(5)  # 5초마다 상태 확인

# 5. 결과 조회
print("\n[결과 조회]")
for result in client.messages.batches.results(batch.id):
    print(f"\n{'='*50}")
    print(f"Custom ID: {result.custom_id}")
    print(f"결과 타입: {result.result.type}")

    if result.result.type == "succeeded":
        print(f"응답: {result.result.message.content[0].text}")
    else:
        print(f"오류: {result.result}")
