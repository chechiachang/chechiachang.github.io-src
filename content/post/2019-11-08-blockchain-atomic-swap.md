---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Ablockchain Atomic Swap"
subtitle: ""
summary: ""
authors: []
tags: ["blockchain", "atomic-swap"]
categories: ["blockchain"]
date: 2019-11-08T08:03:30+08:00
lastmod: 2019-11-08T08:03:30+08:00
featured: false
draft: false

menu:
  main:
    parent: "Blockchain"
    weight: 1
---

[https://en.bitcoin.it/wiki/Atomic_swap](https://en.bitcoin.it/wiki/Atomic_swap)

# Algorithm

* 2 pay txs and 2 claim tx
* claim txs are singed at first, locked with time
* 2 pay txs are encrypted by x, affects only when x is reveal on the network

0. Initialization

A: random number x

tx1: A pay B
  A Pay BTC to B's public key
    if x known & singed by B
    or Signed by A & B

tx2: A claim
  tx1 pay BTC to A's public key
    locked 48 hours
    signed by A

A -> B tx2
B -> A tx2 signed by A & B

1. A -> submit tx1 
      
tx3: B pay A alt-coin
  B Pay A alt-coin
    if x known & singed by A
    or signed by A & B

tx4: B claim
  tx3 pay B alt-coins
  locked 48 hours
  signed by B

B -> A tx4
A -> B tx4 signed by A & B

3. B submit tx3
4. A spends tx3, reveal x
5. B spends tx1 using x

# Specialized Alt-chain
