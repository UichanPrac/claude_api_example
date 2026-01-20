import os
import anthropic
from dotenv import load_dotenv

# .env 파일로부터 환경 변수를 로드합니다.
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Anthropic 클라이언트를 초기화합니다.
client = anthropic.Anthropic(api_key=api_key)

# 답변 시작 부분 제공 (Prefill) 예제
try:
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "대한민국의 수도는 어디야? JSON 형식으로 답변해줘."},
            # 답변의 시작 부분을 미리 제공 (Prefill)
            # 클로드는 이 뒤를 이어서 답변을 완성합니다.
            {"role": "assistant", "content": "{ \"capital\": \""} 
        ]
    )

    # 클로드는 "서울\" }" 과 같이 뒷부분만 완성해서 응답합니다.
    print("\n--- Claude의 Prefill 응답 (뒷부분만 생성됨) ---")
    print(message.content[0].text)
    print("------------------------------------------\n")
    
    # 전체 JSON을 합쳐서 출력해보기
    full_json = "{ \"capital\": \"" + message.content[0].text
    print(f"전체 결과: {full_json}")

except Exception as e:
    print(f"API 호출 중 오류가 발생했습니다: {e}")
