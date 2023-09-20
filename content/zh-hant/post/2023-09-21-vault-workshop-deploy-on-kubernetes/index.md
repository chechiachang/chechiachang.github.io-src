---
# Documentation: https://wowchemy.com/docs/managing-content/

title: "Vault Workshop 10: Deploy with Docker"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2023-09-14T04:42:26+08:00
lastmod: 2023-09-14T04:42:26+08:00
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

# Day 09: Deploy with Docker

### Local with Docker

### minikube

```
r=https://api.github.com/repos/kubernetes/minikube/releases
curl -LO $(curl -s $r | grep -o 'http.*download/v.*beta.*/minikube-darwin-arm64' | head -n1)
sudo install minikube-darwin-arm64 /usr/local/bin/minikube
```

### 如何選擇 VM or Docker or Kubernetes

假議題

### chatGPT

本段部分內容使用 chatGPT-3.5 翻譯
https://developer.hashicorp.com/vault/docs/install
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

