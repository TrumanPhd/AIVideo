# cut the raw music into 5s clips and 10s clips
# file: /Users/truman/AIGC/musicResource/cut_music.py
# raw_music_path = /Users/truman/AIGC/musicResource/raw/
# cut5s_music_path = /Users/truman/AIGC/musicResource/clip5s/
# cut10s_music_path = /Users/truman/AIGC/musicResource/clip10s/

# raw/ 文件下有8个音乐文件，需要将每个音乐文件切割成5s的片段，只保留前5s保存到clip5s/文件夹下。
# 同时也需要将每个音乐文件切割成10s的片段，只保留前10s保存到clip10s/文件夹下。
# 采用遍历的算法完成处理

import os
import subprocess

raw_music_path = "/Users/truman/AIGC/musicResource/raw/"
cut5s_music_path = "/Users/truman/AIGC/musicResource/clip5s/"
cut10s_music_path = "/Users/truman/AIGC/musicResource/clip10s/"

def cut_music(input_path, output_path, duration):
    """使用FFmpeg切割音乐"""
    command = [
        'ffmpeg',
        '-i', input_path,
        '-t', str(duration),
        '-acodec', 'copy',
        output_path
    ]
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"切割音乐失败: {e}")
        return False
    return True

def main():
    
    # 创建输出文件夹
    os.makedirs(cut5s_music_path, exist_ok=True)
    os.makedirs(cut10s_music_path, exist_ok=True)
    
    # 遍历 raw/ 文件夹下的音乐文件
    for filename in os.listdir(raw_music_path):
        if not filename.endswith('.mp3'):
            continue
        input_path = os.path.join(raw_music_path, filename)
        output_path_5s = os.path.join(cut5s_music_path, filename)
        output_path_10s = os.path.join(cut10s_music_path, filename)
        cut_music(input_path, output_path_5s, 5)
        cut_music(input_path, output_path_10s, 10)
        print(f"音乐 {filename} 切割完成")
        
        
if __name__ == "__main__":
    main()
