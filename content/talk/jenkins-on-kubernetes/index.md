+++
title = "Jenkins on Kubernetes"

# Talk start and end times.
#   End time can optionally be hidden by prefixing the line with `#`.
date = 2019-04-20T13:00:00+08:00
date_end = 2019-04-20T18:00:00+08:00
all_day = false

# Schedule page publish date (NOT talk date).
publishDate = 2019-04-09T15:29:21+08:00

# Authors. Comma separated list, e.g. `["Bob Smith", "David Jones"]`.
authors = []

# Location of event.
location = "達文西會議空間 - 羅馬廳（台北市南京東路二段6號6樓）"

# Name of event and optional event URL.
event = "DevOps 大亂鬥"
event_url = "https://battle.devopstw.club/"

# Abstract. What's your talk about?
abstract = "Jenkins is one of the most long popular CI frameworks based on Java. Jenkins provides deep customization, features enriched by hundreds of plugins to support any projects."

# Summary. An optional shortened abstract.
summary = "Working pipeline with jenkins-x on Kubernetes."
# Is this a featured talk? (true/false)
featured = false

# Tags (optional).
#   Set `tags = []` for no tags, or use the form `tags = ["A Tag", "Another Tag"]` for one or more tags.
tags = ["kubernetes", "jenkins", "devops"]

# Markdown Slides (optional).
#   Associate this page with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides = "example-slides"` references 
#   `content/slides/example-slides.md`.
#   Otherwise, set `slides = ""`.
slides = ""

# Optional filename of your slides within your talk folder or a URL.
url_slides = ""

# Projects (optional).
#   Associate this talk with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `projects = ["deep-learning"]` references 
#   `content/project/deep-learning/index.md`.
#   Otherwise, set `projects = []`.
projects = [
  "jenkins-x-on-kubernetes",
]

# Links (optional).
url_pdf = ""
url_video = ""
url_code = ""

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
[image]
  # Caption (optional)
  caption = "jenkins-x.png"

  # Focal point (optional)
  # Options: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight
  focal_point = "Top"
+++

1. How to deploy a cloud-native Jenkins with Jenkins X.
2. A pipeline with Kubernetes based dynamics worker sclaing (jenkins-kubernetes).
3. Give it a try.
4. (Defered) Customized test reports for multiple language (ex. go-junit-report)
