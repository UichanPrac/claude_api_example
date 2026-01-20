# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A learning/practice repository for Anthropic's Claude API. Contains standalone example scripts demonstrating various Claude API features.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Requires `.env` file with `ANTHROPIC_API_KEY=your_key`.

### VSCode 설정

`.vscode/` 폴더에 다음 파일들이 포함되어 있음:
- `launch.json`: F5로 main.py 실행
- `settings.json`: venv 가상환경 자동 활성화

처음 설정 시 `.vscode/` 폴더가 없으면 생성:
```bash
mkdir -p .vscode
```

`.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Run main.py",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/main.py",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        }
    ]
}
```

`.vscode/settings.json`:
```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.terminal.activateEnvironment": true
}
```

## Running Examples

Each example is a standalone script:
```bash
python example/00_api_key.py          # Basic API connection test
python example/01_multi_turn_conversation.py  # Multi-turn conversation
python example/02_prefill_json.py     # Response prefill for JSON output
python example/03_vision_image_analysis.py    # Image analysis (vision)
python example/04_prompt_caching.py   # Prompt caching with large text
python main.py                        # Context editing / tool runner (beta)
```

## Architecture

- `main.py` - 새로운 API 기능을 연습/실험하는 작업 파일
- `example/` - 완성된 예제를 번호순으로 아카이빙 (00_, 01_, ...)
- `data/` - 예제에서 사용하는 샘플 데이터 (텍스트, 이미지)

**워크플로우**: `main.py`에서 먼저 연습 → 완성되면 `example/`로 아카이빙

## Conventions

- All examples use `python-dotenv` to load API key from `.env`
- Client initialization pattern: `load_dotenv()` -> `os.getenv("ANTHROPIC_API_KEY")` -> `anthropic.Anthropic(api_key=api_key)`
- Examples are numbered sequentially (00_, 01_, etc.) by complexity/feature progression
- Korean comments throughout the codebase
