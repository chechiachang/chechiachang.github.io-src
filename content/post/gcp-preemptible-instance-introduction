---
title: "Gcp Preemptible Instance Introduction"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "gcp", "preemptible", "spot-instance"]
category: ["kubernetes"]
date: 2020-09-22T11:03:40+08:00
featured: true
draft: false
---

# 先占虛擬機，技術文件二三事

第一篇的內容大部份還是翻譯跟講解官方文件。後面幾篇才會有實際的需求與解決方案分析。

[Google 先占虛擬機官方文件](https://cloud.google.com/compute/docs/instances/preemptible)

使用不熟悉的產品前一定要好好看文件，才不會踩到雷的時候，發現人家就是這樣設計的，而且文件上寫得清清楚楚。以為是 bug 結果真的是 feature，雷到自己。先占虛擬機是用起來跟普通虛擬機沒什麼兩樣，但實際上超級多細節要注意，毛很多的產品，請務必要小心使用。

以下文章是筆者工作經驗，覺得好用、確實有幫助公司，來跟大家分享。礙於篇幅，這裡只能非常粗略地描述我們團隊思考過的問題，實際上的問題會複雜非常多。文章只是作個發想，並不足以支撐實際的業務，所以如果要考慮導入，還是要

1. 多作功課，仔細查閱官方文件，理解服務的規格
1. 深入分析自身的需求
1. 基於上面兩者，量化分析

# 什麼是先占虛擬機器(Preemptible Instance)

先占虛擬機器，是資料中心的多餘算力，讀者可以想像是目前賣剩的機器，會依據資料中心的需求動態調整，例如

- 目前資料中心的算力需求低，可使用的先占虛擬機釋出量多，可能可以用更便宜的價格使用
- 目前資料中心算力需求高，資料中心會收回部分先占虛擬機的額度，轉化成隨選付費的虛擬機 (pay-as-you-go)

由於先占虛擬機會不定時（但可預期）地被資料中心收回，因此上頭執行的應用，需要可以承受機器的終止，適合有容錯機制 (fault-tolerant) 的應用，或是批次執行的工作也很適合。

# 先占機器的優缺點

除了有一般隨選虛擬機的特性，先占虛擬機還有以下特點

- 比一般的虛擬機器便宜非常多，這也是我們選用先占虛擬機優於一般虛擬機的唯一理由

先占虛擬機有以下限制，以維運的角度，這些都是需要考量的點。

- GCP 不保證會有足夠的先占虛擬機
- 先占虛擬機不能直接轉換成普通虛擬機
- 資料中心觸發維護事件時(ex. 回收先占虛擬機)，先占虛擬機不能設定自動重啟，而是會直接關閉
- 先占機器排除在 [GCP 的服務等級協議 (SLA)](https://cloud.google.com/compute/sla)之外
- 先占虛擬機不適用[GCP 免費額度](https://cloud.google.com/free)

# 費用粗估試算

至於便宜是多便宜呢？這邊先開幾個例子給各位一些概念。

以常用的 N1 standard 虛擬機：https://cloud.google.com/compute/vm-instance-pricing#n1_standard_machine_types

Hourly
Machine type	CPUs	Memory	Price (USD)	Preemptible price (USD)
n1-standard-1	1	3.75GB	$0.0550		$0.0110
n1-standard-2	2	7.5GB	$0.1100		$0.0220
n1-standard-4	4	15GB	$0.2200		$0.0440
n1-standard-8	8	30GB	$0.4400		$0.0880
n1-standard-16	16	60GB	$0.8800		$0.1760
n1-standard-32	32	120GB	$1.7600		$0.3520
n1-standard-64	64	240GB	$3.5200		$0.7040

如果是用 GPU 運算：https://cloud.google.com/compute/gpus-pricing

Model			GPUs	GPU memory	GPU price (USD)	Preemptible GPU price (USD)
NVIDIA® Tesla® T4	1 GPU	16 GB GDDR6	$0.35 per GPU	$0.11 per GPU
NVIDIA® Tesla® V100	1 GPU	16 GB HBM2	$2.48 per GPU	$0.74 per GPU

依據虛擬機規格的不同，先占虛擬機大約是隨選虛擬機價格的 2 到 3 折。在 AWS 與 Azure，由於計費方式不同，有可能拿到 1 折左右的浮動價格。從各種角度來說，都是非常高的折數。

不妨說，這整系列文章，都是衝這著個折數來的 XD。畢竟成本是實實在在的花費，工作負載 (workload) 合適的話，應該盡量嘗試導入。

這個折數還有另外一個效果是，可以在相同成本下，添增更多資源算力，作為解決方案。什麼意思呢？就是如果工作負載合適的話，可以使用更高規格的先占節點，整體成本反而會下降。

至於究竟差多少，需要依據規格與定價詳細試算才知道。底下我們就來算算看。
