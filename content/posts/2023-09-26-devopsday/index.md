---
title: "DevOpsDay: HashiCorp Vault 自建金鑰管理最佳入坑姿勢"
date: 2023-09-26T13:20:00Z
# weight: 1
# aliases: ["/test"]
tags: []
description: "從導入 HashiCorp Vault 作為起點，直接提供實務上經驗，分享建議的入坑設定"
#canonicalURL: "https://canonical.url/to/page"

showToc: true
TocOpen: true
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

- 活動時間: 2023-09-26T13:20:00Z
- [活動連結](https://devopsdays.tw/2023/session-page/2279)
- [Facebook](https://www.facebook.com/engineer.from.scratch)
- [Twitter](https://twitter.com/chechiachang)
- [投影片](../../slides/2023-09-26-devopsday-2023-vault)

---

## HashiCorp Vault 自建金鑰管理最佳入坑姿勢

本次演講從導入 HashiCorp Vault 作為起點，直接提供實務上經驗，分享建議的設定與路上可能有的雷。

- Vault 入坑的困難
- Vault + Terraform 一入坑就 IaC
- mount path + role + policy 命名與管理
- 升級與維護
- 會依據企業需求提供實際用例 demo，當天提供 github code example

中階
- 預期聽眾是有 Vault 使用經驗，希望能更有效率管理 Vault 的人
- 不會講太多基本功能介紹 vault 介紹
