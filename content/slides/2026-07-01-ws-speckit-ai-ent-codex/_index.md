---
title: "Cloud Summit Workshop: Spec-driven development with Spec-kit"
description: "90 分鐘 hands-on workshop，從 Vibe Coding 走向 Spec-driven Development（SDD），用 Spec-kit 完成從規格到實作的完整流程。"
tags: ["ai", "sdd", "spec-kit", "workshop", "devops", "agent"]
categories: ["ai", "workshop"]
date: '2036-05-02T09:00:00Z'
outputs: ["Reveal"]
reveal_hugo:
  custom_theme: "reveal-hugo/themes/robot-lung.css"
  margin: 0.2
  highlight_theme: "color-brewer"
  transition: "slide"
  transition_speed: "fast"
---
{{% section %}}

### Workshop 行前準備

- 攜帶筆電，可上網
- 安裝好操作環境
  - [VS Code](https://code.visualstudio.com/) + [Codex Extension](https://developers.openai.com/codex/ide#extension-setup)
  - [Spec-kit CLI](https://github.com/github/spec-kit#1-install-specify-cli)
- 下載 [workshop 範例程式碼](https://github.com/chechiachang/speckit-playground)
- 講師會提供 Azure OpenAI API Key，也可帶自己習慣的 llm
- 已經會用 VS Code + Codex，用自己的方式參加即可

🔽

---

### VS Code

- 安裝 VS Code：[https://code.visualstudio.com/](https://code.visualstudio.com/)
  - Terminal 或命令提示字元開啟 VS Code

```
git clone https://github.com/chechiachang/speckit-playground.git

code .
```

- VS Code 中 Terminal
  - git clone 程式碼 `speckit-playground`
  - File > Open Folder > 選擇 clone 的 speckit-playground

---

{{< slide background-image="git-clone.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### VS Code Extension

- 安裝 [Codex Extension](https://developers.openai.com/codex/ide#extension-setup)
  - cmd + shift + x，搜尋 Codex，安裝
  - 認明官方網址，其他來源的 extension 可能不安全
- 在 VS Code 右側 Secondary Sidebar 找到 Codex
  - 跟 Codex say hi，使用免費額度，或登入個人的 OpenAI 帳號

---

{{< slide background-image="install-codex-extension.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 安裝 Spec-kit CLI

- 打開 VScode 下方的 Terminal
- 確認 uv 可用，沒有的話[先裝 uv](https://github.github.com/spec-kit/install/uv.html)
- 安裝 [Spec-kit CLI](https://github.github.com/spec-kit/installation.html#installation)

```
# 確認 uv 可用
uv --version

# 安裝指定穩定版
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git@v0.8.9
```

---

{{< slide background-image="install-specify-cli.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### API Key 設定

- 備份原本的 config.toml，以免覆蓋到自己的設定
- codex-config.toml 複製到 codex 的 config.toml
- 如果你本來就有在用 codex
  - 也可自行複製，編輯成喜歡的樣子

```
cp ~/.codex/config.toml ~/.codex/config.toml.bak

cp codex-config.toml ~/.codex/config.toml
```

{{% note %}}

- 打開檔案 `speckit-playground/codex-config.toml`
- 全選複製
- VS Code Extension 右上角齒輪 > Codex settings
- Configuration > Open config.toml
- 貼上複製的內容，存檔
- 如果已經有自己的 config.toml，請把內容貼在檔案的上面

{{% /note %}}

---

{{< slide background-image="copy-config-toml.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

```
# 關掉 VS Code，重新用 Terminal 開啟，讓環境變數生效

export AZURE_OPENAI_API_KEY="講師提供的 api key"

# 啟動 vscode
code .
```
---

### VS Code Extension: Linux/MacOS

- cmd + space，輸入 Terminal，開啟終端機

```
export AZURE_OPENAI_API_KEY="講師提供的 api key"
code .
```

---

{{< slide background-image="export-and-code.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### 如果 Terminal 沒有出現 code 指令

- 打開 VS Code
- cmd + shift + p，輸入 shell command，選擇 Install 'code' command in PATH
- 關掉 VS Code，重新用 Terminal 開啟，讓環境變數生效

---

{{< slide background-image="install-code-command.png" background-size="80%" background-color="#000000" background-opacity="1" >}}

---

### VS Code Extension: Windows

- Win + R，輸入 cmd，開啟命令提示字元

```
set AZURE_OPENAI_API_KEY="講師提供的 api key"
code .
```

---

### 行前準備完成

- 修改完成後，由於缺乏環境變數，Codex 可能會跳出錯誤
  `Missing environment variable: AZURE_OPENAI_API_KEY`
- 活動當天取得 API Key 後，設定好環境變數就可以使用
- 如果要使用 Codex，可以暫時移除 ~/.codex/config.toml，使用預設設定

{{% /section %}}
