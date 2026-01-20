import os
import base64
import anthropic
from dotenv import load_dotenv

# .env 파일로부터 환경 변수를 로드합니다.
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Anthropic 클라이언트를 초기화합니다.
client = anthropic.Anthropic(api_key=api_key)

# 이미지 분석 예제 (Vision)
try:
    image_path = "data/sample_image.jpg"
    
    # 이미지를 읽어 base64로 변환
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "이 사진 속에 무엇이 보이는지 설명해줘."
                    }
                ],
            }
        ],
    )

    # 응답 결과를 출력합니다.
    print("\n--- Claude의 이미지 분석 결과 ---")
    print(message.content[0].text)
    print("--------------------------------\n")

except Exception as e:
    print(f"API 호출 중 오류가 발생했습니다: {e}")
