---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "從零開始的 Infrastructure as Code: Terraform - 01"
subtitle: "Infrastucture as Code: introduce Terraform from scratch"
summary: ""
authors: []
tags: ["kubernetes", "terraform", "devops"]
categories: ["kubernetes", "terraform"]
date: 2020-06-14T16:46:09+08:00
lastmod: 2020-06-14T16:46:09+08:00
featured: false
draft: false

menu:
  main:
    parent: "Kubernetes"
    weight: 1
---

This article is part of [從零開始的 Infrastructu as Code: Terraform]({{< ref "/post/2020-06-14-terraform-infrastructure-as-code" >}})
- [Get-started examples / SOP on Github](https://github.com/chechiachang/terraform-playground)
- [Introducation to Terraform Iac: Speaker transcript]({{< ref "/post/2020-06-15-terraform-infrastructure-as-code-transcript" >}})
- [Presentation](https://slides.com/chechiachang/terraform-introduction/edit)

Check my website [chechia.net](https://chechia.net) for other blog. [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch). Like my page if you really like it :)

---

# Outlline

- our story: issues, steps, & results
- basics IaC, terraform
- benefits
- risks and 坑
- to be or not to be

experience oriented

# Our stories

- 100+ devs, many teams
- 25+ projects
- 50+ GKEs
- 80+ SQLs
- IAMs, redis, VPCs, load-balancers, ...

# Issues

- Ops manually create resources through GUI by SOP.
- We have many isolated, separeated resources, VPCs. It's our culture, and we (devops) want to change.
- Some projects have short life-cycle. Rapid resources created & destroy.

# Our user story

As a devops,
I would like to introduce terraform (IaC)
so that I can
- review all existing resources
- minimize error from manual operation
- ASAP!!

As a devops,
I would like to fully enforce terraform (IaC)
so that I can
- minimize efforts to operate infra
- delegate infra operations to junior team members
- minimize IAM privilges

# Introduction

1. import existing resources
1. review existing resources code
1. plan best practice resource templates
1. create new resources with templates
1. introduce git workflow, plan, commit, PR, and review
1. add wrapper handler
1. automation pipeline
1. repeat 2-4

# IaC

- Programatic way to operate infra
- declarative (functional) vs. imperative (procedural) 
- Perfect for public cloud, cloud native, virtualized resources
- Benefits: cost (reduction), speed (faster execution) and risk (remove errors and security violations)

# Terraform

[Terraform](https://www.terraform.io/)

- Declarative (functional) IaC
- Invoke API delegation
- State management
- providers: azure / aws / gcp /alicloud / ...

# Demo

https://github.com/chechiachang/terraform-playground

# Scope

- Compute Instances
- Kubernetes
- Databases

- IAM
- Networking
- Load Balancer

# Expected benefits

- Minimize manual operation.
- Zero manual operation error
  - Standarized infra. Infra as a (stable) product.
- fast, really fast to duplicate envs

- Infra workflow with infra review
  - Easy to create identical dev, staging, prod envs
  - Reviewed infra. Better workflow. Code needs reviews, so do infra.
- Fully automized infra pipeline.

# Other Benefits

- Don't afraid to change prod sites anymore
  - We made a massive infra migration in this quater!!
- Better readability to GUI. Allow comment everywhere.

# Risks

- Incorrect usage could cause massive destruction.
  - 如果看見 destroy 的提示，請雙手離開鍵盤。 ~ first line in our SOP
  - If see "destroy", cancel operation & call for help.
- State management
- A little latency between infra version and terraform provider version

# Reduce Risks

- Sufficient understanding to infra & terraform
- Sufficient training to juniors
- Minimize IAM privilege: remove update / delete permissions

# Git-flow

[Our SOP](https://github.com/chechiachang/terraform-playground/blob/master/SOP.md)

- edit tf
- push new branch commit
- PR, review & discussion
- merge & apply
- revert to previous tag if necessary

# (Utility) Provide template

- wrap resources for
  - better accesibility
  - lower operation risks
  - uniform naming convention
  - best practice
  - suggested default value

# About introducing new tool

- The hardest part is always people
  - Focus on critical issues (痛點) instead of tool itself. "We introduce tool to solve..."
  - Put result into statistics "The outage due to misconfig is reduced by..."

# Overall, my IaC experience is GREAT!

- IaC to automation.
- Comment (for infra) is important. You have to write doc anyway. Why not put in IaC?

# Q&A

- [Full transcript]()
- [Presentation file]()
- [Source Code on Github](https://github.com/chechiachang/chechiachang.github.io-src/blob/master/content/post/terraform-infrastructure-as-code/index.md)
- [chechia.net](https://chechia.net) <- full contents
- [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch)
  - Like it if you really like it :)

# Appendix.I more about terraform

terraform validate
terraform import
terraform module
terraform cloud & state management

# Appendix.I understand State conflict

- Shared but synced
- watch out for state conflicts when colaborating
  - state diff. could cause terraform mis-plan
- Solution: synced state lock
  - Colatorative edit (git branch & PR), synchronized terraform plan & apply
  - or better: automation


# Appendix.II understand resources from API aspect

GCP Load Balancer

### GCP Load Balancing

- understand resources from API aspect
  - how terraform work with GCP API

- internal
  - regional
    - pass-through: tcp / udp   -> internal TCP/UDP
    - proxy: http / https       -> internal HTTP(S)
- external
  - regional
    - pass-through: tcp / udp   -> tcp/udp network
  - global / effective regional
    - proxy
      - tcp                     -> TCP Proxy
      - ssl                     -> SSL Proxy
      - http / https            -> External HTTP(S)

### Terraform Resource

- forwarding_rule
  - forwarding_rule: tcp & http
  - global_forwarding_rule: only http

- backend_service
  - backend_service
    - health_check
    - http_health_check
    - https_health_check
  - region_backend_service
    - region_health_check
    - region_http_health_check
    - region_https_health_check

# Some ways to do IaC

- Cloud Formation
- bash script with API / client

# 引言 Infrastructure as Code

從字面上解釋，IaC 就是用程式碼描述 infrastructure。那為何會出現這個概念？

如果不 IaC 是什麼狀況？我們還是可以透過 GUI 或是 API 操作。隨叫隨用

雲端運算風行，工程師可以很在 GUI 介面上，很輕易的部署資料中心的架構。輸入基本資訊，滑鼠點個一兩下，就可以在遠端啟用運算機器，啟用資料庫，設置虛擬網路與路由，幾分鐘就可以完成架設服務的基礎建設(infrastructure)，開始運行服務。

然而隨著
- 雲平台提供更多新的（複雜的）服務
  - 服務彼此可能是有相依性（dependency），服務需要仰賴其他服務
  - 或是動態耦合，更改服務會連動其他服務，一髮動全身
- 需要縝密的存取控管（access control）
  - 防火牆，路由規則
  - 雲平台上，團隊成員的存取權限
- 專案的規模與複雜度增加
  - 多環境的部署
  - 多個備援副本設定
  - 大量機器形成的集群

# IaC 的實際需求

以下這些對話是不是很耳熟？

# IaC 的實際需求

沒有需求，就不需要找尋新的解決方案。

有看上面目錄的朋友，應該知道這系列文章的後面，我會實際分享於公司內部導入 Terraform 與 IaC 方法的過程。

各位讀者會找到這篇文，大概都是因為實際搜尋了 Terraform 或是 IaC 的關鍵字才找到這篇。

如果沒有需求，自己因為覺得有趣而拉下來研究，

如果沒有明確需求，就貿然導入
無謂增加亂度

# IaC 的實現工具

# 為何選擇 Terraform 

# 建議

1. 如果不熟，從 import 現有最好的資源開始。把 70 分保住，再向 80 90 邁進。
1. 善用 module 封裝，只露出會用到的參數。
