# 皮影戏AI漫剧工具

🎭 输入故事文字，自动生成皮影戏风格的AI视频

## 在线体验

**Streamlit Cloud**: [部署链接待填写]

本地运行：
```bash
streamlit run app.py
```

## 项目简介

皮影戏AI漫剧工具是一款基于AI技术的创意工具，能够将用户输入的故事文字自动转换为皮影戏风格的视频。

### 核心功能

- **📝 LLM分镜**: 使用七牛云LLM将故事自动转换为分镜脚本
- **🖼️ AI生图**: 使用可灵AI生成皮影戏风格的图片
- **🎬 图生视频**: 使用Veo模型将图片转换为视频
- **🌐 Web界面**: 基于Streamlit的友好交互界面

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
  - Veo视频生成 (veo-3.1-generate-preview)

## 本地部署

### 环境要求

- Python 3.9+
- pip

### 安装步骤

1. 克隆仓库：
```bash
git clone https://github.com/linjwdevc/AI123.git
cd AI123
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置API Key：
编辑 `config.py` 文件，填入你的API Key：
- `QINIU_API_KEY`: 七牛云LLM
- `KLING_IMAGE_KEY`: 可灵AI生图
- `KLING_VIDEO_KEY`: Veo视频生成

4. 运行Web界面：
```bash
streamlit run app.py
```

### 测试脚本

项目包含以下测试脚本用于调试：

- `test_image.py` - 图片生成测试脚本
- `test_sb.py` - 分镜生成测试脚本

运行测试：
```bash
python test_image.py  # 测试图片生成
python test_sb.py    # 测试分镜生成
```

## 项目结构

```
shadow-play-agent/
├── config.py           # 配置文件
├── prompts.py         # 提示词模板
├── llm_client.py      # LLM分镜模块
├── image_client.py    # 图片生成模块
├── video_client.py    # 视频生成模块
├── agent.py           # 主程序
├── app.py             # Web界面
├── storyboard.py      # 分镜工具
├── test_image.py      # 图片测试脚本
├── test_sb.py         # 分镜测试脚本
└── output/            # 输出目录
```

## 使用方法

### Web界面

1. 运行 `streamlit run app.py`
2. 在文本框中输入故事内容
3. 点击"开始生成"按钮
4. 等待视频生成完成

### 命令行

```bash
# 测试分镜生成
python llm_client.py

# 测试图片生成
python test_image.py

# 测试视频生成
python video_client.py

# 运行完整流程
python agent.py
```

## API说明

| 服务 | API | 模型 |
|------|-----|------|
| LLM | 七牛云 | moonshotai/kimi-k2.5 |
| 生图 | 七牛云(可灵) | kling-v1 |
| 视频 | 七牛云(Veo) | veo-3.1-generate-preview |

## 比赛信息

- 用途：AI创意比赛参赛作品
- 资源：七牛云4800万token
- 截止日期：2026年3月27日

## 注意事项

- 视频生成需要等待约2-3分钟
- Veo模型仅支持8秒视频
- 生成结果保存在output目录

## License

MIT License - see [LICENSE](LICENSE) file for details
