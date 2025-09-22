# Step 1 PRD: 코드 모듈화 & FastAPI API 개발

## 1. 개요
- **프로젝트명:** TTS Language Learner
- **현재 상태:**  
  GitHub 저장소 [skybluejae126/Project_2_TTSLanguageLearner](https://github.com/skybluejae126/Project_2_TTSLanguageLearner)  
  의 코드를 `git clone` 후 새로운 작업 디렉토리에서 개발을 재개.
- **1단계 목표:**  
  기존 TTS(Voicevox + Python) 코드를 모듈화하고, 이를 FastAPI 기반 REST API로 제공.

---

## 2. 요구사항

### 핵심 기능
1. **모듈화**
   - 음성 합성(TTS) 로직을 `tts_service.py` 또는 `services/tts.py` 로 분리.
   - 설정 파일(config) 및 의존성(requirements) 명확화.

2. **FastAPI API**
   - 엔드포인트:  
     - `POST /synthesize`  
       - 요청: `{ "text": "안녕하세요" }`
       - 응답: mp3 또는 wav 파일 스트림
   - Swagger UI 자동 문서화(http://localhost:8000/docs)

3. **Docker 연동**
   - Voicevox Docker 컨테이너를 백그라운드에서 실행 중인 환경을 전제.
   - FastAPI 컨테이너 실행 시 Voicevox API와 연동 확인.

### 비기능 요구
- Python 3.10 이상
- FastAPI, Uvicorn, Requests 등
- Docker 및 docker-compose(테스트 용도)

---

## 3. 개발 단계

1. **환경 세팅**
   - 새 디렉토리에서 기존 코드 구조 점검
   - Python 가상환경 생성: `python -m venv venv`
   - `requirements.txt` 업데이트 및 설치

2. **모듈화**
   - `tts_service.py` 작성:  
     - 텍스트를 입력받아 Voicevox API를 호출하고 음성 파일 반환
   - 설정값(`config.py`)으로 API URL, 포트, 목소리 ID 관리

3. **FastAPI 앱 개발**
   - `main.py` 작성
   - `POST /synthesize` 구현
   - Swagger UI 및 간단한 테스트 코드 포함

4. **테스트 & 문서화**
   - 로컬에서 `uvicorn main:app --reload` 로 테스트
   - README에 실행 방법 추가

---

## 4. 산출물
- `main.py` (FastAPI 엔트리포인트)
- `services/tts_service.py` (TTS 모듈)
- `config.py`
- `requirements.txt` 업데이트
- 실행/배포 안내 문서 (README 갱신)

---

## 5. 예상 일정 (gemini는 이 내용을 신경 안써도 괜찮음)
| 작업 | 기간 |
|------|------|
| 환경 세팅 & 구조 점검 | 0.5일 |
| 코드 모듈화 | 1일 |
| FastAPI 개발 | 1일 |
| 테스트 & 문서화 | 0.5일 |

총 예상: **약 3일**

---

## 6. 향후 단계 연결
- **2단계:** React 프론트엔드 개발 및 API 연동
- **3단계:** Docker Compose를 통한 전체 스택(Voicevox + FastAPI) 통합
- **4단계:** Windows 데스크톱 패키징 준비(Electron 또는 PyInstaller)

