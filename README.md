# 手串饰品预测系统 - Vercel部署指南

这是一个针对Vercel平台优化的手串饰品预测系统版本。本指南将帮助您成功部署应用到Vercel平台。

## 文件说明

- `index.py`: Vercel入口点文件
- `app.py`: 主应用程序文件
- `vercel.json`: Vercel配置文件
- `requirements.txt`: 依赖项列表
- `templates/`: HTML模板目录
  - `index.html`: 首页模板
  - `result.html`: 结果页模板
  - `error.html`: 错误页模板

## 部署步骤

### 1. 准备GitHub仓库

1. 登录您的GitHub账号
2. 创建一个新的仓库，例如`feng-shui-bracelet-app`
3. 将本目录中的所有文件上传到该仓库

### 2. 部署到Vercel

1. 登录您的Vercel账号
2. 点击"Add New..."按钮，然后选择"Project"
3. 从列表中找到并选择您刚创建的GitHub仓库
4. 保持默认设置不变
5. 在"Environment Variables"部分，添加以下环境变量（如果需要使用DeepSeek API）：
   - NAME: `DEEPSEEK_API_KEY`
   - VALUE: `sk-b21ed31cf5f34cf483602422613aac4c`
6. 点击"Deploy"按钮开始部署

### 3. 访问您的应用

部署完成后，Vercel会提供一个URL（例如：https://feng-shui-bracelet-app.vercel.app）。点击该URL即可访问您的手串饰品预测系统。

## 故障排除

如果您在部署过程中遇到问题，请检查以下几点：

1. 确保所有文件都已正确上传到GitHub仓库
2. 检查Vercel的构建日志，查找可能的错误信息
3. 确保环境变量已正确设置（如果使用DeepSeek API）

## 更新应用

如果您需要更新应用，只需更新GitHub仓库中的文件，Vercel会自动检测更改并重新部署。

## 注意事项

- 这个版本是专门为Vercel平台优化的，采用了简化的设计以确保兼容性
- 所有功能都在单个app.py文件中实现，以减少依赖和复杂性
- 如果您需要添加更多功能，请确保遵循Vercel的最佳实践
