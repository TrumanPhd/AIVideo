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
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = 'client_secret.json'
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


def up2youtube(video_path, title, thumbnail_path, description="默认描述", privacy_status="public"):  # 修改了 privacy_status 的默认值
    """
    上传视频到YouTube。

    Args:
        video_path: 视频文件路径。
        title: 视频标题。
        thumbnail_path: 缩略图文件路径。
        description: 视频描述。
        privacy_status: 视频隐私状态 (public, private, unlisted)。  默认为 public (公开)

    Returns:
        True if upload was successful, False otherwise.
    """
    print("开始上传视频到 YouTube...")
    youtube = get_authenticated_service()

    # 设置视频类别标签
    video_category_id = '19'  # 默认类别 "生活" (People & Blogs)  你可以根据需要调整。  可以参考: https://developers.google.com/youtube/v3/docs/videoCategories/list

    if "有趣" in description or "搞笑" in description or "娱乐" in title:  # 根据描述和标题判断类别
        video_category_id = '23'  # 娱乐
    elif "科技" in description or "技术" in title or "创新" in title:
        video_category_id = '28'  # 科学与技术

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['AI', 'Generated', 'Shorts', 'ShortVideo'],  # 添加标签，包含 "Shorts"
            'categoryId': video_category_id  # 使用动态设置的类别
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False  # 对于 Shorts，通常设置为 False
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
                                # 缩略图失败不影响上传
                                # return False  # 缩略图失败不应该停止上传过程
                        # 为了确保是Shorts, 可以在这里添加检查，视频时长在1分钟以内
                        # 这里的判断需要先读取视频文件，所以不在这里实现

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
            except googleapiclient.errors.HttpError as e: # Handle google.auth.exceptions.HttpError
               print(f"An HTTP error {e.resp.status} occurred:\n{e.content}")
               return False
            except Exception as e: # Catch other exceptions
                print(f"An unexpected error occurred: {e}")
                return False


        return False  # 达到重试上限仍未成功

    except Exception as e:
        print(f"发生意外错误: {e}")
        return False