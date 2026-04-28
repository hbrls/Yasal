# L7 · Dialect

Gosh 方言维度规范。记录不同 Agent 对标准语的已验证偏差。

**NEVER** 在无明确方言信号的情况下引入方言表达——使用标准语。

---

## S2 方言：示例块格式（Example Block）

标准语为 `<example>/<user>/<response>` XML 标签（参见 `L3-Syntax.md` S2）。各 Agent 存在以下方言变体：

| Agent | 示例块方言 | 特征 |
|------|-----------|------|
| **AMP Claude-Sonnet-4** | `<example>/<user>/<response>` | 标准语，无偏差 |
| **AMP GPT-5** | `**User**` / `**Assistant**` + `>` 引用块 | Markdown 格式替代 XML；出现在 todo_write 示例中 |
| **AMP（两版本）`<git-example>`** | `user: text` / `assistant: text` 冒号标签 | 专用于 git 示例，非对话格式 |
| **Cluely Enterprise** | `<transcript_sample>` / `<response_sample>` | 自定义标签名；用于面试/会议场景 |
| **Augment** | `<augment_code_snippet path=... mode="EXCERPT">` | 专用代码展示标签；无 S2 对话示例 |

### 方言触发条件

只有以下情况允许使用方言：
1. 目标 Agent 极为明确（上述表格中已验证）
2. 标准 `<example>/<user>/<response>` 无法在该 Agent 的渲染上下文中正常显示

---

## L1 方言：约束词大小写（Comet）

Comet 全文使用小写 `never`（如 `Comet never stops prematurely`），而非规范词 `NEVER`。

这是 Comet 的风格偏差，不是标准写法。非 Comet 目标文档 MUST 使用 `NEVER`。

---

## Ref

- [AMP Claude-Sonnet-4](../../raw/System-Prompts/AMP/Claude-Sonnet-4.yaml)
- [AMP GPT-5](../../raw/System-Prompts/AMP/GPT-5.yaml)
- [Cluely Enterprise](../../raw/System-Prompts/Cluely/Enterprise.md)
- [Augment Claude-Sonnet-4](../../raw/System-Prompts/Augment/Claude-Sonnet-4.txt)
- [Comet Assistant](../../raw/System-Prompts/Comet/Assistant.md)
