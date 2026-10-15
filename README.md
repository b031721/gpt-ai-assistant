# GPT AI Assistant

<div align="center">

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/release/memochou1993/gpt-ai-assistant)](https://GitHub.com/memochou1993/gpt-ai-assistant/releases/)

</div>

GPT AI Assistant is an application that is implemented using the OpenAI API and LINE Messaging API. Through the installation process, you can start chatting with your own AI assistant using the LINE mobile app.

## News

- 2023-05-03: The `4.6` version now support `gpt-4` OpenAI model. :fire:
- 2023-03-05: The `4.1` version now support the audio message of LINE and  `whisper-1` OpenAI model. :fire:
- 2023-03-02: The `4.0` version now support `gpt-3.5-turbo` OpenAI model. :fire:

## Demo

<img src="/demo/labot.png" width="300"/>

## Documentations

- <a href="https://memochou1993.github.io/gpt-ai-assistant-docs/" target="_blank">中文</a>
- <a href="https://memochou1993.github.io/gpt-ai-assistant-docs/en" target="_blank">English</a>

## Credits

- [jayer95](https://github.com/jayer95) - Debugging and testing
- [kkdai](https://github.com/kkdai) - Idea of `sum` command
- [Dayu0815](https://github.com/Dayu0815) - Idea of `search` command
- [mics8128](https://github.com/mics8128) - Implementing new features
- [All other contributors](https://github.com/memochou1993/gpt-ai-assistant/graphs/contributors)

## Contact

If there is any question, please contact me at memochou1993@gmail.com. Thank you.

## Changelog

Detailed changes for each release are documented in the [release notes](https://github.com/memochou1993/gpt-ai-assistant/releases).

## License

[MIT](LICENSE)

## 線上電子書閱讀器

`/reader/` 是一個單頁的電子書閱讀器，往下捲動就能連續讀完整本書（不用按上一頁、下一頁）。它有目錄、字體大小和行距調整、米黃／白／夜間三種主題，會自動記住閱讀位置，也可以直接加入手機或電腦裡的 `.epub`（例如從好讀下載的 epub 檔）或 `.txt` 電子書，加入的書會存在瀏覽器裡。

- 書架清單：`public/reader/books/index.json`
- 下載《動物農莊》英文原文（公有領域）：`node scripts/fetch-animal-farm.mjs`

### 用 GitHub Pages 免費上線

`docs/index.html` 是閱讀器的複本，給 GitHub Pages 用（改 `public/reader/index.html` 後要再複製一份過去）。到 GitHub 專案的 Settings → Pages，Source 選「Deploy from a branch」，Branch 選這個分支、資料夾選 `/docs`，存檔後網址會是 `https://<帳號>.github.io/gpt-ai-assistant/`，任何人打開都不用登入。
