# Target: Aider

调研日期: 2026-05-07
官方文档: https://aider.chat/docs/

## 1. 摘要

Aider 是 git-native CLI，配置以 `.aider.conf.yml` 为核心，分用户级与项目级，
按 home -> git root -> cwd 顺序加载（后覆盖前）。

Aider **不自动消费** `AGENTS.md`，必须通过 `read:` 配置或 `--read AGENTS.md`
显式声明；该机制本质是把文件标记为只读上下文并参与 prompt cache。

Aider **不支持任何形式的 skill / agent / persona / 自定义 chat mode**，
只有 4 个内置 chat modes：`code`、`ask`、`architect`、`help`。
唯一扩展点是 `--load <file>` 启动脚本（顺序执行内置 slash 命令）。

## 2. 配置文件路径

| 类型 | 路径 | 说明 |
|---|---|---|
| 用户全局 | `~/.aider.conf.yml` | home 目录 |
| 项目级 P0 | `<git-root>/.aider.conf.yml` | git 仓库根 |
| 项目级 P1 | `<cwd>/.aider.conf.yml` | 当前工作目录 |
| 环境变量 | `<git-root>/.env` | 默认 git root；可被 `--env-file` 覆盖 |
| 忽略文件 | `<git-root>/.aiderignore` | 控制可编辑范围，自动加载 |

加载顺序：home -> git root -> cwd，**后加载者覆盖先加载者**。

## 3. 文件格式

| 文件 | 格式 | frontmatter |
|---|---|---|
| `.aider.conf.yml` | YAML | 无 frontmatter 概念 |
| `AGENTS.md` / `CONVENTIONS.md` | Markdown | 无 |
| 启动脚本（`--load`） | 纯文本，每行一个内置 slash 命令 | 无 |

## 4. .aider.conf.yml 关键字段

```yaml
read:
  - CONVENTIONS.md
  - AGENTS.md
model: claude-sonnet-4-6
auto-commits: true
git: true
test-cmd: "pytest -q"
```

## 5. std-ai 四类映射

| std-ai 类型 | Aider 落点 | 加载方式 |
|---|---|---|
| rules | `CONVENTIONS.md`（推荐）或 `AGENTS.md`，经 `read:` 显式声明 | 显式 |
| skills | 不支持（aider 无 skill / agent / persona / chat-mode 扩展点） | 降级为 rules 段落写入 AGENTS.md |
| commands | `--load <file>` 启动脚本批量注入内置 slash | 启动期一次性执行 |
| references | `read: [file1, file2]` 列表 / `/read-only <path>` | 显式只读上下文 |

## 6. Chat modes（仅 4 个内置，不可扩展）

- `code` 修改代码
- `ask` 讨论不改
- `architect` 双模型工作流（architect 提议 + editor 落地）
- `help` 关于 aider 自身的问答

通过 `--chat-mode` 启动参数或 `/chat-mode` 内置命令切换。

## 7. 内置 slash 命令完整清单（不可扩展）

`/add /architect /ask /chat-mode /clear /code /commit /context /copy
/copy-context /diff /drop /edit /editor /editor-model /exit /git /help
/lint /load /ls /map /map-refresh /model /models /multiline-mode /ok
/paste /quit /read-only /reasoning-effort /report /reset /run /save
/settings /test /think-tokens /tokens /undo /voice /weak-model /web`

可定制项仅限模型选择（`--editor-model`）、edit format（`--editor-edit-format`）、
主模型选择，属于参数级配置而非 agent 扩展点。

## 8. 转换器实现要点

1. v1.0 默认行为：仅生成 / 维护项目根 `AGENTS.md`（已由 codex transformer 写）
2. 可选写入 `<git-root>/.aider.conf.yml`：在 `read:` 字段添加 `AGENTS.md`、
   `CONVENTIONS.md`（如存在）。如该文件已被用户手写，需检测 marker 避免覆盖；
   v1.0 默认不主动改写 `.aider.conf.yml`，只在 `init --aider` 显式开关时写
3. v1.0 不生成 `--load` 启动脚本（不在 commands 转换范围）
4. `.aiderignore` 不主动写入

## 9. 信息来源

- https://aider.chat/docs/config/aider_conf.html
- https://aider.chat/docs/config/options.html
- https://aider.chat/docs/usage/conventions.html
- https://aider.chat/docs/usage/commands.html
- https://aider.chat/docs/usage/modes.html

## 10. 已确认

- aider 完全不支持任何形式的 skill / agent / persona / 自定义 chat mode 扩展
- 唯一扩展点：`--load <file>` 启动脚本（顺序执行内置 slash）
- 当前未见官方 AGENTS.md 自动加载提案；仍需 `read:` 显式声明

无重大剩余 UNKNOWN。
