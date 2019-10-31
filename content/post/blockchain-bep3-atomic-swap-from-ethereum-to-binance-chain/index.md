---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Blockchain Bep3 Atomic Swap From Ethereum to Binance Chain"
subtitle: ""
summary: ""
authors: []
tags: ["blockchain", "bep3", "binance", "ethereum","erc-20"]
categories: []
date: 2019-10-31T15:21:44+08:00
lastmod: 2019-10-31T15:21:44+08:00
featured: false
draft: false

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

### BEP3 Atomic Swap 2 - 從 Ethereum swap 到 Binance Chain

* [在 Binance Chain 上互換兩個 address 的 binance asset]({{< ref "/post/blockchain-bep3-atomic-swap" >}})
* [將 asset 從 ethereum token 與 binance asset 做交換]({{< ref "/post/blockchain-bep3-atomic-swap-from-ethereum-to-binance-chain" >}})

---

# 從 Ethereum swap 到 Binance Chain

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

{{< figure library="1" src="bep3-atomic-swap-failure-01.png" height="70%" width="70%" title="" >}}
{{< figure library="1" src="bep3-atomic-swap-failure-02.png" height="70%" width="70%" title="" >}}

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

# Swap Tokens from Binance Chain to Ethereum

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
