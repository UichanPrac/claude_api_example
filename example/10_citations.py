import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Citations: 인용 기능] ===\n")

# 3. 문서와 함께 질문 (인용 활성화)
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "text",
                        "media_type": "text/plain",
                        "data": """서울은 대한민국의 수도이자 최대 도시입니다.
인구는 약 950만 명으로 세계에서 가장 인구 밀도가 높은 도시 중 하나입니다.
한강이 도시 중심을 가로지르며, 600년 이상의 역사를 가지고 있습니다.
주요 관광지로는 경복궁, 남산타워, 명동 등이 있습니다."""
                    },
                    "citations": {"enabled": True}
                },
                {
                    "type": "text",
                    "text": "서울에 대해 알려줘. 인구와 주요 관광지는?"
                }
            ]
        }
    ]
)

# 4. 응답 파싱 - 텍스트와 인용 정보 분리
print("[응답]")
for block in response.content:
    if block.type == "text":
        print(f"텍스트: {block.text}")

        # 인용 정보가 있으면 출력
        if hasattr(block, "citations") and block.citations:
            print("\n[인용 정보]")
            for i, citation in enumerate(block.citations):
                print(f"  [{i+1}] {citation}")

# 5. 전체 응답 구조 확인
print("\n[전체 응답 구조]")
for i, block in enumerate(response.content):
    print(f"블록 {i}: type={block.type}")
    print(f"  내용: {block}")
