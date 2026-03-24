# Streamlit Cloud 部署指南

本文档说明如何将皮影戏AI漫剧工具部署到 Streamlit Community Cloud。

## 前提条件

- GitHub 账号
- 包含完整代码的 GitHub 仓库
- 七牛云 API 密钥（用于生成 AI 内容）

## 部署方式一：通过 GitHub 登录（推荐）

### 步骤 1：访问 Streamlit Cloud

打开浏览器，访问：https://share.streamlit.io/

### 步骤 2：登录

点击 "Sign in with GitHub" 使用 GitHub 账号登录。

如果没有 GitHub 账号，也可以选择：
- Google 账号登录
- 邮箱注册登录

### 步骤 3：创建新应用

1. 点击页面上的 **"New app"** 按钮
2. 在弹出的配置页面中填写信息：

| 字段 | 填写内容 |
|------|----------|
| Repository | `linjwdevc/AI123` |
| Branch | `clean_master` |
| Main file path | `app.py` |

### 步骤 4：部署

点击 **"Deploy!"** 按钮开始部署。

部署过程大约需要 1-3 分钟，页面会显示 "Deploying your app..." 状态。

### 步骤 5：配置环境变量（重要！）

部署成功后，需要配置 API 密钥：

1. 点击部署完成的 App
2. 进入 **"Settings"** 页面
3. 向下滚动找到 **"Secrets"** 部分
4. 在编辑框中输入以下内容：

```toml
QINIU_API_KEY = "你的七牛API密钥"
KLING_IMAGE_KEY = "你的可灵生图密钥"
KLING_VIDEO_KEY = "你的可灵视频密钥"
```

**示例**：
```toml
QINIU_API_KEY = "sk-6f5434ded0ed241fed00e7bdabb2a25d086abc75f4a3e594ef7393647feecf29"
KLING_IMAGE_KEY = "sk-4b19c3773a4930428c79f7d336bb8e55284d80585a7c250fa8953e6d2406bb59"
KLING_VIDEO_KEY = "sk-6fe617782f0db691d5e17b49d806e54d815d16e4d56963c63ddb86be2f63df41"
```

5. 点击 **"Save"** 保存
6. App 会自动重启，应用新的环境变量

### 步骤 6：获取公开链接

部署和配置完成后，你将获得一个公开访问链接，格式如：

```
https://用户名-仓库名-分支名.streamlit.app/
```

示例：
```
https://sndnnnjyzgxwfeuhirj5wf.streamlit.app/
```

此链接可以直接分享给任何人访问，无需登录。

---

## 部署方式二：通过其他账号登录

### 步骤 1：访问 Streamlit Cloud

打开 https://share.streamlit.io/

### 步骤 2：选择登录方式

- **Google 登录**：点击 "Continue with Google"
- **邮箱登录**：点击 "Sign up with email"，输入邮箱后收到验证码完成验证

### 步骤 3：授权 GitHub 仓库访问

首次部署时，需要授权 Streamlit 访问你的 GitHub 仓库：

1. 在创建 App 页面，选择你的仓库
2. 如果仓库未显示，点击 "Connect GitHub account" 链接
3. 按照提示授权访问

### 步骤 4：后续步骤

授权完成后，按照"部署方式一"的步骤 3-6 完成部署。

---

## 更新部署

当你推送新代码到 GitHub 仓库后，Streamlit Cloud 会自动检测并重新部署。

### 手动重新部署

1. 进入你的 App 管理页面
2. 点击 **"Manage app"**
3. 点击 **"Reboot"** 按钮

### 查看部署历史

在 "Manage app" 页面可以查看：
- 当前部署状态
- 部署历史记录
- 日志信息

---

## 环境变量配置详解

### 什么是环境变量？

环境变量是存储敏感配置（如 API 密钥）的安全方式，不会随代码一起提交到 GitHub。

### 必需的环境变量

| 变量名 | 说明 | 获取方式 |
|--------|------|----------|
| `QINIU_API_KEY` | 七牛云 LLM API 密钥 | 七牛云控制台 |
| `KLING_IMAGE_KEY` | 可灵 AI 生图 API 密钥 | 七牛云控制台 |
| `KLING_VIDEO_KEY` | 可灵 AI 视频 API 密钥 | 七牛云控制台 |

### 获取 API 密钥

1. 登录七牛云控制台：https://console.qnaigc.com/
2. 进入 API Key 管理页面
3. 复制对应的 Key 值

### 本地开发时的环境变量

本地开发时，可以创建 `config_local.py` 文件：

```python
import os

os.environ["QINIU_API_KEY"] = "your-key-here"
os.environ["KLING_IMAGE_KEY"] = "your-key-here"
os.environ["KLING_VIDEO_KEY"] = "your-key-here"
```

**注意**：`config_local.py` 已加入 `.gitignore`，不会提交到 GitHub。

---

## 常见问题

### Q: 部署失败怎么办？

**A:** 检查以下几点：
1. GitHub 仓库是否存在且代码完整
2. `requirements.txt` 是否包含所有依赖
3. `app.py` 是否在仓库根目录
4. 查看部署日志排查具体错误

### Q: 部署成功但功能不工作？

**A:** 检查：
1. 环境变量是否正确配置
2. API Key 是否有效
3. 查看 App 日志排查错误

### Q: 如何修改已部署的 App？

**A:** 直接推送代码到 GitHub，Streamlit Cloud 会自动重新部署。修改环境变量需要在 Settings 中手动更新。

### Q: 可以部署到自定义域名吗？

**A:** Streamlit Community Cloud 免费版不支持自定义域名。如需自定义域名，可以升级到付费版或使用其他部署平台。

### Q: App 休眠了怎么办？

**A:** 免费版 App 如果长时间未访问会进入休眠状态。用户首次访问时会自动唤醒，但可能会有 1-2 分钟的延迟。

---

## 架构说明

### 为什么使用环境变量？

本项目将 API 密钥存储在环境变量中，而不是代码中，原因：

| 方式 | 优点 | 缺点 |
|------|------|------|
| 环境变量 | 安全、不随代码泄露 | 需要额外配置 |
| 代码中硬编码 | 简单 | 密钥会提交到 GitHub，极其危险 |
| 本地配置文件 | 本地开发方便 | 需要添加到 .gitignore |

### Streamlit Cloud 的文件访问

**重要限制**：Streamlit Cloud 服务器上的文件是临时的、重启后会清除。因此：

- 生成的文件无法直接下载
- 不适合存储大量媒体文件
- 建议将生成结果上传到云存储（如七牛云 OSS）

---

## 相关文档

- [README.md](../README.md) - 项目总体说明
- [操作说明.md](./操作说明.md) - 使用指南
- [ARCHITECTURE.md](../ARCHITECTURE.md) - 架构设计文档

---

## 参考链接

- Streamlit 官方文档：https://docs.streamlit.io/
- Streamlit Cloud：https://streamlit.io/cloud
- 七牛云控制台：https://console.qnaigc.com/
