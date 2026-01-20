import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [Token Counting: 토큰 수 계산] ===\n")

# 3. 토큰 수 계산 (API 호출 전에 비용 예측 가능)
response = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    system="당신은 친절한 AI 어시스턴트입니다.",
    messages=[
        {
            "role": "user",
            "content": "안녕하세요! 오늘 날씨가 어때요?"
        }
    ]
)

print("[기본 메시지 토큰 수]")
print(f"- Input tokens: {response.input_tokens}")

# 4. 더 긴 메시지로 테스트
long_message = """
인공지능(AI)은 인간의 학습능력, 추론능력, 지각능력을 인공적으로 구현한 컴퓨터 시스템입니다.
머신러닝, 딥러닝, 자연어 처리 등 다양한 분야가 있으며,
최근에는 대규모 언어 모델(LLM)이 큰 주목을 받고 있습니다.
Claude는 Anthropic에서 개발한 AI 어시스턴트로, 안전하고 도움이 되는 AI를 목표로 합니다.
"""

response_long = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    system="당신은 AI 전문가입니다.",
    messages=[
        {
            "role": "user",
            "content": long_message
        }
    ]
)

print(f"\n[긴 메시지 토큰 수]")
print(f"- Input tokens: {response_long.input_tokens}")

# 5. 멀티턴 대화 토큰 수 계산
response_multi = client.messages.count_tokens(
    model="claude-sonnet-4-5-20250929",
    system="당신은 친절한 AI 어시스턴트입니다.",
    messages=[
        {"role": "user", "content": "안녕하세요!"},
        {"role": "assistant", "content": "안녕하세요! 무엇을 도와드릴까요?"},
        {"role": "user", "content": "파이썬에 대해 알려주세요."},
        {"role": "assistant", "content": "파이썬은 간결하고 읽기 쉬운 프로그래밍 언어입니다."},
        {"role": "user", "content": "감사합니다!"}
    ]
)

print(f"\n[멀티턴 대화 토큰 수]")
print(f"- Input tokens: {response_multi.input_tokens}")
