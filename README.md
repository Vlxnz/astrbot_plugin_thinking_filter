# AstrBot Thinking Filter

在 AstrBot 发送消息前移除模型意外泄露的 `<thinking>` 和 `<analysis>` 推理块，保留正常回答文本。

## 功能

- 过滤成对的 `<thinking>...</thinking>` 标签，大小写不敏感并允许标签属性。
- 过滤成对的 `<analysis>...</analysis>` 标签。
- 过滤没有闭合标签的推理块及其后续内容。
- 在 LLM 响应阶段和最终发送前各检查一次，兼容不同响应链。
- 只修改 `Plain` 文本组件，不改图片、文件、At 等其他消息组件。

## 安装

1. 从 Releases 下载 `astrbot_plugin_thinking_filter.zip`。
2. 在 AstrBot 的插件管理中选择本地 ZIP 安装。
3. 重启或重新加载插件。

ZIP 顶层目录为 `astrbot_plugin_thinking_filter/`。

也可以直接在 AstrBot 中通过本 GitHub 仓库地址安装。

## 说明

这是发送前的文本清理器，不负责阻止模型生成推理内容，也不会删除普通文本中的关键词。没有闭合的 `<thinking>` 或 `<analysis>` 标签会被视为从标签开始直到文本末尾均属于泄露内容，因此后续文本会被丢弃。

## 本地测试

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

## 构建安装包

```powershell
python build_zip.py
```

## 仓库结构

```text
astrbot_plugin_thinking_filter/
|-- __init__.py
|-- main.py
|-- metadata.yaml
|-- test_filter.py
|-- build_zip.py
|-- README.md
`-- LICENSE
```

## 发布前设置

创建 GitHub 仓库后，将 `metadata.yaml` 中的 `repo` 填为仓库完整 URL。作者字段也可以按实际 GitHub 用户名修改。

## 许可证

MIT License，见 [LICENSE](LICENSE)。
