# Step 2 PRD: React 프론트엔드 & FastAPI API 연동

## 1. 개요
- **프로젝트명:** TTS Language Learner
- **이전 단계:**  
  FastAPI 기반 REST API(`/synthesize`)가 정상 동작 중이며, Swagger UI(127.0.0.1:8000/docs)에서 확인 완료.
- **2단계 목표:**  
  사용자에게 텍스트 입력 → 음성 합성 결과를 실시간 재생·다운로드할 수 있는 **웹 인터페이스** 구현.

---

## 2. 요구사항

### 핵심 기능
1. **사용자 인터페이스**
   - 텍스트 입력 박스 + “합성하기” 버튼
   - 합성 후 오디오 플레이어(`<audio>` 태그)로 결과 재생
   - 다운로드 버튼(선택)으로 mp3/wav 파일 저장

2. **API 연동**
   - `POST /synthesize` 엔드포인트 호출
   - JSON 요청: `{ "text": "<사용자 입력>" }`
   - 응답: 음성 파일 (wav/mp3 Blob) → 브라우저에서 재생

3. **CORS & 환경 설정**
   - FastAPI 백엔드에 CORS 허용 설정 (개발 단계: `allow_origins=["*"]`)
   - 프론트엔드에서 API URL을 환경변수(`.env`)로 관리

4. **빌드 및 통합**
   - 개발 단계: React 개발 서버(`npm run dev`)와 FastAPI 서버 병행 실행
   - 배포 단계: `npm run build` 후 빌드 산출물을 FastAPI `StaticFiles` 또는 별도 서버(Nginx 등)에서 서빙 가능

### 비기능 요구
- React + Vite(권장) 또는 CRA
- Node.js 18 이상
- Axios 또는 Fetch API 사용
- 크로스 브라우저(Chrome, Edge) 지원

---

## 3. 개발 단계

1. **프론트엔드 초기화**
   - `frontend/` 폴더 생성
   - `npm create vite@latest` → React + JavaScript 템플릿
   - `npm install` 로 의존성 설치

2. **FastAPI CORS 설정**
   - `main.py`에 `fastapi.middleware.cors.CORSMiddleware` 추가

3. **UI 구현**
   - `App.jsx`에 텍스트 입력, 합성 버튼, `<audio>` 플레이어 작성
   - 버튼 클릭 시 API 호출 로직 구현 (Axios/Fetch)

4. **오디오 재생 처리**
   - API 응답을 Blob 형태로 수신 → `URL.createObjectURL` 로 `<audio>` 소스 설정
   - 다운로드 기능(optional): `<a>` 태그의 `download` 속성 활용

5. **환경 변수 관리**
   - `.env` 파일에 API URL 정의 (예: `VITE_API_BASE_URL=http://127.0.0.1:8000`)

6. **통합 테스트**
   - `uvicorn main:app --reload` (포트 8000)
   - `npm run dev` (포트 5173)
   - 브라우저에서 `http://localhost:5173` 접속 → 텍스트 입력 → 음성 합성 재생

7. **빌드 & 배포 준비**
   - `npm run build` → `dist/` 폴더 산출
   - FastAPI에서 `StaticFiles` 로 정적 서빙하거나 Nginx로 배포 옵션 검토

---

## 4. 산출물
- `frontend/` 디렉터리 및 소스코드
- `.env` (API URL)
- 빌드 결과: `frontend/dist/`
- 통합 실행/배포 설명을 포함한 README 업데이트

---

## 5. 예상 일정
| 작업 | 기간 |
|------|------|
| 프론트엔드 초기 세팅 | 0.5일 |
| UI 구현 및 API 연동 | 1~1.5일 |
| 테스트 및 문서화 | 0.5일 |
총 **약 2~3일**

---

## 6. 향후 단계 연결
- **3단계:** Docker Compose로 FastAPI + Voicevox + React(정적 서빙) 통합
- **4단계:** Windows 데스크톱 앱(Electron or PyInstaller) 패키징
