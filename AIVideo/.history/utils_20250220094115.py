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