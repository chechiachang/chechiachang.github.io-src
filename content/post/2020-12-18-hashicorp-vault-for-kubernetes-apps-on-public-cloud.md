---
title: "Hashicorp Vault for Kubernetes Apps on Public Cloud"
date: 2020-12-07T16:29:26+08:00
draft: true
---

# Event

- https://cntug.kktix.cc/events/year-end-2020
- audience: 112/150

# resources

this presentation
- https://slides.com/chechiachang/terraform-introduction-a56697

github
- https://github.com/chechiachang/terraform-azure
- https://github.com/chechiachang/vault-playground/tree/master/deploy/v0.8.0

# outline

- issues of key management
- what is vault
- why vault
- case: vault & kubernetes
- case: vault & cloud iam
- vault & terraform
- repo example
- maicoin

# CNCF landscape

https://landscape.cncf.io/selected=vault

# Issues of secret management

Secret life cycle
- generate
- exchange
- store
- use
- destroy
- rotate

For some people
- generate
- use

You need when you need

# Approaches

- hard-coded
- instance secrets
- k8s secret & pod env

encrypted
- sealed-secret
  - https://github.com/bitnami-labs/sealed-secrets
- helm secret
- vault

# Vault feature

- secure secret storage
- dynamic secret
- data encryption
- leasing and renewal
- ...

# Vault core concept

Good video Here

https://www.hashicorp.com/resources/introduction-vault-whiteboard-armon-dadgar

I'll skip.

# Use case: auth-method/Token

- Auth method: Help vault control who can access vault
- Token attached to policies


### Token auth is not what we want

- (username, password) -> DB
- TOKEN -> vault -> (username, password) -> DB

- Pros
  - Token rotation is easy
- Cons
  - No better: risks are the same
  - Require more work on vault configuration

- So we use other auth methods: https://www.vaultproject.io/docs/auth

# Use case: auth-method/iam

- Vault trust public cloud: azure, aws, gcp,...

- (username, password) -> DB
- cloud-auth workflow
  - User -> public cloud -> Login -> (credential)
  - User -> (credential) -> Vault
  - Vault -> (credential) -> public cloud -> validate user
  - Vault -> (dynamic vault token) -> User

- Team workflow
  - Vault admin -> save secrets in vault
  - Vault admin -> configure cloud IAM
  - Vault admin -> configure vault auth method
  - Developer -> vault login -method=azure -role=sre

- Pros
  - Reduce risk
    - No password / secret exchange required. Minimize secret exposure
    - Public cloud have good (secured & stable) auth system
    - Easy create/Update/Delete user/iam with cloud
  - Dynamic secrets
    - Secret is generated when needed (Just in time)
    - Secret grant to user is short-live token. Token revoked when not needed
- Cons
  - Require more work on vault configuration

# Use case: auth-method/iam

Since vault can recognize public cloud, we can also make VMs auth to vault automatically.

Cloud also support service IAM
- Auth with VM instance, kubernetes cluster, ... many resources on cloud

- auth workflow
  - VM -> (VM profile) -> Vault
  - Vault -> (VM profile) -> Public Cloud -> which VM is it?
  - Vault -> VM -> "welcom VM api-123, your permission is DB-123"

- Pros
  - Auth to environment (VM group / VPC / security group / ...)
    - Reduce risk: No password / secret exposure during development
- Cons
  - Require more work on vault configuration

# Use case: auth-method/kubernetes

- Vault trust your kubernetes cluster

```
ROLE=chechia

kubectl exec -it ${POD} sh
vault write auth/general-k8s/login role=${ROLE} jwt=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)
```

# Use case: dynamic database password

(admin, password) -> DB -> create user with limited permission
(user, paassword) -> DB

# Issues & Tips

Correctness
- secret content
  - "Is the secret/password correct?"
  - The issue "填錯了" is out of vault scope
- policy / config
  - "Is the policy correct so that
    - token has permission?"
    - token has no excessive permission?"
  - This vault can help

verification
  - staging
    - "Is staging the same as production?"
  - prod dry-run / standby / maintenance mode
    - "After deployment, only accessible in private network"

Approach
  - terraform every configs / policies, as many as possible
  - keep your dev/staging vault as clean as prod
  - Check staging / prod difference regularly

# 
