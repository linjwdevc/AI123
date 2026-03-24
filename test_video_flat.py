"""
视频生成测试 - 强化无阴影提示词版本
"""

import sys

sys.path.insert(0, ".")

from video_client import VideoClient
import os


def test_flat_video():
    client = VideoClient()

    # 使用A9中国古典风格图片
    test_image = (
        "C:/Users/linjiangwen/shadow-play-agent/output/kling_A9_chinese_classic.png"
    )

    print(f"使用图片: {test_image}")

    # 强化无阴影、无渐变的视频提示词 + 丰富色彩
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

    print(f"提示词已强化：纯平 + 丰富色彩")

    # 生成5秒视频节省时间
    result = client.generate_video(
        image_path=test_image, prompt=prompt, duration=5, ratio="16:9"
    )

    if result:
        print(f"\n生成成功: {result}")
        # 复制到桌面
        desktop_path = "C:/Users/linjiangwen/Desktop/ai测试/kling_flat_test.mp4"
        os.system(f'copy "{result}" "{desktop_path}"')
        print(f"已复制到桌面: {desktop_path}")
        return result
    else:
        print("\n生成失败")
        return None


if __name__ == "__main__":
    test_flat_video()
