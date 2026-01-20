import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Search Results: 검색 결과 기반 응답] ===\n")

# 3. 검색 결과를 search_result 형식으로 제공
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "search_result",
                    "source": "https://docs.anthropic.com/api",
                    "title": "API 인증 문서",
                    "content": [
                        {
                            "type": "text",
                            "text": "API 키는 Anthropic Console에서 생성합니다. 요청 시 x-api-key 헤더에 포함하세요."
                        }
                    ],
                    "citations": {"enabled": True}
                },
                {
                    "type": "text",
                    "text": "API 인증 방법을 알려줘"
                }
            ]
        }
    ]
)

# 4. 응답 출력
print("[응답]")
print(response.content[0].text)

# 5. 토큰 사용량
print("\n=== 토큰 사용량 ===")
print(f"- Input tokens: {response.usage.input_tokens}")
print(f"- Output tokens: {response.usage.output_tokens}")
