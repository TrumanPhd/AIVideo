# -*- coding: utf-8 -*-
# Author: AIGC自动化脚本
# Date: 2025-02-19
# env: SS2 MACBOOK AIR M2

from GLM import call_GLM
from Setting import *
from music import *
from utils import *
from uploader import *
from kling import call_kling

# ---- 变量定义----
SCOPES = ['https://www.googleapis.com/auth/youtube.upload'] #upload permission
CLIENT_SECRETS_FILE = 'client_secret.json' #your credential
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# ---- 主流程 ----
if __name__ == "__main__":
    """
    # LLM获取文本提示 
    # GLM-4 is free
    #！！！下面这个初始的文本提示还要修改 ai生成的规范化范式！！！
    initial_prompt = "用英文创作一个吸引人的5s短视频生成的文本提示要求尽量详细，要求大开脑洞有天马行空的想象，只打印用作视频生成模型的提示和视频的标题，用下面格式输出: 英文的视频题目||视频的文本提示"
    text_prompt = call_GLM(GLM_api_key, initial_prompt)

    if text_prompt:
        print(f"用于视频生成的文本提示: {text_prompt}")
        try:
            video_title, text_prompt4video = text_prompt.split("||")
            print(f"视频标题：{video_title}")
            print(f"用于视频生成的文本提示: {text_prompt4video}")
        except ValueError:
            print("生成文本格式不正确，未能提取视频标题和文本提示。")
            video_title = "AI Generated Short Video"  # Default title if extraction fails
            text_prompt4video = text_prompt #Keep Text Prompt for kling generation
    else:
        print("无法生成用于视频生成的文本提示。")
        #video_title = "AI Generated Short Video" # Default title if GLM fails
        #text_prompt4video = initial_prompt #Default text prompt

    # 生成视频
    video_path = call_kling(kling_api_key, kling_secret_key, text_prompt4video=text_prompt4video, video_save_path=output_path)

    if video_path:
        print(f"视频生成成功，保存在: {video_path}")
    else:
        print("视频生成失败。")
        exit()
    """
    
    #debug
    video_path = "/Users/truman/AIGC/Video/V20250220945528.mp4"
    video_title = "AI Generated Short Video"
    
    # 添加背景音乐
    publication_path = add_music(video_path)

    # 提取视频第一帧作为封面
    output_dir = '/Users/truman/AIGC/Publication/cover_img/'
    cover_image_path = extract_first_frame(video_path, output_dir)

    if cover_image_path:
        print(f"封面图片已成功提取并保存到: {cover_image_path}")
    else:
        print("提取封面图片失败")
    
    # 准备视频描述
    video_description = "Subscribe to my channel for more interesting AI-generated videos."

    print("发布材料准备完成") 
     
    # 上传到YouTube
    #if not up2youtube(publication_path, video_title, cover_image_path, video_description):
    #    print("上传到YouTube失败。")
