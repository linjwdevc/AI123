"""
LLM调用模块 - 七牛云
用于生成分镜脚本和角色描述
"""

import requests
import json
import re
from config import QINIU_API_KEY, QINIU_BASE_URL, QINIU_MODEL_ID


class LLMClient:
    def __init__(self):
        self.api_key = QINIU_API_KEY
        self.base_url = QINIU_BASE_URL
        self.model_id = QINIU_MODEL_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def chat(self, prompt: str, system_prompt: str = None) -> str:
        """
        发送对话请求到LLM

        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）

        Returns:
            LLM的回复文本
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model_id,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return None

    def generate_storyboard(self, story: str, system_prompt: str = None) -> str:
        """
        生成分镜脚本

        Args:
            story: 故事内容
            system_prompt: 系统提示词

        Returns:
            分镜脚本JSON
        """
        from prompts import STORYBOARD_PROMPT

        prompt = STORYBOARD_PROMPT % story
        return self.chat(prompt, system_prompt)

    def parse_storyboard(self, raw_response: str) -> list:
        """
        解析LLM返回的分镜脚本，统一字段格式

        Args:
            raw_response: LLM原始返回

        Returns:
            标准化的分镜列表
        """
        if not raw_response:
            return []

        try:
            json_str = raw_response

            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]

            json_str = json_str.strip()
            data = json.loads(json_str)

            if isinstance(data, dict):
                if "分镜列表" in data:
                    data = data["分镜列表"]
                elif "分镜" in data:
                    data = data["分镜"]

            field_mapping = {
                "镜头": "镜头",
                "景别": "景别",
                "画面": "画面",
                "动作": "动作",
                "时长": "时长",
                "场景": "景别",
                "内容": "画面",
                "时间": "时长",
                "描述": "画面",
            }

            normalized = []
            for i, shot in enumerate(data):
                normalized_shot = {}

                for old_key, new_key in field_mapping.items():
                    if old_key in shot:
                        normalized_shot[new_key] = shot[old_key]

                if "镜头" not in normalized_shot:
                    normalized_shot["镜头"] = i + 1
                if "景别" not in normalized_shot:
                    normalized_shot["景别"] = "中景"
                if "画面" not in normalized_shot:
                    normalized_shot["画面"] = str(shot)
                if "动作" not in normalized_shot:
                    normalized_shot["动作"] = ""
                if "时长" not in normalized_shot:
                    normalized_shot["时长"] = 5

                normalized.append(normalized_shot)

            return normalized

        except Exception as e:
            print(f"解析分镜失败: {e}")
            return []

    def generate_character_desc(
        self, name: str, appearance: str, personality: str, system_prompt: str = None
    ) -> str:
        """
        生成角色描述

        Args:
            name: 角色名
            appearance: 外貌
            personality: 性格
            system_prompt: 系统提示词

        Returns:
            角色描述
        """
        from prompts import CHARACTER_PROMPT

        prompt = CHARACTER_PROMPT.format(
            name=name, appearance=appearance, personality=personality
        )
        return self.chat(prompt, system_prompt)


def test_llm():
    """测试LLM调用"""
    client = LLMClient()

    test_story = "葫芦娃七兄弟合力化作一座大山，将蛇精和蝎子精永远镇压在山底。从此，山下百姓过上了安居乐业的生活。"

    print("测试分镜生成...")
    raw = client.generate_storyboard(test_story)

    if raw:
        print("\n原始返回:")
        print(raw)

        print("\n解析后:")
        storyboard = client.parse_storyboard(raw)
        for shot in storyboard:
            print(f"  镜头{shot['镜头']}: {shot['景别']} - {shot['画面'][:30]}...")


if __name__ == "__main__":
    test_llm()
