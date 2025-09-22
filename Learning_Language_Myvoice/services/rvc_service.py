import os
from rvc_python.infer import RVCInference

RVC_OUTPUT_DIR = "RVC_output"
os.makedirs(RVC_OUTPUT_DIR, exist_ok=True)

def convert_voice_rvc(input_wav: str, output_wav: str, model_path: str, device="cuda:0"):
    rvc = RVCInference(device=device)  # RVC 모델 초기화
    rvc.load_model(model_path)  # 모델 로드
    rvc.infer_file(input_wav, output_wav)  # 음성 변환 실행

    print(f"✅ 변환 완료! 저장된 파일: {output_wav}")
    return output_wav  # 변환된 파일 경로 반환
