import os
import anthropic
from dotenv import load_dotenv

# .env 파일로부터 환경 변수를 로드합니다.
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Anthropic 클라이언트를 초기화합니다.
client = anthropic.Anthropic(api_key=api_key)

# Claude에게 메시지를 보냅니다.
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    temperature=0,
    system="당신은 도움이 되는 AI 어시스턴트입니다.",
    messages=[
        {
            "role": "user", 
            "content": "안녕하세요! Claude API 연결이 잘 되었는지 확인하기 위해 인사 한 번 해주세요."
        }
    ]
)

# 응답 결과를 출력합니다.
print("\n--- Claude의 응답 ---")
print(message.content[0].text)

