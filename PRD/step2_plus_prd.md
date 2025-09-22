
# PRD: Voicevox TTS – 화자(여/남) 및 속도 조절 기능

## 1. 개요
현재 TTSLanguageLearner는 기본 텍스트 입력을 Voicevox로 합성할 수 있으나,
화자 선택(여/남)과 속도 조절 기능이 없다.  
이 PRD는 **speaker 선택**과 **speed 조절**을 프론트엔드·백엔드 모두에 추가한다.

---

## 2. 목표
- 사용자가 TTS 합성 시 **화자**(여성/남성)와 **속도(speed)** 를 직접 설정할 수 있다.
- Voicevox API 호출 시 `speaker`와 `speedScale`을 동적으로 적용한다.

---

## 3. 요구사항

### 프론트엔드 (React)
- **UI 추가**
  - 드롭다운: `여성(1)` / `남성(11)`
  - 속도 슬라이더: 0.5 ~ 2.0 (기본 1.0)
- **요청 예시**
  ```json
  POST /synthesize
  {
    "text": "안녕하세요",
    "speaker": 1,
    "speed": 1.2
  }
````

### 백엔드 (FastAPI)

* **엔드포인트 수정**

  * 기존 `/synthesize`에 `speaker: int`, `speed: float` 파라미터 추가
* **Voicevox 연동**

  * Voicevox TTS API 호출 시

    * `speaker` → 사용자 선택값
    * `speedScale` → 사용자 선택값

---

## 4. API 스펙

* **POST /synthesize**

  * body:

    ```json
    {
      "text": "string",
      "speaker": 1,   // 1: female, 11: male
      "speed": 1.0    // 0.5~2.0
    }
    ```
  * response: 합성된 WAV 파일 (Content-Type: audio/wav)

---

## 5. 완료 기준

* 프론트엔드에서 화자와 속도를 선택 후 합성 요청 시,

  * Voicevox에서 해당 설정이 반영된 음성이 정상 반환.
* 잘못된 파라미터(범위 초과 등) 전달 시 400 에러 처리.

---

## 6. 참고

* Voicevox API 문서: `/audio_query`와 `/synthesis` 단계에서

  * `speaker` 파라미터로 화자 선택
  * `speedScale` 파라미터로 속도 조절

```

---

### 개발 팁
1. **백엔드 먼저**: FastAPI의 `/synthesize`를 수정 → `curl`로 테스트  
2. **프론트엔드**: 드롭다운과 슬라이더 값이 API body에 잘 전달되는지 확인  
3. **문서 업데이트**: README와 예제 요청/응답을 갱신  

이 파일을 `PRD_Voicevox_SpeakerSpeed.md` 같은 이름으로 저장해  
Gemini CLI나 GitHub Issue에 바로 활용하시면 됩니다.
```
