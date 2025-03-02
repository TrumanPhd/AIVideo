# Utils and channel upload
from Setting import *
import subprocess
import datetime
import time
import os  # Import the 'os' module

def generate_filename():
    """生成视频文件名"""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    counter = int(time.time() * 1000) % 1000000
    return f"V{date_str}{counter:06d}"

def extract_first_frame(video_path, output_dir):
    """提取视频的第一帧作为封面

    Args:
        video_path (str): 视频文件的完整路径 (例如: /Users/truman/AIGC/Publication/video/V20250220123456.mp4).
        output_dir (str): 封面图片保存的目录 (例如: /Users/truman/AIGC/Publication/cover_img/).

    Returns:
        str: 封面图片的完整路径，如果提取成功；否则返回 None。
    """

    try:
        # 确保输出目录存在
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 根据视频文件名生成图像文件名
        video_filename_without_ext = os.path.splitext(os.path.basename(video_path))[0]
        image_filename = f"img{video_filename_without_ext}.jpg"  # 遵循命名规则
        image_path = os.path.join(output_dir, image_filename)      # 构建完整路径

        command = [
            'ffmpeg',
            '-i', video_path,
            '-ss', '00:00:00',
            '-vframes', '1',
            image_path  # 使用完整的图像文件路径
        ]
        subprocess.run(command, check=True, capture_output=True, text=True)
        return image_path  # 返回封面图片的完整路径
    except subprocess.CalledProcessError as e:
        print(f"提取第一帧失败: {e.stderr}")
        return None
    except Exception as e:
        print(f"提取第一帧时发生错误: {e}")  # 捕获其他可能的异常
        return None