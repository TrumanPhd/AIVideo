# filename: kling.py
# CALL kling for Video Generation
import os
import datetime
import json
import requests
import time
import jwt  # 用于生成JWT Token

# 为了适配段视频，请求体还要修改

# ---- 配置参数 ----
KLING_AI_API_ENDPOINT = "https://api.klingai.com"
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
        "exp": int(time.time()) + 3600,  # 有效时间，此处示例代表当前时间+3600s(1小时)
        "nbf": int(time.time()) - 5  # 开始生效的时间，此处示例代表当前时间-5秒
    }
    try:
        token = jwt.encode(payload, sk, algorithm="HS256", headers=headers) #明确指定算法
        return token
    except Exception as e:
        print(f"JWT 编码失败: {e}")
        return None


def call_kling(api_key, secret_key, model_name="kling-v1-6", duration="5", text_prompt4video="A futuristic city", video_save_path=VIDEO_SAVE_PATH, max_retries = 1):
    """
    调用可灵 AI API 生成视频，单次请求，生成单个视频。

    Args:
        api_key:  可灵 AI API 的 Access Key。
        secret_key: 可灵 AI API 的 Secret Key.
        model_name: 模型型号，默认为 "kling-v1"
        duration: 视频时长，默认为 "5" (秒)。
        text_prompt4video: 用于指导视频生成的文本提示。
        video_save_path: 视频下载后的本地保存路径。
        max_retries: 最大重试次数，用于应对网络波动等问题。

    Returns:
        如果成功下载视频，则返回本地保存路径；否则返回 None。
    """
    for attempt in range(max_retries):
        try:
            # 1. 生成 JWT Token
            api_token = encode_jwt_token(api_key, secret_key)
            if not api_token:
                print("无法生成API Token，视频生成失败。")
                return None

            print(f"生成的 JWT Token: {api_token}")  # 打印生成的Token

            # 2. 构造请求头
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_token}'  # 确保 "Bearer" 后面有一个空格
            }

            # 3. 构造请求体
            data = {
                'prompt': text_prompt4video,
                'duration': duration,
                'model_name': model_name,
                'aspect_ratio': "9:16", # 9:16 纵向视频  16:9 横向视频
            }

            # 4. 创建视频生成任务并获取视频 URL
            create_url = f"{KLING_AI_API_ENDPOINT}/v1/videos/text2video"  # 文生视频API endpoint
            print(f"请求头: {headers}")  # 打印请求头
            print(f"请求体: {data}")  # 打印请求体

            response = requests.post(create_url, headers=headers, json=data)
            response.raise_for_status()
            create_response = response.json()

            if create_response['code'] != 0:
                print(f"创建视频生成任务失败: {create_response['message']}")
                return None

            task_id = create_response['data']['task_id']
            print(f"创建任务成功，任务ID: {task_id}")

            # 查询任务状态，直到完成
            query_url = f"{KLING_AI_API_ENDPOINT}/v1/videos/text2video/{task_id}"
            max_attempts = 100000 # 最大查询次数
            delay = 60       # 查询间隔 (秒)

            for query_attempt in range(max_attempts):
                time.sleep(delay)
                try: #添加对查询任务的try except，否则在查询中如果出现网络或者json解析问题会导致流程中断
                    query_response = requests.get(query_url, headers=headers).json()

                    if query_response['code'] != 0:
                        print(f"查询任务状态失败: {query_response['message']}")
                        return None

                    task_status = query_response['data']['task_status']

                    if task_status == "succeed":
                        video_url = query_response['data']['task_result']['videos'][0]['url']
                        print(f"视频生成成功，URL: {video_url}")
                        break
                    elif task_status == "failed":
                        print(f"视频生成失败：{query_response['data']['task_status_msg']}")
                        return None

                    print(f"任务仍在处理中，已尝试{query_attempt+1}/{max_attempts}次")
                except requests.exceptions.RequestException as e:
                    print(f"查询视频生成任务状态请求失败: {e}")
                    return None
                except (KeyError, TypeError, ValueError) as e:
                    print(f"解析可灵AI API响应失败: {e}")
                    return None

            else:  # 循环正常结束 (未 break)
                print(f"任务超时，已达到最大尝试次数 ({max_attempts}次)")
                return None

            # 5. 下载视频
            filename = generate_filename()
            filepath = os.path.join(video_save_path, f"{filename}.mp4")
            try:
                video_response = requests.get(video_url, stream=True)
                video_response.raise_for_status()
                with open(filepath, 'wb') as video_file:
                    for chunk in video_response.iter_content(chunk_size=8192):
                        video_file.write(chunk)
                print(f"视频已成功下载到: {filepath}")
                return filepath  # 返回本地文件路径 # 成功下载，直接返回
            except requests.exceptions.RequestException as e:
                print(f"下载视频失败: {e}")
                return None
            except OSError as e:
                print(f"保存视频文件失败：{e}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求可灵AI API失败 (尝试次数 {attempt+1}/{max_retries}): {e}")
            # 身份验证失败时，直接返回，不再重试
            if e.response is not None and e.response.status_code == 401: #身份验证失败不再进行重试
                print("身份验证失败，不再重试")
                return None
            time.sleep(5)  # 等待一段时间后重试
        except (KeyError, TypeError, ValueError) as e:
            print(f"解析可灵AI API响应失败(尝试次数 {attempt+1}/{max_retries}): {e}")
            return None

    print("达到最大重试次数，任务失败。")
    return filepath