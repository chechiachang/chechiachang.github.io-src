Source Code of My Github Page
===

[https://chechiachang.github.io](https://chechiachang.github.io)

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
- Add site https://chechiachang.github.io
  - Authorized by google analysis with google email account
- Submit https://chechiachang.github.io/sitemap.xml to console
- Wait for data processing
