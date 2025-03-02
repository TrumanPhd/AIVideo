# -*- coding: utf-8 -*-
# Author: AIGC自动化脚本
# Date: 2025-02-19
# env: SS2 MACBOOK AIR M2

import os
from sklearn.metrics.pairwise import cosine_similarity
from GLM import call_GLM
from Setting import *
from music import *
from utils import *
from kling import call_kling

# ---- 主流程 ----
if __name__ == "__main__":
    # LLM获取文本提示 GLM-4 is free
    #！！！下面这个初始的文本提示还要修改
    initial_prompt = "用英文创作一个吸引人的5s短视频生成的文本提示，要求大开脑洞有天马行空的想象，只打印用作视频生成模型的提示"
    api_key = "3bd4dea3a34b414db6e45e795cb47eff.KNrix0Vn5onaqYza"
    text_prompt = call_GLM(api_key, initial_prompt)

    if text_prompt:
        print(f"用于视频生成的文本提示: {text_prompt}")
    else:
        print("无法生成用于视频生成的文本提示。")
    
    # 调用可灵 AI API 生成视频 100次
    api_key = "500ad6365ba44229a64c1cc79750860a"  # 替换为你的可灵 AI Access Key
    secret_key = "612f42c6ecfb41598b4d6bcc9fc7e649"  # 替换为你的可灵 AI Secret Key
    output_path = "/Users/truman/AIGC/Video" #视频输出路径

    video_path = call_kling(api_key, secret_key, text_prompt4video=text_prompt, video_save_path=output_path)

    if video_path:
        print(f"视频生成成功，保存在: {video_path}")
    else:
        print("视频生成失败。")


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
    # 提取视频第一帧作为封面 (使用带背景音乐的视频或原始视频)
    if not extract_first_frame(video_with_music_filepath, cover_image_filepath):
        print("提取视频封面失败，程序可能继续，但上传的封面将是默认封面。")

    print(f"视频封面保存到: {cover_image_filepath}")

    # 准备视频标题和描述
    video_title = "AI的未来：一段充满希望的旅程"
    video_description = script

    # 上传到YouTube (模拟)
    if not upload_to_youtube(video_with_music_filepath, video_title, video_description):
        print("上传到YouTube失败。")
"""
    # 9. 上传到TikTok (模拟)
    if not upload_to_tiktok(video_with_music_filepath, video_title, video_description):
        print("上传到TikTok失败。")

    print("自动化流程完成！")
"""
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