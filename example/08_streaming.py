import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Streaming Messages: 스트리밍 응답] ===\n")

# 3. 스트리밍 방식으로 메시지 생성
# with 문을 사용해 스트림 컨텍스트 관리
# text_stream으로 텍스트가 생성되는 대로 실시간 출력
with client.messages.stream(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "인공지능의 발전이 인류에게 미치는 영향에 대해 설명해줘."
        }
    ]
) as stream:
    print("[실시간 응답]")
    for text in stream.text_stream:
        print(text, end="", flush=True)

print("\n\n=== 스트리밍 완료 ===")
