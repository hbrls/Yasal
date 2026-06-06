# Imperatives

Imperatives are words and local forms that impose obligation, prohibition, priority, or attention control on an Agent.

## Principle

Imperatives are not governed by uniqueness. They are governed by strength level and scenario fit.

## Strength Levels

| Level | Function | Terms |
|-------|----------|-------|
| ★★★★ | Highest attention flag | `ULTRA IMPORTANT`, `SUPER IMPORTANT` |
| ★★★ | Hard obligation or prohibition | `MUST`, `NEVER`, `ALWAYS`, `MANDATORY`, `STRICTLY FORBIDDEN`, `PROHIBITED`, `FORBIDDEN`, `YOU MUST NEVER`, `REQUIRED`, `ONLY` |
| ★★ | Medium priority or scoped refusal | `IMPORTANT`, `WARNING`, `REFUSE`, `immediately` |
| ★ | Weak forms | `should`, `avoid`, `try to`, `generally`, `usually`, `recommend` |

## Hard Imperatives

| Word | Function | Strength | Replaces |
|------|----------|----------|----------|
| `MUST` | 声明无条件义务 | ★★★ | should, need to, it is recommended to |
| `NEVER` | 声明绝对禁止 | ★★★ | avoid, try not to, refrain from, don't |
| `ALWAYS` | 声明无例外要求 | ★★★ | generally, usually, in most cases |
| `MANDATORY` | 声明强制执行义务，独立前缀标签形式 | ★★★ | should, need to |
| `STRICTLY FORBIDDEN` | 绝对禁止复合形式，强于 `NEVER`，含规则执行语气 | ★★★ | avoid, do not, not allowed |
| `PROHIBITED` | 段落/XML 块级禁止声明，用于列出禁止行为清单 | ★★★ | not allowed, cannot, avoid |
| `FORBIDDEN` | 段落/XML 块级禁止声明，用于列出禁止行为清单 | ★★★ | not allowed, cannot, avoid |
| `YOU MUST NEVER` | `MUST` + `NEVER` 叠加复合形式，用于不可违背的硬性禁令 | ★★★ | YOU MUST NOT, please don't, avoid |
| `REQUIRED` | 属性/参数级义务标注，独立出现，无需主语 | ★★★ | optional, recommended, should |
| `ONLY` | 范围限定型禁止，通过排他性约束禁止范围外行为 | ★★★ | just, limited to, prefer |
| `REFUSE` | 特殊禁止动词，用于拒绝特定类型的请求 | ★★ | decline, reject, do not answer |

## Attention Flags

| Word | Function | Strength | Replaces |
|------|----------|----------|----------|
| `IMPORTANT` | 标记高优先级指令，要求 Agent 重新分配注意力 | ★★ | note that, keep in mind, be aware that, remember |
| `CRITICAL` | 高强度注意力旗帜，用于不可忽视的约束 | ★★★ | very important, key point, essential |
| `ULTRA IMPORTANT` | 强度高于 `CRITICAL`，用于绝对核心约束 | ★★★★ | most important, absolutely critical |
| `SUPER IMPORTANT` | 同 `ULTRA IMPORTANT`，口语化表达 | ★★★★ | extremely important, crucial |
| `WARNING` | 段落标题级注意力旗帜，作为独立行/标题使用 | ★★ | Note:, Caution:, Be careful: |

## Temporal Imperatives

| Word | Function | Strength | Example |
|------|----------|----------|---------|
| `immediately` | 要求立即执行，不得延迟 | ★★ | `Immediately call a tool if the request can be resolved` |

## Local Forms

| Form | Function | Strength | Example |
|------|----------|----------|---------|
| `NEVER X unless Y` | 禁止 + 例外子句：明确边界，防止 Agent 误判例外 | ★★★ | `NEVER modify a user's content unless explicitly asked to do so.` |
| `IMPORTANT: [禁止/义务]` | 优先级前置标记 + 具体约束 | ★★★ | `IMPORTANT: Don't stop to ask whether to search.` |
| `REQUIRED` | 单词独立出现，无主语无解释 | ★★★ | `title: … REQUIRED` |
| `This is CRITICAL` | 强调前置标记 + 内容 | ★★★ | `Start with the design system. This is CRITICAL.` |
| `CRITICAL: [约束]` | 标题级注意力旗帜 + 具体约束 | ★★★ | `CRITICAL: keep explanations short and concise` |
| `MUST NOT X` | `MUST` + `NOT` 复合禁止 | ★★★ | `It MUST NOT be included in the artifact.` |

## Weak Forms

The following forms are weaker than the standard imperatives. When they express the same function, replace them with the standard form.

| Weak Form | Observed Source | Standard Replacement |
|-----------|-----------------|----------------------|
| `Do NOT` / `do NOT` | AMP, Augment, CodeBuddy, Cluely | `NEVER` |
| `Don't` / `don't` | Augment, AMP, Cluely Enterprise, Emergent | `NEVER` |
| `DON'T` | Devin DeepWiki | `NEVER` |
| `Never` | Devin Prompt, Emergent | `NEVER` |
| `Do not` | Devin Prompt, Emergent | `NEVER` |
| `DO NOT` | Devin DeepWiki, CodeBuddy Craft, Emergent | `NEVER` |
| `avoid` | AMP | `NEVER` |
| `never` | Comet, Cluely Enterprise | `NEVER` |

## Corpus Snapshot

Based on `.agents/skills/gosh/raw/System-Prompts/`:

| Class | High Frequency | Medium Frequency | Low Frequency |
|-------|----------------|------------------|---------------|
| Imperatives | `MUST`, `NEVER`, `ALWAYS` | `ONLY`, `DO NOT`, `MUST NOT` | `REQUIRED`, `MANDATORY`, `FORBIDDEN`, `REFUSE` |
| Attention Flags | `IMPORTANT`, `CRITICAL` | `ULTRA IMPORTANT`, `SUPER IMPORTANT` | — |
| Weak Forms | `Avoid`, `avoid`, `cannot` | `Do NOT` | lowercase `never` |

## References

- [AMP Claude-Sonnet-4](../../../raw/System-Prompts/AMP/Claude-Sonnet-4.yaml)
- [AMP GPT-5](../../../raw/System-Prompts/AMP/GPT-5.yaml)
- [Augment Claude-Sonnet-4](../../../raw/System-Prompts/Augment/Claude-Sonnet-4.txt)
- [Augment GPT-5](../../../raw/System-Prompts/Augment/GPT-5.txt)
- [Bolt Prompt](../../../raw/System-Prompts/Bolt/Prompt.md)
- [Cluely Default](../../../raw/System-Prompts/Cluely/Default.md)
- [Cluely Enterprise](../../../raw/System-Prompts/Cluely/Enterprise.md)
- [CodeBuddy Craft](../../../raw/System-Prompts/CodeBuddy/Craft.md)
- [Comet Assistant](../../../raw/System-Prompts/Comet/Assistant.md)
- [Cursor Agent-v2](../../../raw/System-Prompts/Cursor/Agent-v2.md)
- [Cursor GPT-4](../../../raw/System-Prompts/Cursor/GPT-4.md)
- [Cursor GPT-5-20250807](../../../raw/System-Prompts/Cursor/GPT-5-20250807.md)
- [Cursor GPT-5-20250903](../../../raw/System-Prompts/Cursor/GPT-5-20250903.md)
- [Devin DeepWiki](../../../raw/System-Prompts/Devin/DeepWiki.md)
- [Devin Prompt](../../../raw/System-Prompts/Devin/Prompt.md)
- [Emergent Prompt](../../../raw/System-Prompts/Emergent/Prompt.md)
- [Emergent Tools](../../../raw/System-Prompts/Emergent/Tools.json)
- [Gemini Coder](../../../raw/System-Prompts/Gemini/Coder.md)
- [Junie Prompt](../../../raw/System-Prompts/Junie/Prompt.md)
- [Leap Prompt](../../../raw/System-Prompts/Leap/Prompt.md)
- [Lovable Prompt](../../../raw/System-Prompts/Lovable/Prompt.md)
- [Manus Prompt](../../../raw/System-Prompts/Manus/Prompt.md)
- [Notion Expert](../../../raw/System-Prompts/Notion/Expert.md)
- [Notion Prompt](../../../raw/System-Prompts/Notion/Prompt.md)
- [Notion Tools](../../../raw/System-Prompts/Notion/Tools.md)
- [Antigravity Prompt](../../../raw/System-Prompts/Antigravity/Prompt.md)
- [Kiro Prompt](../../../raw/System-Prompts/Kiro/Prompt.md)
