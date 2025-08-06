
# SpiderHello - 多功能API集成平台

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-005C84?style=for-the-badge&logo=mysql&logoColor=white)


SpiderHello 是一个基于Django和MySQL开发的多功能API集成平台，目前提供音乐平台数据、AI媒体处理和虚拟邮箱三大核心功能,后续会持续更新新功能。


### 功能特性表格

#### 1. 音乐平台功能

| 功能                     | 支持状态 |
|--------------------------|----------|
| 搜索音乐                 | ✓        |
| 获取热门歌单分类         | ✓        |
| 根据热门榜单分类ID获取歌曲 | ✓        |
| 获取歌手的音乐           | ✓        |
| 获取歌手的专辑音乐       | ✓        |

#### 2. AI媒体处理功能

| 功能               | 支持状态 |
|--------------------|----------|
| 文字转语音         | ✓        |
| 语音转文字         | ✓        |
| 视频翻译           | ✓        |
| 人声分离           | ✓        |
| 文件上传           | ✓        |

#### 3. 虚拟邮箱功能

| 功能                     | 支持状态 |
|--------------------------|----------|
| 支持无限生成邮箱         | ✓        |
| 支持收信                 | ✓        |
| 支持10-24小时长时间使用  | ✓        |
| 邮箱域名：awamail.com    | ✓        |
| 邮箱域名：internxt.com   | ✓        |

#### 4. 视频解析功能

| 平台       | 支持状态 |
|------------|----------|
| 抖音       | ✓        |
| 哔哩哔哩   | ✓        |
| 快手       | (待支持)  |
| YouTube    | (待支持)  |

### 新增功能说明
1. **虚拟邮箱**：现已支持无限生成邮箱、收信，并可长时间使用（10-24小时）。
2. **视频解析**：新增抖音、哔哩哔哩视频解析功能，后续将逐步扩展至快手、YouTube等平台（灰色勾表示待支持）。

### 其他说明
- 绿色勾（✓）表示功能已支持。
- 灰色勾（(待支持)）表示功能后续更新中。

如果需要进一步调整或补充，请随时告知！

## 使用条款

本项目可自由用于任何合法用途。我们提供以下技术支持服务：

- **免费服务**：
  - 项目基础功能升级
  - Bug修复

- **收费服务**：
  - 自定义二次开发
  - 特殊功能定制

## 技术支持

如需技术支持或定制开发服务，请联系：

微信: `duyanbz`

我们承诺：
- 及时响应
- 专业解决方案
- 合理定价



## 安装与部署

1. 克隆仓库
```bash
git clone https://github.com/YyCloud2024/SpiderHello.git
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置MySQL数据库
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

4. 运行迁移
```bash
python manage.py migrate
```

5. 启动服务
```bash
python manage.py runserver
```

## API文档

详细API文档请参考项目Wiki或联系技术支持获取。

## 贡献

欢迎提交Pull Request。对于重大更改，请先开Issue讨论。

## 许可证

MIT License
