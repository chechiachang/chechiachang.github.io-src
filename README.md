Source Code of My Github Page
===

[https://chechia.net](https://chechia.net)

### hugo

```
hugo version
hugo v0.147.7-189453612e4bedc4f27495a7b1145321c8d89807+extended darwin/arm64 BuildDate=2025-05-31T12:41:12Z VendorInfo=gohugoio
```

### PaperMod Theme for Hugo

https://github.com/adityatelange/hugo-PaperMod/wiki/Installation

```
git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
git submodule update --init --recursive

git submodule update --remote --merge
```

### Reveal Slides

https://github.com/joshed-io/reveal-hugo?tab=readme-ov-file#tutorial-add-a-revealjs-presentation-to-an-existing-hugo-site

```
hugo mod init github.com/chechiachang/chechiachang.github.io-src
hugo mod get github.com/joshed-io/reveal-hugo
```

### Bind google analysis

Google Analytics
- Add a new account
  - Filling form
  - Get Google Analytics tracking ID

Enable analytics by entering your Google Analytics tracking ID
```
# config/_default/config.toml
googleAnalytics = ""
```

### Bind google search

- go to google search console
- Add site https://chechia.net
  - Authorized by google analysis with google email account
- Submit https://chechia.net/sitemap.xml to console
- Wait for data processing
