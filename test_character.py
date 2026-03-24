"""
测试角色一致性功能
"""

import sys

sys.path.insert(0, ".")

from llm_client import LLMClient
from image_client import ImageClient
from prompts import SYSTEM_PROMPT, STORYBOARD_PROMPT


def test_character_consistency():
    """测试角色一致性分镜生成"""
    llm = LLMClient()
    image = ImageClient()

    # 测试故事
    test_story = """
    从前有一个勇敢的葫芦娃，他身穿红色坎肩，赤脚，光着大脑袋。
    有一天，蛇精出现了，想要抓走葫芦娃。
    葫芦娃勇敢地与蛇精战斗，最后取得了胜利。
    """

    print("=" * 50)
    print("测试角色一致性功能")
    print("=" * 50)

    # 生成分镜
    print("\nStep 1: 生成分镜脚本（包含角色定义）...")
    storyboard = llm.generate_storyboard(test_story, SYSTEM_PROMPT)
    print(f"\n分镜脚本:\n{storyboard[:1000]}...")

    # 解析JSON
    import json

    try:
        if "```json" in storyboard:
            storyboard = storyboard.split("```json")[1].split("```")[0]
        elif "```" in storyboard:
            storyboard = storyboard.split("```")[1].split("```")[0]

        data = json.loads(storyboard)

        # 提取角色信息
        character_info = data.get("角色", {})
        character_appearance = character_info.get("外观描述", "")

        print(f"\n角色外观描述: {character_appearance}")

        # 提取分镜
        scenes = data.get("分镜", [])

        if not scenes and isinstance(data, list):
            scenes = data

        print(f"\n分镜数量: {len(scenes)}")

        # 只测试第一个分镜
        if scenes:
            scene = scenes[0]
            scene_desc = scene.get("画面", "")

            # 构建包含角色外观的图片提示词
            if character_appearance:
                image_prompt = f"{character_appearance}. {scene_desc}"
            else:
                image_prompt = scene_desc

            print(f"\n图片提示词: {image_prompt[:200]}...")

            # 生成图片
            print("\nStep 2: 生成图片...")
            image_path = image.generate_shadow_puppet(image_prompt)

            if image_path:
                print(f"图片已保存: {image_path}")
            else:
                print("图片生成失败")

    except Exception as e:
        print(f"解析失败: {e}")


if __name__ == "__main__":
    test_character_consistency()
