Source Code of My Github Page
===

[https://chechia.net](https://chechia.net)

# Powered by Hugo

# Theme

[Academic](https://sourcethemes.com/academic/docs/install/)

# Create Content

Add new talk
```
TITLE=my-talk-title make talk
```

Add new project
```
TITLE=my-talk-title make project
```

# Bind google analysis

Google Analytics
- Add a new account
  - Filling form
  - Get Google Analytics tracking ID

Enable analytics by entering your Google Analytics tracking ID
```
# config/_default/config.toml
googleAnalytics = ""
```

Publish /public to github
```
make hugo publish
```

# Bind google search

- go to google search console
- Add site https://chechia.net
  - Authorized by google analysis with google email account
- Submit https://chechia.net/sitemap.xml to console
- Wait for data processing

# TODOs

- [x] ITHome 30 days ironman challenge
  - [x] https://ithelp.ithome.com.tw/users/20120327/ironman/2444

Features
- [x] step-by-step guide for deployment: guarentee a running deployment on GCP
- [x] basic configuration, usage, monitoring, networking on GKE
- [x] debugging, stability analysis in an aspect of devop
