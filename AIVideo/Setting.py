# ---- 配置参数 ----
# 文件路径
VIDEO_SAVE_PATH = "/Users/truman/AIGC/Video"
VIDEO_SAVE_PATH = "/Users/truman/AIGC/Video"

# LLM API key 参数
# GLM API key 参数
GLM_api_key = ""

# T2V API key 参数
# kling API key 参数设置
KLING_AI_API_ENDPOINT = "https://api.klingai.com"
kling_api_key = ""  # 可灵 AI Access Key
kling_secret_key = ""  # 可灵 AI Secret Key
output_path = "/Users/truman/AIGC/Video" #视频输出路径

# 发布视频
YOUTUBE_ACCOUNT = "@..."
TIKTOK_ACCOUNT = "@..."
YOUTUBE_API_ENDPOINT = "https://www.googleapis.com/youtube/v3"
TIKTOK_API_ENDPOINT = "YOUR_TIKTOK_API_ENDPOINT"
YOUTUBE_API_KEY = ""
TIKTOK_API_KEY = "YOUR_TIKTOK_API_KEY"

# 视频平台数据分析
VIDEO_ANALYSIS_API_ENDPOINT = "YOUR_VIDEO_ANALYSIS_API_ENDPOINT"  # 替换为你的视频分析 API endpoint
VIDEO_ANALYSIS_API_KEY = "YOUR_VIDEO_ANALYSIS_API_KEY"  # 替换为你的视频分析 API key

# 初始化文本提示
initial_prompt = "创作一个吸引人的5s视频画面场景,主题是非常非常丰盛的美食，包含世界各地的特色菜，视频提示文本部分不分段用一个完整自然段输出，不超过400词，用下面格式输出: 英文标题+|||+画面文本提示不分段用一个完整的段落输出 "
# initial_prompt = 'Create a Captivating 5-Second Short Video, The text prompt for the video generation should be as detailed as possible. In the center of the frame, there must be a main character who performs exaggerated or rapid movements. The surrounding environment should be natural and aesthetically pleasing. The video prompt text should be a continuous paragraph of no less than 300 words and no more than 400 words. Think outside the box with fantastical imagination. The visuals should be vibrant and creatively captivating. Your output format: (Title of video) + ||+ (Video Prompt Text) '