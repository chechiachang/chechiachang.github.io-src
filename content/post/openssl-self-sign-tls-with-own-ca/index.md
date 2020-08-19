---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "OpenSSL Self Sign TLS With Ca"
subtitle: ""
summary: ""
authors: []
tags: []
categories: []
date: 2020-08-07T14:28:29+08:00
lastmod: 2020-08-07T14:28:29+08:00
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

TLS Certificate Authority
===

Self-sign certificate with own CA.

# Keys

# Usage

Generate Step
---

- [中文](https://blog.cssuen.tw/create-a-self-signed-certificate-using-openssl-240c7b0579d3)
- [English](https://deliciousbrains.com/ssl-certificate-authority-for-local-https-development/)

### Toolkit: OpenSSL

[https://github.com/openssl/openssl](https://github.com/openssl/openssl)

```shell
openssl version

OpenSSL 1.1.1g  21 Apr 2020

man openssl
```

### Generate CA key

```shell
DIR=tls-certificate-authority

openssl genrsa \
  -out ${DIR}/ca.key 4096

cat ${DIR}/ca.key
```

### Generate root certificate with CA key

```shell
COUNTRY=TW
STATE=Taiwan
LOCATION=Taipei
ORGANIZATION=CheChia
ORGANIZATION_UNIT=DevOps
COMMON_NAME=*.chechia.net

DAYS=1825 # 5 year

openssl req -x509 -new \
  -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=${COMMON_NAME}" \
  -nodes \
  -sha256 \
  -days ${DAYS} \
  -key ${DIR}/ca.key \
  -out ${DIR}/ca.crt
```

### Generate Certificate for each host

Generate Certificate Signing Request(CSR)

```shell
mkdir ${DIR}/${COMMON_NAME}

openssl genrsa -out ${DIR}/${COMMON_NAME}/host.key 4096

openssl req -new \
  -subj "/C=${COUNTRY}/ST=${STATE}/L=${LOCATION}/O=${ORGANIZATION}/OU=${ORGANIZATION_UNIT}/CN=${COMMON_NAME}" \
  -key ${DIR}/${COMMON_NAME}/host.key \
  -sha256 \
  -out ${DIR}/${COMMON_NAME}/host.csr
```

Sign Certificate Signing Request(CSR) with CA key

```shell
openssl x509 -req \
  -in ${DIR}/${COMMON_NAME}/host.csr \
  -CAcreateserial \
  -days ${DAYS} \
  -sha256 \
  -CA ${DIR}/ca.crt \
  -CAkey ${DIR}/ca.key \
  -out ${DIR}/${COMMON_NAME}/host.crt
```

### Directory

```shell
├── tls-certificate-authority
│   ├── *.chechia.net
│   │   ├── host.crt
│   │   ├── host.csr
│   │   └── host.key
│   ├── ca.crt
│   ├── ca.key
│   └── ca.srl
└── tls-certificate-authority.md
```
