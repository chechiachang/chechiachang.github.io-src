---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Blockchain Bep3 Atomic Swap"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2019-10-22T10:35:20+08:00
lastmod: 2019-10-22T10:35:20+08:00
featured: false
draft: true

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
---

# 交換 ethereum 與 binance chain 上的 token

在

# BEP3 Atomic Swap

Binance 在 [BEP3: HTLC and Atomic Peg](https://github.com/binance-chain/BEPs/blob/master/BEP3.md) 提到，BEP 即將在 binance chain 上支援原生的 Hash Timer Locked Contract (HTLC) transaction ，這使跨鏈的原子性交換 (atomic swap) 變得可行，透過 HTLC 在兩邊的鏈上鎖住 (peg) tokens，然後只有在執行交換的時候，透過一次執行雙邊的交易。

主要的資訊來源來自 binance.org 的[官方說明文件](https://docs.binance.org/atomic-swap.html)，這邊針對文章進行驗證，並且補足過程中可能會踩到的雷。

# Outline
