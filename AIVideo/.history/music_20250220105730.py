# 给5s的视频添加长度为5s的背景音乐
# 音乐mp3格式，路径/Users/truman/AIGC/musicResource/clip5s
# 命名方式为m1_5s.mp3 m2_5s.mp3 m3_5s.mp3 ... m8_5s.mp3
# 视频mp4格式，路径/Users/truman/AIGC/Video
# 定义add_music函数，实现给视频添加背景音乐的功能,随机选择一首音乐添加到视频中
# 将生成的视频保存到 /Users/truman/AIGC/Publication
# 命名方式不变
# 成功后打印 "成功添加背景音乐"

import os
import random
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip

def add_music(video_path):
    """
    给指定的视频添加背景音乐，音乐时长与视频相同 (5s)。
    从 /Users/truman/AIGC/musicResource/clip5s 目录下随机选择一首音乐。
    保存到 /Users/truman/AIGC/Publication，文件名与原视频相同。

    Args:
        video_path (str): 视频文件的完整路径。
    """

    music_dir = "/Users/truman/AIGC/musicResource/clip5s"
    output_dir = "/Users/truman/AIGC/Publication"

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取所有音乐文
    music_files = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]

    if not music_files:
        print("没有找到任何 mp3 音乐文件，请检查音乐路径")
        return

    # 随机选择音乐
    random_music_file = random.choice(music_files)
    music_path = os.path.join(music_dir, random_music_file)

    try:
        # 加载视频和音频
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(music_path)

        # 确保音频和视频的时长一致 (重要!)
        # 如果视频大于5s，截取前5s.如果视频小于5s，循环播放
        if video_clip.duration > 5:
            video_clip = video_clip.subclipped(0, 5) #keep first 5 seconds
        elif video_clip.duration < 5:
            #loop the video
            n_repeats = int(5/ video_clip.duration)
            video_clip = video_clip.loop(n_repeats)

        # 组合音频和视频
        final_audio = CompositeAudioClip([audio_clip])  #Ensure music has length exactly video
        video_clip = video_clip.set_audio(final_audio)

        # 构建输出路径
        video_filename = os.path.basename(video_path)
        output_path = os.path.join(output_dir, video_filename)

        # 导出视频
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

        print("成功添加背景音乐")

    except Exception as e:
        print(f"添加背景音乐失败: {e}")
    
    return output_path