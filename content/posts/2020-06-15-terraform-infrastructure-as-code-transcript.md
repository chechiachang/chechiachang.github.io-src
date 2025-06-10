---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Terraform Infrastructure as Code Transcript"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "terraform", "devops", "iac"]
categories: ["kubernetes", "terraform"]
date: 2020-06-15T10:58:56+08:00
lastmod: 2020-07-15T10:58:56+08:00
featured: false
draft: false
---

This article is part of [從零開始的 Infrastructu as Code: Terraform]({{< ref "/posts/2020-06-14-terraform-infrastructure-as-code" >}})
- [Get-started examples / SOP on Github](https://github.com/chechiachang/terraform-playground)
- [Introducation to Terraform Iac: Speaker transcript]({{< ref "/posts/2020-06-15-terraform-infrastructure-as-code-transcript" >}})
- [Presentation](https://slides.com/chechiachang/terraform-introduction/edit)

Check my website [chechia.net](https://chechia.net) for other blog. [Follow my page to get notification](https://www.facebook.com/engineer.from.scratch). Like my page if you really like it :)

---

各位好

# About this presentation

開始之前，先分享一些資源
 - [投影片](https://slides.com/chechiachang/terraform-introduction/edit)
 - [講稿](https://chechia.net/posts/2020-06-15-terraform-infrastructure-as-code-transcript/)
 - [程式碼](https://github.com/chechiachang/terraform-playground)
 - [SOP 範本](https://github.com/chechiachang/terraform-playground/blob/master/SOP.md)
 - [Facebook 粉專](https://www.facebook.com/engineer.from.scratch/)

都放在這裡，因為有附逐字稿，所以如果很忙的朋友，掃了 QR code 就可以回家自己看了，不用客氣。

然後有興趣在追這系列文章的，可以幫我 facebook 粉專按個讚跟追蹤，每周新文章出來，會推播通知。

文章在 chechia.net 上，新文章通知靠 facebook 粉專這樣。也可以只追蹤不按讚。我自己看別人技術 blog 也很常這樣(XD

需求
---

好，今天來講得這個 Terraform

我會實際分享我們公司為雲團隊導入的經驗，前半部會有點像購物頻道的廣告

以下的對話是不是常出現在日常工作中？

# 以下這段對話很耳熟？

「是誰改了這個設定？」
- by 週一上班的 DevOps 與週六值班的維運團隊
- 對啟用的環境的掌握如何
- 環境的變更能否永久保存

「這個環境怎麼少一個設定？」
- 網站噴錯後，整個團隊一步步釐清問題，不是 code，不是變數config，是 infra 有一個小地方沒設定
- 環境複雜，以我們的例子是複雜得多雲網路，常出這種問題
- 環境設定的除錯很費時
- 完全可以避免

「會動就好，沒事不要改環境（抖）」
- Legacy site
- 調整 production 環境是否有信心
- 我們看不慣無人整理的舊架構，導入 terraform 後，（很不要命的）把 production site 搬過一遍
- 我有十成的信心跟你說新舊兩個 site 完全一樣

# Our stories

- 我們是思華科技(ＸＤ)
- 開發團隊大概 100+ 個左右
- 專案很多，而且老闆很喜歡開新專案測試商業模型
- 環境也越開越多，大大小小幾百台 vm，幾十個資料庫，都是不同專案在跑，規模大概這樣
- 每週都有新環境要交付
- 交接缺口

我們公司東西多，但東西多不是問題，問題是什麼呢?

# 問題

- 手動部屬本來不是問題，但漸漸成為問題
  - 開 infrastructure 的方法，跟著 SOP 上去 GCP GUI 介面，點一點，填一填。公有雲開機器很方便。
  - 可是不同人開的環境漸漸出現一些不同，可能差一個設定、一個參數、或是命名規則差一點。這些細節的不同，差一個 config 有時候就會雷到人。「這機器誰建的阿，根本有問題啊」，而且這種雷很多時候都是跑下去出事了，才發現「阿靠原來設定不一樣」
  - 命名差一點不影響功能，但看久了就很煩，「阿就對不齊阿」，有強迫症就很痛苦。然後你維運的自動化腳本就爆掉，命名差一個字，regex 就要大改。突然增加維運成本
- 生產環境大家都不太敢動。架構調整很沒信心
  - 誰知道當初環境設定了那些東西，開機器的人離職了，也不知道他為啥設定，「你知道他當初為什麼要設定這個嗎?」，你問我我是要去擲茭喔。
    - 我們這一季把所有現有環境都搬到新的架構上，因為我們對舊架構不爽很久了(XD)，這個能做到當然有作法，後面細講

有實際需求才找解決方案，沒有需求就不用衝動導入新技術，導入過程中還是蠻累的

# 需求

從維運的角度，需求大概長這樣

- 提升穩定度
  - infra 交付標準化
  - 交付自動化
  -  測試環境
- infra 提交要能夠 review
- 提升效率
  - 老闆要的。超快部屬，腳本跑下去要快，還要更快

- 次要目標
  - 成本，效能最佳化，希望能在整理過程中，找到最適合的可行架構
  - 新人好上手，Junior 同事也能「安全」的操作，看到這個安全兩個字了嗎? 安全第一，在訓練新的 op 時要注意安全，不然他上去 GUI 點一點，一個手起刀落 DB 就不見了，整個維運團隊一周不用睡覺。安全第一吼。
  - 權限控管，IAM 也用 terraform 管理，權限管理人多手雜越用越亂，可以考慮使用 IaC，一覽無遺

# Programatical approach for infra

啊不就是 Infrastructure as code XD
- 導入前，大家都有聽過，大家都覺得很想導入，但沒人有經驗，每個人都超怕，但又不知道在怕三小
- 這表明了一件事，大家都知道要做對的事情，但不是每個人都能改變現況，讓團隊導向對的事情

計畫
- 確定需求
- 開始 survey
- 「小心」導入
- 有經驗領頭羊很棒，但不是必須

技術細節
---

先簡單講一下 IaC (Yeah 終於要講技術了)

# IaC

上面都講概念跟心法，現在實際講用到的技術。

首先是 Infrastructure as Code，這個概念很久了，但導入的公司好像不是那麼多。所以我今天要來傳教，洗腦大家(XD，跟你推薦這個配方保證快又有效(XD)

- 簡單來說就是用程式來操作 infrastructure，今天主講的 terraform 是 IaC 工具中的一個
- IaC 工具可以是宣告式，或是命令式，或是兩種都支援
  - 一個是我告訴你結果，步驟我不管，請你幫我生出這樣的結果。
  - 一個是我告訴你步驟，你一步一步幫我做完，就會得到我要的結果
  - terraform 是宣告式，說明邏輯跟結果，例如我要 1 2 3 台機器，terraform 自己去幫我打 Google API 這樣，把機器生出來
  - ansible 是命令式，我把步驟寫成一堆命令腳本 playbook ，ansible 幫我照著跑下去，理論上跑完後我的機器也準備好


Terraform
---

- 官網在這邊，自己看 https://www.terraform.io/
- 宣告式的 Iac 工具
- 單一語法描述各家 API
- 透過 provider 轉換 tf 成為 API call

# Terraform Core Workflow

https://www.terraform.io/guides/core-workflow.html

- Write 撰寫期待狀態 tf file
- plan 計畫試算結果
- apply 用期待狀態去更新遠端
  - tf file，就是宣告式的表達 infra ，描述期待的infra長這樣，ex. tf file 裡有這些機器 1 2 3 台這樣
    - resource 一個一個物件描述，後面可能是對映 provider 的 API Endpoint (ex. GCP GKE API)
  - remote resources，是真實存在遠端的機器，例如 GCP 雲端實際上只有 1 2 兩台這樣。
  - terraform diff tf vs remote，算出 plan，少的生出來，多的上去砍掉

# Demo 1

- (empty project)
- add my-gce.tf
- git diff
- state
- check GUI remote

- existing my-gce
- remove my-gce.tf
- plan
- 這邊不 apply 我 demo 還要用

這邊這樣有理解 terraform 的基本流程嗎？編寫，計畫，apply 三步驟
很單純
然後講一點細節

- state
- remove (out of scope)
- plan -> addd
- apply (deplicated ID)

- mv state (Danger)
- rename state with the same ID -> destroy and recreate (Danger)

# State

- terraform 經手(apply) 過的 resource 會納入 state (scope)
- 不在 scope 裡的 resource 不會納入 plan，不會被 destroy，但可能會 create duplicated ID
- terraform 允許直接操作 state
  - import
  - remove
  - 但我不允許XD

- 注意是 diff state 喔，所以每次 plan 時候會自動 refresh state
- state 又是什麼? remote 是一個動態環境，可能會多會少，這樣沒辦法 diff，state 是把我執行當下，遠端相關資源的狀態快照存起來，然後根據這個 snapshop 去 diff
- apply 只是拿你的期待去 diff state，terraform 幫你算出來差多少，例如我們這邊就是遠端少一台。terraform 透過 provider 去知道，喔這一台要去打那些 GCP API，把這台生出來。

State，是核心概念，我當初自己卡觀念是卡這邊，所以我特別拉出來講
- 雲端空蕩蕩，refresh state 也是空的，tf file 多加一個 VM，plan 覺得要 create
- 雲端有東西，refresh state 未必會 refresh 到
  - 相同 ID 的資源之前 import 在 state 中，refresh state，tf file 沒東西，plan 覺得要 destroy
  - 相同 ID 的資源不在 state 中，這些 resource 不在當前 state 的 scopor 中，refresh state 是空的，tf file 沒東西，plan 覺得沒增沒減
  - 相同 ID 的資源不在 state 中，這些 resource 不在當前 state 的 scopor 中，refresh state 是空的，tf file 有相同 ID 的資源，plan 覺得要 create，但實際 apply，API error 遠端已經有相同 ID 的資源存在

# 小結

- Write -> Plan -> Apply
- State
- 大家都會 terraform 惹

---

# 初步使用感想

- IaC 地端跟雲端都能做，但雲端做起來效果超級好
  - 完全展現雲端運算的特性，迅速、彈性、隨用隨叫，調度大量的虛擬化資源
  - 新增東西很快，不要的資源，要刪掉也很快
    - 不小心刪錯也很快(大誤)，所以我說新人一個手起刀落公司整個雲弄不見也是有可能的，「啊我的雲勒」「被 terraform 砍了」。不要笑，那個新人就是我，我自己剛學的時候就有把整個 db 變不見過，差點一到職就引咎辭職(XD。用這些技術還是有很多安全要注意，稍後會細講注意的安全事項。    

總之，Iac 就是用程式化的語法，精準的描述雲端的狀態或是步驟，完全沒有模糊的地帶。帶來的好處，降低維運的錯誤風險，加快維運效率，最佳化節省成本。

# 新手 state 的雷

- 多人協作，同時變更 state 會造成不可預期的錯誤
  - 避免直接操作 state
- state 可能有 sensitive 資料
- 推薦使用外部帶有 lock 的 state storage

導入
---

# 導入工具之後

新工具導入時要做好風險評估，每個人都是第一次用 terraform ，用起來很快很爽的同時也要不斷宣導安全概念，雷在哪裡坑在哪裡。

使用 terraform 的風險
- 打 DELET API 超快，砍起來很方便，但很多時候方便 = 危險。眼看小明一個手起刀落，談笑間，公有雲灰飛煙滅(XD，通通變不見。現在在講故事很開心，實際發生的話大家都笑不出來，全公司 RD 都跑來維運部門排隊盯著你看，就算修好也要懲處。壓力超大。但小明砍錯東西不是小明的錯，是大環境的錯是 SOP 的錯(XD。認真的，團隊沒有提供 SOP，新人砍錯東西當然是團隊負責。所以我們 SOP 第一行就寫得很清楚。
- 看見 destroy 就雙手離開鍵盤，直接求救，這樣還能出事嗎
- 再來，給予特殊的 IAM 權限，例如只能新增不能刪除的權限
- 進一步導入 git-flow，push、review、PR，讓他連犯錯的機會都沒有
- 根本還是要給予新人足夠的訓練，然後同時保障公司安全。
  - 給新人過大權限砍錯東西，或是工作流程一堆坑，根本是在誘導新人犯錯，團隊的資深成員要檢討。

# 逐漸導入

- 導入的過程不斷檢討跟修改，最後找出適合我們公司的流程
- 檢討透明，有錯就修 SOP，修工作流程。讓你的工作流程跟工作環境，固若金湯，成員很難在裡面犯錯，這才是 DevOps 在做這的事。
- 官方建議的最佳實作 https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html
- 至於我們是如何逐漸導入 IaC 到公司的開發流程中？具體的導入步驟如下


# Introduction: IaC

1. 舊架構保存。先把雲端上已經有的機器，terraform 裡面叫資源，import 成代碼
1. 檢查舊架構。所有設定都變成代碼了，跟你看程式碼一樣，一拍兩瞪眼沒有任何模稜兩可。整理過程中找出合理跟不合理的設定。有可能會發現一些雷，只是還沒爆炸，也趁機修一修。
1. 然後，依照這些現行的資源，去整理一份適合公司的環境範本，之後所有的新環境都這這個範本部屬，確定新的環境都有合理的規劃。
1. 到此，所有新環境都是同一份範本生出來的，環境已經標準化了。不會再有零碎的小錯誤。聽起來超讚，但有時候出錯就是一起全錯，超慘(XD。當然有錯就修範本，修 SOP。同樣的錯永不再犯，不用再修第二次。

# Introduction: Git-flow

1. 然後，導入版本控管，整合 git-flow 的開發流程。寫 SOP，之後所有變更都要
  1. 先把 master 封起來，所有人都不准直接改架構
  1. 開新 branch，commit
  1. 開 PR 大家 review，大家都看過了吼，再 merge 進去，這樣有錯就不是一個人的鍋而是大家一起背鍋(XD。不是拉，review 能大幅降低錯誤，分享團隊經驗加速新人訓練，並且讓所有人 on the same page，不會再有「阿靠這機器誰開的」有人不知情的事情。
  1. 永遠只使用 master 來部屬雲端資源，也是確定所有架構都經過多人 review。

# Introduction: Pipeline Automation

1. 最後，整合 CICD，讓架構的部屬完全自動化。把人工降到最低，同時也把人工錯誤的機率降到最低，當然這個也是沒錯都沒錯，要錯一起錯的狀態(XD，使用時還是要注意。但如果執行的很穩定的話，自動化絕對是值得投資的。因為現在把架構當作產品做，部屬完要測試功能，網路設定是否正確，監控是否完整，proxy 是不是要打看看。這些都整合進 infra 自動 pipeline。部屬完就是測試，然後交付給其他團隊。
1. 之後就是不斷調整 SOP，跟 CI/CD pipeline。把維運步驟轉成程式維護。

犯錯過一次，永不再犯。這個對於長期團隊經營非常重要，讓經驗跟知識累積，團隊質量才會成長。IaC 在這點幫助很大。

Demo 2
---

- NAME=terraform-devops make gke redis sql
- module
- git commit 
- Review on github
- Merge request

# Repo

我使用的原碼都開源在 github 上，因為是真的拿來導入我們公司的架構，保證可以用。阿不能用的話，幫我發 issue 給我，或是你人更好發個 PR 給我都可以(XD。把 repo 拉下來，這邊有 gcp / azure / aws，雖然有三個但我們公司主要是用 gcp，剩下兩個我自己做興趣的。裡面 templates 跟 modules ，但你不用管，我 makefile 都寫好了

- 我這邊要新增一個 kubernetes 集群
- 我直接進來我的專案， NAME=my-new-k8s make gke，東西就生出來，具體做的事情就是新增兩個程式區塊，每個區塊描述一個機器
- git diff 看多了什麼，這邊多一個 k8s 跟多一個 node-pool
- 然後我 plan，讓 terraform 預測一下試跑結果，我們依據結果好好 review，例如這邊 2 to add 0 to destroy 我的想像是不是真的跟 terraform 計畫一樣。
- 然後 terraform apply，這邊要看清楚，我們是 2 to add 0 to destroy，如果看到有 destroy 就要雙手離開鍵盤，大家不要衝動，看清楚，因為她真的會上去把東西砍掉

P.S. 專案可以按照公司需求分，資源太多太擠就拆分成幾個資料夾好管理，然後分權責管理，例如館 iam 的、管網路、管應用機器的可以分開來

# Git-flow

然後因為我後面會講 git-flow 工作流程整合，所以我順便做完。
- 新的變更 commit ，plan 但是還沒 apply。我要求所有新的 commit 推上去
- 發 PR，其他團隊成員來幫我 review。PR 用的 template ，描述一下新架構的目的，變更的地方，有沒有雷，然後幾個 checklist 檢查
- 其他隊員 review 都 lgtm 才 merge 回 master
- apply 永遠在最新的 master 上 apply，確保所有推到雲端的架構都是多人 review 過的。

有 review 才有品質可言，code 都要 review，infra 自然也需要 review。IaC + git-flow 是必要的。

# Demo 2

# 工具 + 流程

導入的成功與否，不是最佳實踐，而是各個階段，都給予團隊適合的挑戰與協助

- Git-flow SOP 範例
  - 中文版，超長，上面操作過了，這邊不細講，大家自己上去看
  - 但如果團隊是第一次導入 terraform，我強烈建議要有類似的東西
- Provide template

demo 時不是有 makefile，makefile 裡面寫的小腳本跟本身 IaC 沒有關係，提供一些而外的小腳本輔助，可以進一步降低人工操作，提升效率，又增加安全。工具不一定完全適合團隊吧，這時候就需要補足團隊文化跟工具間的落差，潤滑一下。

再說一次，新人做錯，不是他做錯，而是團隊沒有提供他足夠的協助。如何讓新人也能有高產出同時又顧及安全，資深工程師是這邊在資深。提供一些一用性工具是必要的。

- Terraform module

又是一個 terraform 的功能

簡單來說，GKE 也許定義了 2 個子物件(ex. Cluster，Node-pool)，總共有 30 個參數
- 你其實不需要那麼多參數 XD
- 建立一個 my-gke-module，一個物件，5 個必填參數，5 個有預設值的選填參數
- 也許寫錯的機會只剩 5 個，也許工時只需要 5/30
- 需求變更就改 module，讓你的操作物件本身就是符合實際需求的

能手動改的地方就是能犯錯的地方，黑箱封裝可以保護整體架構，並提高易用性

雜項
---

# 其他

- 上面是 IaC 在我們公司的流程
- 我們選 terraformㄨ
- 如果是用 terraform 以外的工具，可以參考流程，也許殊途同歸

https://www.terraform.io/intro/vs/index.html

# 優缺點

好，跟團隊一步一步溝通改進，花了一兩個月，成功導入。是否有解決當初的問題？

- 降低人工操作
  - 避免人工失誤
  - infra 交付標準化，沒有奇怪的設定，再也沒有「啊我機器開錯了」這回事
  - 快，真低快。開一個機器就是我剛剛 demo 這樣，而且保證會動。這樣開出來的機器，對她超有信心，要複製完全一模一樣的環境也超有信心。如果再加上自動化測試就更敢保證。

- 準確
  - 大家都 review 過，比較不會有「啊我當時沒想到」的狀況，infra 出這種萬萬沒想到的問題，很有機率要幹掉重來。菜鳥跟著 review ，試著發 PR，這樣新人訓練才會有效率，他之後才能自己操作，資深工程師只要 review 就好。要給新人足夠的訓練，又要顧慮安全， review 花的時間非常值得。
  - 保證開發、測試、staging、production 環境長的一模一樣。terraform 程式保證的不是我保證的(XD)。但他的保證是有根據的，讓團隊從開發到上限保重相同環境。「阿在我的機器上會跑怎麼上 production 就壞掉」不好意思沒這回事，壞掉就是你扣寫錯(兇。認真地說，排除一些 infra 的問題，可以大幅增加除錯的效率，只要檢查還沒自動化的地方就好。
  - 自動化測試，扣要測試環境也要測試，這邊直接整進去，環境交出去保證是好的  

- 生產環境變動
  - 因為已經轉成程式碼，要有什麼改動都很精確，大家也比較敢動環境，特別是 production 環境。再來因為保留所有環境產生的程式碼，要複製環境也很容易，而且有信心保證一樣。我們就把就架構的 production 複製，然後搬家。安全下庄沒出事。後面就搬上癮，整個公司服務大搬家，搬成團隊理想的架構。搬家已經上線的服務，這個需要多少信心跟勇氣你們知道嗎，維運真的是愛與勇氣的冒險。新架構我們也很滿意。
- 自動化
  - 自動化就是讓你用零倍的時間做十倍的事情嘛。聽起來怪怪的蛋是是真的。
  - 因為我們目標是維運躺著上班嘛(XD)，我們才能把時間拿去做改進，不然以光是開機器，測試環境可用性，維運就飽了，根本沒時間改進跟提升。這樣對公司長期非常不好。

- 可讀性
  - GUI 沒辦法打 comment 阿，誰知道這個機器當初為什是這個設定。IaC 後到處都可以寫 comment，怕你不寫而已。然後 code 的表達性還是很強大，比起 GUI，資深工程師可以把握整個公司的架構狀況，比起去雲平台下一堆搜索，手動比對，程式碼的可維護性真的超高。而 GCP 已經是 GUI 做得很好的公有雲了。

降低人工，快速，準確，自動化，有信心

Q&A
---

還有空我們再來講 terraform 的細節

有事歡迎透過粉專私敲，因為我也需要人討論

還有時間再聊
---

# terraform

- validate 既然是 code，這邊幫你做 lint、語法檢測、type check，過濾第一層錯誤
- import 可以把遠端的資源匯入成 state，一個點讚 follow 追蹤的概念(XD)，不是所有的遠端資源都需要追蹤到 state，我們只需要在對的 scope 裡面關注需要的機器
- module 可以自由撰寫，把有相依性的資源打包，依照團隊使用習慣調整使用
- cloud 可以管理 state，terraform cloud 幫你維護全域同一份 state，有人在使用時會 lock state，避免多人同時修改，打亂 API 造成資源錯誤

# state conflicts

- 如果有多份 state，你電腦上一份 local state，我電腦上一份 local state，其實會造成衝突
- 更怕同時多人憶起 apply，GCP API 直接被打亂，會有不可預期的錯誤
- 解法是使用 terraform remote backend，不要用 local state，使用 DB 、storage 或是 terraform cloud，透過一隻 lock 來保證 synchronized state

# 間接理解 API

ex.  GCP Load Balancer

這個講下去就太多了，基本上透過爬 terraform google provider 的文件，然後去比對

- 因為去點 GUI 其實感受不到 GCP API 的調用，但是使用 terraform 轉寫資源時候就很有感，打這個 API 跟打這個 API，tf 檔案上其實看得出來。
- 進一步去查，才發現 GCP Load Balancer 內網或外網、http 或 tcp、全球或區域，使用的 Load Balancer 行為不一樣，因為底下的實作不一樣。但之前使用 GUI 時其實不會去想為啥設定不一樣，使用 terraform 就會被迫去了解，強迫學習XD。

# 垃圾話

- 最佳實踐不是問題 ，如何導入才是問題
- 可以不用躺著上班，但是不能跪著上班
- 願意多幾個人來看我粉專比較實在
