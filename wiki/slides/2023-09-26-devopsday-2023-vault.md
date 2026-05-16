# DevOpsDay: HashiCorp Vault 自建金鑰管理最佳入坑姿勢

- Source: `content/slides/2023-09-26-devopsday-2023-vault/_index.md`
- Slide: `https://chechia.net/slides/2023-09-26-devopsday-2023-vault/`
- Date: `2023-09-21T00:00:00Z`
- Tags: `vault, terraform, iac, kubernetes`
- Categories: `vault, terraform, kubernetes`
- Description: `從導入 HashiCorp Vault 作為起點，直接提供實務上經驗，分享建議的入坑設定`

## Pages (Section | Summary)

1. `(frontmatter)` | Frontmatter metadata for reveal-hugo settings and slide metadata.
2. `(frontmatter)` | Q1: 有過使用 hashicorp vault 的人請舉手
3. `HashiCorp Vault` | HashiCorp Vault
4. `(frontmatter)` | About Me
5. `Outline` | Outline
6. `Vault 基礎的學習資源` | Vault 基礎的學習資源
7. `production deploy checklist` | production deploy checklist
8. `Infrastructure as Code` | Infrastructure as Code
9. `如何開始 IaC for Vault` | 如何開始 IaC for Vault
10. `(frontmatter)` | https://www.terraform.io/
11. `Deploy on public cloud` | Deploy on public cloud
12. `Deploy terraform-aws-vault` | Deploy terraform-aws-vault
13. `terraform-aws-vault` | terraform-aws-vault
14. `terraform-aws-vault` | terraform-aws-vault
15. `terraform-aws-vault-starter` | terraform-aws-vault-starter
16. `Integrated storage` | Integrated storage
17. `On Kubernetes` | On Kubernetes
18. `Deploy On Kubernetes` | Deploy On Kubernetes
19. `回到 Outline: prod-ready` | 回到 Outline: prod-ready
20. `Vault Configuration IaC` | Vault Configuration IaC
21. `hashicorp official tutorial` | hashicorp official tutorial
22. `hashicorp official tutorial` | hashicorp official tutorial
23. `How to use` | How to use
24. `VCS & PR review` | VCS & PR review
25. `Multiple environment` | Multiple environment
26. `Test` | Test
27. `Test Example` | Test Example
28. `Policy as code for vault` | Policy as code for vault
29. `Gitflow & automation` | Gitflow & automation
30. `Summary` | Summary
31. `Questions?` | Questions?

## Time-to-Syntax

- Markdown:
- `p3:link`
- `p4:image`
- `p4:link`
- `p6:link`
- `p7:link`
- `p10:image`
- `p10:link`
- `p12:image`
- `p12:link`
- `p13:link`
- `p14:image`
- `p14:link`
- `p15:link`
- `p16:link`
- `p17:link`
- `p18:image`
- `p18:link`
- `p21:code-fence`
- `p21:link`
- `p22:code-fence`
- `p22:link`
- `p23:code-fence`
- `p24:link`
- `p27:code-fence`
- `p27:link`
- `p28:link`
- `p29:link`
- Hugo shortcode:
- `p2:{{< slide background-image="onepiece.jpg" >}}`
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{< slide background-image="background.jpg" >}}`
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p5:{{< slide background-image="background.jpg" >}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p13:{{% note %}}`
- `p13:{{% /note %}}`
- `p14:{{% note %}}`
- `p14:{{% /note %}}`
- `p15:{{% note %}}`
- `p15:{{% /note %}}`
- `p16:{{% note %}}`
- `p16:{{% /note %}}`
- `p17:{{% note %}}`
- `p17:{{% /note %}}`
- `p18:{{% note %}}`
- `p18:{{% /note %}}`
- `p20:{{% note %}}`
- `p20:{{% /note %}}`
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p22:{{% note %}}`
- `p22:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p27:{{% note %}}`
- `p27:{{% /note %}}`
- `p29:{{% note %}}`
- `p29:{{% /note %}}`
- Reveal-hugo syntax:
- none.

## Time-to-Sentence

- Markdown:
- `p2:沒使用過的人不是這個 session 的目標聽眾，可以 QR code 拍下來去聽別場。例如對面同題材的session`
- `p2:QR code 有投影片，範例 github repo，投影片裡還有講稿，所以我今天在這裡的用處就是念稿，真的可以 qrcode 拍了回家看`
- `p2:Q2: 有使用過 infrastructure as code / terraform 的人請舉手`
- `p2:有使用 vault 但是沒有使用 IaC 的朋友，才是這場 session 的主要受眾`
- `p2:Q3: 有使用 iac deploy vault stack，或是有使用 iac / vcs 管理 vault 內的 policy 的人請舉手`
- `p3:Che Chia Chang | Vault 鐵人賽 workshop`
- `p5:on aws / azure / gcp / k8s`
- `p5:secret backends / auth method / role / policy / audit ...`
- `p5:工作流程自動化 gitflow / tested / automation`
- `p5:manage vault infra & vault configuration from a aspect of devops`
- `p6:2023 鐵人賽: vault 10- day workshop`
- `p6:2021 鐵人賽: terraform 30 day workshop`
- `p6:第一個 google slides 是我在其他場合的演講，適合第一次接觸 vault，或是正在評估是否要導入 vault 的團隊`
- `p6:第二個今年的 ithome 2023鐵人賽，我寫的內容就是 vault workshop，雖然寫到第十篇就因故停更，但前面 1-8 篇剛好是 vault 操作基礎，使用 chatgpt 翻譯 vault official tutorial，也是適合第一次使用 vault 的人`
- `p6:第三個是如果沒接觸過 infrastructure as code IaC，這個也是鐵人賽的 30 day workshop，這個有完賽佳作`
- `p7:immutable upgrades 指的是當你使用 vault server 與 storage backend，vault server 本身是 immutable 的，你可以自己使用 official binary build VM Image (ex. aws ami)，或是透過 container image release 來更新`
- `p8:是我們要將 deploy / release / upgrade vault 中的風險降到最低`
- `p8:infra: 升級 vault 版本，調整 VM / container，調整 load balancer，除錯`
- `p13:ELB -> AWS Autoscaling Group -> EC2`
- `p15:ELB -> AWS Autoscaling Group -> EC2`
- `p17:server 與 injector 建議分開兩個 argocd applicatoin / helm release獨立deploy`
- `p18:FAQ: on VM or on K8s?`
- `p18:問題不是 vault 在 VM 上安全，還是在 k8s 上安全`
- `p18:而是團隊能不能 secure 底下的 infra，如果熟 VM 就會覺得 VM 好做`
- `p18:secure k8s 是 VM + k8s 都要`
- `p19:auth method / config / role`
- `p20:version control 有多重要？`
- `p20:有 / 沒有 review 的 code 品質，天差地遠`
- `p20:有 / 沒有 經過完整環境測試的 release 品質，天差地遠`
- `p20:reusable module / don't repeat your self`
- `p20:secured admin access only to workflow. developer don't have admin access.`
- `p22:查錯時需要耗費大量 api call 列出 policy 查表`
- `p22:透過 IaC sync policy code to server`
- `p23:terraform 與 terragrunt 我的部落格上都有許多介紹文章，ithome 鐵人賽也有 30day workshop`
- `p24:local lint with git pre-commit hook`
- `p24:pipeline module test terraform test on github action`
- `p24:integration test against vault dev server`
- `p24:release candidate tag will apply to stag automatically`
- `p24:release tag will push to pre-production and production`
- `p25:dev -> stag -> prod 環境很接近`
- `p26:config as code 可以使用 terraform test`
- `p27:description = "default mount_path is ${local.mount_path}"`
- `p27:description = "default max_versions is 10"`
- `p27:description = "default delete_version_after is 10"`
- `p27:這個 module 只是一個 kv engine，所以隨手寫了一個簡單的 test`
- `p27:當你使用 terraform 時間夠久，使用規模越大時，會有復雜的 module，這時有寫測試的 module 就是天差地遠`
- `p29:apply to dev environment automatically with gitflow`
- `p29:release candidate tag will apply to stag automatically`
- `p29:release tag will push to pre-production and production`
- `p29:PR comment 下會有針對 dev environemtn plan 的結果`
- `p29:使用 github webhook，可以直接在 PR approved 後，命令 atlantis 直接 apply 到 dev server`
- `p30:使用 IaC 管理 vault 內部一切 config`
- `p31:Questions?`
- Hugo shortcode:
- `p2:{{< slide background-image="onepiece.jpg" >}}`
- `p2:{{% note %}}`
- `p2:{{% /note %}}`
- `p3:{{< slide background-image="background.jpg" >}}`
- `p3:{{% note %}}`
- `p3:{{% /note %}}`
- `p5:{{< slide background-image="background.jpg" >}}`
- `p5:{{% note %}}`
- `p5:{{% /note %}}`
- `p6:{{% note %}}`
- `p6:{{% /note %}}`
- `p7:{{% note %}}`
- `p7:{{% /note %}}`
- `p8:{{% note %}}`
- `p8:{{% /note %}}`
- `p9:{{% note %}}`
- `p9:{{% /note %}}`
- `p10:{{% note %}}`
- `p10:{{% /note %}}`
- `p11:{{% note %}}`
- `p11:{{% /note %}}`
- `p12:{{% note %}}`
- `p12:{{% /note %}}`
- `p13:{{% note %}}`
- `p13:{{% /note %}}`
- `p14:{{% note %}}`
- `p14:{{% /note %}}`
- `p15:{{% note %}}`
- `p15:{{% /note %}}`
- `p16:{{% note %}}`
- `p16:{{% /note %}}`
- `p17:{{% note %}}`
- `p17:{{% /note %}}`
- `p18:{{% note %}}`
- `p18:{{% /note %}}`
- `p20:{{% note %}}`
- `p20:{{% /note %}}`
- `p21:{{% note %}}`
- `p21:{{% /note %}}`
- `p22:{{% note %}}`
- `p22:{{% /note %}}`
- `p23:{{% note %}}`
- `p23:{{% /note %}}`
- `p27:{{% note %}}`
- `p27:{{% /note %}}`
- `p29:{{% note %}}`
- `p29:{{% /note %}}`
- Reveal-hugo syntax:
- none.
