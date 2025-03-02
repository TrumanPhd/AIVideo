import requests
from urllib.parse import urlencode
import webbrowser  # 用于打开浏览器
import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

# 替换为你自己的值
TIKTOK_APP_ID = ""  # 你的应用 ID
TIKTOK_APP_SECRET = "YOUR_TIKTOK_APP_SECRET"  # 你的应用密钥
REDIRECT_URI = "http://localhost:8080"  # 你的重定向 URI (请与你在应用中配置的 URI 匹配)
SCOPE = "video.publish"  # 申请的权限，发布视频

# 1. 构建授权 URL
authorization_url = "https://open.tiktokapis.com/v2/oauth/authorize?" + urlencode({
    "client_key": TIKTOK_APP_ID,
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "response_type": "code",
    # "state": "YOUR_STATE_STRING"  # 添加一个 CSRF state (可选)
})

print(f"请在浏览器中打开此 URL 进行授权: \n{authorization_url}")
webbrowser.open(authorization_url)  # 自动打开浏览器

# 2. 启动一个简单的 HTTP 服务器来接收授权码
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        if parsed_url.path == "/":  # 匹配重定向的 URI
            query_params = parse_qs(parsed_url.query)
            if "code" in query_params:
                auth_code = query_params["code"][0]
                print(f"获取到授权码: {auth_code}")
                global authorization_code # 定义全局变量
                authorization_code = auth_code
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("授权成功！你可以关闭此页面。") # 提示授权成功
                server.shutdown() # 关闭服务器
            else:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("未获取到授权码。请检查授权流程。")
        else:
            super().do_GET()  # 处理其他请求

PORT = 8080  # 请确保端口号与重定向 URI 匹配
Handler = MyHandler
with socketserver.TCPServer(("", PORT), Handler) as server:
    # 循环接收请求
    print(f"正在启动一个简单的 HTTP 服务器，监听端口 {PORT} ...")
    server.handle_request() # 只处理一次请求，获取授权码。

# 3. 使用授权码获取访问令牌
if authorization_code:
    token_url = "https://open.tiktokapis.com/v2/oauth/token/"  # 令牌端点 (token endpoint)
    token_data = {
        "client_key": TIKTOK_APP_ID,
        "client_secret": TIKTOK_APP_SECRET,
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI
    }
    token_response = requests.post(token_url, data=token_data)

    if token_response.status_code == 200:
        token_json = token_response.json()
        print(f"获取访问令牌成功: {json.dumps(token_json, indent=4)}")
        access_token = token_json["access_token"]
        refresh_token = token_json["refresh_token"]  # 获取刷新令牌
        # 将 access_token 和 refresh_token 保存到安全的地方 (例如，配置文件、数据库)
        print(f"你的 access_token 是: {access_token}") # 打印 access_token，请妥善保管
        # 使用 access_token，完成上传视频的流程
    else:
        print(f"获取访问令牌失败: {token_response.status_code}, {token_response.text}")
else:
    print("未获取到授权码，无法获取访问令牌。")