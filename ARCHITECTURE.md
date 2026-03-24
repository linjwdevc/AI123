# 架构设计文档

## 概述

皮影戏AI漫剧工具是一个基于AI技术的创意工具，旨在将用户输入的故事文字自动转换为皮影戏风格的视频。

### 设计目标

- 模块化：各功能模块独立，便于维护和扩展
- 稳定性：内置重试机制，提高生成成功率
- 高效性：并行处理，加快生成速度
- 可部署性：支持本地运行和云端部署

## 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                         用户输入                            │
│                    (故事文字 via Web界面)                     │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      agent.py (主控)                         │
│                    ShadowPlayAgent                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 1. 调用LLM生成分镜脚本                                │   │
│  │ 2. 并行生成图片 (3 workers)                          │   │
│  │ 3. 并行生成视频 (3 workers)                          │   │
│  │ 4. 合并视频片段                                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│  llm_client   │   │image_client   │   │video_client   │
│   (分镜生成)   │   │   (生图)      │   │   (视频)      │
└───────────────┘   └───────────────┘   └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      video_utils.py                         │
│                    (视频合并处理)                             │
└─────────────────────────────────────────────────────────────┘
```

## 模块说明

### 1. config.py - 配置模块

**职责**: 管理所有API配置和项目配置

**配置项**:
- `QINIU_API_KEY` - 七牛云LLM API密钥
- `KLING_IMAGE_KEY` - 可灵AI生图API密钥
- `KLING_VIDEO_KEY` - 可灵AI视频API密钥
- `OUTPUT_DIR` - 输出目录路径
- `MAX_RETRIES` - 最大重试次数（默认3）
- `REQUEST_TIMEOUT` - 请求超时时间（默认180秒）
- `POLLING_TIMEOUT` - 轮询等待超时（默认600秒）
- `RETRY_DELAY` - 重试间隔（默认3秒）

**环境变量支持**:
```python
# 支持从环境变量读取，用于Streamlit Cloud部署
QINIU_API_KEY = os.environ.get("QINIU_API_KEY", "")
KLING_IMAGE_KEY = os.environ.get("KLING_IMAGE_KEY", "")
KLING_VIDEO_KEY = os.environ.get("KLING_VIDEO_KEY", "")
```

### 2. prompts.py - 提示词模板

**职责**: 存储所有AI模型的提示词模板

**包含内容**:
- `SYSTEM_PROMPT` - 系统提示词
- `STORYBOARD_PROMPT` - 分镜生成提示词
- `CHARACTER_PROMPT` - 角色描述提示词
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

**重试机制**:
```python
def chat_with_retry(prompt, system_prompt=None):
    for attempt in range(MAX_RETRIES):
        try:
            return chat(prompt, system_prompt)
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                raise
            time.sleep(RETRY_DELAY)
```

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

**后处理**:
- 图片自动进行后期处理优化
- 对比度增强 (1.5)
- 亮度调整 (1.1)
- 饱和度调整 (0.85)

### 5. video_client.py - 视频生成模块

**职责**: 调用可灵视频API将图片转换为视频

**类**: `VideoClient`

**方法**:
- `generate_video(image_path, prompt, duration, ratio)` - 生成视频
- `_wait_for_result(task_id, headers)` - 等待视频生成完成
- `_download_video(url)` - 下载视频到本地

**API配置**:
- URL: `https://api.qnaigc.com/v1/videos`
- Model: `kling-video-o1`

**视频参数**:
- 时长: 5-8秒
- 宽高比: 16:9 (可选)
- 质量: 高清

### 6. video_utils.py - 视频处理工具 ⚡新增

**职责**: 提供视频处理功能，包括合并、压缩等

**类**: `VideoMerger`

**方法**:
- `merge_videos(video_paths, output_path)` - 合并多个视频
- `_get_video_duration(video_path)` - 获取视频时长
- `_generate_file_list(video_paths)` - 生成FFmpeg文件列表
- `execute_command(cmd)` - 执行FFmpeg命令

**依赖**: FFmpeg（系统级依赖）

**使用示例**:
```python
merger = VideoMerger()
merger.merge_videos(['video1.mp4', 'video2.mp4'], 'output.mp4')
```

### 7. storyboard.py - 分镜工具

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

### 8. agent.py - 主程序 ⚡更新

**职责**: 串联所有模块，实现完整工作流

**类**: `ShadowPlayAgent`

**方法**:
- `__init__()` - 初始化所有客户端
- `run(story)` - 运行完整工作流
- `generate_single(prompt, generate_video)` - 生成单个场景

**并行处理架构**:
```python
# 使用ThreadPoolExecutor实现并行处理
with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(generate_single, scene) for scene in scenes]
    results = [f.result() for f in futures]
```

**工作流**:
1. 调用LLM生成分镜脚本
2. 解析分镜脚本
3. 并行生成图片（3个worker）
4. 并行生成视频（3个worker）
5. 合并所有视频片段
6. 返回所有生成结果

### 9. app.py - Web界面

**职责**: 提供Streamlit Web交互界面

**功能**:
- 故事输入文本框
- 生成按钮
- 图片展示
- 视频播放（支持直接URL播放）

## 数据流

```
输入故事
    │
    ▼
LLMClient.generate_storyboard() ──► 分镜JSON + 角色描述
    │
    ├──────────────────────────────────────┐
    ▼                                      ▼
ImageClient.generate() × N          VideoClient.generate() × N
（并行3个worker）                    （并行3个worker）
    │                                      │
    └──────────────────────────────────────┤
                                         ▼
                               VideoMerger.merge_videos()
                                         │
                                         ▼
                                     最终视频
```

## 配置管理

### 环境变量（推荐用于云部署）

```python
# config.py 优先从环境变量读取
import os

QINIU_API_KEY = os.environ.get("QINIU_API_KEY", "")
KLING_IMAGE_KEY = os.environ.get("KLING_IMAGE_KEY", "")
KLING_VIDEO_KEY = os.environ.get("KLING_VIDEO_KEY", "")
```

### 本地配置文件（仅本地开发）

创建 `config_local.py`：
```python
import os

os.environ["QINIU_API_KEY"] = "your-key"
os.environ["KLING_IMAGE_KEY"] = "your-key"
os.environ["KLING_VIDEO_KEY"] = "your-key"
```

注意：`config_local.py` 已加入 `.gitignore`，不会提交到GitHub。

## 重试机制

### 实现方式

所有API调用模块都实现了统一的异常处理和重试机制：

```python
MAX_RETRIES = 3
RETRY_DELAY = 3  # 秒
REQUEST_TIMEOUT = 180  # 秒

def retry_on_failure(func):
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                time.sleep(RETRY_DELAY)
                logging.warning(f"重试 {attempt + 1}/{MAX_RETRIES}: {e}")
    return wrapper
```

### 适用场景

- 网络请求超时
- API服务端错误
- 临时性连接失败
- 任务创建成功但结果获取失败

## 并行处理

### 架构设计

采用线程池实现并行处理：

```python
from concurrent.futures import ThreadPoolExecutor

WORKERS = 3  # 并行worker数量

with ThreadPoolExecutor(max_workers=WORKERS) as executor:
    futures = [executor.submit(task, item) for item in items]
    results = [f.result() for f in futures]
```

### 优势

- 充分利用网络IO等待时间
- 相比顺序执行提速约3倍
- 资源占用可控（固定3个线程）

### 注意事项

- 视频生成任务较重，不建议超过3个worker
- 图片生成任务较轻，可以适当增加worker

## 依赖

### Python依赖

```
streamlit>=1.28.0     # Web界面框架
requests>=2.31.0      # HTTP请求库
python-dotenv>=1.0.0  # 环境变量管理
pillow>=10.0.0        # 图片处理
```

### 系统依赖

```
ffmpeg                 # 视频处理（系统级）
```

安装方式：
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows
# 下载预编译二进制文件并添加到PATH
```

## 扩展性

系统设计支持以下扩展:

1. **添加新的AI模型**: 在对应模块中添加新的客户端类
2. **修改提示词**: 直接修改 `prompts.py` 中的模板
3. **添加新的输出格式**: 在 `agent.py` 中扩展输出处理
4. **调整并行度**: 修改 `WORKERS` 常量
5. **自定义后处理**: 在各客户端的 `_post_process()` 方法中添加

## 文件清单

| 文件 | 行数 | 职责 |
|------|------|------|
| config.py | 71 | 配置管理 |
| prompts.py | 250+ | 提示词模板 |
| llm_client.py | 150+ | LLM调用 |
| image_client.py | 200+ | 图片生成 |
| video_client.py | 220+ | 视频生成 |
| video_utils.py | 80+ | 视频处理 |
| agent.py | 300+ | 工作流编排 |
| app.py | 70 | Web界面 |
| storyboard.py | 150+ | 分镜工具 |
