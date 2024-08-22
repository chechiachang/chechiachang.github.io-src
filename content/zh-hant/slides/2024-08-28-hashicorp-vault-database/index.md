---
title: "Hashicorp: managed database credentials with Hashicorp Vault"
summary: 分享如何使用 Hashicorp Vault 管理資料庫的帳號密碼，並透過 AWS IAM Role 與 Kubernetes Service Account 進行驗證，以及如何連線到資料庫，監控與審查。
authors: []
tags: ["kubernetes"]
categories: ["kubernetes"]
date: '2024-08-20T11:00:00Z'
slides:
  # Choose a theme from https://github.com/hakimel/reveal.js#theming
  #theme: black
  theme: white
  # Choose a code highlighting style (if highlighting enabled in `params.toml`)
  #   Light style: github. Dark style: dracula (default).
  highlight_style: dracula
---

{{< slide background-image="onepiece.png" >}}

{{% speaker_note %}}
投影片跟講稿我都放在我的網站上，如果有興趣可以參考
{{% /speaker_note %}}

---

### Managed Database Credentials
### with Hashicorp Vault

[Che Chia Chang](https://chechia.net/)

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 關於我

- Che Chia Chang
- SRE @ [Maicoin](https://www.linkedin.com/company/maicoin/jobs/)
- [Microsoft MVP](https://mvp.microsoft.com/zh-TW/MVP/profile/e407d0b9-5c01-eb11-a815-000d3a8ccaf5)
- 個人部落格[chechia.net](https://chechia.net/)
- presentation and speaker notes
- [從零開始學Vault手把手入門](https://ithelp.ithome.com.tw/users/20120327/ironman/6764)
- [2023 Vault 雲端的端通吃的私要管理平台](https://chechia.net/zh-hant/talk/hashicorp-vault-on-aws-k8s-%E9%9B%B2%E7%AB%AF%E5%9C%B0%E7%AB%AF%E9%80%9A%E5%90%83%E7%9A%84%E7%A7%81%E9%91%B0%E7%AE%A1%E7%90%86%E5%B9%B3%E5%8F%B0/)

---

### 大綱

- database 帳號密碼管理的難題
- 簡介 Vault 與 database secret engine
- 在 vault 中設定 database secret engine
- vault 在需要時自動產生資料庫帳號密碼
- vault 透過安全來源認證 app 身份(使用 k8s service account 與 public cloud 認證(aws iam role))
- 完成 app 連線至 database 的工作週期
- monitoring / audit：vault audit log + prometheus / grafana dashboard / alert manager
- 範例：如何使用 terraform 設定 vault 與 database secret engine

{{% speaker_note %}}
{{% /speaker_note %}}

---

### 參考資料

- https://developer.hashicorp.com/vault/docs/secrets/databases

