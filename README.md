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

## 象棋教練（Xiangqi Coach）

A full-size Chinese chess (象棋) board where you (red) play against the computer (black), with a built-in coach.

- Open `/xiangqi` on the deployed app (or open `xiangqi/index.html` directly in a browser).
- After every move the coach rates it. If it was a mistake, the coach shows the opponent's punishing reply, a better move, and how to think about it, then pauses so you can take the move back (悔棋).
- 「提示」 gives a hint in two steps: first the idea, then the move. 「我該怎麼想？」 walks through a thinking checklist for the current position.
- Pieces that are in danger are circled. You can ask questions in the chat box (rules, terms, threats, "what should I play?").
- Open-ended questions go to the OpenAI chat model through `POST /xiangqi/api/ask`, using `OPENAI_API_KEY`. The engine's analysis is passed along so the answer stays accurate. Without a key, the built-in coach answers instead.

## 圍棋教練（Go Coach）

A Go board at `/weiqi` (or open `weiqi/index.html` directly) with large (19×19), medium (13×13) and small (9×9) sizes. You can play against the computer or with a friend.

- Uses Chinese area scoring with 7.5 komi. After both players pass, the page enters scoring mode. Likely dead stones are marked automatically, and you can tap a group to change it.
- The coach warns about groups with only one liberty (in atari), points out stones you can capture, and flags self-atari or an ignored atari.
- 「提示」 gives a hint in two steps, and 「下一步」 plays the suggested move and explains it.
- The game is saved in the browser and restored when you come back.
- The computer opponent uses simple rules of thumb and plays at beginner level.

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
