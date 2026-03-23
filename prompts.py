# 皮影戏AI智能体 - 提示词模板

# ==================== 动作风格描述（核心要求）====================
ACTION_STYLE = """
【动作风格要求 - 核心】
肢体只能在关节处弯曲和延展，类似皮影戏/木偶的操控方式：
- 手臂只能在肘部弯曲，可伸展或弯曲成角度
- 腿部只能在膝盖弯曲，可站立或弯曲
- 手腕可左右转动
- 头部可左右转动
- 动作具有顿挫感，一帧一帧的关节运动
- 四肢延展而非变形，保持肢体形状只改变角度
- 动作僵硬有节奏感，类似葫芦娃动画的动作风格
"""

# ==================== 系统提示词 ====================
SYSTEM_PROMPT = """你是一个专业的中国传统皮影戏编剧，擅长模仿上海美术电影制片厂《葫芦小金刚》的分镜风格。

核心风格要求：
1. 平面构图 - 所有元素在同一视觉平面，无空间纵深，无前后层次
2. 二维剪纸风格 - 类似敦煌壁画、年画的散点透视
3. 零阴影 - 无阴影无渐变，零三维效果
4. 复古色彩 - 柔和色调，剪纸动画质感

【动作风格 - 核心要求】
肢体只能在关节处弯曲和延展，类似皮影戏/木偶的操控方式：
- 手臂只能在肘部弯曲，可伸展或弯曲成角度
- 腿部只能在膝盖弯曲，可站立或弯曲
- 手腕可左右转动，头部可左右转动
- 动作顿挫感，一帧一帧的关节运动
- 四肢延展而非变形，保持形状只改变角度
- 动作僵硬有节奏感，类似葫芦娃动画

分镜要求：
- 生成分镜10个镜头，总时长50秒
- 每个镜头约5秒
- 中景为主，避免过多远景/特写
- 保持角色一致性
- 动作描述要体现关节弯曲特点

输出格式：JSON数组"""

# ==================== 分镜生成提示词 ====================
STORYBOARD_PROMPT = """请严格按照以下JSON格式生成分镜10个，只输出JSON：

{
  "角色": {
    "名字": "角色名称",
    "外观描述": "详细的角色外观描述，用于生成一致的角色形象（包含服装、发型、肤色、体型特征等），必须使用英文描述"
  },
  "分镜": [
    {"镜头": 1, "景别": "中景", "画面": "paper-cut silhouette场景描述，包含角色外观（与角色定义一致），关节动作描述，pure flat design"},
    {"镜头": 2, "景别": "中景", "画面": "paper-cut art画面，角色外观（与角色定义一致），flat 2D角色动作，手臂腿部关节弯曲描述, no shadow, vintage muted tones"},
    ...
    {"镜头": 10, "景别": "中景", "画面": "paper-cut style场景结尾，角色外观（与角色定义一致），pure flat composition, soft muted colors"}
  ]
}

【角色外观要求 - 非常重要】
- 必须详细描述角色外观，包含：发型、头饰、服装颜色、鞋子，配饰、体型特征等
- 外观描述必须使用英文，用于AI生图
- 外观描述必须包含以下平面风格关键词：
  - flat 2D design（纯平设计）
  - paper-cut animation style（剪纸动画风格）
  - no shading, no 3D effects（无阴影无3D效果）
  - solid color fills（纯色填充）
  - bold black outlines（粗黑轮廓线）
  - Chinese shadow puppet art（中国皮影艺术风格）
- 所有分镜中的角色外观必须与角色定义完全一致

【动作风格要求 - 核心】
- 肢体只能在关节处弯曲：手臂肘部、腿部膝盖
- 动作顿挫感，一帧一帧的关节运动
- 四肢延展而非变形
- 示例："他的手臂在肘部弯曲成90度" "他的腿部在膝盖处弯曲站立"

【画面描述风格要求 - 重要】
画面描述必须同时包含：
1. 动作描述（关节弯曲、肢体运动等）
2. 英文风格引导词（在描述中加入以下关键词）：
   - paper-cut silhouette（剪纸剪影）
   - paper-cut style / paper-cut art（剪纸风格）
   - pure flat design / flat 2D（纯平设计）
   - no shadow / shadow-free（无阴影）
   - vintage muted tones / retro palette（复古色调）
   - flat composition（平面构图）

要求：
- 生成分镜10个，总时长约50秒
- 画面描述要突出角色的关节弯曲动作
- 画面描述必须包含英文风格引导词（paper-cut, flat, no shadow, vintage等）
- 画面描述必须引用角色外观，确保角色一致性
- 所有元素在同一视觉平面，无空间纵深
- 色彩柔和复古风格

故事内容：
%s

只输出JSON："""

# ==================== 角色生成提示词 ====================
CHARACTER_PROMPT = """请为以下角色生成皮影戏风格的描述。

角色信息：
- 名字：{name}
- 外貌：{appearance}
- 性格：{personality}

【动作风格要求 - 核心】
肢体只能在关节处弯曲和延展，类似皮影戏/木偶的操控方式：
- 手臂只能在肘部弯曲，可伸展或弯曲成角度
- 腿部只能在膝盖弯曲，可站立或弯曲
- 手腕可左右转动，头部可左右转动
- 动作顿挫感，一帧一帧的关节运动
- 四肢延展而非变形

要求：
1. 描述应为英文（用于AI生图）
2. 风格：中国传统皮影戏/剪纸动画
3. 包含细节：服装、头饰、动作姿态
4. 保持平面构图，无阴影无渐变
5. 动作描述要体现关节弯曲特点

输出格式：简洁的英文描述（用于AI生图）"""

# ==================== 场景生成提示词 ====================
SCENE_PROMPT = """请为以下场景生成皮影戏风格的描述。

场景：{scene}

【动作风格要求 - 核心】
肢体只能在关节处弯曲和延展，类似皮影戏/木偶的操控方式

要求：
1. 描述应为英文（用于AI生图）
2. 风格：中国传统皮影戏/剪纸动画
3. 包含：背景建筑、道具，简约古朴
4. 平面构图，无阴影无渐变
5. 色彩柔和复古风格

输出格式：简洁的英文描述（用于AI生图）"""

# ==================== 可灵AI生图提示词模板 (A9 - 中国古典绘画风格) ====================
IMAGE_PROMPT_TEMPLATE = """flat 2D Chinese shadow puppet art, Chinese classical painting composition style,
ABSOLUTELY NO SHADOWS, ABSOLUTELY NO GRADIENTS, ABSOLUTELY NO DEPTH PERCEPTION,
all elements on same visual plane, pure 2D flat design,
Dunhuang fresco or Chinese New Year painting flat layout,
solid flat color fills with crisp edges, NO shading effects whatsoever,
smooth pure white background, paper-cut silhouette style,
vector art, minimal, equal scale figures, no spatial layering, no 3D effects

rich color palette with 5-8 diverse hues, varied color scheme,
soft pastel colors, low saturation, muted elegant tones,
watercolor-inspired muted colors, gentle pastel palette,
no bright neon, no oversaturated, elegant color harmony

{subject_description}

【动作风格要求】
Joint-based movement, limbs can only bend at joints (elbows, knees):
- Arms bend at elbows, legs bend at knees
- Limbs extend rather than deform
- Stiff puppet-like poses, rhythmic movements
- Similar to Calabash Brothers animation style
""".strip()

# ==================== 可灵AI图生视频提示词模板 ====================
VIDEO_PROMPT_TEMPLATE = """{action_description}

【动作风格要求 - 核心】
Joint-based movement, limbs can only bend at joints:
- Arms bend at elbows, legs bend at knees
- Abrupt stop-motion animation, frame by frame joint movements
- Limbs extend rather than deform, maintaining shape while changing angles
- Puppet/shadow puppet control style, stiff rhythmic movements
- Similar to Calabash Brothers animation action style

flat 2D Chinese shadow puppet animation, Chinese classical painting composition,
no perspective no depth, all elements on same visual plane,
Dunhuang fresco style, zero shading, vector art aesthetic,
minimal design, smooth white screen background.

rich color palette with diverse hues, varied color scheme,
soft pastel tones, low saturation, muted elegant colors,
watercolor-inspired colors, gentle pastel palette, no bright neon,
vibrant but muted, elegant color harmony, no oversaturated.
""".strip()

# ==================== 测试提示词 ====================
TEST_STORY = """
葫芦娃七兄弟合力化作一座大山，将蛇精和蝎子精永远镇压在山底。
从此，山下百姓过上了安居乐业的生活。
"""

# ==================== 提示词示例 ====================
EXAMPLE_IMAGE_PROMPTS = {
    "warrior": "Chinese warrior with sword, arms bent at elbows, legs bent at knees, flat 2D shadow puppet, joint-based puppet poses",
    "elder": "Wise elderly man with long white beard, arms bent at elbows, standing pose, flat 2D shadow puppet, Calabash Brothers style",
    "village": "Ancient Chinese village scene, traditional architecture, flat composition, Dunhuang fresco style, no perspective",
    "battle": "Two warriors fighting, arms bent at elbows holding swords, legs bent at knees in fighting stance, flat 2D shadow puppet style, stop-motion poses",
    "calabash_brother": "Calabash brother character, arms bent at elbows, legs bent at knees, flat 2D Chinese shadow puppet art, joint-based puppet movements",
    "snake_demon": "Evil snake demon female character, arms bent at elbows, legs bent at knees, flat 2D shadow puppet, Chinese classical painting style",
}
