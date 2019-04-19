+++
title = "Kubernetes Storage and Glusterfs"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date = 2018-02-10T10:00:00+08:00
date_end = 2018-02-10T18:00:00+08:00
all_day = true

# Schedule page publish date (NOT talk date).
publishDate = 2018-02-10T20:49:32+08:00

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Location of event.
location = "國立臺灣科技大學資訊管理系/台科大資管學院 3F, MA316"

# Name of event and optional event URL.
event = "SDN x Cloud Native Meetup #2"
event_url = "https://github.com/TGmeetup/TWcommunities/blob/master/communities/CNTUG.md#20180210"

# Abstract. What's your talk about?
abstract = "Kubernetes storage system: use GlusterFS as an example"

# Summary. An optional shortened abstract.
summary = "Kubernetes storage system: use GlusterFS as an example"

# Is this a featured talk? (true/false)
featured = false

# Tags (optional).
#   Set `tags = []` for no tags, or use the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "storage", "filesystem", "glusterfs"]

# Markdown Slides (optional).
#   Associate this page with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references 
#   `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides = ""

# Optional filename of your slides within your talk folder or a URL.
url_slides = "https://www.slideshare.net/CheChiaChang/k8s-storageglusterfs20180210"

# Projects (optional).
#   Associate this talk with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects = []

# Links (optional).
url_pdf = ""
url_video = ""
url_code = ""

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = ""

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = ""
+++

### Outlines

1. Docker Storage
2. Kubernetes Storage

3. GlusterFS for K8s

### Docker Storage

[Doc](https://docs.docker.com/storage/)

1. within container: inside writable layer of a container
  * deleted with container
  * couple with host machine
  * require storage driver

  ```
  docker ps -s
  docker inspect ubuntu
  dd if=/dev/zero of=1Mfile bs=1k count=1000
  ```

2. Docker volume
  * a directory on host
  * prepare: provision on host
  * usage: set volume on docker run

### Kubernetes Storage

https://kubernetes.io/docs/concepts/storage/volumes/

1. On-disk files:
  * Deleted on container restart
  * File sharing in Pod

2. Kubernetes Volume:
  * a directory
  * Coexist with Pod
  * Data preserved across container restarts
  * Pod can use many volumes of different types

(Some of) Types of volumes :
  * emptyDir
    - first created volume
    - prepare: none
    - usage: always

  * gcePersistentDisk
    - independent to pod
    - prepare: gcp
    - usage: claim by name

    ```
    gcloud compute disks create --size=500GB --zone=us-central1-a my-data-disk
    ```

  * PersistentVolumeClaim
    - prepare: provision by admin
    - usage: add PVC request


  [Example](https://kubernetes.io/docs/tasks/configure-pod-container/configure-persistent-volume-storage/)

### PersistentVolume

  [Doc](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
  * Persistent Volume
    - a piece of provisioned storage
    - Independent lifecycle
    - abstract with k8s object API
    - many implementations: ex. GCEPersistentDisk, NFS, GlusterFS...

  * Why PersistentVolume
    - one APIs, many PV implementations
    - Separates providers (admin) and consumers (users)
    - PV subsystem API handles details of implementation
    - Handle different need like size, access mode, performance...

  * PersistentVolumeClaim
    - PV: a resource
    - PVC: a request for storage
    - Pods consume Node resources and PVCs consume PV resources

  * PVC lifecycle
    - Povisioning
    - Binding
    - Using
    - Reclaiming
    - Deleting

  * PV Access Modes
    - ReadWriteOnce: 1 node R/W
    - ReadOnlyMany: n node R, 1 node W
    - ReadWriteMany: n node R/W

  * StorageClass
    - usage:PV.storageClassName

  [Doc](https://kubernetes.io/docs/concepts/storage/storage-classes/)

### GlusterFS

  [Doc](http://docs.gluster.org/en/latest/Administrator%20Guide/GlusterFS%20Introduction/)

  * Why glusterFS
    - Network FS
    - Distributed FS
      - High Availability
      - Scalability
    - High performance

  * Architecture: Types of Volumes
    - Distributed
    - Replicated
    - Distributed Replicated
    - Striped: file
    - Distributed Striped

    note: glusterFS Volume vs Kubernetes PV

### GlusterFS for k8s

  * Heketi
    - REST storage management API
    - Receive requests from k8s storage driver
    - use secret to control glusterFS

  * Usage
    - has a glusterFS
    - apply storage class and secret to k8s
    - Create PV
    - Request PVC with Pods

### Demo

  * Env
    - Kubernetes 1.9.2
