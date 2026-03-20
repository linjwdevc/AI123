# 贡献指南

感谢你对皮影戏AI漫剧工具项目的兴趣！

## 如何贡献

### 问题反馈

如果你发现任何问题或有功能建议，请：

1. 检查是否已有相关issue
2. 创建新的issue并详细描述问题或建议
3. 提供复现步骤（如适用）

### 代码贡献

1. Fork 本仓库
2. 创建你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/linjwdevc/AI123.git
cd AI123
```

### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 配置API Key

编辑 `config.py` 文件，填入你的API密钥。

### 5. 运行开发服务器

```bash
streamlit run app.py
```

## 代码规范

### Python

- 使用Python 3.9+语法
- 遵循PEP 8代码规范
- 使用有意义的变量和函数命名
- 添加必要的文档字符串

### Git提交信息

请使用清晰的提交信息：

```
feat: 添加新功能
fix: 修复问题
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 其他杂项
```

## 分支策略

- `main` - 主分支，稳定版本
- `feature/*` - 功能分支
- `fix/*` - 修复分支

## Pull Request流程

1. 确保代码通过所有测试
2. 更新相关文档
3. 提交PR并描述你的更改
4. 等待代码审查

## 测试

在提交前，请确保测试通过：

```bash
python test_image.py
python test_sb.py
```

## 许可证

通过贡献代码，你同意你的贡献将按照MIT许可证进行许可。

## 联系方式

- GitHub Issues: https://github.com/linjwdevc/AI123/issues

感谢你的贡献！
