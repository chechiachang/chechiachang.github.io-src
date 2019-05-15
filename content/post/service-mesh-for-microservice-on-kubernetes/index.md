+++
title = "Istio 三分鐘就入坑 部屬篇"
subtitle = "Istio 三分鐘就入坑 部屬篇"

# Add a summary to display on homepage (optional).
summary = "基於 Kubernetes 平台上的 Istio ，實際部署，並一步一步操作Istio 的功能。"

date = 2019-05-06T18:12:15+08:00
draft = false

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Is this a featured post? (true/false)
featured = false

# Tags and categories
# For example, use `tags = []` for no tags, or the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "istio", "service-mesh"]
categories = []

# Projects (optional).
#   Associate this post with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
# projects = ["internal-project"]

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

# Create GKE

```
gcloud beta container --project "istio-playground-239810" clusters create "istio-playground" \
  --zone "asia-east1-b" \
  --username "admin" \
  --cluster-version "1.11.8-gke.6" \
  --machine-type "n1-standard-2" \
  --image-type "COS" \
  --disk-type "pd-standard" \
  --disk-size "100" \
  --preemptible \
  --num-nodes "1" \
  --enable-cloud-logging \
  --enable-cloud-monitoring \
  --no-enable-ip-alias \
  --addons HorizontalPodAutoscaling,HttpLoadBalancing,KubernetesDashboard,Istio \
  --istio-config auth=MTLS_PERMISSIVE \
  --no-enable-autoupgrade \
  --enable-autorepair
```

# Take a Peek

```
$ kubectl get namespaces

NAME           STATUS    AGE
default        Active    2m
istio-system   Active    1m
kube-public    Active    2m
kube-system    Active    2m

$ kubectl get po -n istio-system
NAME                                      READY     STATUS      RESTARTS   AGE
istio-citadel-7f6f77cd7b-nxfbf            1/1       Running     0          3m
istio-cleanup-secrets-h454m               0/1       Completed   0          3m
istio-egressgateway-7c56db84cc-nlrwq      1/1       Running     0          3m
istio-galley-6c747bdb4f-45jrp             1/1       Running     0          3m
istio-ingressgateway-6ff68cf95d-tlkq4     1/1       Running     0          3m
istio-pilot-8ff66f8c4-q9chz               2/2       Running     0          3m
istio-policy-69b78b7d6-c8pld              2/2       Running     0          3m
istio-sidecar-injector-558996c897-hr6q4   1/1       Running     0          3m
istio-telemetry-f96459fb-5cbpg            2/2       Running     0          3m
promsd-ff878d44b-hv8nh                    2/2       Running     1          3m
```

# Deploy app

```
kubectl label namespace default istio-injection=enabled
```

Bookinfo Application
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.1/samples/bookinfo/platform/kube/bookinfo.yaml

kubectl get pods
kubectl get services
```

Gateway
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.1/samples/bookinfo/networking/bookinfo-gateway.yaml

kubectl get gateways

kubectl get svc istio-ingressgateway -n istio-system
```

Go to ingress public ip
```
export INGRESS_HOST=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
export INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
export SECURE_INGRESS_PORT=$(kubectl -n istio-system get service istio-ingressgateway -o jsonpath='{.spec.ports[?(@.name=="https")].port}')

curl -v ${INGRESS_HOST}:{$INGRESS_PORT}/productpage

404 Not Found
```

Apply destination rules
```
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.1/samples/bookinfo/networking/destination-rule-all.yaml

curl -v ${INGRESS_HOST}:{$INGRESS_PORT}/productpage
```

### Brief review

```
kubectl get virtualservices
kubectl get destinationrules
kubectl get gateways
```

# Istio Tasks

https://istio.io/docs/tasks/traffic-management/
