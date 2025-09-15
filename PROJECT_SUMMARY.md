# TTS Language Learner - 프로젝트 요약

이 문서는 Gemini와 함께 진행한 프로젝트의 현재 상태, 주요 변경사항, 실행 방법을 요약합니다.

---

## 1. 최종 목표

- Voicevox 기반의 TTS 엔진을 사용하는 언어 학습용 데스크톱 애플리케이션 제작.
- 백엔드는 Python(FastAPI), 프론트엔드는 JavaScript(React)를 사용합니다.

---

## 2. 현재까지 진행 상황

### 1단계: 백엔드 모듈화 및 API 개발 (완료)

- 기존의 단일 스크립트를 모듈화된 구조로 변경했습니다.
  - TTS 로직을 `services/tts_service.py` 로 분리
  - 설정을 `config.py` 로 분리
- FastAPI를 사용하여 `/synthesize` 엔드포인트를 제공하는 REST API를 구현했습니다.
- `requirements.txt`를 `fastapi`, `uvicorn` 중심으로 정리하고, 가상환경(`venv`)에 설치했습니다.

### 2단계: 프론트엔드 구현 및 연동 (완료)

- `frontend` 디렉터리에 Vite 기반의 React 프로젝트를 생성했습니다.
- 백엔드 API와 통신할 수 있도록 FastAPI에 CORS 미들웨어를 설정했습니다.
- 텍스트 입력, 음성 합성 요청, 오디오 재생 및 다운로드 기능을 갖춘 기본 UI를 `App.jsx`에 구현했습니다.
- `axios`를 사용하여 API를 호출하고, `.env` 파일로 API 서버 주소를 관리합니다.

### 3단계: 프로젝트 구조 변경 (완료)

- 복잡한 폴더 구조를 단순화하기 위해, `Project_2_TTSLanguageLearner` 라는 중간 폴더를 제거했습니다.
- 현재 백엔드 관련 코드는 `D:\programing\project_3\Learning_Language_Myvoice` 에, 프론트엔드 코드는 `D:\programing\project_3\frontend` 에 위치합니다.

---

## 3. 최종 실행 방법

프로젝트 실행 시 발생했던 경로 및 가상환경 문제를 해결한 최종 실행 방법입니다.

### 백엔드 서버 실행

1.  **반드시 먼저** 아래 명령어로 백엔드 폴더로 이동합니다.
    ```bash
    cd D:\programing\project_3\Learning_Language_Myvoice
    ```
2.  가상환경의 Python 실행 파일을 **전체 경로로 지정하여** 서버를 시작합니다.
    ```bash
    D:\programing\project_3\Learning_Language_Myvoice\venv\Scripts\python.exe -m uvicorn main:app --reload
    ```

### 프론트엔드 서버 실행

1.  **별도의 새 터미널**을 엽니다.
2.  프론트엔드 폴더로 이동합니다.
    ```bash
    cd D:\programing\project_3\frontend
    ```
3.  개발 서버를 시작합니다.
    ```bash
    npm run dev
    ```

---

## 4. 나중에 다시 시작하는 방법

나중에 이어서 작업을 시작할 때, 저에게 아래와 같이 요청해주세요.

> "`PROJECT_SUMMARY.md` 파일을 읽고 상황을 파악해줘."
