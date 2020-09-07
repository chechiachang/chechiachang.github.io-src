---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Monitoring GKE With Elk"
subtitle: ""
summary: ""
authors: []
tags: ["kubernetes", "logstash", "ithome", "filebeat", "fluentd"]
categories: ["kubernetes", "logstash"]
date: 2019-09-19T17:06:29+08:00
lastmod: 2019-09-19T17:06:29+08:00
featured: false
draft: false

menu:
  main:
    parent: "Ithelp 鐵人賽"
    weight: 1
---

[2020 It邦幫忙鐵人賽](https://ithelp.ithome.com.tw/2020ironman) 系列文章

- [Self-host ELK stack on GCP]({{< ref "/post/self-host-elk-stack-on-gcp" >}})
- [Secure ELK Stask]({{< ref "/post/secure-elk-stack" >}})
- [監測 Google Compute Engine 上服務的各項數據]({{< ref "/post/monitoring-gce-with-elk" >}})
- [監測 Google Kubernetes Engine 的各項數據]({{<ref "/post/monitoring-gke-with-elk" >}})
- 使用 logstash pipeline 做數據前處理
- Elasticsearch 日常維護：數據清理，效能調校，永久儲存
- Debug ELK stack on GCP

作為範例的 ELK 的版本是當前的 stable release 7.3.1。

由於我比較熟悉 GCP / GKE 的服務，這篇的操作過程都會以 GCP 平台作為範例，不過操作過程大體上是跨平台通用的。

---

這篇來要 Kubernetes 環境(GKE)裡面的 log 抓出來，送到 ELK 上。

[官方文件](https://www.elastic.co/guide/en/beats/filebeat/7.3/running-on-kubernetes.html) ，寫得很簡易，如果已經很熟 kubernetes 的人可以直接腦補其他的部屬設定。

這邊有幾個做法，依照 filebeat 部署的位置與收集目標簡單分為：

* node: 處理每一台 node 的 log ，包含 system log 與 node 監測資料(metrics)
* cluster: 處理 cluster 等級的 log,  event 或是 metrics
* pod: 針對特定 pod 直接去掛一個 sidecar

上面的方法是可以混搭的，kubernetes 個個層級有[log 處理流程](https://kubernetes.io/docs/concepts/cluster-administration/logging/)，我們這邊把 log 送往第三方平台，也是需要依照原本的 log 流程，去收取我們想收集的 log。

簡單來說，是去對的地方找對的 log。在架構上要注意 scalability 與 resource 分配，不要影響本身提供服務的 GKE ，但又能獲得盡量即時的 log。

我們這邊直接進入 kubernetes resource 的設定，底下會附上在 GKE 找 log 的過程。

# Node level log harvest

為每一個 node 配置 filebeat，然後在 node 上面尋找 log，然後如我們上篇所敘述加到 input ，就可以把 log 倒出來。

直覺想到就是透過 daemonsets 為每個 node 部署一個 filebeat pod，然後 mount node 的 log 資料夾，在設置 input。

# Deploy daemonsets

kubernetes resource 的 yaml 請參考 [我的 github elk-kubernetes](https://github.com/chechiachang/elk-kubernetes/tree/master/filebeat/7.3.1)

給予足夠的 clusterrolebinding 到 elk
```
kubectl apply -f filebeat/7.3.1/clusterrolebinding.yaml
```

先更改 filebeat 的設定，如何設定 elasticsearch 與 kibana，請參考上篇。至於 input 的部份已經配置好了。
```
vim filebeat/7.3.1/daemonsets-config-configmap.yaml

kubectl apply -f filebeat/7.3.1/daemonsets-config-configmap.yaml
```

部屬 filebeat daemonsets，會每一個 node 部屬一個 filebeat

```
kubectl apply -f filebeat/7.3.1/daemonsets.yaml
```

取得 daemonsets 的狀態 
```
kubectl --namespcae elk get pods

NAME             READY   STATUS    RESTARTS   AGE
filebeat-bjfp9   1/1     Running   0          6m56s
filebeat-fzr9n   1/1     Running   0          6m56s
filebeat-vpkm7   1/1     Running   0          6m56s
...
```

有設定成功的話，kibana 這邊就會收到 kubernetes 上面 pod 的 log

# log havest for specific pods

由於 kubernetes 上我們可以便利的調度 filebeat 的部屬方式，這邊也可以也可以使用 deployment ，配合 pod affinity，把 filebeat 放到某個想要監測的 pod，這邊的例子是 nginx-ingress-controller。 

* Kubernetes 上有一個或多個 nginx ingress controller
* 部屬一個或多個 filebeat 到有 nginx 的 node 上
* filebeat 去抓取 nginx 的 input， 並使用 filebeat 的 nginx module 做預處理
  * nginx module 預設路徑需要調整，這邊使用 filebeat autodiscover 來處理

一樣 apply 前記得先檢查跟設定
```
vim filebeat/7.3.1/nginx-config-configmap.yaml

kubectl apply -f filebeat/7.3.1/nginx-config-configmap.yaml
```

部屬 filebeat deployment
由於有設定 pod affinity ，這個 filebeat 只會被放到有 nginx ingress controller 的這個節點上，並且依照 autodiscover 設定的條件去蒐集 nginx 的 log
```
kubectl apply -f filebeat/7.3.1/nginx-deployment.yaml
```

有設定成功的話，kibana 這邊就會收到 kubernetes 上面 pod 的 log

另外，由於有啟動 nginx module，logstash 收到的內容已經是處理過得內容。

---

# GCP fluentd

如果是使用 GKE 的朋友，可以投過開啟 stackdriver logging 的功能，把集群中服務的 log 倒到 stackdriver，基本上就是 node -> (daemonsets) fluentd -> stackdriver。

這個 fluentd 是 GCP 如果有啟動 Stackdriver Logging 的話，自動幫你維護的 daemonsets，設定不可改，改了會被 overwrite 會去，所以不太方便從這邊動手腳。

Btw stackdriver 最近好像改版，目前做 example 的版本已經變成 lagency （淚

但我們先假設我們對這個 pod 的 log 很有興趣，然後把這邊的 log 透過 filebeat 送到 ELK 上XD

因為 GKE 透過 fluentd 把 GKE 上面的 log 倒到 stackdriver，而我們是想把 log 倒到 ELK，既然這樣我們的 input 來源是相同的，而且很多處理步驟都可以在 ELK 上面互通，真的可以偷看一下 fluentd 是去哪收集 log ，怎麼處理 log pipeline，我們只要做相應設定就好。

畢竟 google 都幫我們弄得妥妥的，不參考一下他的流程太可惜。

偷看一下 GKE 上 fluentd 是去哪找 log ，這個是 [fluentd gcp configmap](https://github.com/kubernetes/kubernetes/blob/master/cluster/addons/fluentd-gcp/fluentd-gcp-configmap.yaml)，雖然看到這邊感覺扯遠了，但因為很有趣所有我就繼續看下去，各位大德可以跳過XD

configmap 中的這個 input 設定檔，其中一個 source 就是一個資料來源，相當於 filebeat 的 input。這邊這個 source 就是去 `/var/log/containers/*.log`  收 log 

這邊還做了幾件事：

* 打上 `reform.*` tag，讓下個 match 可以 收進去 pipeline 處理
* 附帶 parse 出 time

```
containers.input.conf

<source>
  @type tail
  path /var/log/containers/*.log
  pos_file /var/log/gcp-containers.log.pos
  # Tags at this point are in the format of:
  # reform.var.log.containers.<POD_NAME>_<NAMESPACE_NAME>_<CONTAINER_NAME>-<CONTAINER_ID>.log
  tag reform.*
  read_from_head true
  <parse>
    @type multi_format
    <pattern>
      format json
      time_key time
      time_format %Y-%m-%dT%H:%M:%S.%NZ
    </pattern>
    <pattern>
      format /^(?<time>.+) (?<stream>stdout|stderr) [^ ]* (?<log>.*)$/
      time_format %Y-%m-%dT%H:%M:%S.%N%:z
    </pattern>
  </parse>
</source>
```

他這邊做一些 error handling，然後用 ruby (!) parse，這邊就真的太遠，細節大家可以 google ＸＤ。不過這邊使用的 pattern matching 我們後幾篇在 logstash pipeline 上，也會有機會提到，機制是類似的。

```
<filter reform.**>
  @type parser
  format /^(?<severity>\w)(?<time>\d{4} [^\s]*)\s+(?<pid>\d+)\s+(?<source>[^ \]]+)\] (?<log>.*)/
  reserve_data true
  suppress_parse_error_log true
  emit_invalid_record_to_error false
  key_name log
</filter>

<match reform.**>
  @type record_reformer
  enable_ruby true
  <record>
    # Extract local_resource_id from tag for 'k8s_container' monitored
    # resource. The format is:
    # 'k8s_container.<namespace_name>.<pod_name>.<container_name>'.
    "logging.googleapis.com/local_resource_id" ${"k8s_container.#{tag_suffix[4].rpartition('.')[0].split('_')[1]}.#{tag_suffix[4].rpartition('.')[0].split('_')[0]}.#{tag_suffix[4].rpartition('.')[0].split('_')[2].rpartition('-')[0]}"}
    # Rename the field 'log' to a more generic field 'message'. This way the
    # fluent-plugin-google-cloud knows to flatten the field as textPayload
    # instead of jsonPayload after extracting 'time', 'severity' and
    # 'stream' from the record.
    message ${record['log']}
    # If 'severity' is not set, assume stderr is ERROR and stdout is INFO.
    severity ${record['severity'] || if record['stream'] == 'stderr' then 'ERROR' else 'INFO' end}
  </record>
  tag ${if record['stream'] == 'stderr' then 'raw.stderr' else 'raw.stdout' end}
  remove_keys stream,log
</match>
```

### ssh 進去逛

想看機器上實際的 log 狀況，我們也可以直接 ssh 進去

先透過 kubectl 看一下 pod

```
$ kubectl get daemonsets --namespace kube-system

NAME                       DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR                                  AGE
fluentd-gcp-v3.2.0         7         7         7       7            7           beta.kubernetes.io/fluentd-ds-ready=true       196d

$ kubectl get pods --output wide --namespace kube-system

NAME                                      READY   STATUS    RESTARTS   AGE   IP          NODE                                     NOMINATED NODE   READINESS GATES
fluentd-gcp-scaler-1234567890-vfbhc       1/1     Running   0          37d   10.140.0.   gke-chechiachang-pool-1-123456789-5gqn   <none>           <none>
fluentd-gcp-v3.2.0-44tl7                  2/2     Running   0          37d   10.140.0.   gke-chechiachang-pool-1-123456789-wcq0   <none>           <none>
fluentd-gcp-v3.2.0-5vc6l                  2/2     Running   0          37d   10.140.0.   gke-chechiachang-pool-1-123456789-tp05   <none>           <none>
fluentd-gcp-v3.2.0-6rqvc                  2/2     Running   0          37d   10.140.0.   gke-chechiachang-pool-1-123456789-5gqn   <none>           <none>
fluentd-gcp-v3.2.0-mmwk4                  2/2     Running   0          37d   10.140.0.   gke-chechiachang-pool-1-123456789-vxld   <none>           <none>
```

先透過 kubectl 看一下 node

```
$ kubectl get node

NAME                                     STATUS   ROLES    AGE   VERSION
gke-chechaichang-pool-1-123456789-3bzp   Ready    <none>   37d   v1.13.7-gke.8
gke-chechaichang-pool-1-123456789-5gqn   Ready    <none>   37d   v1.13.7-gke.8
gke-chechaichang-pool-1-123456789-8n8z   Ready    <none>   37d   v1.13.7-gke.8
...

gcloud compute ssh gke-chechaichang-pool-1-123456789-3bzp
```

如使用其他雲平台的 kubernetes service，或是 bare metal 的集群，請依照各自系統的方式連進去看看。

# ssh node 找 log  

ssh 進去後就可以到處來探險，順便看看 GKE 跑在機器上到底做了什麼事情。

如果官方有出文件，可能可以不用進來看。各位大德有發現文件請留言跟我說。我個人很喜歡自己架集群起來連就去看，面對照官方文件上寫的東西，當然大部份時候都是文件沒有帶到，有很多發現。

```
$ ls /var/log

gcp-*-log.pos
kube-proxy.log
containers/
metrics/
pods/
...

```

/var/log/containers 看一下，格式是 `pod_namespace_container` 這邊是 link 到 /var/log/pods/

```
$ ls -al /var/log/containers

lrwxrwxrwx 1 root root   105 Aug 12 07:42 fluentd-gcp-v3.2.0-st6cl_kube-system_fluentd-gcp-5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac.log -> /var/log/pods/kube-system_fluentd-gcp-v3.2.0-st6cl_b76bed0b-bcd4-11e9-a55c-42010a8c0008/fluentd-gcp/0.log
```

看到 pods 就覺得是你了，裡面有 pod 資料夾，格式是 `namespace_pod_uuid`

```
ls /var/log/pods

default_pod-1-1234567890-fxxhp_uuid
kube-system_fluentd-gcp-v3.2.0-st6cl_b76bed0b-bcd4-11e9-a55c-42010a8c0008
kube-system_heapster-v1.6.0-beta.1-
kube-system_kube-proxy-gke-
kube-system_l7-default-backend-
kube-system_prometheus-to-sd-
```

再進去有 container log，格式是 `pod_namespace_container.log`，也是 link 

```
ls -al /var/log/pods/kube-system_fluentd-gcp-v3.2.0-st6cl_b76bed0b-bcd4-11e9-a55c-42010a8c0008/fluentd-gcp/

lrwxrwxrwx 1 root root  165 Aug 12 07:42 0.log -> /var/lib/docker/containers/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac-json.log
```

最終 link 到

```
sudo su

$ ls -alh /var/lib/docker/containers/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac/
total 3.9M
drwx------  4 root root 4.0K Aug 12 07:42 .
drwx------ 92 root root  20K Sep 18 11:28 ..
-rw-r-----  1 root root 3.8M Sep 18 11:29 5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac-json.log
drwx------  2 root root 4.0K Aug 12 07:42 checkpoints
-rw-------  1 root root 7.8K Aug 12 07:42 config.v2.json
-rw-r--r--  1 root root 2.3K Aug 12 07:42 hostconfig.json
drwx------  2 root root 4.0K Aug 12 07:42 mounts
```

頭尾偷喵一下，確定是我們在找的東西
```
head /var/lib/docker/containers/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac-json.log
tail /var/lib/docker/containers/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac/5e38c9b63c8d767091b122a9aa48c576a88cc20b4470d9ca18a820afa5c168ac-json.log
```

這樣就找到我們的 log 了

# 小節

* 使用 filebeat 去查找
* 透過 kubernetes daemonsets 可以快速佈置一份 filebeat 到所有 node，且設定都是一起更新
* 透過 kubernetes deployment 可以指定 filebeat 的位置，去跟隨想要監測的服務
* 如果不熟 log 處理流程，可以直接看偷看大廠的服務，會有很多靈感
* 沒事可以多跑進 Kubernetes 服務節點逛逛，有很多有趣的東西
