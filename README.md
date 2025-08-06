# SpiderHello - 多功能API集成平台

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

SpiderHello 是一个基于Django开发的多功能API集成平台，提供两种灵活的使用方式：
1. **API调用**：通过HTTP接口远程调用服务
2. **本地脚本运行**：下载项目后在本地环境中直接运行

## 功能特性

### 🎵 音乐平台功能
- 搜索音乐
- 获取热门歌单分类
- 根据热门榜单分类ID获取歌曲
- 获取歌手的音乐
- 获取歌手的专辑音乐

### 🤖 AI媒体处理功能
- 文字转语音
- 语音转文字
- 视频翻译
- 人声分离
- 文件上传

### 📧 虚拟邮箱功能
- 支持无限生成邮箱
- 支持收信
- 支持10-24小时长时间使用
- 支持邮箱域名：awamail.com
- 支持邮箱域名：internxt.com

### 🎬 视频解析功能
- 抖音视频解析
- 哔哩哔哩视频解析

## 使用方式说明

### 🔗 API调用方式
- 通过HTTP接口远程调用服务
- 适合快速集成到现有系统中
- 无需担心调用限额，完全开放使用

### 🖥️ 本地脚本运行
- 下载项目后在本地环境中直接运行
- 适合需要深度定制或离线使用的场景
- 无需配置MySQL数据库，仅需Python环境即可运行
- 本地运行同样无功能限制，完全免费使用

## 新增功能说明
- **虚拟邮箱**：现已支持无限生成邮箱、收信，并可长时间使用（10-24小时）。
- **视频解析**：新增抖音、哔哩哔哩视频解析功能。

## 服务说明
本项目所有基础功能均可自由用于任何合法用途，完全免费且无使用限制。

我们提供的技术支持服务：
- **免费服务**：
  - 项目基础功能升级
  - Bug修复

- **收费服务**（仅针对定制开发需求）：
  - 自定义二次开发
  - 特殊功能定制
  - 专属功能开发支持

## 技术支持
如需技术支持或定制开发服务，请联系：

微信: `duyanbz`  
或扫描下方二维码添加微信咨询：

![微信二维码](https://img20.360buyimg.com/openfeedback/jfs/t1/294641/16/20304/18390/6892baceF16adf7e7/5063700cc97877bc.jpg)  

我们承诺：
- 及时响应（工作日1小时内回复）
- 专业解决方案
- 7×12小时技术支持服务

## 安装与部署

### 本地脚本运行（推荐）
1. 克隆仓库
```bash
git clone https://github.com/YyCloud2024/SpiderHello.git
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 直接启动服务（无需数据库配置）
```bash
python manage.py runserver
```

### API服务部署（如需自建API服务）
1. 完成上述"本地脚本运行"的1-2步
2. 配置MySQL数据库（仅API服务部署需要）
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spiderhello',
        'USER': '你的用户名',
        'PASSWORD': '你的数据库密码',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

3. 运行迁移
```bash
python manage.py migrate
```

4. 启动API服务
```bash
python manage.py runserver
```

## API文档

完整API文档已在线发布，包含所有接口的详细说明和示例：

📚 [API文档地址](https://cbvh18yi9h.apifox.cn/)

文档内容包括：
- 接口请求方式
- 参数说明
- 返回示例
- 错误代码
- 使用指南

## 快速开始指南

1. **API方式**：
   - 联系微信：duyanbz获取测试Key
   - 参考API文档调用接口
   - 无调用次数限制，自由使用

2. **本地运行方式**：
   - 按照安装部署步骤配置Python环境
   - 直接运行项目脚本即可使用全部功能
   - 无需数据库，开箱即用

## 常见问题

Q: API调用和本地运行哪种方式更好？  
A: 根据需求选择 - API方式简单快捷，适合快速集成；本地运行更灵活可控，适合离线使用

Q: 项目是否有使用限制？  
A: 所有基础功能完全开放，无任何使用限制，可自由用于合法用途

Q: 如何获取技术支持？  
A: 1. 查阅API文档 2. 加入技术交流群 3. 添加微信 duyanbz 获取一对一支持

## 贡献

欢迎提交Pull Request。对于重大更改，请联系开发者或进入项目组讨论。

## 许可证

MIT License

---

**温馨提示**：项目持续更新中，建议关注项目更新动态。如需第一时间获取新功能通知，请添加微信：duyanbz 加入技术交流群。