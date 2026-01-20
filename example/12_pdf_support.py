import os
import anthropic
from dotenv import load_dotenv

# 1. 환경 변수 로드
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# 2. 클라이언트 초기화
client = anthropic.Anthropic(api_key=api_key)

print("=== [PDF Support: PDF 문서 분석] ===\n")

# Transformer 논문 (Attention Is All You Need)
pdf_url = "https://arxiv.org/pdf/1706.03762.pdf"

# 3. URL 방식으로 PDF 문서 분석
print(f"[분석 대상 PDF]")
print(f"- URL: {pdf_url}")
print(f"- 논문: Attention Is All You Need (Transformer)\n")

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "url",
                        "url": pdf_url
                    }
                },
                {
                    "type": "text",
                    "text": "이 논문의 핵심 내용을 한국어로 요약해줘. 주요 기여점과 Transformer 아키텍처의 특징을 설명해줘."
                }
            ]
        }
    ]
)

# 4. 응답 출력
print("[응답]")
print(response.content[0].text)

# 5. 토큰 사용량 확인
print("\n=== 토큰 사용량 ===")
print(f"- Input tokens: {response.usage.input_tokens}")
print(f"- Output tokens: {response.usage.output_tokens}")
