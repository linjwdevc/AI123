"""
生图模块 - 可灵AI (通过七牛云)
用于生成皮影戏风格的图片
"""

import requests
import time
import os
import base64
import shutil
from PIL import Image, ImageEnhance, ImageFilter
from config import (
    KLING_IMAGE_KEY,
    KLING_IMAGE_URL,
    OUTPUT_DIR,
    TEST_OUTPUT_DIR,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    RETRY_DELAY,
)


def remove_shadow(image_path: str) -> Image.Image:
    """
    后处理：去除阴影，增强剪纸风格效果（方案E1微调）

    处理步骤：
    1. 提高对比度 - 使颜色更鲜明，消除阴影层次
    2. 适度提亮 - 减少暗部
    3. 锐化边缘 - 增强剪纸感
    4. 降低饱和度 - 复古色调
    """
    img = Image.open(image_path).convert("RGB")

    # 1. 提高对比度（微调+0.1）
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # 2. 适度提亮（微调-0.05）
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)

    # 3. 锐化边缘
    img = img.filter(ImageFilter.SHARPEN)
    img = img.filter(ImageFilter.EDGE_ENHANCE)

    # 4. 降低饱和度（微调-0.05）
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.85)

    return img


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
        """生成图片 - 带重试机制"""
        last_error = None

        for attempt in range(MAX_RETRIES):
            try:
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

                if attempt > 0:
                    print(f"重试 {attempt + 1}/{MAX_RETRIES}...")

                response = requests.post(
                    self.api_url, headers=headers, json=payload, timeout=REQUEST_TIMEOUT
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
                last_error = e
                print(f"图片生成失败 (尝试 {attempt + 1}/{MAX_RETRIES}): {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(RETRY_DELAY)

        print(f"图片生成最终失败: {last_error}")
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
        """生成皮影戏风格的图片 - 强化版（无阴影无渐变）"""
        # 多次重复强调关键词
        prompt = f"""paper-cut, paper-cut silhouette, paper-cut art, paper-cut style
paper-cut, paper-cut silhouette, paper-cut art, paper-cut style
ABSOLUTELY NO SHADOW, NO SHADOW, ZERO SHADOW, SHADOW-FREE
ABSOLUTELY NO SHADOW, NO SHADOW, ZERO SHADOW, SHADOW-FREE
ABSOLUTELY NO GRADIENT, NO GRADIENTS, GRADIENT-FREE, FLAT COLORS ONLY
ABSOLUTELY NO GRADIENT, NO GRADIENTS, GRADIENT-FREE, FLAT COLORS ONLY
pure flat design, pure flat design, pure flat design
pure flat, flat 2D, flat 2D figures, flat composition
NO DEPTH, NO 3D, NO SPACE, ALL ON SAME PLANE
rich color palette with 5-8 diverse hues, varied color scheme
soft pastel colors, low saturation, muted elegant tones
watercolor-inspired muted colors, gentle pastel palette
vibrant diverse hues, no bright neon, no oversaturated
Chinese paper-cut animation, Calabash Brothers animation style
Chinese paper-cut art, traditional Chinese flat art
crisp edges, clean outlines, sharp edges, solid color blocks

{subject}

MUST BE FLAT - MUST BE SHADOW-FREE - MUST BE PAPER-CUT STYLE
NO SHADOWS ALLOWED - NO GRADIENTS ALLOWED - NO DEPTH - PURE FLAT ONLY""".strip()

        # 负面提示词（回退到简洁版）
        negative_prompt = """shadow, shadows, shading, shading effects
3D, 2.5D, depth, perspective, spatial, space, dimension
lighting, light, highlight, highlights, darkness, dim, bright
soft shadow, hard shadow, drop shadow, rim light, cast shadow
realistic lighting, natural lighting, dramatic lighting
realistic, photographic, photographic quality
CGI, render, 3D render, illustration 3D, 3D effect
反射,倒影,光线,光效,高光,反光
立体,阴影,渐变,写实,3D,光影,空间,纵深"""

        # 生成图片
        raw_image_path = self.generate_image(prompt, negative_prompt)

        if raw_image_path:
            # 应用后处理去除阴影
            print("应用后处理去除阴影...")
            processed_img = remove_shadow(raw_image_path)

            # 保存处理后的图片（覆盖原图）
            processed_img.save(raw_image_path)
            print("后处理完成")

            return raw_image_path

        return None


def test_image():
    """测试图片生成"""
    client = ImageClient()

    prompt = "Chinese warrior in traditional costume, sword in hand, standing pose"
    result = client.generate_shadow_puppet(prompt)
    print(f"生成图片: {result}")


if __name__ == "__main__":
    test_image()
