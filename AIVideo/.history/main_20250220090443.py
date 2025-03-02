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
    
    # 生成视频
    video_path = call_kling(api_key, secret_key, text_prompt4video=text_prompt, video_save_path=output_path)

    if video_path:
        print(f"视频生成成功，保存在: {video_path}")
    else:
        print("视频生成失败。")

    # 添加音乐
    

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
