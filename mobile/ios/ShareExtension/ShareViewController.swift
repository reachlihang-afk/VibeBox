import UIKit
import Social
import MobileCoreServices

class ShareViewController: SLComposeServiceViewController {
    
    override func isContentValid() -> Bool {
        return true
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.placeholder = "正在保存到 VibeBox..."
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
            // 处理 URL 类型
            if attachment.hasItemConformingToTypeIdentifier(kUTTypeURL as String) {
                attachment.loadItem(forTypeIdentifier: kUTTypeURL as String) { (url, error) in
                    if let shareURL = url as? URL {
                        self.saveToVibeBox(url: shareURL.absoluteString)
                    }
                }
            }
            
            // 处理文本类型（可能包含链接）
            if attachment.hasItemConformingToTypeIdentifier(kUTTypeText as String) {
                attachment.loadItem(forTypeIdentifier: kUTTypeText as String) { (text, error) in
                    if let shareText = text as? String {
                        self.extractAndSaveURL(from: shareText)
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
            "timestamp": Date().timeIntervalSince1970,
            "type": "link"
        ])
        
        sharedDefaults?.set(pendingItems, forKey: "pendingItems")
        
        // 发送通知给主应用
        CFNotificationCenterPostNotification(
            CFNotificationCenterGetDarwinNotifyCenter(),
            CFNotificationName("com.vibebox.newShare" as CFString),
            nil, nil, true
        )
    }
    
    func extractAndSaveURL(from text: String) {
        // 使用正则表达式提取 URL
        let detector = try? NSDataDetector(types: NSTextCheckingResult.CheckingType.link.rawValue)
        let matches = detector?.matches(in: text, options: [], range: NSRange(location: 0, length: text.utf16.count))
        
        if let match = matches?.first, let range = Range(match.range, in: text) {
            let url = String(text[range])
            saveToVibeBox(url: url)
        }
    }
    
    override func configurationItems() -> [Any]! {
        return []
    }
}
