"""
生图模块 - 可灵AI (通过七牛云)
用于生成皮影戏风格的图片
"""

import requests
import time
import os
import base64
import shutil
from config import KLING_IMAGE_KEY, KLING_IMAGE_URL, OUTPUT_DIR, TEST_OUTPUT_DIR


class ImageClient:
    def __init__(self):
        self.api_key = KLING_IMAGE_KEY
        self.api_url = KLING_IMAGE_URL
        self.base_url = KLING_IMAGE_URL.rsplit("/v1/", 1)[0]
        self.output_dir = OUTPUT_DIR
        self.test_dir = TEST_OUTPUT_DIR

        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.test_dir, exist_ok=True)

    def generate_image(
        self, prompt: str, negative_prompt: str = None, size: str = "1024*1024"
    ) -> str:
        """生成图片"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "kling-v1",
            "prompt": prompt,
            "negative_prompt": negative_prompt or "",
            "image_size": size,
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json=payload, timeout=120
            )
            response.raise_for_status()
            result = response.json()

            task_id = result.get("task_id")
            if not task_id:
                print("响应结果:", result)
                return None

            image_url = self._wait_for_result(task_id, headers)
            if image_url:
                return self._download_image(image_url)

            return None

        except Exception as e:
            print(f"图片生成失败: {e}")
            return None

    def _wait_for_result(self, task_id: str, headers: dict, max_wait: int = 120) -> str:
        """等待任务完成"""
        status_url = f"{self.base_url}/v1/images/tasks/{task_id}"

        for _ in range(max_wait // 5):
            try:
                response = requests.get(status_url, headers=headers, timeout=30)
                result = response.json()

                task_status = result.get("status")

                if task_status == "succeed":
                    return result.get("data", [{}])[0].get("url")
                elif task_status == "failed":
                    print("任务失败:", result)
                    return None

                time.sleep(5)
            except Exception as e:
                print(f"查询状态失败: {e}")
                time.sleep(5)

        return None

    def _download_image(self, url: str) -> str:
        """下载图片到本地"""
        try:
            response = requests.get(url, timeout=60)
            response.raise_for_status()

            # 生成文件名
            filename = f"{self.output_dir}/image_{int(time.time() * 1000)}.png"
            test_filename = f"{self.test_dir}/image_{int(time.time() * 1000)}.png"

            # 保存到项目目录
            with open(filename, "wb") as f:
                f.write(response.content)

            # 保存到测试目录
            with open(test_filename, "wb") as f:
                f.write(response.content)

            return filename
        except Exception as e:
            print(f"下载图片失败: {e}")
            return None

    def generate_shadow_puppet(self, subject: str, style: str = "shadow puppet") -> str:
        """生成皮影戏风格的图片 - 中国古典绘画风格"""
        prompt = f"""flat 2D Chinese shadow puppet art, Chinese classical painting composition style,
no perspective no depth no 3D, all elements on same visual plane,
Dunhuang fresco or Chinese New Year painting flat layout,
zero shading zero gradient, solid flat color fills,
smooth pure white background, paper-cut silhouette style,
vector art, minimal, equal scale figures, no spatial layering

{subject}
""".strip()

        return self.generate_image(prompt)


def test_image():
    """测试图片生成"""
    client = ImageClient()

    prompt = "Chinese warrior in traditional costume, sword in hand, standing pose"
    result = client.generate_shadow_puppet(prompt)
    print(f"生成图片: {result}")


if __name__ == "__main__":
    test_image()
