import numpy as np
import librosa
import librosa.display
import torch
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean, cosine
from transformers import Wav2Vec2Processor, Wav2Vec2Model
import matplotlib.pyplot as plt
import os

# ============================
# 디렉토리 설정
# ============================
PLOTS_DIR = "plots"
os.makedirs(PLOTS_DIR, exist_ok=True)

# ============================
# 모델 로드 (최초 1회 실행)
# ============================
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2Model.from_pretrained("facebook/wav2vec2-base-960h")

# ============================
# 오디오 처리 함수
# ============================
def load_audio(file_path):
    y, sr = librosa.load(file_path, sr=16000)
    return y, sr

def normalize_audio(y, target_dB=-20):
    rms = np.sqrt(np.mean(y**2))
    scalar = 10**(target_dB / 20) / (rms + 1e-6)
    return y * scalar

# ============================
# 시각화 함수
# ============================
def plot_waveforms(ref_audio, test_audio, output_path):
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(ref_audio, sr=16000)
    plt.title("Reference Audio Waveform")
    plt.subplot(2, 1, 2)
    librosa.display.waveshow(test_audio, sr=16000, color='orange')
    plt.title("User Audio Waveform")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_spectrograms(ref_audio, test_audio, output_path):
    ref_spec = librosa.feature.melspectrogram(y=ref_audio, sr=16000)
    test_spec = librosa.feature.melspectrogram(y=test_audio, sr=16000)
    ref_spec_db = librosa.power_to_db(ref_spec, ref=np.max)
    test_spec_db = librosa.power_to_db(test_spec, ref=np.max)
    
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    librosa.display.specshow(ref_spec_db, sr=16000, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Reference Audio Mel Spectrogram')
    plt.subplot(2, 1, 2)
    librosa.display.specshow(test_spec_db, sr=16000, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('User Audio Mel Spectrogram')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

# ============================
# 특성 추출 및 유사도 계산
# ============================
def extract_features(audio):
    inputs = processor(audio, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = model(**inputs).last_hidden_state
    return outputs.squeeze(0).numpy()

def calculate_dtw_distance(ref_audio, test_audio, sr=16000):
    ref_mfcc = librosa.feature.mfcc(y=ref_audio, sr=sr, n_mfcc=13)
    test_mfcc = librosa.feature.mfcc(y=test_audio, sr=sr, n_mfcc=13)
    distance, _ = fastdtw(ref_mfcc.T, test_mfcc.T, dist=euclidean)
    return distance / len(test_mfcc.T)

def calculate_cosine_similarity(ref_audio, test_audio, num_segments=10):
    ref_features = extract_features(ref_audio)
    test_features = extract_features(test_audio)
    segment_size = min(len(ref_features), len(test_features)) // num_segments
    if segment_size == 0:
        return 0.0
    cosine_similarities = []
    for i in range(num_segments):
        start = i * segment_size
        end = (i + 1) * segment_size
        ref_segment = ref_features[start:end].mean(axis=0)
        test_segment = test_features[start:end].mean(axis=0)
        similarity = 1 - cosine(ref_segment, test_segment)
        cosine_similarities.append(similarity)
    return np.mean(cosine_similarities)

# ============================
# 최종 점수 계산
# ============================
def score_calculate(dtw_score, cos_score):
    calculated_score = (100 / (1 + (dtw_score / 3.5) ** (cos_score - 1))) * cos_score
    calculated_score = round(calculated_score, 2)
    if calculated_score < 50:
        calculated_score *= 0.6
    else:
        calculated_score *= 1.05
    return min(round(calculated_score, 2), 100.0)

# ============================
# 메인 서비스 함수
# ============================
def calculate_similarity(ref_path: str, test_path: str) -> tuple[float, str, str]:
    """
    두 오디오 파일의 유사도를 계산하고 시각화 결과를 저장합니다.
    반환: (유사도 점수, 파형 이미지 경로, 스펙트로그램 이미지 경로)
    """
    try:
        ref_audio, sr1 = load_audio(ref_path)
        test_audio, sr2 = load_audio(test_path)
        
        ref_audio_norm = normalize_audio(ref_audio)
        test_audio_norm = normalize_audio(test_audio)
        
        dtw_distance = calculate_dtw_distance(ref_audio_norm, test_audio_norm, sr=sr1)
        cosine_avg = calculate_cosine_similarity(ref_audio_norm, test_audio_norm)
        final_score = score_calculate(dtw_distance, cosine_avg)

        # 시각화 파일 경로 생성
        base_filename = os.path.splitext(os.path.basename(test_path))[0]
        waveform_path = os.path.join(PLOTS_DIR, f"{base_filename}_waveform.png")
        spectrogram_path = os.path.join(PLOTS_DIR, f"{base_filename}_spectrogram.png")

        # 시각화 생성 및 저장
        plot_waveforms(ref_audio_norm, test_audio_norm, waveform_path)
        plot_spectrograms(ref_audio_norm, test_audio_norm, spectrogram_path)
        
        return final_score, waveform_path, spectrogram_path

    except Exception as e:
        print(f"Error in calculate_similarity: {e}")
        return 0.0, "", ""
