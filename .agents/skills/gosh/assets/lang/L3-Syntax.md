# L3 · Syntax

Gosh 句法层规范。定义在 Skill 文档和 Prompt 中使用的结构模式。

---

## S0：XML 标签是 Gosh 的结构单元之一

XML 风格的语义标签是 Gosh 使用的结构单元之一。相比散文分隔、Markdown 标题或缩进层级，XML 标签对 Agent 的块边界识别歧义更低，语义角色更明确。

S1 及后续引用 XML 标签的条目均建立在此基础上。

---

## S1：示例块的规范标签名

S1 的实质是词汇选择：示例块的规范标签名是 `<example>`，不是 `<eg>`、`<sample>`、`<demo>` 或 `Example:` 散文标题。

```
<example>
...
</example>
```

**注**：`<example>` 的命名权可能归属 Lexicon，此处暂存，待学习资料充分后重新分类。

---

## S2：角色标签交替标记对话

在 `<example>` 块内，用 `<user>` 和 `<response>` 显式标记角色切换。

```
<example>
<user>[用户输入]</user>
<response>
[Agent 的行为和输出]
</response>
</example>
```

**原因**：显式角色标签建立清晰的刺激-响应边界，Agent 能精确识别"外部输入在哪里结束、自身输出从哪里开始"，而不依赖换行或缩进推断。

**无缩进**：所有标签齐平，不嵌套缩进，保持线性可读。

**避免**：
```
User: [输入]
Agent: [输出]
```

---

## Ref

- [AMP Claude-Sonnet-4](../../raw/System-Prompts/AMP/Claude-Sonnet-4.yaml)

---

## S3：语义段标签（Semantic Section Wrappers）

自定义 XML 标签作为概念域的段容器，每个标签包裹一个独立的主题模块。标签名直接传达段落的语义目的，创建"语义可寻址"的 Prompt 架构。

### 规范

- 标签名使用小写连字符形式：`<section-name>`
- 标签名应描述段落的**概念域**，而非格式：`<database-rules>` 而非 `<section-3>`
- 段标签可嵌套，但深度不超过 3 层

### 合规示例

```
<intro>
You are an AI coding assistant...
</intro>

<database-rules>
NEVER skip RLS setup for any table.
</database-rules>
```

### 方言变体

| Agent | 方言 | 特征 |
|-------|------|------|
| Manus | `<intro>`, `<agent_loop>`, `<todo_rules>`, `<coding_rules>` | 完整 XML 架构，约 15 个语义段标签 |
| Antigravity | `<identity>`, `<user_rules>`, `<workflows>`, `<knowledge_discovery>` | 语义段 + 属性（如 `<budget:token_budget>`） |
| Comet | `<critical_security_rules>`, `<injection_defense_layer>`, `<prohibited_actions>` | 安全类标签命名极具语义 |
| Cluely | `<core_identity>`, `<general_guidelines>`, `<response_quality_requirements>` | 按内容类型分段 |

---

## S4：规则/约束标签（Rule Tags）

XML 标签包裹具体规则、约束或行为指令。区别于 S3 的段容器，规则标签更细粒度，直接指向指令的类别和执行意图。

### 规范

- 规则标签名以 `_rules`、`_instructions`、`_constraints` 结尾：`<coding_rules>`, `<artifact_instructions>`
- 规则标签内的内容 MUST 是可执行的指令，不是描述性文本

### 合规示例

```
<artifact_instructions>
1. ALWAYS provide the FULL, updated content of modified files
2. NEVER use placeholders like "// rest of the code remains the same"
</artifact_instructions>
```

### 方言变体

| Agent | 方言 | 特征 |
|-------|------|------|
| Manus | `<shell_rules>`, `<todo_rules>`, `<file_rules>`, `<coding_rules>` | 细粒度规则标签 |
| Bolt | `<database_instructions>`, `<artifact_instructions>` | 领域指令标签 |
| Leap | `<refusals>`, `<common-errors>` | 行为约束标签 |
| Comet | `<critical_security_rules>`, `<injection_defense_layer>`, `<mandatory_copyright_requirements>` | 安全/合规规则标签 |

---

## S5：动作标签与类型属性（Action Tags with Typed Attributes）

XML 标签表示可执行动作，通过 `type` 属性区分类别，通过 `path`/`filePath` 属性指定目标。这定义了 Agent 的**输出协议**——不仅是消费结构，而是生产结构。

### 规范

- 动作标签使用 `type` 属性区分动作类别：`type="file"`, `type="shell"`, `type="start"`
- 文件操作 MUST 使用 `path` 或 `filePath` 属性指定目标
- Shell 操作不需要 `path` 属性

### 合规示例

```
<boltArtifact id="snake-game" title="Snake Game">
<boltAction type="file" filePath="index.js">
// file content here
</boltAction>
<boltAction type="shell">
node index.js
</boltAction>
</boltArtifact>
```

### 方言变体

| Agent | 方言 | 特征 |
|-------|------|------|
| Bolt | `<boltAction type="file/shell/start">` | 三类动作 + filePath 属性 |
| Devin | `<shell id="..." exec_dir="...">`, `<str_replace path="..." sudo="True/False">` | 动作标签 + 权限属性 |
| Gemini | `<change><file>...</file><content><![CDATA[...]]></content></change>` | 变更描述结构 |

---

## S6：自闭合引用标签（Self-Closing Reference Tags）

自闭合 XML 标签引用外部内容、文件或代码位置，使用 `path`/`url`/`file` 属性指定来源。

### 规范

- 自闭合标签 MUST 使用 `/>` 结尾
- 引用文件 MUST 使用 `path` 或 `file` 属性
- 引用代码片段 SHOULD 使用 `lines` 或 `start`/`end` 属性限定范围

### 合规示例

```
<ref_file file="/home/ubuntu/path/to/file.py" />
<ref_snippet file="/home/ubuntu/path/to/file.py" lines="10-20" />
<cite repo="REPO_NAME" path="FILE_PATH" start="10" end="20" />
```

### 方言变体

| Agent | 方言 | 特征 |
|-------|------|------|
| Devin | `<ref_file file="..."/>`, `<ref_snippet file="..." lines="..."/>` | 文件/片段引用 |
| Devin/DeepWiki | `<cite repo="..." path="..." start="..." end="..."/>` | 跨仓库引用 |
| Notion | `<mention-user url="..."/>`, `<mention-page url="..."/>` | URL 属性引用 |

---

## S7：对比示例标签（Good/Bad Example Tags）

用 `<good-example>` 和 `<bad-example>` 标签显式标记正确和错误的模式对比。

### 规范

- 对比示例 MUST 成对出现：有 `<bad-example>` 就必须有 `<good-example>`
- 对比示例 SHOULD 在同一 `<example>` 块内

### 合规示例

```
<example>
<bad-example>
const { BarChart } = Recharts;
</bad-example>
<good-example>
import { BarChart } from 'recharts';
</good-example>
</example>
```

### 方言变体

| Agent | 方言 | 特征 |
|-------|------|------|
| Cursor | `<good-example>`, `<bad-example>` XML 标签 | 结构化对比 |
| Gemini | `**Incorrect**` / `**Correct**` Markdown 加粗 | 非结构化对比 |
| Lovable | `❌ WRONG` / `✅ CORRECT` emoji 标记 | 视觉对比 |
| Notion | `GOOD EXAMPLES:` / `BAD EXAMPLE:` 散文标题 | 散文对比 |

---

## S8：混排架构（Mixed Markdown + XML Architecture）

Markdown 用于人类可读的散文段落，XML 用于机器可解析的结构化规则。这是实际 Agent Prompts 中最普遍的架构模式。

### 规范

- 散文说明使用 Markdown（标题、段落、列表）
- 结构化规则、工具定义、输出协议使用 XML 标签
- 同一文档内两种格式各司其职，不混用：不在 XML 标签内使用 Markdown 标题，不在 Markdown 段落内嵌入 XML 规则块

### 合规示例

```
# Database Rules

<database-rules>
NEVER skip RLS setup for any table.
</database-rules>
```

### 方言变体

| Agent | 方言 | 特征 |
|-------|------|------|
| Notion | Markdown 标题 + `<advanced-blocks>` | 混排架构 |
| Leap | Markdown + `<encore_ts_domain_knowledge>` | 深度嵌套 XML 知识库 |
| Cursor | Markdown + `<tool_calling>`, `<making_code_changes>` | XML 规则块嵌入 Markdown |
| Bolt | Markdown + `<artifact_instructions>` | XML 指令块嵌入 Markdown |

---

## S9：工具定义格式（Tool Definition Formats）

Agent 定义可用工具的三种主流格式。

### S9.1：JSON Schema 格式

```json
{
  "name": "tool_name",
  "description": "...",
  "parameters": { ... }
}
```

**使用 Agent**：Manus, Notion, Lovable, Augment

### S9.2：TypeScript 类型格式

```typescript
namespace functions {
type tool_name = (_: {
  param: string,
}) => any;
}
```

**使用 Agent**：Cursor

### S9.3：XML 工具列表格式

```xml
<tool name="tool_name">
<description>...</description>
<parameters>...</parameters>
</tool>
```

**使用 Agent**：Devin, Bolt

### 规范

- 同一文档 MUST 只使用一种工具定义格式
- 工具名 MUST 使用 PascalCase 或 snake_case，全文一致

---

## S10：非 XML 结构模式（Non-XML Structural Patterns）

### S10.1：YAML Front Matter

`---` 界定的元数据块，附着在 Markdown 文档开头。

**使用 Agent**：Kiro, Antigravity

### S10.2：GitHub-Style Alerts

`> [!NOTE]`, `> [!WARNING]`, `> [!IMPORTANT]` 分级提示语法。

**使用 Agent**：Antigravity, Notion

### S10.3：Diff / SEARCH-REPLACE 标记

```
<<<<<<< SEARCH
exact content to find
=======
new content to replace with
>>>>>>> REPLACE
```

**使用 Agent**：CodeBuddy, Antigravity

### S10.4：EARS 需求语法

`WHEN [event] THEN [system] SHALL [response]` — 形式化需求表达。

**使用 Agent**：Kiro

### S10.5：复选框任务列表（扩展状态）

`- [ ]` 未完成 / `- [/]` 进行中 / `- [x]` 已完成

**使用 Agent**：Kiro, Antigravity

---

## Ref（更新版）

- [AMP Claude-Sonnet-4](../../raw/System-Prompts/AMP/Claude-Sonnet-4.yaml)
- [AMP GPT-5](../../raw/System-Prompts/AMP/GPT-5.yaml)
- [Antigravity Prompt](../../raw/System-Prompts/Antigravity/Prompt.md)
- [Bolt Prompt](../../raw/System-Prompts/Bolt/Prompt.md)
- [Bolt Tools](../../raw/System-Prompts/Bolt/Tools.md)
- [Cluely Default](../../raw/System-Prompts/Cluely/Default.md)
- [CodeBuddy Craft](../../raw/System-Prompts/CodeBuddy/Craft.md)
- [Comet Assistant](../../raw/System-Prompts/Comet/Assistant.md)
- [Cursor Agent-v2](../../raw/System-Prompts/Cursor/Agent-v2.md)
- [Devin Prompt](../../raw/System-Prompts/Devin/Prompt.md)
- [Devin DeepWiki](../../raw/System-Prompts/Devin/DeepWiki.md)
- [Gemini Coder](../../raw/System-Prompts/Gemini/Coder.md)
- [Kiro Prompt](../../raw/System-Prompts/Kiro/Prompt.md)
- [Kiro Spec](../../raw/System-Prompts/Kiro/Spec.md)
- [Leap Expert](../../raw/System-Prompts/Leap/Expert.md)
- [Lovable Prompt](../../raw/System-Prompts/Lovable/Prompt.md)
- [Manus Modules](../../raw/System-Prompts/Manus/Modules.md)
- [Notion Expert](../../raw/System-Prompts/Notion/Expert.md)

---

## S11：YAML 信封架构（YAML Envelope Architecture）

系统 Prompt 作为结构化数据对象（YAML/JSON），而非文本文档。`system`、`tools`、`stream`、`thinking`、`cache_control` 等作为一等字段。

### 规范

- YAML 信封中的文本段 MUST 通过 `system:` 字段传递
- 工具定义 MUST 通过 `tools:` 字段传递
- 缓存控制 SHOULD 通过 `cache_control` 字段标注

### 合规示例

```yaml
system:
  - type: text
    text: |
      You are Amp, a powerful AI coding agent...
    cache_control:
      type: ephemeral
tools:
  - name: Read
    description: Read a file from the file system
    input_schema: { ... }
thinking:
  type: enabled
  budget_tokens: 4000
```

**使用 Agent**：AMP（Claude-Sonnet-4.yaml, GPT-5.yaml）

---

## S12：流程工作流块（Procedural Workflow Block）

`<workflow-definition>` 包裹顺序阶段（含约束、审批门和排障），编码时序逻辑。区别于 S3（静态语义段），S12 编码的是动态流程。

### 规范

- 工作流 MUST 包含有序阶段（Requirements → Design → Tasks 等）
- 每个阶段 SHOULD 有明确的审批门（用户确认工具调用）
- 工作流 MUST 用 XML 标签包裹整个流程定义

### 合规示例

```xml
<workflow-definition>
1. Requirements Gathering
   - The model MUST create requirements.md
   - The model MUST NOT proceed until receiving approval
2. Design Document
   - The model MUST create design.md
3. Task List
   - The model MUST create tasks.md with checkbox items
</workflow-definition>
```

**使用 Agent**：Kiro（Spec.md）

---

## S13：RFC 2119 约束模态（RFC 2119 Constraint Modality）

系统性使用 MUST / MUST NOT / SHOULD / MAY / SHOULD NOT 作为约束前缀，语义词来自 RFC 2119。

### 规范

- MUST = 无条件义务
- MUST NOT = 绝对禁止
- SHOULD = 推荐但允许例外
- SHOULD NOT = 不推荐但非绝对禁止
- MAY = 可选项

### 合规示例

- `The model MUST create a requirements.md file`
- `The model MUST NOT proceed to the design document until receiving approval`
- `The model SHOULD ask the user for clarification`

**使用 Agent**：Kiro（Spec.md）

---

## S14：模式门控工具面（Mode-Gated Tool Surface）

工具可用性根据操作模式（CRAFT vs CHAT）条件化。不同模式下，Agent 可访问的工具集不同。

### 规范

- 模式切换 MUST 通过显式指令或工具调用触发
- 每个模式 MUST 有明确定义的可用工具集
- 模式间切换 MUST 有明确的进入/退出条件

**使用 Agent**：CodeBuddy（Craft.md — CRAFT MODE vs CHAT MODE）

---

## S15：内联项目脚手架（Inlined Project Scaffold）

将完整文件内容（数百行代码）作为运行时上下文嵌入 Prompt，为模板化 Agent 提供起点。

### 规范

- 内联脚手架 MUST 放在独立的上下文标签内（如 `<initial context>`）
- 文件内容 MUST 使用代码围栏包裹并标注语言
- 脚手架文件 MUST 是可执行的，不是伪代码

**使用 Agent**：Emergent（Prompt.md — `<initial context>` 包含 use-toast.js, App.js, App.css 等）
