# CALL kling for Video Generation
import os
import datetime
import json
import subprocess
import requests
import time
import jwt  # 用于生成JWT Token

# ---- 配置参数 ----
KLING_AI_API_ENDPOINT = "https://api.klingai.com"  # 替换为你的 Kling AI API endpoint
VIDEO_SAVE_PATH = "/Users/truman/AIGC/Video"

# ---- 辅助函数 ----
def generate_filename():
    """生成视频文件名"""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y%m%d")
    counter = int(time.time() * 1000) % 1000000
    return f"V{date_str}{counter:06d}"

def encode_jwt_token(ak, sk):
    """生成JWT Token"""
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800,  # 有效时间，此处示例代表当前时间+1800s(30min)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token


def call_kling(api_key, secret_key, model_name="kling-v1", duration="5", text_prompt4video="A futuristic city", video_save_path=VIDEO_SAVE_PATH):
    """
    调用可灵 AI API 生成视频。
    Args:
        api_key:  可灵 AI API 的 Access Key。
        secret_key: 可灵 AI API 的 Secret Key.
        model_name: 模型型号，默认为 "kling-v1"
        duration: 视频时长，默认为 "5" (秒)。
        text_prompt4video: 用于指导视频生成的文本提示。
        video_save_path: 视频下载后的本地保存路径。

    Returns:
        如果成功下载视频，则返回本地保存路径；否则返回 None。
    """

    # 1. 生成 JWT Token
    api_token = encode_jwt_token(api_key, secret_key)
    if not api_token:
        print("无法生成API Token，视频生成失败。")
        return None

    # 2. 构造请求头
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    # 3. 构造请求体
    data = {
        'prompt': text_prompt4video,
        'duration': duration,
        'model_name': model_name,
    }

    # 4. 创建视频生成任务
    create_url = f"{KLING_AI_API_ENDPOINT}/v1/videos/text2video"  # 文生视频API endpoint
    try:
        response = requests.post(create_url, headers=headers, json=data)
        response.raise_for_status()
        create_response = response.json()
        if create_response['code'] != 0:
            print(f"创建视频生成任务失败: {create_response['message']}")
            return None

        task_id = create_response['data']['task_id']
        print(f"创建任务成功，任务ID: {task_id}")

    except requests.exceptions.RequestException as e:
        print(f"创建视频生成任务请求失败: {e}")
        return None
    except (KeyError, TypeError) as e:
        print(f"创建视频生成任务响应解析失败: {e}")
        return None

    # 5. 查询视频生成任务状态，直到完成
    query_url = f"{KLING_AI_API_ENDPOINT}/v1/videos/text2video/{task_id}"
    max_attempts = 20  # 最大查询次数
    delay = 10  # 查询间隔 (秒)
    video_url = None  # 存储最终的视频url
    for attempt in range(max_attempts):
        try:
            response = requests.get(query_url, headers=headers)
            response.raise_for_status()
            query_response = response.json()

            if query_response['code'] != 0:
                print(f"查询任务状态失败: {query_response['message']}")
                return None

            task_status = query_response['data']['task_status']
            print(f"任务状态: {task_status}")

            if task_status == 'succeed':
                try:
                    video_url = query_response['data']['task_result']['videos'][0]['url']  # 提取视频URL
                    break  # 任务成功，跳出循环

                except (KeyError, TypeError) as e:
                    print(f"获取视频URL失败: {e}")
                    return None
            elif task_status == 'failed':
                print(f"视频生成任务失败: {query_response['data']['task_status_msg']}")
                return None
            elif task_status == 'submitted' or task_status == 'processing':
                print(f"任务仍在处理中... 第 {attempt + 1}/{max_attempts} 次尝试")
            else:
                 print(f"未知任务状态: {task_status}")
                 return None

        except requests.exceptions.RequestException as e:
            print(f"查询视频生成任务状态请求失败: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}")
            return None

        time.sleep(delay)  # 等待一段时间再查询

    if not video_url:
        print("达到最大查询次数，视频生成可能超时或失败。")
        return None
    # 6. 下载视频
    filename = generate_filename()
    filepath = os.path.join(video_save_path, f"{filename}.mp4")
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"视频已成功下载到: {filepath}")

    except requests.exceptions.RequestException as e:
        print(f"视频下载失败: {e}")
        return None

    return filepath # 返回本地文件路径