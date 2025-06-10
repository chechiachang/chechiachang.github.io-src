---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop ??: Integrated Storage"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-10-10T04:42:26+08:00
lastmod: 2023-10-10T04:42:26+08:00
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: false

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["internal-project"]` references `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects: []

tags: ["vault", "iac", "workshop", "docker", "terraform", "鐵人賽2023", "chatgpt"]
categories: ["vault", "docker"]
---

如果你希望追蹤最新的草稿，請見[鐵人賽2023](https://chechia.net/zh-hant/tag/%E9%90%B5%E4%BA%BA%E8%B3%BD2023/)

本 workshop 也接受網友的許願清單，[如果有興趣的題目可於第一篇底下留言](https://ithelp.ithome.com.tw/articles/10317378)，筆者會盡力實現，但不做任何保證

整篇 Workshop 會使用的範例與原始碼，放在 [Github Repository: vault-playground](http://chechia.net/zh-hant/#projects)

# Day ??: Integrated Backend

集成存儲

Vault 支援多種存儲選項，用於持久存儲 Vault 資訊。自 Vault 1.4 起，提供了整合式存儲選項。此存儲後端不依賴於任何第三方系統，實現高可用性語義，支援企業複製功能，並提供備份/還原工作流。

該選項將 Vault 的數據存儲在服務器的文件系統上，並使用共識協議將數據複製到集群中的每個服務器。有關整合式存儲內部的更多信息，請參閱整合式存儲內部文檔。此外，配置文檔可以幫助配置 Vault 以使用整合式存儲。

以下各節將詳細介紹如何使用整合式存儲操作 Vault。

服務器間通信
一旦節點加入到彼此，它們開始使用 Vault 的叢集端口進行 mTLS 通信。叢集端口的默認值為 8201。TLS 信息在加入時交換，並按一定的節奏進行輪換。

整合式存儲的要求之一是必須設置 cluster_addr 配置選項。這允許 Vault 在加入時為節點 ID 分配地址。

叢集成員資格
本節將概述如何引導和管理運行整合式存儲的 Vault 節點集群。

整合式存儲在初始化過程中引導，並且結果是大小為 1 的集群。根據所需的部署大小，可以將節點加入到活動 Vault 節點中。

加入節點
加入是將未初始化的 Vault 節點並使其成為現有集群成員的過程。為了將新節點驗證到集群，它必須使用相同的密封機制。如果使用自動解封，則必須配置新節點以使用與其嘗試加入的集群相同的 KMS 提供程序和密鑰。如果使用 Shamir 密封，則必須在加入過程完成之前為新節點提供解封密鑰。一旦節點成功加入，來自活動節點的數據就可以開始複制到它。一旦節點加入，則不能重新加入到不同的集群。

您可以通過配置文件自動加入節點，也可以通過 API 手動加入（下面描述了這兩種方法）。在加入節點時，必須使用領導節點的 API 地址。我們建議在所有節點上設置 api_addr 配置選項，以使加入過程更簡單。

retry_join 配置
此方法允許在配置文件中設置一個或多個目標領導節點。當未初始化的 Vault 服務器啟動時，它將嘗試加入每個已定義的潛在領導者，直到成功。當指定的領導者之一變為活動狀態時，此節點將成功加入。當使用 Shamir 密封時，已加入的節點仍然需要手動解封。當使用自動解封時，節點將能夠自動加入並自動解封。

下面是一個示例 retry_join 配置：

```bash
storage "raft" {
  path    = "/var/raft/"
  node_id = "node3"

  retry_join {
    leader_api_addr = "https://node1.vault.local:8200"
  }
  retry_join {
    leader_api_addr = "https://node2.vault.local:8200"
  }
}
```

```bash
storage "raft" {
  path    = "/var/raft/"
  node_id = "node3"

  retry_join {
    auto_join = "provider=aws region=eu-west-1 tag_key=vault tag_value=... access_key_id=... secret_access_key=..."
  }
}
```

### chatGPT

本段部分內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/docs/concepts/integrated-storage
內容，並由筆者人工校驗

base context
```
我希望你能充當一名繁體中文翻譯，拼寫修正者和改進者。我將用英文與程式語言與你對話，你將翻譯它，並以已糾正且改進的版本回答，以繁體中文表達。我希望你能用更美麗和優雅、高級的繁體中文詞語和句子替換我簡化的詞語和句子。保持意義不變。我只希望你回答糾正和改進，不要寫解釋。

很重要：不要使用敬語，翻譯結果中若出現"您"，請用"你"取代"您"。
```

result correction
```
部分英文內容為專有名詞，產生的繁體中文翻譯結果中，這些名詞維持英文，不需要翻譯成中文：key，value，certificate，token，policy，policy rule，path，path-based，key rolling，audit，audit trail，plain text，key value，Consul，S3 bucket，Leasing，Renewal，binary，prefix，instance，metadata。

修正下列翻譯：將 "數據" 改為 "資料"，將 "數據庫" 改為 "資料庫"，將 "數據" 改為 "資料"，將 "訪問" 改為 "存取"，將 "源代碼" 改為 "原始碼"，將 "信息" 改為 "資訊"，將 "命令" 改為 "指令"，將 "禁用" 改為 "停用"，將 "默認" 改為 "預設"。
```

