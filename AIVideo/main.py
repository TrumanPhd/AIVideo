# -*- coding: utf-8 -*-
# Author: AIGC自动化脚本
# Date: 2025-02-19
# env: SS2 MACBOOK AIR M2

from GLM import call_GLM
from Setting import *
from music import *
from utils import *
from kling import call_kling
from Uploader import *

# ---- 变量定义----
SCOPES = ['https://www.googleapis.com/auth/youtube.upload'] #upload permission
CLIENT_SECRETS_FILE = 'client_secret.json' #your credential
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# ---- 主流程 ----
def run_one():
    #"""
    # LLM获取文本提示 
    # GLM-4 is free
    #！！！下面这个初始的文本提示还要修改 ai生成的规范化范式！！！
    text_prompt = call_GLM(GLM_api_key, initial_prompt)

    if text_prompt:
        #print(f"用于视频生成的文本提示: {text_prompt}")
        try:
            video_title, text_prompt4video = text_prompt.split("|||")
            print(f"视频标题：{video_title}")
            print(f"用于视频生成的文本提示: {text_prompt4video}")
        except ValueError:
            print("生成文本格式不正确，未能提取视频标题和文本提示。")
    else:
        print("无法生成用于视频生成的文本提示。")

    # 生成视频
    video_path = call_kling(kling_api_key, kling_secret_key, text_prompt4video=text_prompt4video, video_save_path=output_path)

    if video_path:
        print(f"视频生成成功，保存在: {video_path}")
    else:
        print("视频生成失败。")
        exit()
    #"""
    
    #debug
    #video_path = "/Users/truman/AIGC/Video/V20250220945528.mp4"
    #video_title = "AI Generated Short Video"
    
    # 添加背景音乐
    publication_path = add_music(video_path)

    # 提取视频第一帧作为封面
    output_dir = '/Users/truman/AIGC/Publication/cover_img/'
    cover_image_path = extract_first_frame(video_path, output_dir)
    print(f"封面图片已成功提取并保存到: {cover_image_path}")

    # 准备视频描述
    video_description = "Subscribe to my channel for more interesting AI-generated videos."

    print("发布材料准备完成") 
     
    # 发布视频
    if not up2youtube(publication_path, video_title, cover_image_path, video_description):
        print("上传到YouTube失败。")
        
    #if not up2Tiktok(publication_path, video_title, cover_image_path, video_description):
    #    print("上传到Tiktok失败。")

for i in range(4):
    run_one()
    print(f"第{i+1}次发布完成。")