"""
分镜生成模块 v2
增强战斗场景处理
"""

import re


def split_sentences(text: str) -> list:
    """将故事文本拆分成句子"""
    sentences = re.split(r'[。！？\n]+', text)
    return [s.strip() for s in sentences if s.strip()]


def expand_combat_sentence(sentence: str) -> list:
    """
    展开战斗场景句子为多个分镜
    
    Args:
        sentence: 包含战斗内容的句子
    
    Returns:
        展开后的分镜列表
    """
    parts = re.split(r'[，,、]', sentence)
    parts = [p.strip() for p in parts if p.strip()]
    
    if len(parts) <= 1:
        return [sentence]
    
    shots = []
    for i, part in enumerate(parts):
        if any(kw in part for kw in ["战斗", "打", "斗", "冲", "攻"]):
            shots.append({"画面": part, "景别": "特写", "时长": 2})
        elif any(kw in part for kw in ["闪", "光", "爆发", "变身"]):
            shots.append({"画面": part, "景别": "特写", "时长": 2})
        elif i == 0:
            shots.append({"画面": part, "景别": "中景", "时长": 3})
        elif i == len(parts) - 1:
            shots.append({"画面": part, "景别": "中景", "时长": 3})
        else:
            shots.append({"画面": part, "景别": "近景", "时长": 2})
    
    return shots


def estimate_duration(画面: str, 景别: str) -> int:
    """根据内容和景别估计时长"""
    combat_keywords = ["战斗", "打", "斗", "冲", "攻", "飞", "闪", "爆发"]
    calm_keywords = ["安静", "沉思", "看", "站", "安居", "欢笑"]
    
    if 景别 == "特写":
        return 2
    elif any(kw in 画面 for kw in combat_keywords):
        return 3
    elif any(kw in 画面 for kw in calm_keywords):
        return 6
    elif len(画面) > 40:
        return 5
    return 4


def generate_storyboard(story: str) -> list:
    """
    生成分镜脚本
    
    Args:
        story: 故事文本
    
    Returns:
        分镜列表
    """
    sentences = split_sentences(story)
    raw_shots = []
    
    for sentence in sentences:
        if not sentence:
            continue
        
        combat_keywords = ["战斗", "打", "斗", "冲", "攻", "挣扎", "爆发"]
        if any(kw in sentence for kw in combat_keywords):
            expanded = expand_combat_sentence(sentence)
            raw_shots.extend(expanded)
        else:
            raw_shots.append({"画面": sentence})
    
    if not raw_shots:
        raw_shots = [{"画面": story}]
    
    storyboard = []
    total = len(raw_shots)
    
    for i, shot in enumerate(raw_shots):
        shot_num = i + 1
        画面 = shot.get("画面", "")
        
        if shot_num == 1:
            景别 = "远景"
        elif shot_num == total:
            景别 = "远景"
        elif shot.get("景别"):
            景别 = shot.get("景别")
        elif any(kw in 画面 for kw in ["闪", "光", "爆发", "变身"]):
            景别 = "特写"
        elif shot_num % 2 == 0:
            景别 = "中景"
        else:
            景别 = "近景"
        
        时长 = estimate_duration(画面, 景别)
        
        storyboard.append({
            "镜头": shot_num,
            "景别": 景别,
            "画面": 画面,
            "动作": "",
            "时长": 时长
        })
    
    return storyboard


def format_storyboard(storyboard: list) -> str:
    """格式化分镜为文本"""
    lines = []
    lines.append("=" * 50)
    lines.append(f"分镜脚本（共 {len(storyboard)} 个镜头）")
    lines.append("=" * 50)
    
    total_duration = sum(shot["时长"] for shot in storyboard)
    lines.append(f"总时长：约 {total_duration} 秒")
    lines.append("")
    
    for shot in storyboard:
        lines.append(f"【镜头 {shot['镜头']}】 {shot['景别']} | {shot['画面']} | {shot['时长']}秒")
    
    return "\n".join(lines)


if __name__ == "__main__":
    story = """蛇精带领蝎子怪冲出妖洞，与葫芦娃七兄弟展开激烈战斗。
七兄弟使出浑身解数，一道金光闪过，他们化作一座巍峨大山。
大山压下，蛇精和蝎子怪被永远封印在山底。
从此，七色山脚下百姓安居乐业，孩子们在田间欢笑嬉戏。
年迈的樵夫望着大山，感叹葫芦娃的英勇牺牲。
山风吹过，仿佛传来葫芦娃爽朗的笑声。"""
    
    sb = generate_storyboard(story)
    print(format_storyboard(sb))
