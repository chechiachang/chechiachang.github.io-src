---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Blockchain Bep3 Atomic Swap"
subtitle: ""
summary: ""
authors: []
tags: ["blockchain", "bep3", "binance", "ethereum","erc-20"]
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

### 動機

在部署 asset / token 的時候，我們會選擇合適的鏈作為發布資產並運行 block chain app。常用的應用鏈如 ethereum 與 binance chain 等等。不同的主鏈上有各自的優缺點，例如使用 ethereum ，可以與許多 token 與應用互動，也是最多人使用的應用主鏈。而在 binance 鏈上執行，則能夠快速的發生 transactions，並且可以與 binance 上的資產與交易所互動。

在某些應用場景，我們會希望兩個獨立主鏈上的資產能後互動，例如在 binance chain 上執行快速的 transaction，然而也要使用 etheruem 上既有的 ERC-20 tokens，這時便需要一個溝通兩條鏈的機制。

我們今天會實作 Atomic Peg Swap，透過 HTLT 鎖住兩邊鏈上的資產，再原子性的一次交易，來達成不同鏈上的資產互換。

### BEP3 Atomic Swap

Binance 在 [BEP3: HTLC and Atomic Peg](https://github.com/binance-chain/BEPs/blob/master/BEP3.md) 提到，BEP 即將在 binance chain 上支援原生的 Hash Timer Locked Transfer (HTLT) ，這使跨鏈的原子性交換 (atomic swap) 變得可行，透過 HTLC 在兩邊的鏈上鎖住 (peg) tokens，然後只有在執行交換的時候，透過 hash 交換，一次執行雙邊的交易。

主要的資訊來源來自 binance.org 的[官方說明文件](https://docs.binance.org/atomic-swap.html)，這邊針對文章進行驗證，並且補足過程中可能會踩到的雷。

---

### Outline

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

### 運作流程

(TODO)

---

# Task 1: 使用 bnbcli 交換資產

### 取得 tbnbcli

[tbnbcli 的說明文件](https://docs.binance.org/api-reference/cli.html)

由於 bnbcli repo 中使用 Git Large File Storage 來存放 binary，這邊要啟用 git-lfs 來下載 binary
```
# Mac port
sudo port install git-lfs
```

Git clone repo
```bash
git clone git@github.com:binance-chain/node-binary.git
cd node-binary

git chechout v0.6.2
git lfs pull --include cli/testnet/0.6.2/mac/tbnbcli
sudo copy cli/testnet/0.6.2/mac/tbnbcli /usr/local/bin
```

這邊要注意使用 v0.6.2+ 的版本，不然會沒有 HTLT 的 subcommands

### 測試 tbnbcli

```bash
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

### Acquire Valid Binance Testnet Account

Check [Testnet Doc](https://www.binance.com/en/support/articles/360023912272)

* Go to [Binance Testnet](https://testnet.binance.org/en/)
* Create a wallet
* Save address, mn, keystore, private key
* Use [testnet faucet](https://www.binance.vision/tutorials/binance-dex-funding-your-testnet-account) to fund testnet account
* Receive 200 BNB on testnet

### Acquire Ropsten (ethereum testnet) Address

---

### HTLT

這邊使用簡單的範例，鎖住兩個 BEP2 tokens 來進行交換，展示一下 tbnbcli 的 HTLT

準備兩個 address，這邊是我自己的兩個 testnet address

* tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p (179 BNB) [Explorer 上查看](https://testnet-explorer.binance.org/address/tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p)
* tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce (20 BNB) [Exporler 上查看](https://testnet-explorer.binance.org/address/tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce)

目標：

* HTLT
* tbnb...j9p -> 3 BNB -> tbnb...7ce
* tbnb...j9p <- 1 BNB <- tbnb...7ce

參數：

* hightspan: 360

tbnbcli 執行 HTLT，從 from address 執行 HTLT，給 recipient-addr amount 的 token，並預期對方回 expected-income，等待 height-span 個 block 時間(360 > 2 minutes)

height-span 是發起 HTLT，受方 deposit，發方去 claim 的時限。

```bash
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

```bash
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

```bash
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

```bash
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

### Query Atomic Swap

產生了 atomic swap，這邊可以使用 tbnbcli 查詢 swap 的狀態

```bash
SWAP_ID=4e29c60f73175e985735e1c50cb674e5f6fa371909667f30de88362c9b27819b 

tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

回傳 swap 的狀態

```json
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

### Deposit HTLT

受方 reciept-address 這邊要把 1 BNB 打進去 swap 中

注意這邊的 from-address 已經變成當初的 recipient-addr tbnb...j9p

當然這邊要存取，也要有 tbnb...j9p 的 key，這樣我們本地就會有發受兩方的 key，但一般來說應該是兩個不同的人

```bash
tbnbcli keys add tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p--recover

tbnbcli keys list

NAME:	                                      TYPE:	ADDRESS:						                        PUBKEY:
tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	local	tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	bnbp1addwnpepq0pw06d3y7ykg2j33pc604j3awgqgl5vhd88wdjhjg5sptnsfpqyx2rmhl4
tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p	local	tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p	bnbp1addwnpepqwk5zx3jnrq5guxc9tsgrte9aw9knla0ahunwynypkm0jvst6y7l2q83ueq
```

受方把約好的錢存進去

```bash
tbnbcli token deposit \
  --swap-id ${SWAP_ID}  \
  --amount 1:BNB \
  --from ${RECIPIENT_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

收到回覆

```json
ERROR: {
  "codespace":8,
  "code":14,
  "abci_code":524302,
  "message":"Current block height is 46046996, the swap expire height(46043293) is passed"
}
```

XD，超過 swap block height 了，受方這邊逾時去存錢，導致整個 swap expired，不能在做什麼事

發方去透過 refund 解鎖

### Refund HTLT

若是已經 complete 或是 timeout expired，發起 HTLT 的 address 可以透過 refund 來取回資產

```bash
tbnbcli token refund \
  --swap-id ${SWAP_ID} \
  --from ${FROM_ADDR}  \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

回覆 tx 的狀態，[可以在explorer 上看到](https://testnet-explorer.binance.org/tx/F0F5AB40EF7B1CCFE54EBAE0B8022E9B3C381D0029C55A8FE7C3C87E8ACF800D)，transaction type 為 refund swap

```bash
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

```bash
tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

```json
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

### 再來一次XD

這次我們動作快一點

Create HTLT

```bash
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

Random number: d31d3ae2fa19af574f8cdc2550e5f22bc73c647134b92b864b2c046a56034834
Timestamp: 1571913062
Random number hash: b084835ee18524841ebab84ea80e97e53dc63308d7177a5d50de565d016f34b5
Password to sign with 'tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p':
Committed at block 46056697 (
  tx hash: 883787539F504093701FDB2E61526F6CF5715721DB621BFAE63CFD8C27E331FB, 
  response: {
    Code:0 
    Data:[24 201 56 185 148 198 43 204 233 232 206 220 180 38 166 3 134 61 149 86 90 36 108 50 58 29 248 157 92 66 38 193] 
    Log:Msg 
    0: 
      swapID: 18c938b994c62bcce9e8cedcb426a603863d95565a246c323a1df89d5c4226c1 
      Info: 
        GasWanted:0 
        GasUsed:0 
        Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 104 113 54 118 52 57 97 110 51 119 119 104 114 100 56 110 121 55 113 106 51 101 120 103 102 109 118 112 118 117 101 108 107 99 97 106 57 112] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}]
        Codespace: 
          XXX_NoUnkeyedLiteral:{} 
          XXX_unrecognized:[] 
          XXX_sizecache:0
  }
)
```

發方沒有指定 random number hash，這邊自動產生，記得要記下
```bash
RANDOM_NUMBER=70b85d0ef8f3887ba24fc80bebd2430bc3ae79a7dd71f54b157f52fcdb9284a2
```

### 受方 deposit

```bash
SWAP_ID=c2be98ac3b9ee7153e5ba84edfefca1917b6e2ec72d2576bf6cce584cbd6095e

tbnbcli token deposit \
  --swap-id ${SWAP_ID}  \
  --amount 1:BNB \
  --from ${RECIPIENT_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

可以成功 deposit，[檢查這次 tx Deposit swap 的內容](https://testnet-explorer.binance.org/tx/5C1BA1E79E53BD622BEC602DA7615B370851F18E47AB97AD29C93F3B1229078B)

```bash
Committed at block 46056751 (
  tx hash: 5C1BA1E79E53BD622BEC602DA7615B370851F18E47AB97AD29C93F3B1229078B, 
  response: {
    Code:0 
    Data:[] 
    Log:Msg 
    0:  
      Info: 
        GasWanted:0 
        GasUsed:0 
        Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[100 101 112 111 115 105 116 72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] 
      Codespace: 
        XXX_NoUnkeyedLiteral:{} 
        XXX_unrecognized:[] 
        XXX_sizecache:0
  }
)
```

### Claim HTLT

針對每筆 HTLT ，解鎖鎖住的 assets。每個 HTLT 只能被解鎖一次。

```bash
tbnbcli token claim \
  --swap-id  ${SWAP_ID} \
  --random-number ${RANDOM_NUMBER} \
  --from ${FROM_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80

Committed at block 46056769 (
  tx hash: 15790AF6A17F2300553ADDA776FACBF9DF1B913EB8ECE276F8D8EC78D549A63B, 
  response: {
    Code:0 
    Data:[] 
    Log:Msg 
    0:  
      Info: 
        GasWanted:0 
        GasUsed:0 
        Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 104 113 54 118 52 57 97 110 51 119 119 104 114 100 56 110 121 55 113 106 51 101 120 103 102 109 118 112 118 117 101 108 107 99 97 106 57 112] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[99 108 97 105 109 72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] 
        Codespace: 
          XXX_NoUnkeyedLiteral:{} 
          XXX_unrecognized:[] 
          XXX_sizecache:0
  }
)
```

查詢 swap 狀態，從 open 變成 completed

```bash
tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

```json
{
	"from": "tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p",
	"to": "tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce",
	"out_amount": [{
		"denom": "BNB",
		"amount": "3"
	}],
	"in_amount": [{
		"denom": "BNB",
		"amount": "1"
	}],
	"expected_income": "1:BNB",
	"recipient_other_chain": "",
	"random_number_hash": "b084835ee18524841ebab84ea80e97e53dc63308d7177a5d50de565d016f34b5",
	"random_number": "d31d3ae2fa19af574f8cdc2550e5f22bc73c647134b92b864b2c046a56034834",
	"timestamp": "1571913062",
	"cross_chain": false,
	"expire_height": "46057057",
	"index": "2241",
	"closed_time": "1571913109",
	"status": "Completed"
}
```

---

TODO 分另外一篇

# 從 Ethereum swap 到 Binance Chain

這邊我們要從 ethereum 上，將 ERC-20 token 與 binance chain 上的 BNB 做交換

### 準備需要用到的東西

##### binance testnet

* 準備好 address 與 BNB，這邊沿用我們上篇使用的 address [tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p](https://testnet-explorer.binance.org/address/tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p)

##### ethereum testnet (ropsten)

* Admin Address [[ropsten etherscan]](https://ropsten.etherscan.io/address/0x938a452d293c23c2cdeae0bf01760d8ecc4f826b)
* 部署 ERC20 token [[ropsten etherscan]](https://ropsten.etherscan.io/address/0xDec348688B060fB44144971461b3BAaC8BD1e571)，我自己發行的 [Party Parrot Token (PPT)](https://ropsten.etherscan.io/token/0xDec348688B060fB44144971461b3BAaC8BD1e571) ![](https://cultofthepartyparrot.com/parrots/hd/parrot.gif)
* ERC20 Atomic Swapper 智能合約
  * [binance-chain/bep3-smartcontract](https://github.com/chechiachang/bep3-smartcontracts) 提供

##### Node/VM

* 用來執行 bep3 deputy process 
  * [https://github.com/binance-chain/bep3-deputy](https://github.com/binance-chain/bep3-deputy) 提供

### workflow

我們看一下官方提供的這張圖

![](https://docs.binance.org/assets/eth2bnc.png)

1. Wallet Address 在 ERC20 Token (PPToken) approve() Swap Contract 一部分 Token
2. 初始化 Swap Transaction(tx)
3. Deputy 監測到 Ethereum 鏈上的 swap tx，向 Binance Chain 發起一個對應的 HTLT tx，等待 Binance 上的 claim tx
4. Wallet Address 向 Binance Chain 執行 HTLT claim()
5. Deputy 監測到 Binance Chain 上的 claim tx 與 swap complete，代為向 Ethereum claim ERC-20

### 執行 deputy

我們可以先將 deputy 程序跑起來，這邊使用的是 [Binance Chaing/bep3-deputy](https://github.com/binance-chain/bep3-deputy)

```bash
go get github.com/binance-chain/bep3-deputy
cd ${GOPATH}/src/github.com/binance-chain/bep3-deputy

$ go mod download
$ make build
go build  -o build/deputy main.go
```

啟動本地 MySQL，這邊直接用 docker 起一個無密碼的
```
$ docker run \
  --name some-mysql \
  -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
  -e MYSQL_DATABASE=deputy \
  -d \
  mysql:5.7.27
```

設定 config/confg.json

```json
{
  "db_config": {
    "dialect": "mysql",
    "db_path": "root:@(localhost:3306)/deputy?charset=utf8&parseTime=True&loc=Local",
  },
  "chain_config": {
    "bnb_start_height": 42516056,

    "other_chain": "ETH",
    "other_chain_start_height": 6495598
  },
  "admin_config": {
    "listen_addr": "127.0.0.1:8080"
  },
  "bnb_config": {
    "key_type": "mnemonic",
    "mnemonic": "<my-mnemonic>",
    "rpc_addr": "tcp://data-seed-pre-0-s1.binance.org:80",
    "symbol": "BNB",
    "deputy_addr": "tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce",
    "fetch_interval": 2,
  },
  "eth_config": {
    "swap_type": "erc20_swap",
    "key_type": "private_key",
    "private_key": "<my-private-key>",
    "provider": "https://ropsten.infura.io/v3/cd9643b1870b489b93477921cb767882",
    "swap_contract_addr": "0xA08E0F38462eCd107adE62Ee3004850f2448f3d6",
    "token_contract_addr": "0xDec348688B060fB44144971461b3BAaC8BD1e571",
    "deputy_addr": "0x938a452d293c23C2CDEae0Bf01760D8ECC4F826b",
    "gas_limit": 300000,
    "gas_price": 20000000000,
  }
}
```

這樣注意幾個地方

* db_config 填上 mysql url，有設密碼的話一並帶入
* chain_config.bnb_start_height 可以先追到目前的 block height，畢竟我們的 swap tx 都在 deputy 起來之後才會產生，可以跳過啟動時 sync block 的時間。如果是要追過去的 tx，就要調整 block 的高度，並且給予足夠的時間上 deputy 去 sync block。可以到 [testnet-explorer](https://testnet-explorer.binance.org/) 查目前的 block height。
* chain_config.other_chain_start_height 也追到最新的 eth block height，可以到 [Etherscan](https://ropsten.etherscan.io/) 查目前的 block height
* bnb_config 填上 bnb addr 與助記祠
* eth_config 填上 eth addr 與 private key
* eth_config.deupty_addr 使用 Admin addr，並填上 private key

把 deputy 以 testnet 為目標執行起來

```bash
./build/deputy --help

./build/deputy \
  --bnb-network 0 \
  --config-type local \
  --config-path config/config.json

2019-10-25 17:16:48 DEBUG Debug sent a request
2019-10-25 17:16:48 INFO fetch ETH cur height: 6641795
2019-10-25 17:16:48 DEBUG Debug sent a request
2019-10-25 17:16:48 DEBUG Debug sent a request
2019-10-25 17:16:48 INFO fetch BNB cur height: 46215517
2019-10-25 17:16:48 DEBUG Debug sent a request
2019-10-25 17:16:48 INFO fetch try to get ahead block, chain=BNB, height=46215518
```

deputy 啟動後，就會依據 db 中的 block 資料，開始一路追 block，發現是相關的 addr 就把 tx 拉下來處理。

由於我們這邊是新 db，我們又直接跳到最新的 block，應該不會需要太多時間就能追上。

deputy 有 admin api 可以使用
```bash
curl http://localhost:8080

curl http://localhost:8080/failed_swaps/1
the number of total failed swaps is 0, the offset of query is 0

curl http://localhost:8080/status
```

```json
{
    "mode": "NormalMode",
    "bnb_chain_height": 46215719,
    "bnb_sync_height": 46215718,
    "other_chain_height": 6641804,
    "other_chain_sync_height": 6641804,
    "bnb_chain_last_block_fetched_at": "2019-10-25T17:18:52+08:00",
    "other_chain_last_block_fetched_at": "2019-10-25T17:18:40+08:00",
    "bnb_status": {
        "balance": [
            {
                "symbol": "BNB",
                "free": "18.99812504",
                "locked": "0.00000000",
                "frozen": "0.00000000"
            }
        ]
    },
    "other_chain_status": {
        "allowance": "9.8e+13",
        "erc20_balance": "9.999999969e+20",
        "eth_balance": "6.982922764"
    }
}
```

可以看到 deputy 上設定的 bnb_addr, eth_addr 的狀態 

* other_chain_status.allowance: 9.8e+13

---

### References

* [Binace Chain Doc](https://docs.binance.org/atomic-swap.html)
* [Binance BEP3 spec](https://github.com/binance-chain/BEPs/blob/master/BEP3.md)
