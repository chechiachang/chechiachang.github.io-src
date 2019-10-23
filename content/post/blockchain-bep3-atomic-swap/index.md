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

交換 ethereum 與 binance chain 上的 token

# 動機

在部署 asset / token 的時候，我們會選擇合適的鏈作為發布資產並運行 block chain app。常用的應用鏈如 ethereum 與 binance chain 等等。不同的主鏈上有各自的優缺點，例如使用 ethereum ，可以與許多 token 與應用互動，也是最多人使用的應用主鏈。而在 binance 鏈上執行，則能夠快速的發生 transactions，並且可以與 binance 上的資產與交易所互動。

在某些應用場景，我們會希望兩個獨立主鏈上的資產能後互動，例如在 binance chain 上執行快速的 transaction，然而也要使用 etheruem 上既有的 ERC-20 tokens，這時便需要一個溝通兩條鏈的機制。

我們今天會實作 Atomic Peg Swap，透過 HTLT 鎖住兩邊鏈上的資產，再原子性的一次交易，來達成不同鏈上的資產互換。

# BEP3 Atomic Swap

Binance 在 [BEP3: HTLC and Atomic Peg](https://github.com/binance-chain/BEPs/blob/master/BEP3.md) 提到，BEP 即將在 binance chain 上支援原生的 Hash Timer Locked Transfer (HTLT) ，這使跨鏈的原子性交換 (atomic swap) 變得可行，透過 HTLC 在兩邊的鏈上鎖住 (peg) tokens，然後只有在執行交換的時候，透過 hash 交換，一次執行雙邊的交易。

主要的資訊來源來自 binance.org 的[官方說明文件](https://docs.binance.org/atomic-swap.html)，這邊針對文章進行驗證，並且補足過程中可能會踩到的雷。

---

# Outline

* 基本運作流程說明
* 將 asset 從 ethereum token 與 binance asset 做交換
* 將 asset 從 binance asset 與 ethereum token 做交換

# 使用情境

### 角色

* Client: 擁有一部分 token 或 asset，希望執行資產互換
* Owner: 擁有 ERC-20 token 與 Binance Asset，通常是 token 的 issuers，負責提供服務執行 Atomic Peg Swap (APS)

### 服務元件

* Ethereum Smart Contract: 支持 APS 的 token contract
* HTLT transactions on binance chain: 來鎖住並 claim assets
* Deputy 程序: 持續並自動的執行交換
* Client tooling: 讓客戶可以操作，監測鏈上的狀況

# 運作流程

(TODO)

---

# Task 1: 使用 bnbcli 交換資產

# 取得 tbnbcli

[tbnbcli 的說明文件](https://docs.binance.org/api-reference/cli.html)

```
git clone git@github.com:binance-chain/node-binary.git
cd node-binary
git chechout v0.6.0
sudo copy cli/testnet/0.6.0/mac/tbnbcli /usr/local/bin
```

# 測試 tbnbcli

```
tbnbcli status --node http://data-seed-pre-0-s3.binance.org:80

{
	"node_info": {
		"protocol_version": {
			"p2p": "7",
			"block": "10",
			"app": "0"
		},
		"id": "34ac6eb6cd914014995b5929be8d7bc9c16f724d",
		"listen_addr": "aa13359cd244f11e988520ad55ba7f5a-c3963b80c9b991b7.elb.us-east-1.amazonaws.com:27146",
		"network": "Binance-Chain-Nile",
		"version": "0.31.5",
		"channels": "36402021222330380041",
		"moniker": "data-seed-0",
		"other": {
			"tx_index": "on",
			"rpc_address": "tcp://0.0.0.0:27147"
		}
	},
	"sync_info": {
		"latest_block_hash": "359AD9BF36B7DEEB069A86D53D3B65D9F4BB77A1A65E40E1289B5798D4C1094F",
		"latest_app_hash": "E748CFA5806B587D9678F55DFDDB336E3669CDF421191CDA6D2DF8AA7A3461F3",
		"latest_block_height": "45868456",
		"latest_block_time": "2019-10-23T07:36:38.176957281Z",
		"catching_up": false
	},
	"validator_info": {
		"address": "1C360E22E04035E22A71A3765E4A8C5A6D586132",
		"pub_key": {
			"type": "tendermint/PubKeyEd25519",
			"value": "T56yDoH+B+OY8PP2tmeFtJtk+9ftnBUVHykKfLS45Es="
		},
		"voting_power": "0"
	}
}
```

# Acquire Valid Binance Testnet Account

Check [Testnet Doc](https://www.binance.com/en/support/articles/360023912272)

* Go to [Binance Testnet](https://testnet.binance.org/en/)
* Create a wallet
* Save address, mn, keystore, private key
* Use [testnet faucet](https://www.binance.vision/tutorials/binance-dex-funding-your-testnet-account) to fund testnet account
* Receive 200 BNB on testnet

# Acquire Ropsten (ethereum testnet) Address

# HTLT

```
tbnbcli token HTLT \
  --recipient-addr <recipient-addr> \
  --amount 10:BNB \
  --expected-income 10:BNB \
  --height-span <heightSpan> \
  --from <from-addr> \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

# Deposit HTLT

```
tbnbcli token deposit \
  --swap-id <swapID>  \
  --amount 10000:TEST-599 \
  --from <from-key> \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

---

# References

* [Binace Chain Doc](https://docs.binance.org/atomic-swap.html)
* [Binance BEP3 spec](https://github.com/binance-chain/BEPs/blob/master/BEP3.md)
