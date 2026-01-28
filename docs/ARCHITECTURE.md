# VibeBox 技术架构文档

**版本**: v1.0  
**更新日期**: 2026-01-28

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                     用户界面层                           │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Flutter Mobile App                     │  │
│  │  ┌────────────┐  ┌────────────┐                 │  │
│  │  │ iOS Share  │  │  Android   │                 │  │
│  │  │ Extension  │  │  Intent    │                 │  │
│  │  └────────────┘  └────────────┘                 │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    业务逻辑层                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  剪贴板监听  │  │  链接解析    │  │  下载管理    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  AI 分类     │  │  媒体播放    │  │  搜索引擎    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   数据存储层                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   SQLite     │  │  File System │  │  Hive Cache  │  │
│  │  (元数据)    │  │  (媒体文件)  │  │  (配置)      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  外部服务层 (可选)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  链接解析API │  │  AI 服务     │  │  官方 API    │  │
│  │  (FastAPI)   │  │  (OpenAI)    │  │  (YouTube)   │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 二、移动端架构 (Flutter)

### 2.1 项目结构

```
mobile/
├── lib/
│   ├── main.dart                    # 应用入口
│   │
│   ├── core/                        # 核心功能
│   │   ├── database/
│   │   │   ├── database_helper.dart
│   │   │   └── models.dart
│   │   ├── network/
│   │   │   ├── api_client.dart
│   │   │   └── link_parser.dart
│   │   └── utils/
│   │       ├── constants.dart
│   │       └── helpers.dart
│   │
│   ├── models/                      # 数据模型
│   │   ├── bookmark.dart
│   │   ├── media_file.dart
│   │   └── tag.dart
│   │
│   ├── services/                    # 业务逻辑
│   │   ├── clipboard_monitor.dart   # 剪贴板监听
│   │   ├── download_manager.dart    # 下载管理
│   │   ├── link_parser_service.dart # 链接解析
│   │   └── sync_service.dart        # 同步服务
│   │
│   ├── screens/                     # 页面
│   │   ├── home/
│   │   │   ├── home_screen.dart
│   │   │   └── feed_list.dart
│   │   ├── detail/
│   │   │   └── detail_screen.dart
│   │   ├── settings/
│   │   │   └── settings_screen.dart
│   │   └── onboarding/
│   │       └── onboarding_screen.dart
│   │
│   └── widgets/                     # 通用组件
│       ├── bookmark_card.dart
│       ├── video_player.dart
│       └── quick_add_dialog.dart
│
├── ios/
│   ├── Runner/
│   └── ShareExtension/              # iOS 分享扩展
│       ├── ShareViewController.swift
│       └── Info.plist
│
├── android/
│   └── app/
│       ├── src/main/
│       │   ├── AndroidManifest.xml
│       │   └── kotlin/
│       │       └── ShareActivity.kt # Android 分享处理
│       └── build.gradle
│
└── pubspec.yaml                     # 依赖配置
```

### 2.2 核心依赖

```yaml
dependencies:
  flutter:
    sdk: flutter
  
  # 数据库
  sqflite: ^2.3.0
  path: ^1.8.3
  
  # 轻量存储
  hive: ^2.2.3
  hive_flutter: ^1.1.0
  
  # 网络请求
  dio: ^5.4.0
  http: ^1.1.0
  
  # 状态管理
  provider: ^6.1.1
  riverpod: ^2.4.9
  
  # UI 组件
  cached_network_image: ^3.3.0
  flutter_staggered_grid_view: ^0.7.0
  
  # 视频播放
  video_player: ^2.8.1
  chewie: ^1.7.4
  
  # 工具
  url_launcher: ^6.2.2
  share_plus: ^7.2.1
  permission_handler: ^11.1.0
  
  # 剪贴板
  clipboard: ^0.1.3
  
  # 下载
  flutter_downloader: ^1.11.5
```

### 2.3 数据流

```
用户操作 (分享/复制)
    ↓
ShareExtension / ClipboardMonitor
    ↓
LinkParserService.parse(url)
    ↓
DownloadManager.enqueue(content)
    ↓
DatabaseHelper.insert(bookmark)
    ↓
UI 更新 (Provider/Riverpod)
```

---

## 三、iOS Share Extension

### 3.1 配置文件

```xml
<!-- Info.plist -->
<key>NSExtension</key>
<dict>
    <key>NSExtensionAttributes</key>
    <dict>
        <key>NSExtensionActivationRule</key>
        <dict>
            <key>NSExtensionActivationSupportsText</key>
            <true/>
            <key>NSExtensionActivationSupportsWebURLWithMaxCount</key>
            <integer>1</integer>
        </dict>
    </dict>
    <key>NSExtensionMainStoryboard</key>
    <string>MainInterface</string>
    <key>NSExtensionPointIdentifier</key>
    <string>com.apple.share-services</string>
</dict>
```

### 3.2 核心代码

```swift
// ShareViewController.swift
import UIKit
import Social

class ShareViewController: SLComposeServiceViewController {
    
    override func isContentValid() -> Bool {
        return true
    }
    
    override func didSelectPost() {
        if let item = extensionContext?.inputItems.first as? NSExtensionItem {
            processSharedContent(item)
        }
        
        self.extensionContext?.completeRequest(returningItems: [], completionHandler: nil)
    }
    
    func processSharedContent(_ item: NSExtensionItem) {
        guard let attachments = item.attachments else { return }
        
        for attachment in attachments {
            if attachment.hasItemConformingToTypeIdentifier("public.url") {
                attachment.loadItem(forTypeIdentifier: "public.url") { (url, error) in
                    if let shareURL = url as? URL {
                        self.saveToVibeBox(url: shareURL.absoluteString)
                    }
                }
            }
        }
    }
    
    func saveToVibeBox(url: String) {
        // 使用 App Groups 共享数据
        let sharedDefaults = UserDefaults(suiteName: "group.com.vibebox.shared")
        var pendingItems = sharedDefaults?.array(forKey: "pendingItems") as? [[String: Any]] ?? []
        
        pendingItems.append([
            "url": url,
            "timestamp": Date().timeIntervalSince1970
        ])
        
        sharedDefaults?.set(pendingItems, forKey: "pendingItems")
        
        // 通知主应用
        CFNotificationCenterPostNotification(
            CFNotificationCenterGetDarwinNotifyCenter(),
            CFNotificationName("com.vibebox.newShare" as CFString),
            nil, nil, true
        )
    }
}
```

---

## 四、Android Intent Filter

### 4.1 Manifest 配置

```xml
<!-- AndroidManifest.xml -->
<activity
    android:name=".ShareActivity"
    android:label="保存到 VibeBox"
    android:theme="@style/Theme.Transparent"
    android:exported="true">
    
    <intent-filter>
        <action android:name="android.intent.action.SEND" />
        <category android:name="android.intent.category.DEFAULT" />
        <data android:mimeType="text/plain" />
    </intent-filter>
    
</activity>
```

### 4.2 核心代码

```kotlin
// ShareActivity.kt
class ShareActivity : AppCompatActivity() {
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        when {
            intent?.action == Intent.ACTION_SEND -> {
                if (intent.type == "text/plain") {
                    handleTextShare(intent)
                }
            }
        }
        
        finish()
    }
    
    private fun handleTextShare(intent: Intent) {
        val sharedText = intent.getStringExtra(Intent.EXTRA_TEXT)
        if (sharedText != null) {
            saveToVibeBox(sharedText)
        }
    }
    
    private fun saveToVibeBox(url: String) {
        val sharedPref = getSharedPreferences("vibebox_shared", Context.MODE_PRIVATE)
        val pendingItems = sharedPref.getStringSet("pendingItems", mutableSetOf()) ?: mutableSetOf()
        
        pendingItems.add(url)
        
        with(sharedPref.edit()) {
            putStringSet("pendingItems", pendingItems)
            apply()
        }
        
        // 启动后台服务
        val serviceIntent = Intent(this, SyncService::class.java)
        startService(serviceIntent)
        
        Toast.makeText(this, "已保存到 VibeBox", Toast.LENGTH_SHORT).show()
    }
}
```

---

## 五、后端服务架构 (FastAPI)

### 5.1 项目结构

```
backend/
├── main.py                 # FastAPI 主文件
├── config.py              # 配置文件
├── requirements.txt       # 依赖
│
├── parsers/               # 链接解析器
│   ├── __init__.py
│   ├── base.py           # 基类
│   ├── xiaohongshu.py    # 小红书解析器
│   ├── douyin.py         # 抖音解析器
│   ├── bilibili.py       # B站解析器
│   └── weibo.py          # 微博解析器
│
├── models/               # 数据模型
│   └── content.py
│
└── utils/                # 工具函数
    ├── http_client.py
    └── helpers.py
```

### 5.2 核心 API

```python
# main.py
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from parsers import get_parser

app = FastAPI(title="VibeBox Link Parser API")

class ParseRequest(BaseModel):
    url: str
    user_id: str

class ParseResponse(BaseModel):
    status: str
    task_id: str
    message: str

@app.post("/api/parse", response_model=ParseResponse)
async def parse_link(request: ParseRequest, background_tasks: BackgroundTasks):
    """解析分享链接"""
    task_id = generate_task_id()
    
    background_tasks.add_task(
        parse_and_notify,
        url=request.url,
        user_id=request.user_id,
        task_id=task_id
    )
    
    return ParseResponse(
        status="processing",
        task_id=task_id,
        message="正在解析内容..."
    )

async def parse_and_notify(url: str, user_id: str, task_id: str):
    """后台解析任务"""
    parser = get_parser(url)
    content = await parser.parse(url)
    
    # 通知客户端（通过 WebSocket 或推送）
    await notify_client(user_id, task_id, content)
```

### 5.3 解析器基类

```python
# parsers/base.py
from abc import ABC, abstractmethod
import httpx
from bs4 import BeautifulSoup

class BaseParser(ABC):
    """链接解析器基类"""
    
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'
            },
            timeout=30.0
        )
    
    @abstractmethod
    async def parse(self, url: str) -> dict:
        """解析链接，返回内容数据"""
        pass
    
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """判断是否能处理该链接"""
        pass
    
    async def fetch_page(self, url: str) -> str:
        """获取页面内容"""
        response = await self.client.get(url, follow_redirects=True)
        return response.text
    
    def extract_meta(self, html: str) -> dict:
        """提取 meta 标签信息"""
        soup = BeautifulSoup(html, 'html.parser')
        
        return {
            'title': self._get_meta(soup, 'og:title'),
            'description': self._get_meta(soup, 'og:description'),
            'image': self._get_meta(soup, 'og:image'),
        }
    
    def _get_meta(self, soup, property: str) -> str:
        tag = soup.find('meta', property=property)
        return tag['content'] if tag else ''
```

---

## 六、数据库设计

### 6.1 SQLite Schema

```sql
-- 收藏内容表
CREATE TABLE bookmarks (
    id TEXT PRIMARY KEY,
    url TEXT NOT NULL UNIQUE,
    title TEXT,
    description TEXT,
    platform TEXT NOT NULL,
    author TEXT,
    thumbnail_path TEXT,
    content_type TEXT,  -- video, image, article
    created_at INTEGER NOT NULL,
    saved_at INTEGER NOT NULL,
    is_offline_ready INTEGER DEFAULT 0,
    is_read INTEGER DEFAULT 0
);

CREATE INDEX idx_bookmarks_platform ON bookmarks(platform);
CREATE INDEX idx_bookmarks_saved_at ON bookmarks(saved_at DESC);

-- 媒体文件表
CREATE TABLE media_files (
    id TEXT PRIMARY KEY,
    bookmark_id TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_type TEXT NOT NULL,  -- image, video
    file_size INTEGER,
    mime_type TEXT,
    downloaded_at INTEGER,
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE
);

CREATE INDEX idx_media_bookmark ON media_files(bookmark_id);

-- 标签表
CREATE TABLE tags (
    id TEXT PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    color TEXT,
    created_at INTEGER NOT NULL
);

-- 内容-标签关联表
CREATE TABLE bookmark_tags (
    bookmark_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    PRIMARY KEY (bookmark_id, tag_id),
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- 下载队列表
CREATE TABLE download_queue (
    id TEXT PRIMARY KEY,
    bookmark_id TEXT NOT NULL,
    url TEXT NOT NULL,
    status TEXT NOT NULL,  -- pending, downloading, completed, failed
    progress INTEGER DEFAULT 0,
    error_message TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY (bookmark_id) REFERENCES bookmarks(id) ON DELETE CASCADE
);

CREATE INDEX idx_queue_status ON download_queue(status);
```

---

## 七、安全与隐私

### 7.1 数据加密

- 本地数据库使用 SQLCipher 加密
- 敏感配置使用 Flutter Secure Storage
- 媒体文件存储在应用沙盒内

### 7.2 网络安全

- 所有 HTTP 请求使用 HTTPS
- API 请求添加签名验证
- 防止中间人攻击

### 7.3 隐私保护

- 不收集用户个人信息
- 剪贴板监听需要用户授权
- 数据不上传到云端（除非用户开启云同步）

---

## 八、性能优化

### 8.1 启动优化

- 延迟加载非关键模块
- 预加载常用数据
- 使用 Isolate 处理耗时任务

### 8.2 列表优化

- 使用 ListView.builder 懒加载
- 图片缓存和预加载
- 分页加载数据

### 8.3 下载优化

- 断点续传
- 并发下载控制
- WiFi/流量智能切换

---

## 九、监控与日志

### 9.1 错误追踪

- 集成 Sentry 或 Firebase Crashlytics
- 记录关键操作日志
- 用户反馈收集

### 9.2 性能监控

- 启动时间
- 页面加载时间
- 网络请求耗时
- 内存使用情况

---

<div align="center">
  <p><strong>VibeBox 技术架构 v1.0</strong></p>
</div>
