"""
视频生成模块 - Kling/Veo (通过七牛云)
用于将图片转换为视频
"""

import requests
import time
import os
import base64
import json
from config import KLING_IMAGE_KEY, OUTPUT_DIR, TEST_OUTPUT_DIR


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
        """
        图生视频 - 尝试多个API端点

        Args:
            image_path: 输入图片路径
            prompt: 视频描述
            duration: 视频时长，默认5秒
            ratio: 宽高比，默认16:9

        Returns:
            生成视频的路径
        """
        with open(image_path, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode()

        if not prompt:
            prompt = """2D flat animation, traditional Chinese shadow puppet (PI YING XI).
Keep the original 2D silhouette style.
Joint-based movement - arms bend at elbows, legs bend at knees.
Gentle movement, rhythmic puppet-like animation.
Pure paper-cut shadow puppet style, no 3D effects."""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        print(f"Prompt: {prompt[:80]}...")

        # 尝试多个端点
        endpoints = [
            # 通用视频端点（可能支持kling）
            {
                "url": f"{self.base_url}/v1/kling/video/generations",
                "payload": {
                    "model": "kling-v1",
                    "prompt": prompt,
                    "image_base64": image_base64,
                    "duration": duration,
                    "aspect_ratio": ratio,
                },
            },
            {
                "url": f"{self.base_url}/v1/videos/generations",
                "payload": {
                    "model": "kling-v1",
                    "prompt": prompt,
                    "image_base64": image_base64,
                    "duration": duration,
                    "aspect_ratio": ratio,
                },
            },
            # Veo端点（原有）
            {
                "url": f"{self.base_url}/v1/videos/generations",
                "payload": {
                    "prompt": prompt,
                    "image": {
                        "bytesBase64Encoded": image_base64,
                        "mimeType": "image/png",
                    },
                    "parameters": {
                        "generateAudio": True,
                        "durationSeconds": duration,
                        "sampleCount": 1,
                        "aspectRatio": ratio,
                    },
                    "model": "veo-3.1-generate-preview",
                },
            },
        ]

        for i, endpoint in enumerate(endpoints):
            print(f"\n尝试端点 {i + 1}/{len(endpoints)}: {endpoint['url']}")
            try:
                response = requests.post(
                    endpoint["url"],
                    headers=headers,
                    json=endpoint["payload"],
                    timeout=60,
                )
                result = response.json()

                if response.status_code == 400:
                    error_msg = result.get("error", {}).get("message", str(result))
                    print(f"  端点不支持: {error_msg[:100]}")
                    continue

                response.raise_for_status()
                print(f"  成功! 响应: {json.dumps(result, ensure_ascii=False)[:200]}")

                task_id = result.get("id") or result.get("task_id")
                if not task_id:
                    print(f"  未获取到任务ID")
                    continue

                print(f"  任务ID: {task_id}")
                video_url = self._wait_for_result(task_id, headers, endpoint["url"])
                if video_url:
                    return self._download_video(video_url)

            except requests.exceptions.HTTPError as e:
                print(f"  HTTP错误: {e}")
            except Exception as e:
                print(f"  请求失败: {e}")

        print("\n所有端点均失败")
        return None

    def _wait_for_result(
        self, task_id: str, headers: dict, base_url: str, max_wait: int = 300
    ) -> str:
        """等待任务完成"""
        status_url = f"{base_url.rsplit('/v1/', 1)[0]}/v1/videos/generations/{task_id}"

        for _ in range(max_wait // 10):
            try:
                response = requests.get(status_url, headers=headers, timeout=30)
                result = response.json()

                status = result.get("status")

                if status == "Completed" or status == "SUCCESS":
                    # 尝试多种可能的返回格式
                    if "data" in result and "videos" in result["data"]:
                        return result["data"]["videos"][0]["url"]
                    elif "video" in result:
                        return result["video"].get("url") or result["video"].get(
                            "data", {}
                        ).get("url")
                    elif "url" in result:
                        return result["url"]

                elif status == "Failed" or status == "ERROR":
                    print(f"  任务失败: {result.get('message', result)}")
                    return None

                print(f"  状态: {status}, 等待中...")
                time.sleep(10)
            except Exception as e:
                print(f"  查询状态失败: {e}")
                time.sleep(10)

        print("  等待超时")
        return None

    def _download_video(self, url: str) -> str:
        """下载视频到本地"""
        try:
            response = requests.get(url, timeout=300)
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
