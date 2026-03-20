# 皮影戏AI智能体 - 队友任务书

## 项目概述
开发一个Web工具：输入故事文字 → 输出MP4皮影戏视频

## 技术架构
```
用户输入故事 
    ↓
LLM(七牛云) → 分镜脚本 + 角色描述
    ↓
AI生图(通义万相) → 皮影风格角色图
    ↓
图生视频(即梦AI) → MP4视频
    ↓
返回给用户
```

## 文件结构
```
shadow-play-agent/
├── config.py           # 配置文件（填API Key）
├── prompts.py         # 提示词模板
├── llm_client.py      # LLM调用模块
├── image_client.py    # 生图模块
├── video_client.py    # 视频生成模块
├── agent.py           # 主程序（串联工作流）
├── app.py             # Streamlit Web界面
├── requirements.txt   # 依赖
└── README.md         # 使用说明
```

## 任务分配

### 队友任务（代码开发）

#### 任务1：配置文件（今天完成）
- 填入三个平台的API Key到config.py

#### 任务2：LLM调用模块（1小时）
- 实现llm_client.py
- 调用七牛云API生成分镜脚本

#### 任务3：生图模块（1小时）
- 实现image_client.py
- 调用通义万相API生成皮影图

#### 任务4：视频生成模块（1小时）
- 实现video_client.py
- 调用即梦AI API生成视频

#### 任务5：主程序（2小时）
- 实现agent.py
- 串联以上三个模块

#### 任务6：Web界面（1小时）
- 实现app.py
- Streamlit对话界面

### 你的任务（提示词设计）
- 设计皮影风格的提示词
- 测试生图/视频效果

## 快速开始

1. 克隆仓库后：
```bash
pip install -r requirements.txt
```

2. 填入API Key到config.py

3. 运行测试：
```bash
python llm_client.py  # 测试LLM
python image_client.py  # 测试生图
python video_client.py  # 测试视频
```

4. 运行完整流程：
```bash
python agent.py
```

5. 运行Web界面：
```bash
streamlit run app.py
```

## API文档

### 七牛云LLM
- Base URL: https://api.qnaigc.com
- Model: moonshotai/kimi-k2.5
- 文档：七牛云控制台查看

### 通义万相
- API: https://dashscope.aliyuncs.com
- 模型：wanx2.1
- 文档：阿里云百炼

### 即梦AI
- API: https://jimeng.jianying.com
- 模型：cogvideox
- 文档：即梦开放平台

## 遇到问题？
- 查看各平台官方API文档
- 用OpenCode问AI
