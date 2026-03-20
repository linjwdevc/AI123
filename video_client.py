"""
视频生成模块 - Veo (通过七牛云)
用于将图片转换为视频
"""

import requests
import time
import os
import base64
import random
from config import KLING_VIDEO_KEY, KLING_VIDEO_URL, OUTPUT_DIR, TEST_OUTPUT_DIR


class VideoClient:
    def __init__(self):
        self.api_key = KLING_VIDEO_KEY
        self.api_url = KLING_VIDEO_URL
        self.base_url = KLING_VIDEO_URL.rsplit("/v1/", 1)[0]
        self.output_dir = OUTPUT_DIR
        self.test_dir = TEST_OUTPUT_DIR

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)

    def generate_video(
        self,
        image_path: str,
        prompt: str = None,
        duration: int = 8,
        ratio: str = "16:9",
    ) -> str:
        """
        图生视频

        Args:
            image_path: 输入图片路径
            prompt: 视频描述
            duration: 视频时长，默认8秒
            ratio: 宽高比，默认16:9

        Returns:
            生成视频的路径
        """
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()

        if not prompt:
            prompt = """2D flat animation, traditional Chinese shadow puppet (PI YING XI).
Keep the original 2D silhouette style.
Gentle movement of arms and body.
NO 3D effect, NO realistic rendering.
Pure paper-cut shadow puppet on white screen."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        # 根据七牛云Veo API格式构建请求
        payload = {
            "instances": [
                {
                    "prompt": prompt,
                    "image": {
                        "bytesBase64Encoded": image_base64,
                        "mimeType": "image/png",
                    },
                }
            ],
            "parameters": {
                "generateAudio": True,
                "durationSeconds": duration,
                "sampleCount": 1,
                "aspectRatio": ratio,
                "seed": random.randint(0, 4294967295),
                "negativePrompt": "blurry, low quality, distorted",
                "personGeneration": "allow_adult",
            },
            "model": "veo-3.1-generate-preview",
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json=payload, timeout=60
            )
            response.raise_for_status()
            result = response.json()

            task_id = result.get("id")
            if not task_id:
                print("响应结果:", result)
                return None

            print(f"任务ID: {task_id}")
            video_url = self._wait_for_result(task_id, headers)
            if video_url:
                return self._download_video(video_url)

            return None

        except Exception as e:
            print(f"视频生成失败: {e}")
            return None

    def _wait_for_result(self, task_id: str, headers: dict, max_wait: int = 300) -> str:
        """等待任务完成"""
        status_url = f"{self.base_url}/v1/videos/generations/{task_id}"

        for _ in range(max_wait // 10):
            try:
                response = requests.get(status_url, headers=headers, timeout=30)
                result = response.json()

                status = result.get("status")

                if status == "Completed":
                    return result["data"]["videos"][0]["url"]
                elif status == "Failed":
                    print("任务失败:", result.get("message"))
                    return None

                print(f"状态: {status}, 等待中...")
                time.sleep(10)
            except Exception as e:
                print(f"查询状态失败: {e}")
                time.sleep(10)

        return None

    def _download_video(self, url: str) -> str:
        """下载视频到本地"""
        try:
            response = requests.get(url, timeout=300)
            response.raise_for_status()

            # 生成文件名
            filename = f"{self.output_dir}/video_{int(time.time() * 1000)}.mp4"
            test_filename = f"{self.test_dir}/video_{int(time.time() * 1000)}.mp4"

            # 保存到项目目录
            with open(filename, "wb") as f:
                f.write(response.content)

            # 保存到测试目录
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

    test_image = "output/image_1773927549475.png"

    if os.path.exists(test_image):
        result = client.generate_video(
            test_image, "Shadow puppet warrior walking forward, gentle movement"
        )
        print(f"生成视频: {result}")
    else:
        print("测试图片不存在")


if __name__ == "__main__":
    test_video()
