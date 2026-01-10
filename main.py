import os
import anthropic
from dotenv import load_dotenv

# .env 파일로부터 환경 변수를 로드합니다.
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Anthropic 클라이언트를 초기화합니다.
client = anthropic.Anthropic(api_key=api_key)

# 이 파일은 현재 비어 있습니다. 새로운 실습 코드를 작성하거나 필요한 기능을 테스트해 보세요.
