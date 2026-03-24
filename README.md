# 皮影戏AI漫剧工具

🎭 输入故事文字，自动生成皮影戏风格的AI视频

## 在线体验

**Streamlit Cloud**: https://sndnnnjyzgxwfeuhirj5wf.streamlit.app/

本地运行：
```bash
streamlit run app.py
```

## 项目简介

皮影戏AI漫剧工具是一款基于AI技术的创意工具，能够将用户输入的故事文字自动转换为皮影戏风格的视频。

### 核心功能

- **📝 LLM分镜**: 使用七牛云LLM将故事自动转换为分镜脚本
- **🖼️ AI生图**: 使用可灵AI生成皮影戏风格的图片
- **🎬 图生视频**: 使用可灵视频模型将图片转换为视频
- **🌐 Web界面**: 基于Streamlit的友好交互界面
- **🔄 并行处理**: 3个worker并行加速生成
- **⚡ 自动重试**: 网络波动时自动重试提高稳定性

### 风格特点

- 平面构图，无空间纵深
- 二维剪纸风格，类似敦煌壁画/年画
- 关节动作设计，类似皮影戏/木偶操控
- 复古色彩，剪纸动画质感

## 技术栈

- **语言**: Python 3.9+
- **框架**: Streamlit
- **AI模型**: 
  - 七牛云LLM (moonshotai/kimi-k2.5)
  - 可灵AI生图 (kling-v1)
  - 可灵视频 (kling-video-o1)
- **部署**: Streamlit Community Cloud

## 本地部署

### 环境要求

- Python 3.9+
- pip
- Git

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/linjwdevc/AI123.git
cd AI123
```

2. 创建虚拟环境（推荐）：
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置API Key：

创建 `config_local.py` 文件，填入你的API密钥：
```python
import os

os.environ["QINIU_API_KEY"] = "你的七牛API密钥"
os.environ["KLING_IMAGE_KEY"] = "你的可灵生图密钥"
os.environ["KLING_VIDEO_KEY"] = "你的可灵视频密钥"
```

5. 运行Web界面：
```bash
streamlit run app.py
```

### 配置说明

API密钥支持两种配置方式：

| 方式 | 适用场景 | 说明 |
|------|----------|------|
| 环境变量 | Streamlit Cloud | 在Settings→Secrets中配置 |
| config_local.py | 本地开发 | 文件已加入.gitignore |

### 测试脚本

项目包含以下测试脚本：

| 文件 | 用途 |
|------|------|
| `test_image.py` | 图片生成测试 |
| `test_sb.py` | 分镜生成测试 |
| `test_character.py` | 角色一致性测试 |
| `test_video_flat.py` | 视频平面效果测试 |
| `test_video_single.py` | 单个视频生成测试 |

运行测试：
```bash
python test_image.py    # 测试图片生成
python test_sb.py      # 测试分镜生成
python test_character.py  # 测试角色一致性
```

## 项目结构

```
shadow-play-agent/
├── config.py              # 配置模块（环境变量）
├── config_template.py     # 配置模板
├── config_local.py        # 本地配置（不提交到Git）
├── prompts.py             # AI提示词模板
├── llm_client.py          # LLM分镜模块
├── image_client.py        # 图片生成模块
├── video_client.py       # 视频生成模块
├── video_utils.py        # 视频处理工具
├── agent.py              # 主程序（工作流编排）
├── app.py                 # Web界面
├── storyboard.py         # 分镜工具
├── requirements.txt       # Python依赖
├── README.md              # 项目说明
├── ARCHITECTURE.md        # 架构设计文档
├── 操作说明.md            # 详细使用指南
├── STREAMLIT_DEPLOY.md   # Streamlit部署指南
└── output/                # 输出目录
```

## 使用方法

### Web界面

1. 运行 `streamlit run app.py`
2. 在文本框中输入故事内容
3. 点击"开始生成"按钮
4. 等待视频生成完成

### 命令行

```bash
# 运行完整流程
python agent.py

# 测试各个模块
python llm_client.py      # 测试分镜生成
python image_client.py    # 测试图片生成
python video_client.py    # 测试视频生成
```

## API配置

| 服务 | API端点 | 模型 |
|------|---------|------|
| LLM | 七牛云 | moonshotai/kimi-k2.5 |
| 生图 | 七牛云 | kling-v1 |
| 视频 | 七牛云 | kling-video-o1 |

详细配置说明请参考 [STREAMLIT_DEPLOY.md](./STREAMLIT_DEPLOY.md)

## 架构设计

系统采用模块化设计，各模块职责清晰：

- **config.py**: 统一配置管理，支持环境变量
- **prompts.py**: AI提示词模板集中管理
- **llm_client.py**: LLM调用封装，包含重试逻辑
- **image_client.py**: 图片生成封装，包含轮询和下载
- **video_client.py**: 视频生成封装，包含任务轮询
- **video_utils.py**: 视频处理工具（FFmpeg封装）
- **agent.py**: 工作流编排，串联各模块
- **app.py**: Web界面，基于Streamlit

详细架构说明请参考 [ARCHITECTURE.md](./ARCHITECTURE.md)

## 比赛信息

- **用途**: AI创意比赛参赛作品
- **资源**: 七牛云4800万token
- **截止日期**: 2026年3月27日

## 注意事项

- 视频生成需要等待约2-3分钟
- 可灵视频模型支持5-8秒视频片段
- 生成结果保存在output目录
- 并行处理使用3个worker提高效率
- 包含自动重试机制（最多3次）

## License

MIT License - see [LICENSE](LICENSE) file for details
