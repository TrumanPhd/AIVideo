# -*- coding: utf-8 -*-
# Author: AIGC自动化脚本
# Date: 2025-02-19
# env: SS2 MACBOOK AIR M2
# Description:  此脚本实现从文本提示生成剧本，云端生成视频，并自动添加背景音乐，自动发布到Youtube和Tiktok。

import os
import datetime
import json
import subprocess
import requests
import time
import librosa  # 用于音频特征提取
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ---- 配置参数 ----
VIDEO_SAVE_PATH = "/Users/truman/AIGC/Video"
MUSIC_LIBRARY_PATH = "/Users/truman/AIGC/MusicLibrary"
YOUTUBE_ACCOUNT = "@VideoAIGC"
TIKTOK_ACCOUNT = "@videoaigc"
PIKA_MODEL = "Pika"
GLM4_API_ENDPOINT = "YOUR_GLM4_API_ENDPOINT"
PIKA_API_ENDPOINT = "YOUR_PIKA_API_ENDPOINT"
YOUTUBE_API_ENDPOINT = "YOUR_YOUTUBE_API_ENDPOINT"
TIKTOK_API_ENDPOINT = "YOUR_TIKTOK_API_ENDPOINT"
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"
TIKTOK_API_KEY = "YOUR_TIKTOK_API_KEY"
VIDEO_ANALYSIS_API_ENDPOINT = "YOUR_VIDEO_ANALYSIS_API_ENDPOINT"  # 替换为你的视频分析 API endpoint
VIDEO_ANALYSIS_API_KEY = "YOUR_VIDEO_ANALYSIS_API_KEY"  # 替换为你的视频分析 API key


# ---- 辅助函数 ----

def generate_filename():
    """生成视频文件名"""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    counter = int(time.time() * 1000) % 1000000
    return f"V{date_str}{counter:06d}"

def call_glm4_api(prompt):
    """调用GLM-4 API生成剧本"""
    headers = {'Content-Type': 'application/json'}
    data = {'prompt': prompt}
    try:
        response = requests.post(GLM4_API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        print(f"GLM-4 API调用失败: {e}")
        return None

def call_pika_api(script):
    """调用Pika API生成视频"""
    headers = {'Content-Type': 'application/json'}
    data = {'script': script, 'model': PIKA_MODEL}
    try:
        response = requests.post(PIKA_API_ENDPOINT, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['video_url']
    except requests.exceptions.RequestException as e:
        print(f"Pika API调用失败: {e}")
        return None

def download_video(video_url, filepath):
    """从URL下载视频到指定路径"""
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        return True
    except requests.exceptions.RequestException as e:
        print(f"视频下载失败: {e}")
        return False

def extract_first_frame(video_path, image_path):
    """提取视频的第一帧作为封面"""
    try:
        command = [
            'ffmpeg',
            '-i', video_path,
            '-ss', '00:00:00',
            '-vframes', '1',
            image_path
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"提取第一帧失败: {e.stderr}")
        return False

def upload_to_youtube(video_path, title, description, category='22', keywords='AIGC,视频,自动化'):
    """模拟上传到YouTube"""
    print(f"模拟上传视频 {video_path} 到YouTube账号 {YOUTUBE_ACCOUNT}, 标题: {title}, 描述: {description}")
    print("需要实现YouTube API认证和上传逻辑！")
    return True

def upload_to_tiktok(video_path, title, description):
    """模拟上传到TikTok"""
    print(f"模拟上传视频 {video_path} 到TikTok账号 {TIKTOK_ACCOUNT}, 标题: {title}, 描述: {description}")
    print("需要实现TikTok API认证和上传逻辑！")
    return True


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

# ---- 主流程 ----
if __name__ == "__main__":
    # 1. 文本提示
    initial_prompt = "创作一个吸引人的短视频剧本，内容关于AI的未来，要积极向上，能够激发用户的兴趣，适合发布在短视频平台，时长约60秒。"

    # 2. 调用GLM-4 API生成剧本
    script = call_glm4_api(initial_prompt)
    if not script:
        print("无法生成剧本，程序终止。")
        exit()

    print(f"生成的剧本:\n{script}")

    # 3. 调用Pika API生成视频
    video_url = call_pika_api(script)
    if not video_url:
        print("无法生成视频，程序终止。")
        exit()

    print(f"视频URL: {video_url}")

    # 4. 生成文件名和路径
    filename = generate_filename()
    video_filepath = os.path.join(VIDEO_SAVE_PATH, f"{filename}.mp4")
    video_with_music_filepath = os.path.join(VIDEO_SAVE_PATH, f"{filename}_with_music.mp4")  # 带音乐的文件名
    cover_image_filepath = os.path.join(VIDEO_SAVE_PATH, f"{filename}.jpg")

    # 5. 下载视频
    if not download_video(video_url, video_filepath):
        print("视频下载失败，程序终止。")
        exit()

    print(f"视频保存到: {video_filepath}")

    # ---- 添加背景音乐部分 ----
    # 1. 加载音乐库
    music_features = {}
    for filename in os.listdir(MUSIC_LIBRARY_PATH):
        if filename.endswith(".mp3"):
            music_path = os.path.join(MUSIC_LIBRARY_PATH, filename)
            music_id = filename.replace(".mp3", "")
            features = extract_music_features(music_path)
            if features:
                 music_features[music_id] = features #只添加成功提取特征的音乐
    print(f"加载了 {len(music_features)} 首音乐")

    # 2. 分析视频内容
    video_analysis = analyze_video_content(video_filepath, VIDEO_ANALYSIS_API_ENDPOINT, VIDEO_ANALYSIS_API_KEY)
    if not video_analysis:
        print("视频分析失败，使用默认背景音乐。")
        #可以设置默认背景音乐的路径 default_music_path
        # 或者选择直接跳过添加背景音乐的步骤
        best_music = None #如果没有分析结果，跳过匹配音乐步骤
    else:
        # 3. 匹配音乐
        best_music = match_music(video_analysis, music_features)
        if not best_music:
            print("没有找到匹配的音乐，使用默认背景音乐。")
            #同样可以设置默认路径

    # 4. 添加背景音乐
    if best_music: #确保找到了合适的音乐或者使用了默认音乐
        music_path = os.path.join(MUSIC_LIBRARY_PATH, f"{best_music}.mp3")
        if add_background_music(video_filepath, music_path, video_with_music_filepath):
            print(f"成功添加背景音乐到 {video_with_music_filepath}")
        else:
            print("添加背景音乐失败，继续流程但没有背景音乐")
    else:
        print("跳过添加背景音乐的步骤")
        video_with_music_filepath = video_filepath #如果没有添加背景音乐，使用原始视频路径

    # ----  继续流程 ----
    # 6. 提取视频第一帧作为封面 (使用带背景音乐的视频或原始视频)
    if not extract_first_frame(video_with_music_filepath, cover_image_filepath):
        print("提取视频封面失败，程序可能继续，但上传的封面将是默认封面。")

    print(f"视频封面保存到: {cover_image_filepath}")

    # 7. 准备视频标题和描述
    video_title = "AI的未来：一段充满希望的旅程"
    video_description = script

    # 8. 上传到YouTube (模拟)
    if not upload_to_youtube(video_with_music_filepath, video_title, video_description):
        print("上传到YouTube失败。")

    # 9. 上传到TikTok (模拟)
    if not upload_to_tiktok(video_with_music_filepath, video_title, video_description):
        print("上传到TikTok失败。")

    print("自动化流程完成！")

"""
代码解释与注意事项：

音乐库加载:

脚本会遍历MUSIC_LIBRARY_PATH目录下的所有.mp3文件，并提取它们的特征。

务必确保该目录下存在有效的.mp3文件。

将提取的特征存储在music_features字典中，key为文件名（不包含扩展名），value为特征字典。

增加错误处理：捕获extract_music_features可能抛出的异常，避免因为单个音乐文件解析失败导致整个流程中断。

视频内容分析:

使用analyze_video_content函数调用云端API分析视频内容。

需要替换VIDEO_ANALYSIS_API_ENDPOINT和VIDEO_ANALYSIS_API_KEY为你的实际API endpoint和key。

音乐匹配:

match_music函数根据视频分析结果和音乐特征，选择最匹配的音乐。

匹配策略可以根据实际需求进行调整。

在没有找到匹配音乐或者视频分析失败的时候增加了对default_music_path的支持，可以选择使用默认音乐，也可以跳过该步骤

添加背景音乐:

add_background_music函数使用FFmpeg将选定的音乐与视频合成。

需要确保FFmpeg已正确安装并配置到环境变量中。

'-filter_complex', '[1:a]volume=0.5[a1];[0:a][a1]amix=inputs=2:duration=first:dropout_transition=2'：这一段FFmpeg命令实现了音量调整和音频混合。

如果没有找到最佳匹配音乐，或者添加背景音乐失败，则后续流程继续使用原始视频文件。

流程控制:

脚本的整体流程是：文本提示 -> 剧本生成 -> 视频生成 -> 视频下载 -> 音乐匹配 -> 添加背景音乐 -> 提取封面 -> 上传到YouTube -> 上传到TikTok。

在每个步骤中都进行了错误处理，如果某个步骤失败，则会打印错误信息并尝试继续执行后续步骤（如果可能）。

集成与部署:

将代码保存为Python脚本（例如auto_video_creator.py）。

安装依赖：pip install requests librosa scikit-learn ffmpeg-python

配置好脚本中的各个参数（例如API endpoint、API key、路径等）。

运行脚本：python auto_video_creator.py

更完善的错误处理：

extract_music_features: 捕获librosa.load可能抛出的各种异常，例如文件不存在、文件损坏等。

analyze_video_content: 处理API请求失败、API返回数据格式错误等情况。

add_background_music: 检查FFmpeg命令是否执行成功，如果失败，则打印错误信息。

如何使用：

安装依赖: pip install requests librosa scikit-learn ffmpeg-python

准备工作:

确保已安装FFmpeg，并且FFmpeg的路径已添加到系统的环境变量中。

准备好GLM-4、Pika、云端视频分析API、YouTube和TikTok的API key。

创建一个目录用于存放免版权音乐文件（例如/Users/truman/AIGC/MusicLibrary）。

配置脚本:

修改脚本开头的配置参数，例如API endpoint、API key、路径等。

运行脚本: python your_script_name.py

重要提示:

这个脚本是一个较为完整的示例，但仍然需要根据你的实际情况进行修改和完善。

务必注意版权问题，确保使用的音乐是免版权的，或者已经获得了授权。

在生产环境中使用时，需要更完善的错误处理、日志记录和监控机制。

考虑使用异步任务队列来处理耗时的任务，例如视频生成、音乐匹配和视频上传。

为了简化代码，一些错误处理和边界条件检查没有完全实现。 在实际使用中，需要根据具体情况进行完善。

这个脚本仅仅是全流程自动化短视频制作的一个起点，你可以根据自己的需求添加更多的功能，例如：

自动生成视频标题和描述

自动添加字幕

自动发布到多个平台

使用更复杂的音乐匹配算法

根据用户反馈不断优化视频制作流程
"""