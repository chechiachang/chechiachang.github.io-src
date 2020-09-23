---
title: "Gcp Preemptible Instance"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance"]
category: ["kubernetes"]
date: 2020-09-22T09:22:17+08:00
featured: true
draft: false
---

# 前言

鐵人賽的第二部分，要帶來公有雲省錢系列文章。

架構的成本，很多時候會影響架構的設計與需求。公司的營運都需要在成本與需求之前平衡，成本其實是影響公司決策的重要因素。身為架構管理員，應該要試著量化並且進行成本管理，提出解決方案時，也需要思考如何幫公司開源節流。

一昧消減架構的成本也未必是最佳方案，帳面上消減的成本有時也會反映在其他地方，例如：使用比較便宜的解決方案，或是較低的算力，但卻造成維運需要花更多時間維護，造成隱性的人力成本消耗。用什麼替代方案 (trade-off) 省了這些錢。

Kubernetes 是一個很好的例子：例如：有人說「Kubernetes 可以省錢」，但也有人說「Kubernetes 產生的 Overhead 太重會虧錢」。

「要不要導入 Kubernetes 是一個好問題」。應該回歸基本的需求，了解需求是什麼。例如：Google 當初開發容器管理平台，是面對什麼樣的使用需求，最終開發出 Kubernetes，各位可以回顧前篇文章「Borg Omega and Kubernete，Kubernetes 的前日今生，與 Google 十餘年的容器化技術」，從 Google 的角度理解容器管理平台，反思自身團隊的實際需求。

這套解決方案是否真的適合團隊，解決方案帶來的效果到底是怎樣呢？希望看完這系列文章後，能幫助各位，從成本面思考這些重要的問題。

這篇使用 GCP 的原因，除了是我最熟悉的公有雲外，也是因為 GCP 提供的免費額度，讓我可以很輕鬆地作為社群文章的 Demo，如果有別家雲平台有提供相同方案，請留言告訴我，我可能就會多開幾家不同的範例。

# 先占虛擬機 TL;DR

- 先占虛擬機為隨選虛擬機定價的 2-3 折，使用先占虛擬機可能可以節省 7 成的雲平台支出
- 先占虛擬機比起隨選虛擬機，外加有諸多限制，e.g. 最長壽命 24 hr、雲平台會主動終止先占虛擬機...等
- 配合使用自動水平擴展 (auto-scaler)，讓舊的先占虛擬機回收的同時，去購買新的先占虛擬機
- 配合可容錯 (fault-tolerent) 的分散式應用，讓應用可以無痛在虛擬機切換轉移，不影響服務
- 要讓應用可以容錯，需要做非常多事情
- 搭配 kubernetes ，自動化管理來簡化工作
- 配合正確的設定，可以穩定的執行有狀態的分散式資料庫或儲存庫

或是看 Google 官方 Blog：[Cutting costs with Google Kubernetes Engine: using the cluster autoscaler and Preemptible VMs](https://cloud.google.com/blog/products/containers-kubernetes/cutting-costs-with-google-kubernetes-engine-using-the-cluster-autoscaler-and-preemptible-vms)

預計內容

1. 需求假設、釐清需求，並且精準計價
1. 精準計價使用先占虛擬機的節省成本
1. 先占虛擬機的規格、額外限制
1. 額外限制，造成技術要多做很多額外的事情
1. 實務經驗分享：API server
1. 實務經驗：從使用隨選虛擬機，移轉到先占虛擬機，公司實際導入經驗
1. 實務經驗：Elasticsearch
1. 實務經驗分享：其他分散式資料庫，也許是 Cassandra 或是 cockroachDB

上面的內容不曉得會寫幾篇看感覺 XD

有寫過鐵人賽的都知道 30 篇真的很漫長，一篇文章幾千字，都要花好幾個小時。我去年後半，真的都會看讀者的留言跟按讚，取暖一波，才有動力繼續寫。留言的人多就會多寫，留言的人少就會少寫，各位覺得文章還看得下去，請務必來我粉專按讚留個言，不管是推推、鞭鞭、或是有想看的文章來許願，都十分歡迎。有你們的支持，我才有動力繼續寫。

請大家務必以實際行動支持好文章，不要讓劣幣驅逐良幣。不然 iThome 上面之後只剩洗觀看數的熱門文章了 XD

當然，沒人留言我就會當作自己才是垃圾文 (自知之明XD)，就會收一收回家嚕貓睡覺，掰掰~

->我的粉專，等你來留言
