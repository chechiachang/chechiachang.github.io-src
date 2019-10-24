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

啟用 Git Large File Storage
```
sudo port install git-lfs
```

Git clone repo
```
git clone git@github.com:binance-chain/node-binary.git
cd node-binary

git chechout v0.6.2
git lfs pull --include cli/testnet/0.6.2/mac/tbnbcli
sudo copy cli/testnet/0.6.2/mac/tbnbcli /usr/local/bin
```

這邊要注意使用 v0.6.2+ 的版本，不然會沒有 HTLT 的 subcommands

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

---

# HTLT

這邊使用簡單的範例，鎖住兩個 BEP2 tokens 來進行交換，展示一下 tbnbcli 的 HTLT

準備兩個 address，這邊是我自己的兩個 testnet address

* tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p (179 BNB) [Explorer 上查看](https://testnet-explorer.binance.org/address/tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p)
* tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce (20 BNB) [Exporler 上查看](https://testnet-explorer.binance.org/address/tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce)

目標：

* HTLT
* tbnb...j9p -> 3 BNB -> tbnb...7ce
* tbnb...j9p <- 1 BNB <- tbnb...7ce

參數：

* hightspan: 400

tbnbcli 執行 HTLT，從 from address 執行 HTLT，給 recipient-addr amount 的 token，並預期對方回 expected-income，等待 height-span 個 block 時間(360 > 2 minutes)
```
FROM_ADDR=tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p
RECIPIENT_ADDR=tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce
HEIGHT_SPAN=360

tbnbcli token HTLT \
  --recipient-addr ${RECIPIENT_ADDR} \
  --amount 3:BNB \
  --expected-income 1:BNB \
  --height-span ${HEIGHT_SPAN} \
  --from ${FROM_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

實際執行前，由於我們需要透過 tbnbcli 操作 from-address，要先[透過 tbnbcli 把 address 的 key 加進到本地](https://docs.binance.org/keys.html)

```
tbnbcli keys add tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce --recover

tbnbcli keys list

NAME:	                                      TYPE:	ADDRESS:						                        PUBKEY:
tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	local	tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	bnbp1addwnpepq0pw06d3y7ykg2j33pc604j3awgqgl5vhd88wdjhjg5sptnsfpqyx2rmhl4
```

實際執行

從 tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p 執行 HTLT
給 tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce 3 BNB
預期對方回 1 BNB
等待 360 個 block 時間

```
tbnbcli token HTLT \
  --recipient-addr ${RECIPIENT_ADDR} \
  --amount 3:BNB \
  --expected-income 1:BNB \
  --height-span ${HEIGHT_SPAN} \
  --from ${FROM_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

產生 swap 的結果，可以於[Testnet Explorer 上看到](https://testnet-explorer.binance.org/tx/366E24B0722FCACD4256A09C58755F06362EAAF220030E443E7CFBDA22577AFF)
```
Random number: fe1c49c02b2d8133750ab36e2f48d1261c8dc38dd32a41fead46535aef1aef76
Timestamp: 1571905650
Random number hash: 2c2588c81a5f08bf55a183cc2d61a123368405638741169933e200c90f4532e5
Password to sign with 'tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce':

Committed at block 46042933 (
  tx hash: 366E24B0722FCACD4256A09C58755F06362EAAF220030E443E7CFBDA22577AFF, 
  response: {
    Code:0 Data:[78 41 198 15 115 23 94 152 87 53 225 197 12 182 116 229 246 250 55 25 9 102 127 48 222 136 54 44 155 39 129 155] 
    Log:Msg 
    0: 
      swapID: 4e29c60f73175e985735e1c50cb674e5f6fa371909667f30de88362c9b27819b 
      Info: 
        GasWanted:0 
        GasUsed:0 
        Tags:[
          {
            Key:[115 101 110 100 101 114] 
            Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] 
            XXX_NoUnkeyedLiteral:{} 
            XXX_unrecognized:[] 
            XXX_sizecache:0
          } {
            Key:[114 101 99 105 112 105 101 110 116] 
            Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] 
            XXX_NoUnkeyedLiteral:{} 
            XXX_unrecognized:[] 
            XXX_sizecache:0
          } {
            Key:[97 99 116 105 111 110] 
            Value:[72 84 76 84] 
            XXX_NoUnkeyedLiteral:{} 
            XXX_unrecognized:[] 
            XXX_sizecache:0
          }
        ] 
        Codespace: 
          XXX_NoUnkeyedLiteral:{} 
          XXX_unrecognized:[] 
          XXX_sizecache:0
  }
)
```

# Query Atomic Swap

產生了 atomic swap，這邊可以使用 tbnbcli 查詢 swap 的狀態

```
SWAP_ID=4e29c60f73175e985735e1c50cb674e5f6fa371909667f30de88362c9b27819b 

tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

回傳 swap 的狀態
```
  {
	"from": "tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce",
	"to": "tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p",
	"out_amount": [{
		"denom": "BNB",
		"amount": "3"
	}],
	"in_amount": null,
	"expected_income": "1:BNB",
	"recipient_other_chain": "",
	"random_number_hash": "2c2588c81a5f08bf55a183cc2d61a123368405638741169933e200c90f4532e5",
	"random_number": "",
	"timestamp": "1571905650",
	"cross_chain": false,
	"expire_height": "46043293",
	"index": "2239",
	"closed_time": "0",
	"status": "Open"
}
```

# Deposit HTLT

受方 reciept-address 這邊要把 1 BNB 打進去 swap 中

注意這邊的 from-address 已經變成當初的 recipient-addr tbnb...j9p

當然這邊要存取，也要有 tbnb...j9p 的 key，這樣我們本地就會有發受兩方的 key，但一般來說應該是兩個不同的人

```
tbnbcli keys add tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p--recover

tbnbcli keys list

NAME:	                                      TYPE:	ADDRESS:						                        PUBKEY:
tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	local	tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	bnbp1addwnpepq0pw06d3y7ykg2j33pc604j3awgqgl5vhd88wdjhjg5sptnsfpqyx2rmhl4
tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p	local	tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p	bnbp1addwnpepqwk5zx3jnrq5guxc9tsgrte9aw9knla0ahunwynypkm0jvst6y7l2q83ueq
```

受方把約好的錢存進去

```
tbnbcli token deposit \
  --swap-id ${SWAP_ID}  \
  --amount 1:BNB \
  --from ${RECIPIENT_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

收到回覆

```
ERROR: {
  "codespace":8,
  "code":14,
  "abci_code":524302,
  "message":"Current block height is 46046996, the swap expire height(46043293) is passed"
}
```

XD，超過 swap block height 了，受方這邊逾時去存錢整個 swap expired，不能在做什麼事

發方去透過 refund 解鎖

# Refund HTLT

若是已經 complete 或是 timeout expired，發起 HTLT 的 address 可以透過 refund 來取回資產

```
tbnbcli token refund \
  --swap-id ${SWAP_ID} \
  --from ${FROM_ADDR}  \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

回覆 tx 的狀態，[可以在explorer 上看到](https://testnet-explorer.binance.org/tx/F0F5AB40EF7B1CCFE54EBAE0B8022E9B3C381D0029C55A8FE7C3C87E8ACF800D)，transaction type 為 refund swap

```
Committed at block 46047771 (
  tx hash: F0F5AB40EF7B1CCFE54EBAE0B8022E9B3C381D0029C55A8FE7C3C87E8ACF800D, 
  response: {
    Code:0 
    Data:[] 
    Log:Msg 
    0:  
      Info: 
        GasWanted:0 
        GasUsed:0 
        Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[114 101 102 117 110 100 72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] 
        Codespace: 
          XXX_NoUnkeyedLiteral:{} 
          XXX_unrecognized:[] 
          XXX_sizecache:0
  }
)
```

重新查詢 swap 狀態，已經變成 expired

```
tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80

{
	"from": "tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce",
	"to": "tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p",
	"out_amount": [{
		"denom": "BNB",
		"amount": "3"
	}],
	"in_amount": null,
	"expected_income": "1:BNB",
	"recipient_other_chain": "",
	"random_number_hash": "2c2588c81a5f08bf55a183cc2d61a123368405638741169933e200c90f4532e5",
	"random_number": "",
	"timestamp": "1571905650",
	"cross_chain": false,
	"expire_height": "46043293",
	"index": "2239",
	"closed_time": "1571908256",
	"status": "Expired"
}
```

---

再來一次XD，把 height span 拉長一點

# Deposit HTLT

可以成功 deposit

# Claim HTLT

針對每筆 HTLT ，解鎖鎖住的 assets。每個 HTLT 只能被解鎖一次。

```
tbnbcli token claim \
  --swap-id  <swapID> \
  --random-number <random-number> \
  --from <from-key> \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```


---

# 從 Binance Chain swap 到 ethereum

增加兩個參數

* recipient-addr <deputy-bep2-addr>
* recipient-other-chain <client ethereum address> \

```
./tbnbcli token HTLT \
  --from <from-addr> \
  --chain-id Binance-Chain-Nile  \
  --height-span <heightSpan> \
  --amount <amount> \
  --expected-income <expectedIncome> \
  --recipient-addr <deputy-bep2-addr>  \
  --recipient-other-chain <client ethereum address> \
  --cross-chain \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

# 從 Ethereum swap 到 Binance Chain

```
./tbnbcli token HTLT \
  --from  <from-addr> \
  --chain-id Binance-Chain-Nile \
  --height-span  <heightSpan>  \
  --amount <amount> \
  --expected-income <expectedIncome> \
  --recipient-other-chain <deputy ethereum address> \
  --sender-other-chain <client ethereum address> \
  --recipient-addr <client bep2 address> \
  --cross-chain \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

---

架設 swap deputy，實現自動 atomic swap

# Prerequisites

git clone git@github.com:binance-chain/bep3-deputy.git

# References

* [Binace Chain Doc](https://docs.binance.org/atomic-swap.html)
* [Binance BEP3 spec](https://github.com/binance-chain/BEPs/blob/master/BEP3.md)
