# Effort 파라미터는 Claude Opus 4.5에서만 지원 (Beta)

import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Effort: 응답 노력 수준 비교] ===\n")

# 테스트할 질문
question = "마이크로서비스와 모놀리식 아키텍처의 장단점을 분석해줘"

# effort 수준별로 비교
effort_levels = ["low", "medium", "high"]

for effort in effort_levels:
    print(f"{'='*60}")
    print(f"[Effort: {effort.upper()}]")
    print(f"{'='*60}\n")

    response = client.beta.messages.create(
        model="claude-opus-4-5-20251101",
        betas=["effort-2025-11-24"],
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": question
            }
        ],
        output_config={
            "effort": effort
        }
    )

    # 응답 출력
    print("[응답]")
    print(response.content[0].text)

    # 토큰 사용량
    print(f"\n[토큰 사용량]")
    print(f"- Input: {response.usage.input_tokens}")
    print(f"- Output: {response.usage.output_tokens}")
    print(f"- 총합: {response.usage.input_tokens + response.usage.output_tokens}")
    print("\n")
