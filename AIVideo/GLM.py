# API CALL GLM for Text prompt Generation

from zhipuai import ZhipuAI

def call_GLM(api_key, initial_prompt, model="glm-4v-plus"):
    """
    调用 GLM-4V 系列模型生成视频文本提示。

    Args:
        api_key: 智谱 AI API Key.
        initial_prompt:  用户提供的初始文本提示。
        model:  使用的 GLM-4V 模型名称 (glm-4v-plus, glm-4v, glm-4v-flash).

    Returns:
        生成的用于指导视频生成的文本提示，如果出现错误则返回 None。
    """

    try:
        client = ZhipuAI(api_key=api_key)  # 填写您自己的APIKey
        response = client.chat.completions.create(
            model=model,  # 填写需要调用的模型名称
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": initial_prompt
                        }
                    ]
                }
            ]
        )

        if response and response.choices and len(response.choices) > 0: # 确保response不为空, choices不为空，且有内容。
            generated_text = response.choices[0].message.content
            #print(f"GLM-4 生成的文本提示: {generated_text}")
            return generated_text #返回生成的结果
        else:
            print("GLM-4 API 返回结果为空或格式不正确。")
            return None

    except Exception as e:
        print(f"调用 GLM-4 API 失败: {e}")
        return None