# PRD 3-3: 유사도 시각화 & 점수 알고리즘 개선

## 개요
유사도 측정 결과를 **파형(Waveform) 및 스펙트로그램**으로 시각화해 제공하고,
기존 점수 함수를 고도화한다.

> **참고**: 'Voice_similiarity.py`를 참고.

---

## 요구사항
- 백엔드에서 두 음성의 파형과 Mel Spectrogram을 생성해 이미지 반환
- 프론트엔드에서 이미지와 점수를 함께 표시
- 점수 알고리즘:
  - DTW + MFCC + 스펙트럼 유사도 가중치 조정
  - 노이즈·볼륨 차이 보정

---

## API 설계
- `GET /compare-voice-visual/{session_id}`
  - return: `{ similarity_score: float, waveform_plot: image, spectrogram_plot: image }`

---

## 완료 기준
- 점수와 함께 파형·스펙트럼 이미지가 UI에 표시
- 다양한 길이/잡음 조건에서 안정적인 점수 산출
