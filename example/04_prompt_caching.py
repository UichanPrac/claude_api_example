import os
import time
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

# 3. 데이터 로드 (프란츠 카프카 - 변신)
try:
    with open("data/book_metamorphosis.txt", "r", encoding="utf-8") as f:
        book_text = f.read()
        print(f"로드된 텍스트 길이: {len(book_text)} 자\n")
except FileNotFoundError:
    print("오류: 파일을 찾을 수 없습니다. (data/book_metamorphosis.txt)")
    exit(1)

# 타겟 모델 (프롬프트 캐싱 지원 모델)
TARGET_MODEL = "claude-sonnet-4-20250514"

# ==========================================
# [Step 1] 첫 번째 질문: 캐시 생성 (Cache Creation)
# ==========================================
question1 = "주인공 그레고르 잠자에게 일어난 변화는 무엇이며, 그의 첫 반응은 어떠했나요?"
print(f"=== [첫 번째 요청] 질문: {question1} ===")

start_time = time.time()
try:
    response1 = client.messages.create(
        model=TARGET_MODEL,
        max_tokens=1024,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
        system=[
            {
                "type": "text",
                "text": "당신은 문학 비평가입니다. 제공된 텍스트를 분석하세요."
            },
            {
                "type": "text",
                "text": f"--- 소설 본문 ---\n{book_text}\n--- 본문 끝 ---",
                "cache_control": {"type": "ephemeral"} # ★ 캐싱 포인트
            }
        ],
        messages=[{"role": "user", "content": question1}]
    )
    end_time = time.time()

    # 결과 출력
    print(f"응답 시간: {end_time - start_time:.2f}초")
    print(f"답변: {response1.content[0].text[:100]}...")
    
    # 토큰 스탯 출력
    usage1 = response1.usage
    print(f"입력 토큰: {usage1.input_tokens}")
    print(f"캐시 생성: {getattr(usage1, 'cache_creation_input_tokens', 0)} (예상: 높음)")
    print(f"캐시 읽기: {getattr(usage1, 'cache_read_input_tokens', 0)}")
    print("------------------------------------------\n")

except Exception as e:
    print(f"첫 번째 요청 실패: {e}")


# ==========================================
# [Step 2] 두 번째 질문: 캐시 읽기 (Cache Read)
# ==========================================
question2 = "'Vermin(해충)'이라는 단어가 주는 상징적 의미를 분석해줘."
print(f"=== [두 번째 요청] 질문: {question2} ===")

start_time = time.time()
try:
    # 동일한 시스템 프롬프트 내용을 사용해야 캐시가 적중합니다.
    response2 = client.messages.create(
        model=TARGET_MODEL,
        max_tokens=1024,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
        system=[
            {
                "type": "text",
                "text": "당신은 문학 비평가입니다. 제공된 텍스트를 분석하세요."
            },
            {
                "type": "text",
                "text": f"--- 소설 본문 ---\n{book_text}\n--- 본문 끝 ---",
                "cache_control": {"type": "ephemeral"} # ★ 동일한 내용, 동일한 캐싱 포인트
            }
        ],
        messages=[{"role": "user", "content": question2}]
    )
    end_time = time.time()

    # 결과 출력
    print(f"응답 시간: {end_time - start_time:.2f}초 (단축 예상)")
    print(f"답변: {response2.content[0].text[:100]}...")
    
    # 토큰 스탯 출력
    usage2 = response2.usage
    print(f"입력 토큰: {usage2.input_tokens}")
    print(f"캐시 생성: {getattr(usage2, 'cache_creation_input_tokens', 0)}")
    print(f"캐시 읽기: {getattr(usage2, 'cache_read_input_tokens', 0)} (예상: 높음 -> 비용 절감 및 속도 향상)")
    print("------------------------------------------")

except Exception as e:
    print(f"두 번째 요청 실패: {e}")
