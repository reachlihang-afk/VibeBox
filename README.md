# VibeBox

<div align="center">
  <h3>🎯 跨平台 AI 智能内容收藏与离线管理工具</h3>
  <p>一个 App，管理所有平台的精彩内容</p>
</div>

---

## 📱 产品简介

VibeBox 是一款专注于**移动端**的跨平台内容聚合工具，通过**系统分享菜单**和**智能剪贴板监听**，让你轻松保存来自小红书、抖音、B站、YouTube、Reddit 等平台的内容，并支持**完全离线**查看。

### 核心特性

- 🔗 **一键分享保存** - 在任何 App 点击"分享"即可保存到 VibeBox
- 🤖 **AI 智能分类** - 自动识别内容类型并打标签（投资、美食、旅行等）
- 📥 **离线优先** - WiFi 自动下载，地铁飞机也能流畅刷
- 🎨 **统一 Feed 流** - 所有平台内容聚合在一个界面
- 🔒 **隐私安全** - 数据完全本地存储，加密保护

---

## 🚀 支持的平台

### 核心支持（通过分享链接）
- ✅ **小红书** - 图文笔记、视频
- ✅ **抖音** - 短视频
- ✅ **B站** - 视频、专栏
- ✅ **微博** - 微博内容
- ✅ **雪球** - 投资文章

### 官方 API 集成（自动同步）
- ✅ **YouTube** - 播放列表、收藏
- ✅ **Reddit** - Saved Posts
- ✅ **Pocket** - 书签同步

---

## 🏗️ 技术架构

```
┌─────────────────────────────────────────┐
│          移动端 (Flutter)                │
│  ┌────────────┐  ┌────────────┐         │
│  │ iOS Share  │  │  Android   │         │
│  │ Extension  │  │  Intent    │         │
│  └────────────┘  └────────────┘         │
│         ↓              ↓                 │
│  ┌──────────────────────────┐           │
│  │   剪贴板智能监听          │           │
│  └──────────────────────────┘           │
│         ↓                                │
│  ┌──────────────────────────┐           │
│  │   本地数据库 (SQLite)     │           │
│  └──────────────────────────┘           │
└─────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────┐
│      后端服务 (FastAPI - 可选)           │
│  ┌──────────────────────────┐           │
│  │   链接解析服务            │           │
│  │  - 小红书解析器           │           │
│  │  - 抖音解析器             │           │
│  │  - B站解析器              │           │
│  └──────────────────────────┘           │
└─────────────────────────────────────────┘
```

### 技术栈

**移动端**
- Flutter 3.x
- SQLite (本地数据库)
- Hive (轻量级存储)
- Dio (网络请求)

**后端服务**
- Python 3.11+
- FastAPI (Web 框架)
- BeautifulSoup4 (HTML 解析)
- httpx (异步 HTTP)

---

## 📦 项目结构

```
VibeBox/
├── mobile/                 # Flutter 移动端
│   ├── lib/
│   │   ├── main.dart      # 应用入口
│   │   ├── models/        # 数据模型
│   │   ├── services/      # 业务逻辑
│   │   ├── screens/       # 页面
│   │   └── widgets/       # UI 组件
│   ├── ios/               # iOS 配置
│   │   └── ShareExtension/ # 分享扩展
│   ├── android/           # Android 配置
│   └── pubspec.yaml       # 依赖配置
│
├── backend/               # 后端服务
│   ├── main.py           # FastAPI 主文件
│   ├── parsers/          # 链接解析器
│   └── requirements.txt  # Python 依赖
│
├── docs/                 # 文档
│   ├── PRD.md           # 产品需求文档
│   ├── ARCHITECTURE.md  # 技术架构
│   └── API.md           # API 文档
│
└── README.md            # 项目说明
```

---

## 🛠️ 快速开始

### 环境要求

- Flutter SDK >= 3.0.0
- Dart >= 3.0.0
- Python >= 3.11 (后端服务)
- iOS 14+ / Android 8+

### 移动端开发

```bash
# 1. 克隆项目
git clone https://github.com/reachlihang-afk/VibeBox.git
cd VibeBox/mobile

# 2. 安装依赖
flutter pub get

# 3. 运行应用
flutter run
```

### 后端服务（可选）

```bash
# 1. 进入后端目录
cd backend

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 启动服务
uvicorn main:app --reload
```

---

## 📖 使用指南

### 1. 保存内容

**方式 A：系统分享菜单**
1. 在小红书/抖音等 App 看到喜欢的内容
2. 点击"分享"按钮
3. 选择"VibeBox"
4. 自动保存并后台下载

**方式 B：复制链接**
1. 复制内容分享链接
2. 打开 VibeBox
3. 自动检测并提示保存

### 2. 离线查看

- 所有保存的内容会在 WiFi 环境下自动下载
- 断网状态也能流畅查看视频和图片
- 支持视频播放、图片浏览、文章阅读

### 3. AI 智能分类

- 系统自动识别内容类型
- 自动打标签（#投资、#美食、#旅行等）
- 支持自定义文件夹整理

---

## 🗺️ 开发路线图

### ✅ v1.0 MVP (当前版本)
- [x] 系统分享菜单集成
- [x] 剪贴板智能监听
- [x] 小红书/抖音/B站链接解析
- [x] 本地离线存储
- [x] 基础 Feed 流展示

### 🚧 v1.5 (计划中)
- [ ] AI 自动分类和标签
- [ ] YouTube/Reddit 官方 API 集成
- [ ] 内容全文搜索
- [ ] 视频播放优化

### 🔮 v2.0 (未来)
- [ ] AI 内容摘要
- [ ] OCR 图片文字搜索
- [ ] 跨设备云同步
- [ ] 桌面端应用

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 📮 联系方式

- GitHub Issues: [提交问题](https://github.com/reachlihang-afk/VibeBox/issues)
- 项目主页: [VibeBox](https://github.com/reachlihang-afk/VibeBox)

---

<div align="center">
  <p>用 ❤️ 打造 | Made with ❤️</p>
  <p>© 2026 VibeBox. All rights reserved.</p>
</div>
