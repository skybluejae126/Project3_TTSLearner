# PRD 3-1: 사용자 목소리 변환 (RVC)

## 개요
Voicevox가 생성한 TTS 결과를, 사용자가 제공한 음색 모델(.pth)을 이용해
**사용자 목소리로 변환**한다.

> **참고**: RVC 처리 로직은 `originalFile/origin_main.py`를 참고하여 구현한다.

---

## 요구사항
- 사용자가 `.pth` 파일을 드래그&드롭 또는 파일 선택으로 업로드
- 업로드된 모델을 서버(RVC 엔진)에 로드
- 텍스트 입력 → Voicevox TTS → RVC 변환 → 사용자 음색 WAV 생성

---

## API 설계
- `POST /upload-voice-model`
  - body: `.pth` 파일
  - return: `{status: "success", model_name: "xxx"}`
- `POST /synthesize-user-voice`
  - body: `{ text: string, speaker: string, speed: float }`
  - return: 사용자 음색 WAV

---

## 완료 기준
- .pth 모델 업로드 및 로딩 성공
- 지정된 텍스트가 사용자 음색으로 변환된 WAV 파일로 반환
