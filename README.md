# Claude API 연습 프로젝트

이 프로젝트는 Anthropic의 Claude API를 통합하고 사용하는 방법을 익히기 위한 연습 환경입니다.

## 🚀 시작하기

### 사전 준비 사항

- Python 3.8 이상
- Anthropic API 키 (Anthropic Console에서 발급 가능)

### 설치 및 설정

1.  **저장소 클론:**
    ```bash
    git clone <repository-url>
    cd claude_api_prac
    ```

2.  **가상 환경 설정 (권장):**
    최신 macOS/Linux 시스템에서는 가상 환경 사용이 권장됩니다.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **환경 변수 설정:**
    루트 디렉토리에 `.env` 파일을 생성하고 발급받은 API 키를 입력합니다.
    ```env
    ANTHROPIC_API_KEY=your_api_key_here
    ```

4.  **의존성 패키지 설치:**
    ```bash
    pip install -r requirements.txt
    ```
