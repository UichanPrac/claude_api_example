import os
import json
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Structured Outputs: 구조화된 출력] ===\n")

# 3. JSON Schema 방식 - 이메일에서 정보 추출
print("[1] JSON Schema 방식")
email_text = """
안녕하세요, 저는 김철수입니다.
귀사의 AI 솔루션에 관심이 있어 연락드립니다.
데모 시연을 요청하고 싶습니다.
연락처: chulsoo@example.com
"""

response = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    betas=["structured-outputs-2025-11-13"],
    messages=[
        {
            "role": "user",
            "content": f"다음 이메일에서 정보를 추출해줘:\n\n{email_text}"
        }
    ],
    output_format={
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"},
                "demo_requested": {"type": "boolean"}
            },
            "required": ["name", "email", "demo_requested"],
            "additionalProperties": False
        }
    }
)

print(f"응답: {response.content[0].text}")
parsed = json.loads(response.content[0].text)
print(f"- 이름: {parsed['name']}")
print(f"- 이메일: {parsed['email']}")
print(f"- 데모 요청: {parsed['demo_requested']}")

# 4. Tool 방식 - strict 모드
print("\n[2] Tool + strict 모드")
response2 = client.beta.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    betas=["structured-outputs-2025-11-13"],
    messages=[
        {
            "role": "user",
            "content": "서울 날씨 알려줘"
        }
    ],
    tools=[
        {
            "name": "get_weather",
            "description": "특정 위치의 날씨 정보를 가져옵니다.",
            "strict": True,
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                },
                "required": ["location", "unit"],
                "additionalProperties": False
            }
        }
    ]
)

print(f"Stop reason: {response2.stop_reason}")
for block in response2.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}")
        print(f"Input: {block.input}")
