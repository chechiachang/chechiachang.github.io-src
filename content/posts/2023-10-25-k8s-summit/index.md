---
title: "Kubernetes Summit: Resource as Code for Kubernetes: Stop kubectl apply"
date: 2023-10-25T13:20:00Z
# weight: 1
# aliases: ["/test"]
tags: ["vault", "iac", "aws", "terraform", "kubernetes"]
description: "將 k8s resource 以 code 管理，推上 VCS，並使用 ArgoCD、Secret Operator 等工具進行管理，以避免人工操作錯誤，降低團隊整體失誤率與管理成本，提升效率。"
#canonicalURL: "https://canonical.url/to/page"

showToc: true
TocOpen: false
#UseHugoToc: true

draft: false

hidemeta: false
comments: true
disableHLJS: false

hideSummary: false
ShowReadingTime: true
ShowBreadCrumbs: true
ShowPostNavLinks: true
ShowWordCount: true
ShowRssButtonInSectionTermList: true

searchHidden: false
disableShare: false

#cover:
#    image: "" # image path/url
#    alt: "" # alt text
#    caption: "" # display caption under cover
#    relative: false # when using page bundles set this to true
#    hidden: false # only hide on current single page
---

- 活動時間: 2023-10-25T13:20:00Z
- [活動連結](https://k8s.ithome.com.tw/2023/session-page/2331)
- [Facebook](https://www.facebook.com/engineer.from.scratch)
- [Twitter](https://twitter.com/chechiachang)
- [投影片](../../slides/2023-10-25-k8s-resource-as-code)

---

## Info

Title: Resource as Code for Kubernetes: stop kubectl apply

https://k8s.ithome.com.tw/CFP

Infrastrure as Code (IaC) 與 PaC，在萬物都該 as Code 得時代，你還在不斷的 kubectl apply 嗎？

## 手動 apply 的痛點：

- 人就是會忘：是誰 apply 這個在 k8s 上的？是誰上次漏 apply 所以壞了？
- 人就是會寫錯：能否 apply 
- 管理大量的 label, taint, annotation
- 安全：apply 變更內容是否有經過資訊安全的 review

當服務的 app code base 都已經用 chart 打包，使用 vcs 管理後，為何依賴的 k8s resource (namespace, secret, label, crd, ...) 不需要推上 vcs 管理的？

本次演講集合幾個管理 k8s 的範例，將 k8s resource 以 code 管理，推上 vcs，並使用 argoCD, secret operator, ... 等工具進行管理，來讓避免低級的人工操作錯誤，降低團隊整體失誤率，並降低 k8s admin 管理的成本，提高管理效率

## target group

Kubernetes User who want to increase performance in k8s management
