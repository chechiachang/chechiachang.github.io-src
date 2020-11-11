---
title: "20201109 Vault Experience"
date: 2020-11-09T11:24:22+08:00
draft: true
---

My app need a secret

- secret need to be stored
- secret need to be rotated
- secret need to be distributed

# Issue 0: My secrets is secured in source code

My secrets is hardcoded in source code

- As a devops, I don't discuss source code outside Version Control System
- Source code in VCS
  - secrest all over the commit history
  - anyone (developers/attackers) access VCS can access secrets. Have both app and secret
  - "We don't rorate,  because rotate need source code modification"

# Issue 1: How about k8s-secrets (encrypted / not-encrypted) + container environments variable

K8s pods
- a k8s namespace: good
  - same namespace usually means same permission
    - it not (e.g. all pods in default namespace), improve your k8s namespace management
  - risk control: blast radius within a namespace
  - accessiblilty: vault-k8s auth
    - auth with k8s API. no static access token required
    - Enforce restrict path&policy for each k8s-namespace/k8s-service-account

VMs

# Issue 1: two keys is better than 1 key

1 key
- authentication and authorization at same place

2 key
- dynamic secrets generated for app when needed
- real database key never expose to app

# Issue 1: Don't let them in

A: "I have a "
dev/app-a/app-a-secret

B: "Oh, you already got a path. Let me join you"
dev/app-a/app-a-secret
dev/app-a/app-b-secret

"dev/app-a become a shared path. This means"
- app-b depends on app-b policy

Suggestion 1: "Don't let then in. Keep app has their own policy, own path, own secret"

But: "What if thers's a shared key"

Suggestion 2-1: "Create a new shared path. Bind policy/app-a and policy/app-b"
- dev/app-a/app-a-secret
- dev/app-b/app-b-secret
- dev/app-ab/app-ab-secret

```yaml
policies
  app-a:
    - dev/app-a/*
    - dev/app-ab/*
  app-b:
    - dev/app-b/*
    - dev/app-ab/*
```

Suggestion 2-2: "Put shared secret on upper level path. Bind policy/app-a and app-b to upper path"

```yaml
policies
  app-a:
    - dev/app/app-a/*
    - dev/app/*
  app-b:
    - dev/app/app-b/*
    - dev/app/*
```

CONS: "there will always be a app-c. This solution will "

# Issue 3: IAM auth

root token is a double-edged sword
quorum unseal keys can generate-root

Keep there keys safe and away

Transfer risks in authentication to IAM oauth

vault login -method=aws -path=aws role=chechia

---

# Internal

### Security Model

https://www.vaultproject.io/docs/internals/security

Threat model
- Secured backend: Eavesdropping on any Vault communication
- Transaction Audit: Tampering with data at rest or in transit
- Policy: Access to data or controls without authentication or authorization
- Log: Access to data or controls without accountability
- Encrypted: Confidentiality of stored secrets
- HA: Availability of secret material in the face of failure
Not threat model
- Protecting against arbitrary control of the storage backend
- rotecting against the leakage of the existence of secret material
- Protecting against memory analysis of a running Vault

### External Threat

no trust between vault client & server
- client requires TLS
- server requries token

Encrypted Backend
- encrypt all requests from vault server to backend

### Internal Threat

Client to vault server
- ACL

---

# Terraform

key management
path policy
很怕低級錯誤

有一種強不是強，不出錯，是開發習慣好很多
