"""
测试10个分镜 - 完整工作流验证
"""

import sys

sys.path.insert(0, ".")

from agent import ShadowPlayAgent


def test_10_scenes():
    """测试10个分镜的完整并行生成"""
    agent = ShadowPlayAgent()

    print("\n" + "=" * 50)
    print("完整模式: 生成10个分镜")
    print("=" * 50)

    test_story = """
    葫芦娃七兄弟合力化作一座大山，将蛇精和蝎子精永远镇压在山底。
    从此，山下百姓过上了安居乐业的生活。
    """

    print(f"\n故事内容: {test_story[:100]}...")
    print(f"\n使用并行3个线程测试...")

    result = agent.run(test_story, max_workers=3)

    print("\n" + "=" * 50)
    print("测试完成!")
    print(f"生成了 {len(result['images'])} 张图片")
    print(f"生成了 {len(result['videos'])} 个视频")

    print("\n所有图片:")
    for i, img in enumerate(result["images"]):
        print(f"  {i + 1}. {img['path']}")

    print("\n所有视频:")
    for i, vid in enumerate(result["videos"]):
        print(f"  {i + 1}. {vid['path']}")

    if result.get("merged_video"):
        print(f"\n合并后的完整视频:")
        print(f"  {result['merged_video']}")


if __name__ == "__main__":
    test_10_scenes()
