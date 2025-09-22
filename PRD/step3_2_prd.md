# PRD 3-2: 사용자 발음 업로드 & 유사도 측정

## 개요
사용자가 변환된 TTS(사용자 음색)를 듣고 따라 말한 음성을 업로드하면
**발음 유사도 점수**를 계산한다.

> **참고**: RVC 관련 코드는 `originalFile/origin_main.py`를 참고.

---

## 요구사항
- 프론트엔드: 녹음 기능 또는 파일 업로드 UI
- 백엔드: 업로드된 음성과 RVC 변환된 TTS를 비교
- 유사도 점수(float, 0~1) 반환

---

## API 설계
- `POST /compare-voice`
  - body: `{ user_recording: wav, reference_tts_id: string }`
  - return: `{ similarity_score: float }`

---

## 비교 방식
- MFCC 기반 DTW + 스펙트럼 코사인 유사도 혼합 알고리즘
- 샘플레이트, 길이 차이를 보정

---

## 완료 기준
- 사용자가 녹음 업로드 → 점수 정상 반환
- 잘못된 파일 입력 시 에러 처리
