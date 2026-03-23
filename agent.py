"""
皮影戏AI智能体 - 主程序
串联LLM、生图、视频生成模块
支持并行生成优化
"""

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from llm_client import LLMClient
from image_client import ImageClient
from video_client import VideoClient
from video_utils import merge_videos, check_ffmpeg
from prompts import SYSTEM_PROMPT
from config import OUTPUT_DIR


class ShadowPlayAgent:
    def __init__(self):
        """初始化智能体"""
        self.llm = LLMClient()
        self.image = ImageClient()
        self.video = VideoClient()

        # 创建输出目录
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def run(self, story: str, max_workers: int = 4) -> dict:
        """
        运行完整工作流（并行优化版本）

        Args:
            story: 用户输入的故事
            max_workers: 并行处理数量，默认4

        Returns:
            包含所有生成素材的字典
        """
        start_time = time.time()
        result = {"story": story, "storyboard": None, "images": [], "videos": []}

        print("=" * 50)
        print("葫芦娃皮影戏AI智能体")
        print("=" * 50)

        # Step 1: 生成分镜脚本
        print("\n[Step 1] 生成分镜脚本...")
        storyboard = self.llm.generate_storyboard(story, SYSTEM_PROMPT)
        result["storyboard"] = storyboard
        print(f"分镜脚本生成完成")

        # 解析分镜
        try:
            if "```json" in storyboard:
                storyboard = storyboard.split("```json")[1].split("```")[0]
            elif "```" in storyboard:
                storyboard = storyboard.split("```")[1].split("```")[0]

            storyboard_data = json.loads(storyboard)

            # 解析角色信息
            character_info = storyboard_data.get("角色", {})
            character_name = character_info.get("名字", "角色")
            character_appearance = character_info.get("外观描述", "")

            print(f"\n角色信息:")
            print(f"  名字: {character_name}")
            print(
                f"  外观: {character_appearance[:80]}..."
                if character_appearance
                else "  外观: 未提供"
            )

            # 解析分镜列表
            scenes = storyboard_data.get("分镜", [])
            if not scenes and isinstance(storyboard_data, list):
                scenes = storyboard_data

            print(f"\n解析到 {len(scenes)} 个分镜")

        except Exception as e:
            print(f"JSON解析失败: {e}")
            scenes = [{"画面": storyboard, "景别": "中景"}]
            character_appearance = ""

        total_scenes = len(scenes)

        # Step 2: 并行生成图片
        print(f"\n{'=' * 50}")
        print(f"[Step 2] 并行生成图片 ({max_workers}个线程)...")

        def generate_single_image(scene, index):
            """为单个分镜生成图片"""
            scene_desc = scene.get("画面", "") or scene.get("description", "")

            if character_appearance:
                image_prompt = f"""{character_appearance}. {scene_desc}
no shadow, no gradients, pure flat design
paper-cut style, flat 2D design
solid color fills, bold black outlines
all elements on same visual plane"""
            else:
                image_prompt = f"""{scene_desc}
no shadow, no gradients, pure flat design
paper-cut style, flat 2D design
solid color fills, bold black outlines
all elements on same visual plane"""

            try:
                image_path = self.image.generate_shadow_puppet(image_prompt)
                return {
                    "scene": index + 1,
                    "description": scene_desc,
                    "path": image_path,
                    "status": "success" if image_path else "failed",
                    "error": None if image_path else "生成失败",
                }
            except Exception as e:
                return {
                    "scene": index + 1,
                    "description": scene_desc,
                    "path": None,
                    "status": "failed",
                    "error": str(e),
                }

        # 并行提交任务
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for i, scene in enumerate(scenes):
                future = executor.submit(generate_single_image, scene, i)
                futures[future] = i + 1

            # 收集结果
            for future in as_completed(futures):
                scene_num = futures[future]
                try:
                    img_result = future.result()
                    if img_result["status"] == "success":
                        result["images"].append(img_result)
                        pct = int(len(result["images"]) / total_scenes * 50)
                        print(f"  [OK] [{pct:3d}%] 分镜{scene_num} 图片生成成功")
                    else:
                        print(
                            f"  [FAIL] 分镜{scene_num} 图片失败: {img_result.get('error', '')}"
                        )
                except Exception as e:
                    print(f"  [ERROR] 分镜{scene_num} 异常: {e}")

        image_time = time.time() - start_time
        success_images = len(result["images"])
        print(
            f"\n  图片生成完成: {success_images}/{total_scenes} 成功 (耗时: {int(image_time)}秒)"
        )

        # Step 3: 并行生成视频
        print(f"\n{'=' * 50}")
        print(f"[Step 3] 并行生成视频 ({max_workers}个线程)...")

        def generate_single_video(img_result):
            """为单张图片生成视频"""
            scene_num = img_result["scene"]
            scene_desc = img_result["description"]
            image_path = img_result["path"]

            video_prompt = f"""{scene_desc}

no shadow, no gradients, pure flat 2D animation
paper-cut style, Chinese shadow puppet (PI YING XI)
all elements on same visual plane
Joint-based movement - arms bend at elbows, legs bend at knees
Gentle rhythmic puppet-like animation, stop-motion style
soft pastel colors, low saturation, elegant color harmony"""

            try:
                video_path = self.video.generate_video(image_path, video_prompt)
                return {
                    "scene": scene_num,
                    "path": video_path,
                    "status": "success" if video_path else "failed",
                    "error": None if video_path else "生成失败",
                }
            except Exception as e:
                return {
                    "scene": scene_num,
                    "path": None,
                    "status": "failed",
                    "error": str(e),
                }

        # 并行提交视频生成任务
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}
            for img_result in result["images"]:
                future = executor.submit(generate_single_video, img_result)
                futures[future] = img_result["scene"]

            # 收集结果
            for future in as_completed(futures):
                scene_num = futures[future]
                try:
                    video_result = future.result()
                    if video_result["status"] == "success":
                        result["videos"].append(video_result)
                        pct = 50 + int(len(result["videos"]) / success_images * 50)
                        print(f"  [OK] [{pct:3d}%] 分镜{scene_num} 视频生成成功")
                    else:
                        print(
                            f"  [FAIL] 分镜{scene_num} 视频失败: {video_result.get('error', '')}"
                        )
                except Exception as e:
                    print(f"  [ERROR] 分镜{scene_num} 异常: {e}")

        total_time = time.time() - start_time
        success_videos = len(result["videos"])

        # 计算预计总时间
        if success_videos == success_images:
            # 如果全部成功，计算10个分镜的预估时间
            estimated_total = (
                int(total_time / success_videos * total_scenes)
                if success_videos > 0
                else 0
            )
            time_str = f"预估总耗时: {estimated_total // 60}分{estimated_total % 60}秒"
        else:
            time_str = (
                f"部分失败，实际耗时: {int(total_time // 60)}分{total_time % 60:.0f}秒"
            )

        print(f"\n{'=' * 50}")
        print(f"全流程完成! {time_str}")
        print(f"  图片: {success_images}/{total_scenes} 成功")
        print(f"  视频: {success_videos}/{success_images} 成功")

        # 合并视频
        if success_videos > 0:
            # 按分镜顺序排序视频
            sorted_videos = sorted(result["videos"], key=lambda x: x["scene"])
            video_paths = [v["path"] for v in sorted_videos if v.get("path")]

            if video_paths and check_ffmpeg():
                output_dir = (
                    os.path.dirname(video_paths[0]) if video_paths else OUTPUT_DIR
                )
                merged_path = os.path.join(output_dir, f"final_{int(time.time())}.mp4")

                print(f"\n{'=' * 50}")
                print(f"正在合并 {len(video_paths)} 个视频...")

                merged_result = merge_videos(video_paths, merged_path)

                if merged_result:
                    result["merged_video"] = merged_result
                    print(f"  合并成功: {merged_result}")
                else:
                    print(f"  合并失败，保留独立视频文件")
            elif not check_ffmpeg():
                print(f"\n警告: 未检测到FFmpeg，无法合并视频")

        print(f"{'=' * 50}")

        return result

    def generate_single(self, prompt: str, generate_video: bool = True) -> dict:
        """
        生成单个场景

        Args:
            prompt: 场景描述
            generate_video: 是否生成视频

        Returns:
            生成结果
        """
        result = {}

        # 生成图片
        print("生成图片...")
        image_path = self.image.generate_shadow_puppet(prompt)

        if image_path:
            result["image"] = image_path

            # 生成视频
            if generate_video:
                print("生成视频...")
                video_path = self.video.generate_video(
                    image_path,
                    "Traditional Chinese shadow puppet animation, gentle movement",
                )
                result["video"] = video_path

        return result


def test_agent():
    """测试智能体"""
    from prompts import TEST_STORY

    agent = ShadowPlayAgent()
    result = agent.run(TEST_STORY)

    print("\n" + "=" * 50)
    print("测试完成！")
    print(f"生成了 {len(result['images'])} 张图片")
    print(f"生成了 {len(result['videos'])} 个视频")


if __name__ == "__main__":
    test_agent()
