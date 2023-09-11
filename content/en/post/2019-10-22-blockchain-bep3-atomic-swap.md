---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Blockchain Bep3 Atomic Swap"
subtitle: ""
summary: ""
authors: []
tags: ["blockchain", "bep3", "binance", "ethereum","erc-20"]
categories: ["blockchain"]
date: 2019-10-22T10:35:20+08:00
lastmod: 2019-10-22T10:35:20+08:00
featured: false
draft: false

#menu:
#  main:
#    parent: "Blockchain"
#    weight: 1
---

# BEP3 Atomic Swap

Binance 在 [BEP3: HTLC and Atomic Peg](https://github.com/binance-chain/BEPs/blob/master/BEP3.md) 提到，BEP 即將在 binance chain 上支援原生的 Hash Timer Locked Transfer (HTLT) ，這使跨鏈的原子性交換 (atomic swap) 變得可行，透過 HTLC 在兩邊的鏈上鎖住 (peg) tokens，然後只有在執行交換的時候，透過 hash 交換，一次執行雙邊的交易。

關於 Atomic Swap 網路有非常多的訊息，有興趣的話可以看[這篇](https://en.bitcoin.it/wiki/Atomic_swap)

* 交易只有在雙邊完成後才完成，完成之前不能動用交換的資產
* 在任何階段失效都可以完全 fallback，並進行 refund
* 交易的認證是去中心化的 
  * 這邊有個但書，Ethereum 上是透過 smart contract 實現，但 Binance chain 上還是靠 Binance 認證 XD

Binance 在 BEP3 中支援 HTLC，我們這邊主要的資訊來源是 binance.org 的[官方說明文件](https://docs.binance.org/atomic-swap.html)，這邊針對文章進行驗證，並且補足文件缺漏的部分，提醒過程中可能會踩到的雷。

### 跨鍊(Cross Chain) 交易

在部署 asset / token 的時候，我們會選擇合適的鏈作為發布資產並運行 block chain app。常用的應用鏈如 ethereum 與 binance chain 等等。不同的主鏈上有各自的優缺點，例如使用 ethereum ，可以與許多 token 與應用互動，也是最多人使用的應用主鏈。而在 binance 鏈上執行，則能夠快速的發生 transactions，並且可以與 binance 上的資產與交易所互動。

在某些應用場景，我們會希望兩個獨立主鏈上的資產能後互動，例如在 binance chain 上執行快速的 transaction，然而也要使用 etheruem 上既有的 ERC-20 tokens，這時便需要一個溝通兩條鏈的機制。

### 文章分為三個部分

* <a href="#swap-on-binance-chain">在 Binance Chain 上互換兩個 address 的 binance asset</a>
* <a href="#from-ethereum-to-binance-chain">從 ethereum token 到 binance</a>
* <a href="#from-binance-chain-to-ethereum">從 binance chain 到 ethereum</a>

---

### Atomic Swap on Binance Chain {#swap-on-binance-chain}

我們今天會實作 Atomic Peg Swap，透過 HTLT 鎖住 Binance Chain 上兩個 address 的資產，並進行原子性的一次交易，來達成鏈上的資產互換。這邊直接使用 binance 提供的 bnbcli 來執行。

### 使用情境

兩個在 Binance Chain 上的 address 想交換資產

* Client: HTLT 的發起方，擁有一部分 asset，發起 HTLT 希望執行資產互換
* Recipient: HTLT 的收受方，收到 HTLT，需要於時限內 deposit 指定數量的資產到 swap 中

### 服務元件

* HTLT transactions on binance chain: 來鎖住並 claim assets
* Client tooling: tbnbcli 讓客戶可以操作，監測鏈上 swap 的狀況

### 流程

1. Client 使用 tbnbcli 發起 HTLT
1. Recipient 收到發起方送來的 swap info 與 asset (frozen)
1. Recipient Deposit 指定數量的 asset 到 swap 中
1. Binance Chain 自動完成 swap，完成交換，解鎖兩邊交換的資產

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

---

### Client Create HTLT

這邊使用簡單的範例，鎖住兩個 BEP2 tokens 來進行交換，展示一下 tbnbcli 的 HTLT

準備兩個 address，這邊是我自己的兩個 testnet address

* tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p (179 BNB) [Explorer 上查看](https://testnet-explorer.binance.org/address/tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p)
* tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce (20 BNB) [Exporler 上查看](https://testnet-explorer.binance.org/address/tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce)

目標：

* HTLT
* tbnb...j9p -> 0.3 BNB -> tbnb...7ce
* tbnb...j9p <- 0.1 BNB <- tbnb...7ce

tbnbcli 執行 HTLT，從 from address 執行 HTLT，給 recipient-addr 0.3 BNB，並預期對方回 0.1 BNB，等待 height-span 個 block 時間(360 > 2 minutes)

### tbnbcli key

實際執行前，由於我們需要透過 tbnbcli 操作 from-address，要先[透過 tbnbcli 把 address 的 key 加進到本地](https://docs.binance.org/keys.html)

```bash
tbnbcli keys add tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce --recover

tbnbcli keys list

NAME:	                                      TYPE:	ADDRESS:						                        PUBKEY:
tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	local	tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce	bnbp1addwnpepq0pw06d3y7ykg2j33pc604j3awgqgl5vhd88wdjhjg5sptnsfpqyx2rmhl4
```

### 實際執行

參數：

* FROM ADDR: tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p
* RECIPIENT ADDR: tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce
* hightspan: 3600，height-span 是發起 HTLT，受方 deposit，發起方去 claim 的時限。
* amount: asset * 10^8

* tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p 執行 HTLT
* 給 tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce 0.3 BNB
* 預期對方回 0.1 BNB
* 等待 3600 個 block 時間

```bash
FROM_ADDR=tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p
RECIPIENT_ADDR=tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce
HEIGHT_SPAN=3600

tbnbcli token HTLT \
  --recipient-addr ${RECIPIENT_ADDR} \
  --amount 30000000:BNB \
  --expected-income 10000000:BNB \
  --height-span ${HEIGHT_SPAN} \
  --from ${FROM_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

產生 swap 的結果，可以於[Testnet Explorer 上看到](https://testnet-explorer.binance.org/tx/8F865C5C9E5CD06239DE99746BCE73AACA2F3AD881C26765FB90C9465EF06EF0)

```bash
Committed at block 47218942 (tx hash: 8F865C5C9E5CD06239DE99746BCE73AACA2F3AD881C26765FB90C9465EF06EF0, response: {Code:0 Data:[77 138 29 51 186 65 213 125 105 217 5 102 170 194 248 149 189 188 56 208 166 93 48 159 188 196 143 111 31 66 151 249] Log:Msg 0: swapID: 4d8a1d33ba41d57d69d90566aac2f895bdbc38d0a65d309fbcc48f6f1f4297f9 Info: GasWanted:0 GasUsed:0 Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 104 113 54 118 52 57 97 110 51 119 119 104 114 100 56 110 121 55 113 106 51 101 120 103 102 109 118 112 118 117 101 108 107 99 97 106 57 112] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] Codespace: XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0})
```

### Query Atomic Swap

產生了 atomic swap，這邊可以使用 tbnbcli 查詢 swap 的狀態

```bash
SWAP_ID=4d8a1d33ba41d57d69d90566aac2f895bdbc38d0a65d309fbcc48f6f1f4297f9

tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

回傳 swap 的狀態

```json
{"from":"tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p","to":"tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce","out_amount":[{"denom":"BNB","amount":"30000000"}],"in_amount":null,"expected_income":"10000000:BNB","recipient_other_chain":"","random_number_hash":"4cf88f1acf8bcbc628609f3257406913f67e009e5c61f2671b601e40f4e5cc6a","random_number":"","timestamp":"1572506189","cross_chain":false,"expire_height":"47222542","index":"2254","closed_time":"0","status":"Open"}
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
  --amount 10000000:BNB \
  --from ${RECIPIENT_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

可以成功 deposit，[檢查這次 tx Deposit swap 的內容](https://testnet-explorer.binance.org/tx/FDCC528B9F98E9CEEDCB113A398A747F440666061340535D44C526D79F9CD667)

```bash
Password to sign with 'tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce':
Committed at block 47219070 (tx hash: FDCC528B9F98E9CEEDCB113A398A747F440666061340535D44C526D79F9CD667, response: {Code:0 Data:[] Log:Msg 0:  Info: GasWanted:0 GasUsed:0 Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[100 101 112 111 115 105 116 72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] Codespace: XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0})
```

### 發起方 Claim HTLT

針對每筆 HTLT ，解鎖鎖住的 assets。每個 HTLT 只能被解鎖一次。

```bash
tbnbcli token claim \
  --swap-id  ${SWAP_ID} \
  --random-number ${RANDOM_NUMBER} \
  --from ${FROM_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

可以成功 claim，[檢查這次 tx Deposit swap 的內容](https://testnet-explorer.binance.org/tx/D08F81D0315F0A7B13E510782F6E56804803B5198F4914C8EB10E3A5084F2BAA)

```bash
Password to sign with 'tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p':
Committed at block 47219128 (tx hash: D08F81D0315F0A7B13E510782F6E56804803B5198F4914C8EB10E3A5084F2BAA, response: {Code:0 Data:[] Log:Msg 0:  Info: GasWanted:0 GasUsed:0 Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 104 113 54 118 52 57 97 110 51 119 119 104 114 100 56 110 121 55 113 106 51 101 120 103 102 109 118 112 118 117 101 108 107 99 97 106 57 112] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[99 108 97 105 109 72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] Codespace: XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0})
```

### 查詢 swap 狀態

從 open 變成 completed

```bash
tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

```json
{"from":"tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p","to":"tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce","out_amount":[{"denom":"BNB","amount":"30000000"}],"in_amount":[{"denom":"BNB","amount":"10000000"}],"expected_income":"10000000:BNB","recipient_other_chain":"","random_number_hash":"4cf88f1acf8bcbc628609f3257406913f67e009e5c61f2671b601e40f4e5cc6a","random_number":"cb5f6296078fd73b86d03eb58bc8a6e0af8d4b60c1cd678b71f8c185e206db53","timestamp":"1572506189","cross_chain":false,"expire_height":"47222542","index":"2254","closed_time":"1572506323","status":"Completed"}
```

這樣 swap 就完成了

### 超時 (Expired) 處理

由於 HTLT 是有時間限制，有可能會超時，會無法繼續操作，例如另外一筆 HTLT 在受方 deposit 時無法 deposit

```bash
tbnbcli token deposit \
  --swap-id ${SWAP_ID}  \
  --amount 1:BNB \
  --from ${RECIPIENT_ADDR} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

```json
ERROR: {
  "codespace":8,
  "code":14,
  "abci_code":524302,
  "message":"Current block height is 46046996, the swap expire height(46043293) is passed"
}
```

超過 swap block height 了，受方這邊逾時去存錢，導致整個 swap expired，不能在做什麼事

發起方去透過 refund 解鎖

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

# 從 Ethereum swap 到 Binance Chain {#from-ethereum-to-binance-chain}

這邊我們要從 ethereum 上，將 ERC-20 token 與 binance chain 上的 BNB 做交換，先準備需要用到的東西

### binance testnet

* 準備好 address 與 BNB，這邊沿用我們上篇使用的 address [tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p](https://testnet-explorer.binance.org/address/tbnb1hq6v49an3wwhrd8ny7qj3exgfmvpvuelkcaj9p)

### ethereum testnet (ropsten)

* Admin Address [[ropsten etherscan]](https://ropsten.etherscan.io/address/0x938a452d293c23c2cdeae0bf01760d8ecc4f826b)
* 部署 ERC20 token [[ropsten etherscan]](https://ropsten.etherscan.io/address/0xDec348688B060fB44144971461b3BAaC8BD1e571)，我自己發行的 [Party Parrot Token (PPT)](https://ropsten.etherscan.io/token/0xDec348688B060fB44144971461b3BAaC8BD1e571) ![](https://cultofthepartyparrot.com/parrots/hd/parrot.gif)
* 部署 ERC20 Atomic Swapper 智能合約
  * [binance-chain/bep3-smartcontract](https://github.com/chechiachang/bep3-smartcontracts) 提供

### Node/VM

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

* db_config 填上 mysql url，有設密碼的話一併帶入
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

# 開始 Swap

複習一下流程

![](https://docs.binance.org/assets/eth2bnc.png)

0. 部署好 swap contract & deputy，啟動 deputy process
1. Wallet Address 在 ERC20 Token (PPToken) approve()，給 Swap Contract 一部分 Token
2. 初始化 Swap Transaction(tx)
3. Deputy 監測到 Ethereum 鏈上的 swap tx，向 Binance Chain 發起一個對應的 HTLT tx，等待 Binance 上的 claim tx
4. Wallet Address 向 Binance Chain 執行 HTLT claim()
5. Deputy 監測到 Binance Chain 上的 claim tx 與 swap complete，代為向 Ethereum claim ERC-20

### ERC20 contract Approve() 

到 ERC20 contract 的頁面，選擇 approve 

spender: swap contract address
value: 10000 PPToken (乘上 10^18)

[到 etherscan 上查看](https://ropsten.etherscan.io/address/0xdec348688b060fb44144971461b3baac8bd1e571#events)

### Call HTLT function

Go to swap contract，call  htlt()

用 etherscan 送上去，然後就壞掉了，[Etherscan 上壞掉的 tx](https://ropsten.etherscan.io/tx/0xbd0c829ad2466fcd6e49a12bbac1849827fb9e7a251271816401ed4c9bfe2fa8) 不知為什麼 QAQ

{{< figure library="1" src="bep3-atomic-swap-failure-01.jpg" height="70%" width="70%" title="" >}}
{{< figure library="1" src="bep3-atomic-swap-failure-02.jpg" height="70%" width="70%" title="" >}}

開 remix IDE，重新嘗試參數

* randomNumberHash: 
  * SHA256(randomNumber||timestamp), randomNumber is 32-length random byte array. 
  * 0x0000000000000000000000000000000000000000000000000000000000000000
* timestamp: 
  * it should be about 10 mins span around current timestamp. [unix timestamp](https://www.unixtimestamp.com/) 
  * 1572250902 (now + 60 sec * 10 min)
* heightSpan: 
  * it's a customized filed for deputy operator. it should be more than 200 for this deputy.
  * 10000
* recipientAddr: 
  * deputy address on Ethereum. 
  * 0x938a452d293c23C2CDEae0Bf01760D8ECC4F826b
* bep2SenderAddr: 
  * omit this field with 0x0
  * 0x0000000000000000000000000000000000000000
* bep2RecipientAddr: 
  * Decode your testnet address from bech32 encoded to hex
  * 0xee82ca237387495e9603f4d8d7efed128bdd59a6
* outAmount: 
  * approved amount, should be bumped by e^10. 
  * 10 0000000000
* bep2Amount: 
  * outAmount * exchange rate, the default rate is 1. 
  * 10 0000000000

### Deputy Call HTLT on Binance Chain

Deputy 監測 Ethereum 上的 block 狀態，特別是會取得 Swap contract address 的 swap tx，並在 Binance Chain 上產生對應的 HTLT。

### Claim HTLT on Binance Chain

Binance Chain 上產生 HTLT 後，客戶端這邊可以使用 tbnb 以 recipient addr 查詢 Binance Chain 上的 Swap ID

```bash
tbnbcli token query-swapIDs-by-recipient  \
  --recipient-addr tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

獲得過去產生的 swap list

```json
[
  "c2be98ac3b9ee7153e5ba84edfefca1917b6e2ec72d2576bf6cce584cbd6095e",
  "18c938b994c62bcce9e8cedcb426a603863d95565a246c323a1df89d5c4226c1",
  "5c4fdd60ce44fa4be6de70e65df3f8295df88178fd381b4242a8c2d047663a1b",
  "a47c89dfca910cbb34dec92acebebb59d2c62e7f90bf216a87c2c23c84e48d4f"
]
```

都是過去使用的 swap id，如果都沒有新的 swap 出來，可能是 height span 太高，導致一直都爬不到

```
SWAP_ID=c2be98ac3b9ee7153e5ba84edfefca1917b6e2ec72d2576bf6cce584cbd6095e
tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

這邊要對一下 random number, to wallet addr, out amount 等參數，如果 HTLT 符合，客戶就可以執行 Claim HTLT

```
tbnbcli token claim \
  --swap-id ${SWAP_ID} \
  --random-number ${RANDOM_NUMBER} \
  --from ${FROM_KEY} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

### Deputy Claim ERC20 Token

客戶端在 Binance Chain 上 Claim HTLT，Deputy 在 Ethereuem 上 Claim HTLT，至此完成 Atomic Swap 兩邊的流程。客戶端從 Binance Chain Claim，Deputy 從 Ethereuem 上 Claim。完整流程
如下：

* Client Call HTLT on Ethereum -> Deputy Call HTLT on Binance Chain
* Client Check HTLT Status on Binance Chain
* Client Call Claim HTLT on Binance Chain -> Deputy Call Claim HTLT on Ethereum

### Client APP javascript Demo

[希望直接寫成 javascript app 可以參考這篇](https://docs.binance.org/atomic-swap.html#6-demo-for-client-app-swap-erc20-to-bep2)

---

# Swap Tokens from Binance Chain to Ethereum {#from-binance-chaing-to-ethereum}

這邊進行反向操作，客戶發起從 Binance Chain 換到 Ethereum 上的請求，Deputy 做對應的處理，把 Token Swap 到 Ethereum。我們依樣依照[這份文件](https://docs.binance.org/atomic-swap.html#swap-tokens-from-binance-chain-to-ethereum)操作。

1. 客戶端在 Binance Chain 上 Call HTLT()
2. Deputy 在 Ethereum 上 Init Swap tx
3. Deputy Call Approve() 到 ethereum swap contract
4. 客戶端取得 swap 資訊
5. 客戶端在 Ethereum 上 Call Claim()，取得 ERC-20 Token
6. Deputy 在 Binance 上 Call Claim()，取得 Binance Chain Token

### 在 Binance Chain 上 HTLT

客戶端發起 HTLT 請求，需要從客戶端 Wallet 送出（但因為我們這邊只使用一個 Binance Address，所以發起的 Addr 跟 Deputy Binance addr 是一樣的。

這邊鎖進 10:BNB，等待 100:PPT 從 ethereum 近來

```
DEPUTY_BNB_WALLET_ADDR=tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce
CLIENT_BNB_WALLET_ADDR=${DEPUTY_BNB_WALLET_ADDR}
CLIENT_ETHEREUM_ADDR=0x938a452d293c23C2CDEae0Bf01760D8ECC4F826b

tbnbcli token HTLT \
  --from ${CLIENT_BNB_WALLET_ADDR} \
  --recipient-addr ${DEPUTY_BNB_WALLET_ADDR}  \
  --chain-id Binance-Chain-Nile  \
  --height-span 500 \
  --amount  10:BNB  \
  --expected-income 100:PPT  \
  --recipient-other-chain ${CLIENT_ETHEREUM_ADDR}  \
  --cross-chain \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

HTLT 回復的結果如下，可以在[Binance Testnet Explorer](https://testnet-explorer.binance.org/tx/D653FC7B5D2048A2A165F49426CDCAD733703CF534367133819091892E3A1F14)

```
Random number: 75267ba4cc4f2d9ddbf9f90dc1ea813ae2a4d2114eb2ef2cb7ff0a5d285c7396
Timestamp: 1572337686
Random number hash: dabd990af86582969d47218012ecdb09899b9ad2b069c05be94ef82bea889a1b
Password to sign with 'tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce':
Committed at block 46889130 (tx hash: D653FC7B5D2048A2A165F49426CDCAD733703CF534367133819091892E3A1F14, response: {Code:0 Data:[119 24 196 176 181 1 29 177 60 107 100 166 55 16 253 136 159 3 204 56 109 46 63 87 93 9 239 158 138 172 21 129] Log:Msg 0: swapID: 7718c4b0b5011db13c6b64a63710fd889f03cc386d2e3f575d09ef9e8aac1581 Info: GasWanted:0 GasUsed:0 Tags:[{Key:[115 101 110 100 101 114] Value:[116 98 110 98 49 97 54 112 118 53 103 109 110 115 97 121 52 97 57 115 114 55 110 118 100 48 109 108 100 122 50 57 97 54 107 100 120 121 101 51 55 99 101] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[114 101 99 105 112 105 101 110 116] Value:[116 98 110 98 49 119 120 101 112 108 121 119 55 120 56 97 97 104 121 57 51 119 57 54 121 104 119 109 55 120 99 113 51 107 101 52 102 102 97 115 112 51 100] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0} {Key:[97 99 116 105 111 110] Value:[72 84 76 84] XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0}] Codespace: XXX_NoUnkeyedLiteral:{} XXX_unrecognized:[] XXX_sizecache:0})
```

取得 swap id 與 random number，使用 swap ip 查詢

```
SWAP_ID=7718c4b0b5011db13c6b64a63710fd889f03cc386d2e3f575d09ef9e8aac1581
tbnbcli token query-swap \
  --swap-id ${SWAP_ID} \
  --chain-id Binance-Chain-Nile \
  --trust-node \
  --node http://data-seed-pre-0-s3.binance.org:80
```

回復當前的狀態

```json
{
   "from":"tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce",
   "to":"tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce",
   "out_amount":[
      {
         "denom":"BNB",
         "amount":"10"
      }
   ],
   "in_amount":null,
   "expected_income":"100:PPT",
   "recipient_other_chain":"0x938a452d293c23C2CDEae0Bf01760D8ECC4F826b",
   "random_number_hash":"dabd990af86582969d47218012ecdb09899b9ad2b069c05be94ef82bea889a1b",
   "random_number":"",
   "timestamp":"1572337686",
   "cross_chain":true,
   "expire_height":"46889630",
   "index":"2245",
   "closed_time":"0",
   "status":"Open"
}
```

### Deputy Appove Token

Deputy 已經抓到 Binance Chain 上的 tx，會記錄在 Mysql 內

```
use deputy;

select * from tx_log limit 10;

| id | chain | swap_id                                                          | tx_type   | tx_hash                                                          | contract_addr | sender_addr                                 | receiver_addr                               | sender_other_chain                         | other_chain_addr                           | in_amount | out_amount | out_coin | random_number_hash                                               | expire_height | timestamp  | random_number | block_hash                                                       | height   | status    | confirmed_num | create_time | update_time |
|  2 | BNB   | 7718c4b0b5011db13c6b64a63710fd889f03cc386d2e3f575d09ef9e8aac1581 | BEP2_HTLT | d653fc7b5d2048a2a165f49426cdcad733703cf534367133819091892e3a1f14 |               | tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce | tbnb1a6pv5gmnsay4a9sr7nvd0mldz29a6kdxye37ce |                                            | 0x938a452d293c23C2CDEae0Bf01760D8ECC4F826b | 100:PPT   | 10         | BNB      | dabd990af86582969d47218012ecdb09899b9ad2b069c05be94ef82bea889a1b |      46889630 | 1572337686 |               | 6948f34e4013da29c9922306b60b2c12f174925c63ff2a46d6b2fc3acd7a3774 | 46889130 | CONFIRMED |             6 |  1572337694 |  1572337695 |
```

### Deputy Send HTLT on Ethereum

查詢 Ethereum 上的 HTLT

### 客戶端 Call Claim 取得 ERC-20 Token

客戶端取得 100:PPT

### Deputy Call HTLT Claim 取得 Binance Token

Deputy 取得 10:BNB

---

### GCE

```
gcloud compute ssh dep3-deputy

sudo apt-get update
sudo apt-get install mysql-server
sudo cat /etc/mysql/debian.cnf

wget https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.13.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

go get github.com/binance-chain/bep3-deputy
go mod tidy
go build  -o build/deputy main.go
```

### References

* [Binace Chain Doc](https://docs.binance.org/atomic-swap.html)
* [Binance BEP3 spec](https://github.com/binance-chain/BEPs/blob/master/BEP3.md)
