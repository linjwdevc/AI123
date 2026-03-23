"""
视频生成模块 - Kling/Veo (通过七牛云)
用于将图片转换为视频
"""

import requests
import time
import os
import base64
import json
from config import (
    KLING_IMAGE_KEY,
    OUTPUT_DIR,
    TEST_OUTPUT_DIR,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    RETRY_DELAY,
)


class VideoClient:
    def __init__(self):
        self.api_key = KLING_IMAGE_KEY
        self.base_url = "https://api.qnaigc.com"
        self.output_dir = OUTPUT_DIR
        self.test_dir = TEST_OUTPUT_DIR

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)

    def generate_video(
        self,
        image_path: str,
        prompt: str = None,
        duration: int = 5,
        ratio: str = "16:9",
    ) -> str:
        """图生视频 - 带重试机制"""
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
                result = self._generate_video_once(image_path, prompt, duration, ratio)
                if result:
                    return result
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)
            except Exception as e:
                last_error = e
                print(f"视频生成失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        print(f"视频生成最终失败: {last_error}")
        return None

    def _generate_video_once(
        self,
        image_path: str,
        prompt: str = None,
        duration: int = 5,
        ratio: str = "16:9",
    ) -> str:
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()

        if not prompt:
            prompt = """ABSOLUTELY NO SHADOW, ZERO SHADOW, SHADOW-FREE
NO GRADIENTS, NO SHADING, FLAT COLORS ONLY
pure flat 2D animation style, NO depth perception
Chinese paper-cut silhouette, Chinese shadow puppet (PI YING XI)
all elements on same visual plane, all elements FLAT
Joint-based movement - arms bend at elbows, legs bend at knees
Gentle rhythmic puppet-like animation, stop-motion style
rich color palette with 5-8 DIVERSE HUES, MULTIPLE COLORS
vibrant diverse hues, varied color scheme, colorful composition
soft pastel tones, low saturation, muted elegant colors
watercolor-inspired colors, gentle pastel palette, no bright neon
COLORFUL SCENE - use many different colors - red blue green yellow purple orange
elegant color harmony, varied color blocks, diverse color areas
ABSOLUTELY FLAT - NO 3D EFFECTS - NO REALISTIC LIGHTING
pure paper-cut style, no shading, no shadows, no gradients"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # 转换比例格式：16:9 -> 1280x720, 9:16 -> 720x1280
        if ratio == "16:9":
            size = "1280x720"
        elif ratio == "9:16":
            size = "720x1280"
        else:
            size = "1280x720"

        # Kling API格式（七牛云正确格式）
        payload = {
            "model": "kling-video-o1",
            "prompt": prompt,
            "image_list": [{"image": image_base64}],
            "seconds": str(duration),
            "size": size,
            "mode": "std",
        }

        api_url = f"{self.base_url}/v1/videos"

        print(f"使用Kling模型生成视频...")
        print(f"API URL: {api_url}")
        print(f"Prompt: {prompt[:60]}...")
        print(f"Size: {size}, Duration: {duration}s")

        try:
            response = requests.post(
                api_url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
            )
            result = response.json()

            print(f"响应: {json.dumps(result, ensure_ascii=False)[:300]}")

            if response.status_code != 200:
                error_msg = result.get("error", {}).get("message", str(result))
                print(f"API错误: {error_msg}")
                return None

            task_id = result.get("id")
            if not task_id:
                print("未获取到任务ID")
                return None

            print(f"任务ID: {task_id}")
            video_url = self._wait_for_result(task_id, headers)
            if video_url:
                return self._download_video(video_url)

            return None

        except requests.exceptions.HTTPError as e:
            print(f"HTTP错误: {e}")
            if hasattr(e, "response") and e.response:
                print(f"响应内容: {e.response.text}")
            return None
        except Exception as e:
            print(f"视频生成失败: {e}")
            return None

    def _wait_for_result(self, task_id: str, headers: dict, max_wait: int = 600) -> str:
        """等待Kling视频任务完成"""
        status_url = f"{self.base_url}/v1/videos/{task_id}"

        print(f"查询状态: {status_url}")

        for i in range(max_wait // 10):
            try:
                response = requests.get(status_url, headers=headers, timeout=30)
                result = response.json()

                status = result.get("status")
                print(f"[{i + 1}] 状态: {status}")

                if status == "completed":
                    # Kling成功响应格式
                    videos = result.get("task_result", {}).get("videos", [])
                    if videos and len(videos) > 0:
                        video_url = videos[0].get("url")
                        if video_url:
                            print(f"视频生成成功!")
                            return video_url
                    print(f"未找到视频URL: {result}")
                    return None

                elif status == "failed":
                    error_msg = result.get("error", {}).get("message", str(result))
                    print(f"任务失败: {error_msg}")
                    return None

                elif status in [
                    "initializing",
                    "queued",
                    "in_progress",
                    "downloading",
                    "uploading",
                ]:
                    print(f"  等待中...")
                    time.sleep(10)
                else:
                    print(f"  未知状态: {status}, 等待中...")
                    time.sleep(10)

            except Exception as e:
                print(f"  查询状态失败: {e}")
                time.sleep(10)

        print("等待超时")
        return None

    def _download_video(self, url: str) -> str:
        """下载视频到本地（带认证）"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
            }
            response = requests.get(url, headers=headers, timeout=300)
            response.raise_for_status()

            filename = f"{self.output_dir}/video_{int(time.time() * 1000)}.mp4"
            test_filename = f"{self.test_dir}/video_{int(time.time() * 1000)}.mp4"

            with open(filename, "wb") as f:
                f.write(response.content)
            with open(test_filename, "wb") as f:
                f.write(response.content)

            print(f"视频已保存: {filename}")
            return filename
        except Exception as e:
            print(f"下载视频失败: {e}")
            return None


def test_video():
    """测试视频生成"""
    client = VideoClient()

    test_image = "C:/Users/linjiangwen/Desktop/ai测试/compare_B_with_english.png"

    if os.path.exists(test_image):
        result = client.generate_video(
            test_image,
            "Shadow puppet warrior arms bent at elbows, legs bent at knees, gentle joint movement, flat 2D Chinese shadow puppet animation, stop-motion style",
        )
        print(f"\n生成结果: {result}")
    else:
        print(f"测试图片不存在: {test_image}")


if __name__ == "__main__":
    test_video()
