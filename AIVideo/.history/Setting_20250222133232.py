# ---- 配置参数 ----
# 文件路径
VIDEO_SAVE_PATH = "/Users/truman/AIGC/Video"
VIDEO_SAVE_PATH = "/Users/truman/AIGC/Video"

# LLM API key 参数
# GLM API key 参数
GLM_api_key = "3bd4dea3a34b414db6e45e795cb47eff.KNrix0Vn5onaqYza"

# T2V API key 参数
# kling API key 参数设置
KLING_AI_API_ENDPOINT = "https://api.klingai.com"
kling_api_key = "500ad6365ba44229a64c1cc79750860a"  # 可灵 AI Access Key
kling_secret_key = "612f42c6ecfb41598b4d6bcc9fc7e649"  # 可灵 AI Secret Key
output_path = "/Users/truman/AIGC/Video" #视频输出路径

# 发布视频
YOUTUBE_ACCOUNT = "@VideoAIGC"
TIKTOK_ACCOUNT = "@videoaigc"
YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
TIKTOK_API_ENDPOINT = "YOUR_TIKTOK_API_ENDPOINT"
YOUTUBE_API_KEY = "AIzaSyByW3Pxi3_yw4h0Un293iGC4XBBbEYgEE4"
TIKTOK_API_KEY = "YOUR_TIKTOK_API_KEY"

# 视频平台数据分析
VIDEO_ANALYSIS_API_ENDPOINT = "YOUR_VIDEO_ANALYSIS_API_ENDPOINT"  # 替换为你的视频分析 API endpoint
VIDEO_ANALYSIS_API_KEY = "YOUR_VIDEO_ANALYSIS_API_KEY"  # 替换为你的视频分析 API key

# 初始化文本提示
#initial_prompt = "用英文创作一个吸引人的5s短视频生成的文本提示要求尽量详细，在画面中间要有一个主角，主角要有夸张或者快速的动作，环境的部分要自然美观，视频提示文本部分不分段，用一个完整自然段输出，不少于400词，不超过600词，要求大开脑洞有天马行空的想象，画面要鲜艳脑洞吸引人，只打印用作视频生成模型的提示和视频的标题，用下面格式输出: 英文的视频题目||英文的视频的文本提示，不分段用一个完整的段落输出  此外不要含有任何其他符号"
initial_prompt = 'Create a Captivating 5-Second Short Video, The text prompt for the video generation should be as detailed as possible. In the center of the frame, there must be a main character who performs exaggerated or rapid movements. The surrounding environment should be natural and aesthetically pleasing. The video prompt text should be a continuous paragraph of no less than 300 words and no more than 400 words. Think outside the box with fantastical imagination. The visuals should be vibrant and creatively captivating. Your output format: (Title of video, only title) + ||+ (Video Prompt Text in one paragraph) '
# 模型s