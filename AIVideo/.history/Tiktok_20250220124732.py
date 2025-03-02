# -*- coding: utf-8 -*-
# file: Tiktok.py
# 视频自动发布到Tiktok 的功能
# fun name: up2Tiktok

import os
import time
import random
import requests
import json  # 用于处理 JSON 响应
from urllib.parse import urlparse, urlencode

# ---- 变量定义 ----
TIKTOK_API_ENDPOINT = "https://open-api.tiktok.com/v1.3/video/upload/"  # TikTok 开放平台上传 API (请查阅最新的 API 文档)
# 请注意，这只是一个示例 API endpoint。  你需要根据 TikTok 开放平台的最新 API 文档，
# 获取正确的 API endpoint。
TIKTOK_ACCESS_TOKEN = "YOUR_TIKTOK_ACCESS_TOKEN"  # 替换为你的 TikTok 访问令牌  (需要申请和获取)
# 这里需要替换成你的 TikTok 访问令牌，你需要注册 TikTok 开放平台账号，创建一个应用，
# 并获取访问令牌。 访问令牌的获取和刷新机制和 YouTube 类似。
#  具体步骤请参考 TikTok 开放平台的 API 文档。
#  通常，访问令牌有过期时间，你需要实现刷新令牌的机制。
#  在开发和测试阶段，你可以使用一个固定的访问令牌，但在生产环境中，
#  建议实现访问令牌的自动刷新。
TIKTOK_APP_ID = "YOUR_TIKTOK_APP_ID"  # 替换为你的 TikTok 应用 ID
TIKTOK_APP_SECRET = "YOUR_TIKTOK_APP_SECRET"  # 替换为你的 TikTok 应用密钥  (用于获取访问令牌)
#  请确保你的应用 ID 和应用密钥是正确的。

# ---- up2Tiktok 函数 ----
def up2Tiktok(video_path, title, description="默认描述", enable_watermark=True):  # 添加 enable_watermark 参数
    """
    上传视频到 TikTok。

    Args:
        video_path (str): 视频文件路径。
        title (str): 视频标题。
        description (str): 视频描述。
        enable_watermark (bool):  是否启用 TikTok 水印 (默认启用).
            有些 API  可能不支持该参数，或者需要不同的方式来控制水印，
            请查阅 TikTok API 文档。

    Returns:
        bool: True 如果上传成功，False 如果上传失败。
    """
    print("开始上传视频到 TikTok...")

    try:
        # 1.  构造请求头 (headers)
        headers = {
            "Content-Type": "application/octet-stream",  # TikTok API 通常接受这种类型的视频上传
            "Authorization": f"Bearer {TIKTOK_ACCESS_TOKEN}"  # 使用访问令牌进行身份验证
            # 根据 TikTok API 文档，可能需要其他的请求头。  请查阅 TikTok API 文档。
        }

        # 2. 准备上传数据 (data, params, files)
        #   TikTok 的 API 可能需要不同的参数。  请查阅 TikTok API 文档。

        # TikTok 的上传 API 可能需要将视频文件作为文件上传，也可能需要将文件内容编码为 base64 字符串
        #  根据不同的 API，需要使用不同的方式来上传视频。  以下是两种常见的上传方式的示例。
        #  请查阅 TikTok API 文档，确定应该使用哪种方式。

        # 方式 1: 将视频文件作为文件上传 (file)
        files = {
            "video": (os.path.basename(video_path), open(video_path, "rb"), "video/mp4")  # 请根据视频格式调整 mimetype
            #  请注意 "video/mp4" 只是一个示例，你需要根据你的视频的实际格式设置正确的 MIME 类型。
        }

        data = {
            "title": title,  # 视频标题
            "description": description,  # 视频描述
            "enable_watermark": str(enable_watermark).lower(),  # 是否启用水印。将布尔值转换为字符串
            "app_id": TIKTOK_APP_ID  # 你的应用 ID
            #   其他可能需要的参数，请查阅 TikTok API 文档。
        }
        params = {}

        # 方式 2: 将视频文件内容作为 base64 编码的字符串上传 (data)  (示例)
        #  这种方式通常不太常见，但有些 API 可能会使用这种方式。
        #  你需要先读取视频文件，将其编码为 base64 字符串，然后将字符串作为 API 请求的数据发送。
        # with open(video_path, "rb") as f:
        #     video_content = f.read()
        # import base64
        # video_base64 = base64.b64encode(video_content).decode("utf-8") # 编码为字符串
        # data = {
        #     "title": title,
        #     "description": description,
        #     "video_content": video_base64 # 将 base64 字符串作为数据发送
        #     # 其他参数
        # }
        # files = {}  # 不需要文件上传

        # 3. 发送 API 请求
        response = requests.post(
            TIKTOK_API_ENDPOINT,
            headers=headers,
            files=files,  # 如果使用文件上传
            data=data, # 如果使用 data 上传
            # params = params #  如果你的 API 需要使用查询参数 (query parameters)  传递数据
        )

        # 4.  处理 API 响应
        if response.status_code == 200:
            try:
                response_json = response.json()  # 尝试将响应解析为 JSON
                print(f"TikTok API 响应: {json.dumps(response_json, indent=4, ensure_ascii=False)}") # 打印完整响应
                # 检查响应中的错误
                if "error_code" in response_json and response_json["error_code"] != 0: # 检查错误码
                    print(f"上传到 TikTok 失败，错误代码: {response_json['error_code']},  错误信息: {response_json['message']}")
                    return False
                elif "data" in response_json and "video_id" in response_json["data"]: # 检查视频 ID
                    video_id = response_json["data"]["video_id"]
                    print(f"视频上传成功！视频 ID: {video_id}")
                    # 你可以保存 video_id  用于后续的操作，例如发布视频。
                    return True
                else:
                    print("上传到 TikTok 成功，但无法获取视频 ID")
                    return True #  可能上传成功，但获取不到视频 ID
            except json.JSONDecodeError:
                print(f"成功上传到 TikTok，但无法解析 JSON 响应: {response.text}")
                #  如果无法解析 JSON，可能是因为 API 返回了其他格式的响应。
                #  在这种情况下，你需要仔细分析 API 文档，确定响应的格式，并相应地修改代码。
                return True  #  可能上传成功，但无法解析 JSON 响应
        else:
            print(f"上传到 TikTok 失败，HTTP 状态码: {response.status_code}, 响应内容: {response.text}")
            return False

    except FileNotFoundError:
        print(f"视频文件未找到: {video_path}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"上传到 TikTok 时发生网络错误: {e}")
        return False
    except Exception as e:
        print(f"上传到 TikTok 时发生未知错误: {e}")
        return False

# ---- 循环上传的示例 (主程序) ----
if __name__ == "__main__":
    num_videos = 3  #  要上传的视频数量
    for i in range(num_videos):
        print(f"开始上传第 {i + 1} 个视频到 TikTok...")

        # --- 准备视频信息 ---
        video_path = "/Users/truman/AIGC/Video/V20250220945528.mp4"  # 替换为你的视频文件路径 (或动态生成)
        video_title = f"TikTok AI 视频 {i+1}"  #  动态生成标题
        video_description = "This is an AI-generated TikTok video. #AI #Shorts"  #  替换为你的描述
        #  设置是否启用水印。  TikTok API 可能不支持，或者需要其他方式控制水印。
        enable_watermark = True

        # --- 调用 up2Tiktok 函数 ---
        if up2Tiktok(video_path, video_title, video_description, enable_watermark):
            print(f"第 {i + 1} 个视频上传到 TikTok 成功！")
        else:
            print(f"第 {i + 1} 个视频上传到 TikTok 失败。")
        # 添加适当的延迟，避免过于频繁地调用 API。
        sleep_time = random.randint(5, 15)  # 随机休眠时间 (秒)
        print(f"等待 {sleep_time} 秒...")
        time.sleep(sleep_time)

    print("所有视频上传完成!")