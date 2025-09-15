# Project_2_TTSLanguageLearner – 진행 현황

## 개요
- **프로젝트명**: TTS Language Learner  
- **목표**: 사용자가 텍스트를 입력하면 Voicevox 기반의 TTS(텍스트-투-스피치) 엔진으로 음성을 생성하고, 학습/복습을 지원하는 데스크톱 앱 제작  
- **주요 기술 스택**
  - Python 3.x
  - FastAPI (API 서버)
  - Docker + Voicevox Engine
  - GitHub Actions (향후 CI/CD 계획)
  - Windows 환경 우선 지원

## 현재 코드 저장소
- **GitHub**: [Project_2_TTSLanguageLearner](https://github.com/skybluejae126/Project_2_TTSLanguageLearner.git)
- **현재까지 구현된 내용**
  - 프로젝트 기본 구조 세팅
  - Voicevox Docker 컨테이너 구동 및 간단한 TTS 변환 스크립트
  - requirements.txt, 기본 Python 모듈 및 테스트 코드 작성
  - Project_2_TTSLanguageLearner 폴더 내부에 해당 코드들이 있음

## 다음 단계
1. **코드 모듈화**
   - TTS 기능을 `tts_service` 모듈로 분리
   - 설정 파일(config) 및 로깅 체계 추가
2. **FastAPI API화**
   - `/speak` 엔드포인트: 텍스트를 받아 음성 파일을 반환
   - `/voices` 엔드포인트: 사용 가능한 목소리 목록 제공
3. **테스트 & 문서화**
   - pytest 기반 유닛테스트 작성
   - API 스펙 자동 문서(Swagger/OpenAPI) 연동
4. **Windows용 패키징(후속 단계)**
   - Docker Desktop 자동 구동 스크립트 추가
   - PyInstaller 또는 Electron을 통한 GUI/EXE 배포 준비

## 참고
- **개발 환경**: Windows 10/11 + WSL2(선택)
- **실행 순서(현재)**  
  1. Docker Desktop 실행  
  2. `docker run`으로 Voicevox Engine 컨테이너 실행  
  3. Python 스크립트로 TTS 호출
