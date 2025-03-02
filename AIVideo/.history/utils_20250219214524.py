# Utils and channel upload
from Setting import *
import subprocess
import datetime
import time

def generate_filename():
    """生成视频文件名"""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    counter = int(time.time() * 1000) % 1000000
    return f"V{date_str}{counter:06d}"

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