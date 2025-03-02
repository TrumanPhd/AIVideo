# -*- coding: utf-8 -*-
# file: Tiktok.py
# 视频自动发布到TikTok 的功能
# fun name: up2Tiktok

import os
import time
import random
import requests
import json  # 用于处理 JSON 响应
from urllib.parse import urlparse, urlencode

# ---- 变量定义 ----
TIKTOK_API_ENDPOINT_INIT = "/v2/post/publish/video/init/"  #  初始化上传
TIKTOK_API_ENDPOINT_UPLOAD = "" # PUT 请求的 endpoint，需要动态获取
TIKTOK_ACCESS_TOKEN = "YOUR_TIKTOK_ACCESS_TOKEN"  # 替换为你的 TikTok 访问令牌
TIKTOK_APP_ID = "YOUR_TIKTOK_APP_ID"  # 替换为你的 TikTok 应用 ID
# 注意：以下 API 需要替换为实际的 URL
TIKTOK_BASE_URL = "https://open.tiktokapis.com"

def up2Tiktok(video_path, title, description="默认描述", privacy_level="MUTUAL_FOLLOW_FRIENDS",
                disable_duet=False, disable_stitch=False, disable_comment=True,
                video_cover_timestamp_ms=1000, is_aigc=False):  # 添加 is_aigc 参数
    """
    上传视频到 TikTok. 遵循 Direct Post API 的流程.

    Args:
        video_path (str): 视频文件路径.
        title (str): 视频标题.
        description (str): 视频描述.
        privacy_level (str): 隐私级别.  可选值: "PUBLIC_TO_EVERYONE", "MUTUAL_FOLLOW_FRIENDS",
                             "FOLLOWER_OF_CREATOR", "SELF_ONLY".  默认为 "MUTUAL_FOLLOW_FRIENDS".
        disable_duet (bool): 是否禁用合拍 (Duet). 默认为 False.
        disable_stitch (bool): 是否禁用拼接 (Stitch). 默认为 False.
        disable_comment (bool): 是否禁用评论. 默认为 True.
        video_cover_timestamp_ms (int): 视频封面时间戳 (毫秒). 默认为 1000 毫秒.
        is_aigc (bool):  是否为 AI 生成内容。 默认为 False.

    Returns:
        bool: True 如果上传成功，False 如果上传失败.
    """
    print("开始上传视频到 TikTok (Direct Post)...")

    try:
        # 1. 初始化上传请求 (Initialize the posting request)
        init_data = {
            "post_info": {
                "title": title,
                "privacy_level": privacy_level,
                "disable_duet": disable_duet,
                "disable_stitch": disable_stitch,
                "disable_comment": disable_comment,
                "video_cover_timestamp_ms": video_cover_timestamp_ms,
                "is_aigc": is_aigc  # 添加 is_aigc
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": os.path.getsize(video_path),  # 获取文件大小
                "chunk_size": 10000000,  # 10MB chunk size  (根据 API 文档调整)
                "total_chunk_count": -1 # 需要计算, 这里先设置成 -1 占位
            }
        }
        # 计算总的 chunk count
        file_size = os.path.getsize(video_path)
        chunk_size = init_data["source_info"]["chunk_size"]
        total_chunk_count = (file_size + chunk_size - 1) // chunk_size  # 计算总的块数
        init_data["source_info"]["total_chunk_count"] = total_chunk_count


        init_headers = {
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}",
            "Content-Type": "application/json; charset=UTF-8",
        }
        init_url = TIKTOK_BASE_URL + TIKTOK_API_ENDPOINT_INIT
        init_response = requests.post(init_url, headers=init_headers, data=json.dumps(init_data))

        if init_response.status_code == 200:
            init_json = init_response.json()
            print(f"TikTok Init API 响应: {json.dumps(init_json, indent=4, ensure_ascii=False)}")

            if init_json["error"]["code"] == "ok":
                upload_url = init_json["data"]["upload_url"]
                publish_id = init_json["data"]["publish_id"] # 用于追踪发布状态
                # 验证 upload_url 是否存在
                if not upload_url:
                    print("初始化请求成功，但未获取到 upload_url")
                    return False
                print(f"初始化上传成功，upload_url: {upload_url}, publish_id: {publish_id}")

                # 2. 上传视频 (Send Video to TikTok Servers - Chunked Upload)
                with open(video_path, "rb") as f:
                    offset = 0
                    chunk_index = 0
                    while True:
                        chunk = f.read(chunk_size)
                        if not chunk:
                            break

                        content_length = len(chunk)
                        content_range = f"bytes {offset}-{offset + content_length - 1}/{file_size}"
                        upload_headers = {
                            "Content-Type": "video/mp4",  # 确保 MIME 类型正确,  请根据视频文件调整.
                            "Content-Range": content_range,
                            "Content-Length": str(content_length),
                        }
                        print(f"上传 Chunk {chunk_index + 1}/{total_chunk_count}, Content-Range: {content_range}")
                        upload_response = requests.put(upload_url, headers=upload_headers, data=chunk)

                        if upload_response.status_code != 200:
                            print(f"上传 Chunk {chunk_index + 1} 失败，HTTP 状态码: {upload_response.status_code}, 响应内容: {upload_response.text}")
                            return False
                        print(f"上传 Chunk {chunk_index + 1} 成功")
                        offset += content_length
                        chunk_index += 1
                print("所有 Chunk 上传完成")
                # TODO: 3. 发布视频 (Publish the video) 需要调用另一个 API, 这里省略

                return True  # 上传成功
            else:
                print(f"初始化上传失败，错误代码: {init_json['error']['code']}, 错误信息: {init_json['error']['message']}")
                return False
        else:
            print(f"初始化上传失败，HTTP 状态码: {init_response.status_code}, 响应内容: {init_response.text}")
            return False

    except FileNotFoundError:
        print(f"视频文件未找到: {video_path}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"上传到 TikTok 时发生网络错误: {e}")
        return False
    except json.JSONDecodeError as e:
         print(f"解析 JSON 响应时出错：{e},  响应内容: {init_response.text if 'init_response' in locals() else '未获取到响应'}")
         return False

    except Exception as e:
        print(f"上传到 TikTok 时发生未知错误: {e}")
        return False