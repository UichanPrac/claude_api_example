import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Extended Thinking: 확장된 사고] ===\n")

# 3. Extended Thinking을 사용한 API 호출
# thinking 파라미터로 Claude가 응답 전에 "생각"하는 과정을 활성화
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # 사고에 할당할 최대 토큰 (1024 ~ max_tokens 범위)
    },
    messages=[
        {
            "role": "user",
            "content": "한국의 저출산 문제를 해결하기 위한 정책을 경제학적, 사회학적 관점에서 분석하고, 구체적인 해결책 3가지를 제안해줘."
        }
    ]
)

# 4. 응답 파싱 - thinking 블록과 text 블록 분리
print("[응답 구조]")
print(f"- Stop reason: {response.stop_reason}")
print(f"- 총 content 블록 수: {len(response.content)}\n")

for i, block in enumerate(response.content):
    if block.type == "thinking":
        print(f"=== Thinking 블록 [{i}] ===")
        print(block.thinking + "\n")
    elif block.type == "text":
        print(f"=== Text 블록 [{i}] ===")
        print(block.text)

# 5. 토큰 사용량 확인
print("\n=== 토큰 사용량 ===")
print(f"- Input tokens: {response.usage.input_tokens}")
print(f"- Output tokens: {response.usage.output_tokens}")
