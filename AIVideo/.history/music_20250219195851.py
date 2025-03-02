# add music to video

import subprocess
import requests
import librosa  # 用于音频特征提取
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity
from Setting import *

# ---- 音频处理函数 ----
def extract_music_features(music_path):
    """提取音乐特征"""
    try:
        y, sr = librosa.load(music_path)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
        energy = np.mean(librosa.feature.rms(y=y))
        sentiment_score = energy * spectral_centroid
        return {
            'tempo': tempo,
            'sentiment_score': sentiment_score,
        }
    except Exception as e:
        print(f"提取音乐特征失败: {e}")
        return None

def analyze_video_content(video_path, api_endpoint, api_key):
    """使用云端API分析视频内容"""
    headers = {'Content-Type': 'application/json'}
    data = {'video_path': video_path, 'api_key': api_key}
    try:
        response = requests.post(api_endpoint, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"视频内容分析API调用失败: {e}")
        return None

def match_music(video_analysis, music_features):
    """匹配音乐"""
    video_sentiment = video_analysis.get('sentiment', 0)
    video_tempo = video_analysis.get('tempo', 120)
    best_match = None
    best_similarity = -1
    for music_id, music_feature in music_features.items():
        music_sentiment = music_feature.get('sentiment_score', 0)
        music_tempo = music_feature.get('tempo', 120)
        sentiment_similarity = cosine_similarity(np.array([[video_sentiment]]), np.array([[music_sentiment]]))[0][0]
        tempo_similarity = 1 - abs(video_tempo - music_tempo) / max(video_tempo, music_tempo)
        overall_similarity = 0.6 * sentiment_similarity + 0.4 * tempo_similarity
        if overall_similarity > best_similarity:
            best_similarity = overall_similarity
            best_match = music_id
    return best_match

def add_background_music(video_path, music_path, output_path):
    """使用FFmpeg添加背景音乐"""
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', music_path,
        '-filter_complex', '[1:a]volume=0.5[a1];[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-map', '0:v:0',
        '-map', '0:a',
        output_path
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"添加背景音乐失败: {e.stderr}")
        return False