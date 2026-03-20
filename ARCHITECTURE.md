# 架构设计文档

## 概述

皮影戏AI漫剧工具是一个基于AI技术的创意工具，旨在将用户输入的故事文字自动转换为皮影戏风格的视频。

## 系统架构

```
用户输入故事 
    ↓
LLM分镜 → 分镜脚本 + 角色描述
    ↓
AI生图 → 皮影风格角色图
    ↓
图生视频 → MP4视频
    ↓
返回给用户
```

## 模块说明

### 1. config.py - 配置模块

**职责**: 管理所有API配置和项目配置

**配置项**:
- `QINIU_API_KEY` - 七牛云LLM API密钥
- `KLING_IMAGE_KEY` - 可灵AI生图API密钥
- `KLING_VIDEO_KEY` - Veo视频生成API密钥
- `OUTPUT_DIR` - 输出目录路径
- `MAX_RETRIES` - 最大重试次数
- `REQUEST_TIMEOUT` - 请求超时时间

### 2. prompts.py - 提示词模板

**职责**: 存储所有AI模型的提示词模板

**包含内容**:
- `SYSTEM_PROMPT` - 系统提示词
- `STORYBOARD_PROMPT` - 分镜生成提示词
- `CHARACTER_PROMPT` - 角色描述提示词
- `SCENE_PROMPT` - 场景描述提示词
- `IMAGE_PROMPT_TEMPLATE` - 图片生成提示词模板
- `VIDEO_PROMPT_TEMPLATE` - 视频生成提示词模板
- `ACTION_STYLE` - 动作风格描述

**提示词设计原则**:
- 平面构图，无空间纵深
- 二维剪纸风格
- 关节动作设计
- 复古色彩

### 3. llm_client.py - LLM分镜模块

**职责**: 调用七牛云LLM API生成分镜脚本

**类**: `LLMClient`

**方法**:
- `chat(prompt, system_prompt)` - 发送对话请求
- `generate_storyboard(story, system_prompt)` - 生成分镜脚本
- `parse_storyboard(raw_response)` - 解析分镜脚本
- `generate_character_desc(name, appearance, personality)` - 生成角色描述

**API配置**:
- Base URL: `https://api.qnaigc.com/v1`
- Model: `moonshotai/kimi-k2.5`

### 4. image_client.py - 图片生成模块

**职责**: 调用可灵AI API生成皮影戏风格图片

**类**: `ImageClient`

**方法**:
- `generate_image(prompt, negative_prompt, size)` - 生成图片
- `_wait_for_result(task_id, headers)` - 等待图片生成完成
- `_download_image(url)` - 下载图片到本地
- `generate_shadow_puppet(subject)` - 生成皮影风格图片

**API配置**:
- URL: `https://api.qnaigc.com/v1/images/generations`
- Model: `kling-v1`

### 5. video_client.py - 视频生成模块

**职责**: 调用Veo API将图片转换为视频

**类**: `VideoClient`

**方法**:
- `generate_video(image_path, prompt, duration, ratio)` - 生成视频
- `_wait_for_result(task_id, headers)` - 等待视频生成完成
- `_download_video(url)` - 下载视频到本地

**API配置**:
- URL: `https://api.qnaigc.com/v1/videos/generations`
- Model: `veo-3.1-generate-preview`

### 6. storyboard.py - 分镜工具

**职责**: 本地规则分镜生成（不消耗token）

**函数**:
- `split_sentences(text)` - 将故事文本拆分成句子
- `expand_combat_sentence(sentence)` - 展开战斗场景句子为多个分镜
- `estimate_duration(画面, 景别)` - 估计分镜时长
- `generate_storyboard(story)` - 生成分镜脚本
- `format_storyboard(storyboard)` - 格式化分镜为文本

**分镜规则**:
- 战斗场景展开为多个特写镜头
- 首尾镜头为远景
- 战斗镜头时长3秒
- 安静镜头时长6秒

### 7. agent.py - 主程序

**职责**: 串联所有模块，实现完整工作流

**类**: `ShadowPlayAgent`

**方法**:
- `__init__()` - 初始化所有客户端
- `run(story)` - 运行完整工作流
- `generate_single(prompt, generate_video)` - 生成单个场景

**工作流**:
1. 调用LLM生成分镜脚本
2. 解析分镜脚本
3. 为每个分镜生成图片
4. 为每张图片生成视频
5. 返回所有生成结果

### 8. app.py - Web界面

**职责**: 提供Streamlit Web交互界面

**功能**:
- 故事输入文本框
- 生成按钮
- 图片展示
- 视频播放

## 数据流

```
输入故事
    ↓
LLMClient.generate_storyboard() → 分镜JSON
    ↓
for each scene:
    ImageClient.generate_shadow_puppet() → 图片路径
    ↓
    VideoClient.generate_video() → 视频路径
    ↓
返回结果字典
```

## 配置文件

所有配置集中在 `config.py`:

```python
# API配置
QINIU_API_KEY = "..."
KLING_IMAGE_KEY = "..."
KLING_VIDEO_KEY = "..."

# 项目配置
OUTPUT_DIR = "output"
MAX_RETRIES = 3
REQUEST_TIMEOUT = 120
```

## 依赖

- `streamlit>=1.28.0` - Web界面框架
- `requests>=2.31.0` - HTTP请求库
- `python-dotenv>=1.0.0` - 环境变量管理

## 扩展性

系统设计支持以下扩展:

1. **添加新的AI模型**: 在对应模块中添加新的客户端类
2. **修改提示词**: 直接修改 `prompts.py` 中的模板
3. **添加新的输出格式**: 在 `agent.py` 中扩展输出处理
