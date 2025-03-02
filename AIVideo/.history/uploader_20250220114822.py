# -*- coding: utf-8 -*-
# Author: AIGC自动化脚本
# Date: 2025-02-19
# file: uploader.py
# 视频上传到 YouTube 的功能

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import os
import time
import random

# ---- 全局变量 ----
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']  # 上传权限
CLIENT_SECRETS_FILE = 'client_secret.json'  # 你的凭证文件
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def get_authenticated_service():
    """
    认证并返回YouTube API服务对象。
    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)  # 运行本地服务器进行认证
    youtube = googleapiclient.discovery.build(
        YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)
    return youtube


def up2youtube(video_path, title, thumbnail_path, description="默认描述", privacy_status="private"):
    """
    上传视频到YouTube。

    Args:
        video_path: 视频文件路径。
        title: 视频标题。
        thumbnail_path: 缩略图文件路径。
        description: 视频描述。
        privacy_status: 视频隐私状态 (public, private, unlisted)。  默认为 private

    Returns:
        True if upload was successful, False otherwise.
    """
    print("开始上传视频到 YouTube...")
    youtube = get_authenticated_service()

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['AI', 'Generated', 'ShortVideo'],  # 添加更多相关标签
            'categoryId': '28'  # 科学与技术类别。  请参考：https://developers.google.com/youtube/v3/docs/videoCategories/list
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media_file = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    try:
        insert_request = youtube.videos().insert(
            part=','.join(request_body.keys()),
            body=request_body,
            media_body=media_file
        )

        response = None
        retry = 0
        while response is None and retry < 5:
            try:
                print("正在上传视频...")
                status, response = insert_request.next_chunk()
                if response is not None:
                    if 'id' in response:
                        print(f"视频上传成功！视频 ID: {response['id']}")

                        # 上传缩略图
                        if thumbnail_path:
                            try:
                                youtube.thumbnails().set(
                                    videoId=response['id'],
                                    media_body=MediaFileUpload(thumbnail_path)
                                ).execute()
                                print("缩略图上传成功！")
                            except googleapiclient.errors.HttpError as e:
                                print(f"上传缩略图时发生 HTTP 错误 {e.resp.status}：\n{e.content}")
                                return False # Thumbnail failure shouldn't halt the whole process

                        return True  # 视频上传成功
                    else:
                        print(f"上传失败，返回意外响应：{response}")
                        return False

            except googleapiclient.errors.HttpError as e:
                if e.resp.status in [400, 401, 403, 404]:  # 不可重试的错误
                    print(f"发生 HTTP 错误 {e.resp.status}：\n{e.content}")
                    return False
                elif e.resp.status in [500, 502, 503, 504]:  # 可重试的服务器错误
                    print(f"发生 HTTP 错误 {e.resp.status}：\n{e.content}\n正在重试...")
                    time.sleep((2 ** retry) + random.random())  # 指数退避
                    retry += 1
                else:
                    print(f"发生意外的 HTTP 错误 {e.resp.status}：\n{e.content}")
                    return False
            except HttpError as e: # Handle google.auth.exceptions.HttpError
               print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
               return False
            except Exception as e: # Catch other exceptions
                print(f"An unexpected error occurred: {e}")
                return False


        return False  # 达到重试上限仍未成功

    except Exception as e:
        print(f"发生意外错误: {e}")
        return False