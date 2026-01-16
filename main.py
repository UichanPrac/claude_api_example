import os
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
        # 컨텍스트 압축(Compaction) 효과를 보려면 텍스트가 길어야 하므로 반복해서 늘립니다.
        base_text = f.read()
        long_book_text = base_text * 50  # 텍스트를 50배로 늘려 대용량 컨텍스트 시뮬레이션
        print(f"로드된 텍스트 길이: {len(long_book_text)} 자 (압축 테스트용 증폭)")
except FileNotFoundError:
    print("오류: 파일을 찾을 수 없습니다.")
    exit(1)

# 4. 테스트용 도구 정의
tools = [
    {
        "name": "analyze_text_segment",
        "description": "텍스트의 특정 부분을 분석합니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "segment": {"type": "string", "description": "분석할 텍스트 부분"}
            },
            "required": ["segment"]
        }
    }
]

print("=== [Context Editing: Tool Runner w/ Metamorphosis] ===")

try:
    # 사용자가 요청한 tool_runner 및 compaction_control 설정
    # (주의: 실제 SDK 지원 여부에 따라 실행이 안 될 수 있음)
    runner = client.beta.messages.tool_runner(
        model="claude-3-5-sonnet-20241022",
        
        # [핵심 설정]
        compaction_control={
            "enabled": True,
            "context_token_threshold": 2000, # 예제를 위해 임계값을 낮춤 (실제: 100000 등)
            "summary_prompt": """지금까지의 소설 분석 작업을 요약해줘:
            1. 현재까지 파악된 줄거리
            2. 주인공의 심리 상태 변화
            3. 놓치지 말아야 할 상징적 요소
            반드시 <summary> 태그 안에 작성해."""
        },
        
        messages=[
            {
                "role": "user", 
                "content": f"다음은 소설 '변신'의 (반복된) 본문입니다. 이 내용을 바탕으로 심층 분석 보고서를 작성해 주세요.\n\n<book_content>\n{long_book_text[:5000]}... (생략) ...\n</book_content>"
            }
        ],
        tools=tools
    )

    print("Tool Runner가 설정되었습니다. (가상 실행)")
    
    # 실제로는 아래와 같이 실행하여 이벤트를 처리합니다.
    # for event in runner:
    #     print(event)

except AttributeError:
    print("\n[오류] 현재 SDK 버전에서는 'tool_runner' 기능을 찾을 수 없습니다.")
    print("이 기능은 Private Beta이거나 특정 버전에서만 지원될 수 있습니다.")
except Exception as e:
    print(f"\n[오류 발생] {e}")
