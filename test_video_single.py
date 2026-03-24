"""
视频生成测试 - 使用 compare_B_with_english.png
"""

import sys

sys.path.insert(0, ".")

from video_client import VideoClient


def test_single_video():
    client = VideoClient()

    test_image = "C:/Users/linjiangwen/Desktop/ai测试/compare_B_with_english.png"

    print(f"使用图片: {test_image}")

    prompt = """Traditional Chinese shadow puppet animation, Calabash Brothers style.
Keep the original 2D paper-cut silhouette style.
Joint-based movement - arms bend at elbows, legs bend at knees.
Gentle waving movement of arms, rhythmic puppet-like animation.
Pure flat design, no 3D effects, vintage muted tones.
"""

    result = client.generate_video(
        image_path=test_image, prompt=prompt, duration=8, ratio="16:9"
    )

    if result:
        print(f"\n✅ 视频生成成功: {result}")
    else:
        print("\n❌ 视频生成失败")


if __name__ == "__main__":
    test_single_video()
