# 皮影戏AI智能体 - 配置文件
# 优先从环境变量读取API密钥，用于Streamlit Cloud部署
# 本地运行时，如果存在config_local.py，会自动加载本地密钥

import os
import sys

# 检查是否存在本地配置文件
_local_config_exists = os.path.exists("config_local.py")


def get_api_key(env_name: str, default: str = "") -> str:
    """从环境变量获取API密钥"""
    return os.environ.get(env_name, default)


# 七牛云 - LLM API配置
QINIU_API_KEY = get_api_key("QINIU_API_KEY", "")
QINIU_BASE_URL = "https://api.qnaigc.com/v1"
QINIU_MODEL_ID = "moonshotai/kimi-k2.5"

# 可灵AI - 生图API配置 (七牛云平台)
KLING_IMAGE_KEY = get_api_key("KLING_IMAGE_KEY", "")
KLING_IMAGE_URL = "https://api.qnaigc.com/v1/images/generations"

# 可灵AI - 生视频API配置 (七牛云平台)
KLING_VIDEO_KEY = get_api_key("KLING_VIDEO_KEY", "")
KLING_VIDEO_URL = "https://api.qnaigc.com/v1/videos/generations"

# 即梦AI - 图生视频API配置 (备用)
JIMENG_API_KEY = get_api_key("JIMENG_API_KEY", "")
JIMENG_MODEL = "cogvideox"

# 通义万相 - 生图API配置 (备用)
TONGYI_API_KEY = get_api_key("TONGYI_API_KEY", "")
TONGYI_IMAGE_MODEL = "wanx2.1"

# 项目配置
OUTPUT_DIR = "output"
TEST_OUTPUT_DIR = "output"

# API重试和超时配置
MAX_RETRIES = 3  # 最大重试次数
REQUEST_TIMEOUT = 180  # 请求超时时间（秒）
POLLING_TIMEOUT = 600  # 轮询等待超时（秒）
RETRY_DELAY = 3  # 重试间隔（秒）

# 如果本地配置文件存在，加载它（会覆盖上面的环境变量读取）
if _local_config_exists:
    try:
        from config_local import (
            QINIU_API_KEY as _local_qiniu,
            KLING_IMAGE_KEY as _local_kling_img,
            KLING_VIDEO_KEY as _local_kling_vid,
            JIMENG_API_KEY as _local_jimeng,
            TONGYI_API_KEY as _local_tongyi,
        )

        # 使用本地配置（如果有值的话）
        if _local_qiniu:
            QINIU_API_KEY = _local_qiniu
        if _local_kling_img:
            KLING_IMAGE_KEY = _local_kling_img
        if _local_kling_vid:
            KLING_VIDEO_KEY = _local_kling_vid
        if _local_jimeng:
            JIMENG_API_KEY = _local_jimeng
        if _local_tongyi:
            TONGYI_API_KEY = _local_tongyi
    except Exception as e:
        print(f"加载本地配置失败: {e}")
