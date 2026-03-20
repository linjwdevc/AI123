# 皮影戏AI智能体 - 配置文件

# ==================== API配置 ====================
# 注意：请填入你自己的API密钥

# 七牛云 - LLM API配置
QINIU_API_KEY = "YOUR_QINIU_API_KEY"  # 替换为你的七牛云API Key
QINIU_BASE_URL = "https://api.qnaigc.com/v1"
QINIU_MODEL_ID = "moonshotai/kimi-k2.5"

# 可灵AI - 生图API配置 (七牛云平台)
KLING_IMAGE_KEY = "YOUR_KLING_IMAGE_KEY"  # 替换为你的可灵AI API Key
KLING_IMAGE_URL = "https://api.qnaigc.com/v1/images/generations"

# 可灵AI - 生视频API配置 (七牛云平台)
KLING_VIDEO_KEY = "YOUR_KLING_VIDEO_KEY"  # 替换为你的Veo API Key
KLING_VIDEO_URL = "https://api.qnaigc.com/v1/videos/generations"

# 即梦AI - 图生视频API配置 (备用)
JIMENG_API_KEY = "YOUR_JIMENG_API_KEY"  # 替换为你的即梦AI API Key
JIMENG_MODEL = "cogvideox"

# 通义万相 - 生图API配置 (备用)
TONGYI_API_KEY = "YOUR_TONGYI_API_KEY"  # 替换为你的通义万相API Key
TONGYI_IMAGE_MODEL = "wanx2.1"

# ==================== 项目配置 ====================
OUTPUT_DIR = "output"
TEST_OUTPUT_DIR = "output"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 120
