import re
import json
import sys

def split_sentences(text):
    sentences = re.split(r'[.。！？\n]+', text)
    return [s.strip() for s in sentences if s.strip()]

def estimate_duration(content):
    if any(kw in content for kw in ["战斗", "打", "冲", "飞"]):
        return 3
    elif any(kw in content for kw in ["安静", "沉思", "看", "站"]):
        return 6
    elif len(content) > 30:
        return 5
    return 4

def generate_storyboard(story):
    sentences = split_sentences(story)
    storyboard = []
    
    for i, sentence in enumerate(sentences):
        if not sentence:
            continue
        shot = {
            "镜头": i + 1,
            "景别": "远景" if i == 0 else ("远景" if i == len(sentences)-1 else "中景"),
            "画面": sentence,
            "动作": "",
            "时长": estimate_duration(sentence)
        }
        storyboard.append(shot)
    
    if not storyboard:
        storyboard.append({"镜头": 1, "景别": "远景", "画面": story, "动作": "", "时长": 10})
    
    return storyboard

story = "葫芦娃七兄弟合力化作一座大山，将蛇精和蝎子精永远镇压在山底。从此，山下百姓过上了安居乐业的生活。"
sb = generate_storyboard(story)

output = []
output.append("=" * 50)
output.append(f"分镜脚本（共 {len(sb)} 个镜头）")
output.append("=" * 50)
total = sum(shot["时长"] for shot in sb)
output.append(f"总时长：约 {total} 秒")
output.append("")
for shot in sb:
    output.append(f"【镜头 {shot['镜头']}】")
    output.append(f"  景别：{shot['景别']}")
    output.append(f"  画面：{shot['画面']}")
    output.append(f"  时长：{shot['时长']}秒")
    output.append("")

with open('output/storyboard_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))
