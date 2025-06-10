---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code: Atlantis"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform", "鐵人賽2020", "iac", "aws"]
categories: ["kubernetes", "terraform"]
date: 2020-10-07T11:15:48+08:00
lastmod: 2020-10-07T11:15:48+08:00
featured: false
draft: false
---

This article is part of [從零開始的 Infrastructu as Code: Terraform]({{< ref "/posts/2020-06-14-terraform-infrastructure-as-code" >}})
- [Get-started examples / SOP on Github](https://github.com/chechiachang/terraform-playground)
- [Introducation to Terraform Iac: Speaker transcript]({{< ref "/posts/2020-06-15-terraform-infrastructure-as-code-transcript" >}})
- [Presentation](https://slides.com/chechiachang/terraform-introduction/edit)

Check my website [chechia.net](https://chechia.net) for other blog. [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch). Like my page if you really like it :)

---

# 需求與問題

隨著 terraform 在團隊內的規模持續成長，團隊需要讓工作流程更加順暢，來面對大量的 tf 變更查核與變更請求。想像幾十個工程師同時在修改幾十個不同的 terraform projects / modules，這時可能會有幾個問題

- 需要一個穩定乾淨的環境執行 terraform
  - 工程師的開發本機不是個好選擇
  - 需要 24/7 的 terraform 執行中心
    - 執行中心會有各個環境 (dev / stage / prod) 的存取權限，希望設置在內部
- 下列兩個工作會切換工作平台，例如 Github
  - review，檢視 difference，與討論
  - PR
- review 完有時會忘記 merge，merge 完有時會忘記 apply
  - repository 越多，忘得越多...

團隊已經導入 Git-flow，希望把工作流程做得更完整自動化更加便利

[Atlantis 解決方案](https://www.runatlantis.io/)是與版本控制整合，提供 terraform 執行的 worker，病可以與 Git Host (e.g. Github) 整合做 PR + Review，來達成持續的 CI/CD 遠端執行，自動 plan 與自動 apply merge。也就是 Atlantis 幫我們處理以下幾件事

- Git-flow
- TODO 自動化 plan
- TODO Webhook 回傳 plan 結果
- TODO 透過 bot 控制 apply
- TODO 自動 merge

# 需求與工作流程

以下的範例使用

- Github 作為版本控管工具
  - 是整個工作流程的控制中心
  - tf code，review，plan，apply 的結果都會在 Github
  - 進一步整合到 Slack 上也非常方便
- Atlantis 放在 Kubernetes 上
  - 使用 helm chart 部署

如果需要其他的版本控制工具或是安裝方式，請見[Atlantis 官方文件](https://www.runatlantis.io/docs/installation-guide.html)，Atlantis 支援非常多版本控制工具，例如 Github，Gitlab，Bitbucket，...等

整個工作流程

- Github commit push
  - Github event -> Atlantis webhook
  - Atlantis run terraform validate plan
- Github PR push
  - Github event -> Atlantis webhook
  - Atlantis run terraform validate plan
- Github Merge event / main branch push
  - Github event -> Atlantis webhook
  - Atlantis run terraform validate plan
  - Atlantis acquire access to site (dev / stage)
  - Atlantis apply to site
- Github release tag push (eg. 1.2.0-rc)
  - Github event -> Atlantis webhook
  - Atlantis run terraform validate plan
  - Atlantis acquire access to site (dev/stage)
  - Atlantis apply to site (release-candidate / prod)

依據上面的環境，安裝需要準備以下幾個東西
- Git
  - Git Host 上設定 Atlantis 存取 Git Repository 的權限
  - 為 Git Host 設定存取私鑰，讓 Atlantis 認證 webhook
- Terraform Backend State storage: Atlantis 需要存取外部的 state storage
- Terraform 使用的版本要注意一下。Atlantis 可以支援不同 repository / project 使用不同版本
- Environment credential (provider credential)
  - Atlantis 會需要存取不同的環境 (dev / stage / prod)
  - 為這些環境獨立配置 credential 讓 Atlantis 存取

實際 Atlantis 的環境會有

- Docker 作為孤城師本機開發測試使用
- Kubernetes Atlantis
  - 我們的團隊會是一個環境一個獨立的 Atlantis
    - 安全性：切分各個環境的權限與 Access
    - 各個 Atlantis webhook 只接收屬於自己的 event

### Docker

使用 Docker 作為本地開發與測試的容器 runtime：

```
docker pull runatlantis/atlantis:v0.15.0

docker run runatlantis/atlantis:v0.15.0 atlantis \
  --gh-user=GITHUB_USERNAME \
  --gh-token=GITHUB_TOKEN
```

### Helm Chart

Helm 的安裝十分簡易
```
helm repo add runatlantis https://runatlantis.github.io/helm-charts
helm inspect values runatlantis/atlantis > values.yaml
```

更改 values.yaml
```
github:
  user: chechiachang
  token: ...
  secret: ...

orgWhitelist: github.com/chechiachang/*
```

安裝到 Kubernetes 上

```
helm install atlantis runatlantis/atlantis -f values.yaml
```

# 結果

- 工程師透過 Github 就可以完成所有工作
  - 加上 Github Slack 整合，就完全不用離開 Slack，跟 bot 聊天就可以完成所有 terraform 工作
- 安全穩定的 terraform 執行環境
- 獨立的 in-cluster credential，集群的存取權限都控制在集群內，不會暴露到外部環境
- 自動 plan 與 apply，不會遺忘

# 優劣

優點

- 可以 self-hosted，credential 不外洩，確保最高的安全性
- 已經整合 Kubernetes, helm chart
- webhook 整合許多版本控制庫，例如 github, gitlab,...
- 實現安全的遠端執行
  - 本地執行還是會有諸多問題
  - terraform cloud 提供的遠端執行

缺點，其實沒什麼缺點

- 就需要多養一組 Atlantis
  - 使用 stateless deployment，其實是應該不會有什麼負擔

Terraform 系列至此應該是全部完結，感謝各位

