"""
皮影戏AI智能体 - 主程序
串联LLM、生图、视频生成模块
"""

import json
import os
from llm_client import LLMClient
from image_client import ImageClient
from video_client import VideoClient
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
    
    def run(self, story: str) -> dict:
        """
        运行完整工作流
        
        Args:
            story: 用户输入的故事
        
        Returns:
            包含所有生成素材的字典
        """
        result = {
            "story": story,
            "storyboard": None,
            "images": [],
            "videos": []
        }
        
        # Step 1: 生成分镜脚本
        print("=" * 50)
        print("Step 1: 生成分镜脚本...")
        storyboard = self.llm.generate_storyboard(story, SYSTEM_PROMPT)
        result["storyboard"] = storyboard
        print(f"分镜脚本生成完成")
        print(storyboard[:200] + "..." if len(storyboard) > 200 else storyboard)
        
        # 解析分镜
        try:
            # 尝试解析JSON
            if "```json" in storyboard:
                storyboard = storyboard.split("```json")[1].split("```")[0]
            elif "```" in storyboard:
                storyboard = storyboard.split("```")[1].split("```")[0]
            
            scenes = json.loads(storyboard)
        except:
            # 如果解析失败，手动分割
            scenes = [{"description": storyboard, "action": "default action"}]
        
        # Step 2: 为每个分镜生成图片和视频
        print("\n" + "=" * 50)
        print("Step 2: 生成图片和视频...")
        
        for i, scene in enumerate(scenes):
            print(f"\n--- 分镜 {i+1}/{len(scenes)} ---")
            
            # 生成图片
            description = scene.get("description", "")
            action = scene.get("action", "gentle movement")
            
            print(f"生成图片: {description[:50]}...")
            image_prompt = f"Traditional Chinese shadow puppet art style. {description}"
            image_path = self.image.generate_shadow_puppet(image_prompt)
            
            if image_path:
                result["images"].append({
                    "scene": i + 1,
                    "description": description,
                    "path": image_path
                })
                print(f"图片保存: {image_path}")
                
                # 生成视频
                print(f"生成视频...")
                video_prompt = f"{action}, traditional Chinese shadow puppet animation"
                video_path = self.video.generate_video(image_path, video_prompt)
                
                if video_path:
                    result["videos"].append({
                        "scene": i + 1,
                        "path": video_path
                    })
                    print(f"视频保存: {video_path}")
            else:
                print(f"图片生成失败，跳过该分镜")
        
        print("\n" + "=" * 50)
        print("完成！")
        print(f"生成了 {len(result['images'])} 张图片")
        print(f"生成了 {len(result['videos'])} 个视频")
        
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
                    "Traditional Chinese shadow puppet animation, gentle movement"
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
