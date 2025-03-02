# cut the raw music into 5s clips and 10s clips
# file: /Users/truman/AIGC/musicResource/cut_music.py
# raw_music_path = /Users/truman/AIGC/musicResource/raw/
# cut5s_music_path = /Users/truman/AIGC/musicResource/clip5s/
# cut10s_music_path = /Users/truman/AIGC/musicResource/clip10s/

# raw/ 文件下有8个音乐文件，需要将每个音乐文件切割成5s的片段，只保留前5s保存到clip5s/文件夹下。
# 同时也需要将每个音乐文件切割成10s的片段，只保留前10s保存到clip10s/文件夹下。
# 采用遍历的算法完成处理
# 命名方式为m1_5s.mp3 m1_10s.mp3 m2_5s.mp3 m2_10s.mp3 ...

import os
from pydub import AudioSegment

raw_music_path = "/Users/truman/AIGC/musicResource/raw/"
cut5s_music_path = "/Users/truman/AIGC/musicResource/clip5s/"
cut10s_music_path = "/Users/truman/AIGC/musicResource/clip10s/"

# 确保目标文件夹存在
if not os.path.exists(cut5s_music_path):
    os.makedirs(cut5s_music_path)

if not os.path.exists(cut10s_music_path):
    os.makedirs(cut10s_music_path)

# 获取 raw 文件夹下的所有音乐文件
music_files = [f for f in os.listdir(raw_music_path) if f.endswith(('.mp3', '.wav', '.flac'))]  # Add more extensions if needed

# 遍历每个音乐文件
for i, music_file in enumerate(music_files):
    # 构建完整的文件路径
    raw_file_path = os.path.join(raw_music_path, music_file)

    # 加载音频文件
    try:
        audio = AudioSegment.from_file(raw_file_path)
    except Exception as e:
        print(f"Error loading file {music_file}: {e}")
        continue

    # 切割成 5 秒的片段
    clip_5s = audio[:5000]  # 5000 毫秒 = 5 秒
    clip_5s_name = f"m{i+1}_5s.mp3"
    clip_5s_path = os.path.join(cut5s_music_path, clip_5s_name)

    # 切割成 10 秒的片段
    clip_10s = audio[:10000]  # 10000 毫秒 = 10 秒
    clip_10s_name = f"m{i+1}_10s.mp3"
    clip_10s_path = os.path.join(cut10s_music_path, clip_10s_name)

    # 导出 5 秒的片段
    try:
        clip_5s.export(clip_5s_path, format="mp3")
        print(f"Successfully created: {clip_5s_name}")
    except Exception as e:
        print(f"Error exporting {clip_5s_name}: {e}")

    # 导出 10 秒的片段
    try:
        clip_10s.export(clip_10s_path, format="mp3")
        print(f"Successfully created: {clip_10s_name}")
    except Exception as e:
        print(f"Error exporting {clip_10s_name}: {e}")

print("Done!")