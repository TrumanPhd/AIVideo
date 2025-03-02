# -*- coding: utf-8 -*-
# Author: AIGC自动化脚本
# Date: 2025-02-19
# env: SS2 MACBOOK AIR M2

import os
from Setting import *
from music import *
from utils import *
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# ---- 变量定义----
SCOPES = ['https://www.googleapis.com/auth/youtube.upload'] #upload permission
CLIENT_SECRETS_FILE = 'client_secret.json' #your credential
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_authenticated_service():
    """
    获取 YouTube Data API V3 认证服务。
    """
    creds = None
    # token.pickle 文件存储了用户的访问和刷新令牌
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # 如果没有可用的凭证（第一次运行或令牌已过期），则让用户登录
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # 保存凭证以备下次运行
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=creds)

def up2youtube(video_file_path, video_title, cover_image_path, video_description):
    """
    将视频上传到 YouTube。

    Args:
        video_file_path (str): 视频文件的完整路径。
        video_title (str): 视频标题。
        cover_image_path (str): 封面图片的完整路径。
        video_description (str): 视频描述。

    Returns:
        bool: True 如果上传成功，否则为 False。
    """
    try:
        youtube = get_authenticated_service()

        body = {
            'snippet': {
                'title': video_title,
                'description': video_description,
                'tags': ['AI', 'Generated', 'Short Video']  # Add relevant tags
            },
            'status': {
                'privacyStatus': 'public'  # Set to 'private' if you want it unlisted
            }
        }

        # 上传视频
        media = MediaFileUpload(video_file_path, mimetype='video/mp4', resumable=True)
        request = youtube.videos().insert(
            part='snippet,status',
            body=body,
            media=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"上传进度: {int(status.progress() * 100)}%")

        video_id = response['id']
        print(f"视频上传成功，视频ID: {video_id}")

        # 设置封面 (如果提供了封面图片)
        if cover_image_path:
            try:
                request = youtube.thumbnails().set(
                    videoId=video_id,
                    media=MediaFileUpload(cover_image_path, mimetype='image/jpeg') # Adjust mimetype if needed
                )
                response = request.execute()
                print("成功设置视频封面")
            except Exception as e:
                print(f"设置视频封面失败: {e}")
        else:
            print("没有提供封面图片，跳过设置封面")

        return True

    except Exception as e:
        print(f"上传到 YouTube 失败: {e}")
        return False