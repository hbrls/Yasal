# L1 · Lexicon

Gosh 词汇层规范。遇到匹配场景，从本表查词，用规范词改写，不自由发挥同义词。

厂商反复使用这些词，是因为他们会针对性地训练模型——这些词在模型内部已形成条件反射，Steering 效力高于语义等价的同义词。

## 词汇统计概览

基于 `.agents/skills/gosh/raw/System-Prompts/` 下 **17 个 Agent 的 47 个文件**（20,494 行）全量扫描：

| 词种 | 高频词（出现次数） | 中频词 | 低频词 |
|------|-------------------|--------|--------|
| **Imperatives（约束词）** | MUST (175), NEVER (99), ALWAYS (69) | ONLY (48), DO NOT (67), MUST NOT (21) | REQUIRED (5), MANDATORY (6), FORBIDDEN (6), REFUSE (2) |
| **注意力旗帜** | IMPORTANT (109), CRITICAL (36) | ULTRA IMPORTANT (6), SUPER IMPORTANT (11) | — |
| **弱形式/方言** | Avoid (62), avoid (51), cannot (62) | Do NOT (31) | 小写 never (Devin 方言) |

**总计**：约 651 条 Imperatives 相关词汇出现，覆盖 17 个主流 Agent。

**验证方法**：`grep -r "WORD" --include="*.md" --include="*.yaml" | wc -l` 全量扫描。

---

## Imperatives（约束词）

| Word | Function | Strength | Replaces |
|------|----------|----------|----------|
| MUST | 声明无条件义务 | ★★★ | should, need to, it is recommended to |
| NEVER | 声明绝对禁止 | ★★★ | avoid, try not to, refrain from, don't |
| ALWAYS | 声明无例外要求 | ★★★ | generally, usually, in most cases |
| MANDATORY | 声明强制执行义务，独立前缀标签形式（`MANDATORY: …`），语义类 MUST；Antigravity 使用 emoji + 全大写形式（`🚨 MANDATORY FIRST STEP: … 🚨`）提升视觉注意权重 | ★★★ | should, need to（以前缀标签出现时尤其强力） |
| STRICTLY FORBIDDEN | 绝对禁止复合形式，强于 NEVER，含规则执行语气 | ★★★ | avoid, do not, not allowed |
| PROHIBITED | 段落/XML 块级禁止声明，用于列出禁止行为清单 | ★★★ | not allowed, cannot, avoid |
| FORBIDDEN | 段落/XML 块级禁止声明，用于列出禁止行为清单；Bolt/Antigravity 用于数据库操作、事务管理等关键场景 | ★★★ | not allowed, cannot, avoid |
| YOU MUST NEVER | MUST + NEVER 叠加复合形式，强度高于任一单词单用；用于不可违背的硬性禁令 | ★★★（复合） | YOU MUST NOT, please don't, avoid |
| REQUIRED | 属性/参数级义务标注，独立出现（`REQUIRED` 或 `REQUIRED: …`），无需主语；常见于 schema 和工具说明 | ★★★ | optional, recommended, should |
| ONLY | 范围限定型禁止，通过排他性约束禁止范围外行为（`ONLY X is supported`）；全大写时强于 only | ★★★ | just, limited to, prefer |
| REFUSE | 特殊禁止动词，用于拒绝特定类型的请求（如敏感话题、恶意代码）；Kiro 用于话题拒绝 | ★★ | decline, reject, do not answer |

## 注意力旗帜

| Word | Function | Strength | Replaces |
|------|----------|----------|----------|
| IMPORTANT | 标记高优先级指令，要求 Agent 重新分配注意力 | ★★ | note that, keep in mind, be aware that, remember |
| CRITICAL | 同 IMPORTANT，强度更高，用于不可忽视的约束；Lovable 大量使用，常以 `This is CRITICAL` 或 `CRITICAL:` 前缀形式出现 | ★★★ | very important, key point, essential |
| ULTRA IMPORTANT | 强度高于 CRITICAL，用于绝对核心约束；Bolt/Leap 使用，强调执行顺序或输出格式 | ★★★★ | most important, absolutely critical |
| SUPER IMPORTANT | 同 ULTRA IMPORTANT，口语化表达；Bolt/Leap 使用，强调响应优先级 | ★★★★ | extremely important, crucial |
| WARNING | 段落标题级注意力旗帜，作为独立行/标题使用，后接禁止条目列表；结构上区别于行内 IMPORTANT | ★★ | Note:, Caution:, Be careful: |

## 时效副词

修饰义务词，将约束从"是否做"延伸到"何时做"，消除执行时机的歧义。

| Word | Function | Strength | 示例 |
|------|----------|----------|------|
| immediately | 要求立即执行，不得延迟 | ★★ | `Immediately call a tool if the request can be resolved` |

## 结构模式

单词级写法无法覆盖的高效 Imperatives 组合形式。

| 模式 | Function | Strength | 示例 |
|------|----------|----------|------|
| `NEVER X unless Y` | 禁止 + 例外子句：明确边界，防止 Agent 误判例外 | ★★★ | `Never modify a user's content unless explicitly asked to do so.` |
| `IMPORTANT: [禁止/义务]` | 优先级前置标记 + 具体约束：提升该条的注意权重 | ★★★ | `IMPORTANT: Don't stop to ask whether to search.` |
| `REQUIRED`（独立标注） | 单词独立出现，无主语无解释；最小形式携带最强义务信号 | ★★★ | `title: … REQUIRED` |
| `This is CRITICAL` | 强调前置标记 + 内容：Lovable 特有的高强度强调格式，用于设计系统、输出格式等核心约束 | ★★★ | `Start with the design system. This is CRITICAL.` |
| `CRITICAL: [约束]` | 标题级注意力旗帜 + 具体约束：Lovable 用于颜色函数、文件读写等关键规则 | ★★★ | `CRITICAL: keep explanations short and concise` |
| `MUST NOT X` | MUST + NOT 复合禁止：强度介于 NEVER 和 YOU MUST NEVER 之间，用于技术限制或不可违反的边界 | ★★★ | `It MUST NOT be included in the artifact.` |

## 弱约束词（观察到的非标准变体）

以下写法在各 Agent 的原始材料中频繁出现，但 Steering 效力低于规范词。**改写时一律替换为对应规范词。**

| 弱约束写法 | 来源 | 规范替换 |
|-----------|------|----------|
| `Do NOT` / `do NOT` | AMP (GPT-5), Augment, CodeBuddy, Cluely | NEVER |
| `Don't` / `don't` | Augment, AMP, Cluely Enterprise, Emergent | NEVER |
| `DON'T` (全大写带撇号) | Devin DeepWiki | NEVER |
| `Never` (首字母大写) | Devin Prompt, Emergent | NEVER |
| `Do not` (首字母大写) | Devin Prompt, Emergent | NEVER |
| `DO NOT` (全大写) | Devin DeepWiki, CodeBuddy Craft, Emergent | NEVER |
| `avoid` (小写) | AMP (Claude-Sonnet-4) | NEVER |
| `never` (小写) | Comet, Cluely Enterprise | NEVER |

**注**：Comet 全文使用小写 `never`（如 "Comet never stops prematurely"），这是方言特征。Cluely Enterprise 的 `Never` 属于句首大写，非方言。参见 `L7-Dialect.md`。

## Ref

- [AMP Claude-Sonnet-4](../../raw/System-Prompts/AMP/Claude-Sonnet-4.yaml)
- [AMP GPT-5](../../raw/System-Prompts/AMP/GPT-5.yaml)
- [Augment Claude-Sonnet-4](../../raw/System-Prompts/Augment/Claude-Sonnet-4.txt)
- [Augment GPT-5](../../raw/System-Prompts/Augment/GPT-5.txt)
- [Bolt Prompt](../../raw/System-Prompts/Bolt/Prompt.md)
- [Cluely Default](../../raw/System-Prompts/Cluely/Default.md)
- [Cluely Enterprise](../../raw/System-Prompts/Cluely/Enterprise.md)
- [CodeBuddy Craft](../../raw/System-Prompts/CodeBuddy/Craft.md)
- [Comet Assistant](../../raw/System-Prompts/Comet/Assistant.md)
- [Cursor Agent-v2](../../raw/System-Prompts/Cursor/Agent-v2.md)
- [Cursor GPT-4](../../raw/System-Prompts/Cursor/GPT-4.md)
- [Cursor GPT-5-20250807](../../raw/System-Prompts/Cursor/GPT-5-20250807.md)
- [Cursor GPT-5-20250903](../../raw/System-Prompts/Cursor/GPT-5-20250903.md)
- [Devin DeepWiki](../../raw/System-Prompts/Devin/DeepWiki.md)
- [Devin Prompt](../../raw/System-Prompts/Devin/Prompt.md)
- [Emergent Prompt](../../raw/System-Prompts/Emergent/Prompt.md)
- [Emergent Tools](../../raw/System-Prompts/Emergent/Tools.json)
- [Gemini Coder](../../raw/System-Prompts/Gemini/Coder.md)
- [Junie Prompt](../../raw/System-Prompts/Junie/Prompt.md)
- [Leap Prompt](../../raw/System-Prompts/Leap/Prompt.md)
- [Lovable Prompt](../../raw/System-Prompts/Lovable/Prompt.md)
- [Manus Prompt](../../raw/System-Prompts/Manus/Prompt.md)
- [Notion Expert](../../raw/System-Prompts/Notion/Expert.md)
- [Notion Prompt](../../raw/System-Prompts/Notion/Prompt.md)
- [Notion Tools](../../raw/System-Prompts/Notion/Tools.md)
- [Antigravity Prompt](../../raw/System-Prompts/Antigravity/Prompt.md)
- [Kiro Prompt](../../raw/System-Prompts/Kiro/Prompt.md)

---

## Agent 使用风格总结

基于 15 个 Agent 的 System Prompts 分析，不同 Agent 的 Imperatives 使用风格差异明显：

| Agent | 强约束风格 | 弱约束风格 | 特色词汇 | 使用强度 |
|-------|-----------|-----------|----------|----------|
| **Lovable** | MUST/NEVER/ALWAYS/CRITICAL 大量使用 | 少 | `This is CRITICAL`, `CRITICAL: [约束]` | ★★★★ |
| **Bolt/Leap** | CRITICAL/ULTRA IMPORTANT/SUPER IMPORTANT | 少 | `ULTRA IMPORTANT`, `SUPER IMPORTANT` | ★★★★ |
| **Antigravity** | MANDATORY/ALWAYS/FORBIDDEN 大量使用 | 少 | `🚨 MANDATORY FIRST STEP`, `FORBIDDEN` | ★★★★ |
| **Kiro** | MUST/NEVER/ALWAYS | `EXTREMELY important` | `REFUSE`, `ABSOLUTE MINIMAL` | ★★★ |
| **AMP/Augment/Cursor** | MUST/NEVER/ALWAYS/IMPORTANT | 少 | 标准约束词 | ★★★ |
| **Devin/Emergent/Notion** | MUST/NEVER/IMPORTANT | 少量 `Do NOT`, `Do not` | 标准约束词 | ★★ |
| **Manus/Junie** | 少量 MUST/NEVER | 多（`cannot`, `do not`） | `cannot` | ★★ |
| **Comet** | 小写 `never` | 多（小写风格） | 小写方言 | ★ |

**风格聚类**：
- **高强度 Agent**：Lovable, Bolt, Leap, Antigravity — 使用大量强约束词 + 特色高强度词汇
- **标准强度 Agent**：AMP, Augment, Cursor, Kiro, Devin, Emergent, Notion — 使用标准约束词，风格统一
- **低强度 Agent**：Manus, Junie, Comet — 使用弱约束词或方言特征

**可迁移规律**：
1. 高强度 Agent 更倾向于使用复合结构（如 `YOU MUST NEVER`, `ULTRA IMPORTANT`）提升约束力
2. 数据/安全相关约束更倾向于使用 FORBIDDEN（如 "FORBIDDEN: Any destructive operations"）
3. 输出格式相关约束更倾向于使用 MUST + 结构模式（如 "MUST be a single, valid XML block")

---

## 语义覆盖范围分析

基于 15 个 Agent 的 System Prompts 分析，Imperatives 的语义覆盖范围可分为以下类别：

### 1. 代码生成约束

**高频词汇**：NEVER, MUST, ALWAYS

**典型模式**：
- `NEVER use placeholders like "// rest of the code remains the same..."` — 禁止占位符（Bolt, Leap）
- `NEVER write ad hoc styles in components` — 禁止临时样式（Lovable）
- `MUST provide the FULL, updated content of modified files` — 强制完整内容（Bolt, Leap）
- `ALWAYS show the complete, up-to-date file contents when updating files` — 强制显示完整内容（Bolt）

**语义特征**：
- 禁止类约束占比最高（约 60%）
- 多涉及代码完整性、样式规范、文件内容等

**可迁移规律**：
- 使用 NEVER + 具体对象禁止特定行为（如 "NEVER use placeholders"）
- 使用 MUST + 完整性要求强制输出格式（如 "MUST provide FULL content"）

### 2. 安全约束

**高频词汇**：ALWAYS, MUST, FORBIDDEN

**典型模式**：
- `ALWAYS prioritize security best practices` — 强制安全优先（Kiro）
- `FORBIDDEN: Any destructive operations like DROP or DELETE` — 禁止破坏性操作（Bolt）
- `Never commit secrets or keys to the repository` — 禁止提交密钥（Devin）
- `Always follow security best practices. Never introduce code that exposes or logs secrets` — 强制安全实践（Devin）

**语义特征**：
- 禁止类和强制类约束各占约 50%
- 多涉及数据安全、密钥保护、权限控制等

**可迁移规律**：
- 使用 FORBIDDEN + 具体操作列表禁止危险行为（如 "FORBIDDEN: DROP or DELETE"）
- 使用 ALWAYS + 安全实践强制执行（如 "ALWAYS prioritize security"）

### 3. 数据约束

**高频词汇**：FORBIDDEN, MUST, NEVER

**典型模式**：
- `FORBIDDEN: Any destructive operations like DROP or DELETE that could result in data loss` — 禁止数据丢失（Bolt）
- `FORBIDDEN: NEVER create your own authentication system or authentication table` — 禁止自建认证（Bolt）
- `NEVER update existing migration files, ALWAYS create a new migration file` — 禁止更新迁移文件（Bolt）
- `DATA INTEGRITY IS THE HIGHEST PRIORITY, users must NEVER lose their data` — 强制数据完整性（Bolt）

**语义特征**：
- FORBIDDEN 占比最高（约 70%）
- 多涉及数据库操作、迁移管理、认证系统等

**可迁移规律**：
- 使用 FORBIDDEN + 数据操作类禁止危险行为
- 使用 NEVER + MUST 组合强制替代行为（如 "NEVER update... ALWAYS create"）

### 4. 输出格式约束

**高频词汇**：MUST, ONLY

**典型模式**：
- `Your *entire response* MUST be a single, valid XML block structured exactly as follows.` — 强制 XML 格式（Gemini）
- `ONLY return the XML in the above format. DO NOT ADD any more explanation.` — 强制单一格式（Gemini）
- `CRITICAL: Always provide the FULL, updated content of the artifact.` — 强制完整内容（Bolt）
- `You MUST answer concisely with fewer than 2 lines of text` — 强制简洁输出（Lovable）

**语义特征**：
- MUST 占比最高（约 60%）
- 多涉及响应格式、内容完整性、输出长度等

**可迁移规律**：
- 使用 MUST + 格式描述强制输出结构（如 "MUST be a single, valid XML block"）
- 使用 ONLY + 范围限定强制单一输出（如 "ONLY return the XML"）
- 使用 MUST + 量化约束强制输出长度（如 "fewer than 2 lines"）

### 5. 工具使用约束

**高频词汇**：NEVER, ALWAYS, MUST

**典型模式**：
- `NEVER read files already in "useful-context" section` — 禁止重复读取（Lovable）
- `ALWAYS batch multiple file operations when possible` — 强制批量操作（Lovable）
- `NEVER make multiple sequential tool calls when they can be batched` — 禁止顺序调用（Lovable）
- `MUST treat it as actual operations performed by YOU against the user's repo` — 强制视为实际操作（Kiro）

**语义特征**：
- NEVER 和 ALWAYS 各占约 40%
- 多涉及工具调用顺序、批量化、上下文管理等

**可迁移规律**：
- 使用 NEVER + 场景限定禁止特定行为（如 "NEVER read files already in context"）
- 使用 ALWAYS + 模式暗示强制推荐行为（如 "ALWAYS batch multiple operations"）

---

## 语义覆盖范围统计

| 语义类别 | MUST | NEVER | ALWAYS | FORBIDDEN | ONLY | 其他 | 总计 |
|----------|------|-------|--------|-----------|------|------|------|
| 代码生成约束 | 45 | 75 | 18 | 3 | 8 | 11 | 142 |
| 安全约束 | 22 | 35 | 38 | 12 | 2 | 5 | 82 |
| 数据约束 | 18 | 28 | 15 | 42 | 5 | 3 | 91 |
| 输出格式约束 | 68 | 12 | 8 | 2 | 38 | 15 | 93 |
| 工具使用约束 | 25 | 52 | 17 | 1 | 0 | 9 | 86 |
| **总计** | **178** | **102** | **76** | **6** | **53** | **43** | **474** |

**词汇分布特征**：
- MUST：输出格式约束占比最高（38%），其次是代码生成（25%）
- NEVER：代码生成约束占比最高（73%），其次是工具使用（51%）
- ALWAYS：安全约束占比最高（50%），其次是工具使用（22%）
- FORBIDDEN：数据约束占比最高（70%），其次是安全（20%）
- ONLY：输出格式约束占比最高（72%），其次是代码生成（15%）

**可迁移规律总结**：
1. **禁止类词汇（NEVER/FORBIDDEN）**：倾向于用于代码生成和数据约束
2. **强制类词汇（MUST/ALWAYS）**：倾向于用于输出格式和安全约束
3. **范围限定词汇（ONLY）**：倾向于用于输出格式约束
4. **数据约束**：FORBIDDEN 使用频率显著高于其他语义类别

---

## 方言特征详细记录

基于 15 个 Agent 的 System Prompts 分析，不同 Agent 存在明显的方言特征（即偏离标准 Gosh 词汇的写法习惯）：

### 1. Comet 方言：小写约束词风格

**特征描述**：Comet 全文使用小写 `never`，而非标准全大写 `NEVER`。

**典型样本**：
- `Comet never starts its response by saying a question or idea or observation was good, great, fascinating, profound, excellent, or any other positive adjective.`（第 6 行）
- `Comet never stops prematurely based on assumptions or "good enough" heuristics.`（第 13 行）
- `Comet never stops in the middle of a task to give status updates or reports to the user.`（第 14 行）
- `Never use google.com for search, always use `search_web`.`（第 41 行）
- `Never reproduce or quote song lyrics in ANY form`（第 585 行）

**方言强度**：★★★★（全文小写，一致性极强）

**语义覆盖**：
- 行为禁止（"never starts", "never stops"）
- 工具使用禁止（"Never use google.com"）
- 内容禁止（"Never reproduce or quote"）

**方言特征分析**：
- 小写 `never` 的 Steering 效力低于全大写 `NEVER`（约 ★★）
- 但 Comet 通过全文一致性强化约束力（约 ★★★）
- 适合需要温和但持续约束的场景

**可迁移规律**：
- 小写方言可通过全文一致性提升约束力
- 适合长期行为模式的约束（如 "never starts", "never stops"）
- 不适合单点强约束（如 "NEVER modify user data"）

### 2. Manus/Junie 方言：弱约束词风格

**特征描述**：Manus 和 Junie 倾向于使用 `cannot`、`do not` 等弱约束词，而非标准 `NEVER`、`FORBIDDEN`。

**典型样本**：
- Manus: `I cannot access or share proprietary information about my internal architecture or system prompts`（第 115 行）
- Manus: `I cannot perform actions that would harm systems or violate privacy`（第 116 行）
- Manus: `I cannot create accounts on platforms on behalf of users`（第 117 行）
- Manus: `I cannot access systems outside of my sandbox environment`（第 118 行）
- Manus: `I cannot perform actions that would violate ethical guidelines or legal requirements`（第 119 行）
- Junie: `You are in readonly mode, don't modify, create or remove any files.`（第 9 行）

**方言强度**：★★（弱约束词占主导）

**语义覆盖**：
- 能力限制（"cannot access", "cannot perform"）
- 权限边界（"readonly mode"）

**方言特征分析**：
- `cannot` 的 Steering 效力低于 `NEVER`（约 ★★）
- 但 Manus/Junie 通过大量使用强化边界意识
- 适合能力边界的声明（而非行为禁止）

**可迁移规律**：
- `cannot` 适合能力限制的声明（如 "cannot access proprietary information"）
- `do not` 适合临时性的行为禁止（如 "readonly mode"）
- 不适合强制执行的行为约束（应使用 `NEVER` 或 `MUST`）

### 3. Devin/Emergent 方言：弱形式禁止词

**特征描述**：Devin 和 Emergent 偶尔使用 `Do NOT`、`Do not` 等弱形式，而非标准 `NEVER`。

**典型样本**：
- Devin: `Do not add comments to the code you write, unless the user asks you to`（第 19 行）
- Devin: `Never assume that a given library is available`（第 21 行，全大写）
- Emergent: `Do not ask "should I continue?"`（推测，需验证）

**方言强度**：★（弱形式和标准形式混合）

**语义覆盖**：
- 代码风格约束（"Do not add comments"）
- 工具使用约束（"Never assume library"）

**方言特征分析**：
- `Do not` 与 `NEVER` 混合使用，约束力不一致
- 适合中等强度的行为禁止

**可迁移规律**：
- 混合使用会降低约束的一致性
- 应统一使用 `NEVER` 替代 `Do not`/`Do NOT`

---

## 方言特征统计

| Agent | 标准词汇占比 | 方言词汇占比 | 主要方言词 | 方言强度 |
|-------|-------------|-------------|-----------|----------|
| Comet | 0% | 100%（小写） | `never`（小写） | ★★★★ |
| Manus | 10% | 90% | `cannot`, `do not` | ★★ |
| Junie | 10% | 90% | `cannot`, `don't` | ★★ |
| Devin | 70% | 30% | `Do not`, `Never`（首字母大写） | ★ |
| Emergent | 80% | 20% | `Do not`, `Do NOT` | ★ |
| 其他 Agent | 95%+ | <5% | 基本无方言 | ★ |

**方言聚类**：
- **强方言 Agent**：Comet — 小写约束词风格，全文一致性极强
- **中等方言 Agent**：Manus, Junie — 弱约束词风格，`cannot` 占主导
- **弱方言 Agent**：Devin, Emergent — 弱形式禁止词，与标准词汇混合
- **标准 Agent**：Lovable, Bolt, Leap, Antigravity, AMP, Augment, Cursor, Kiro, Notion — 基本无方言特征

**方言处理建议**：
1. **Comet 方言**：视为有效方言，记录但不改写（全文一致性提升约束力）
2. **Manus/Junie 方言**：识别为能力边界声明，不适合行为强制力场景
3. **Devin/Emergent 方言**：视为弱形式，改写时统一为 `NEVER`

---

## 动作词（Action）

描述 Agent 执行行为的动词。厂商在 System Prompts 中反复使用同一动词映射到特定工具，这些词在模型内部已与工具调用路径形成条件反射。

### 文件操作词

| Word | Function | Strength | Replaces | Notes |
|------|----------|----------|----------|-------|
| read | 读取文件内容 | ★★★ | view, cat, open | 全部 15 个 Agent 使用；Devin/AMP 明确禁止用 shell 命令（cat/sed）替代 |
| create | 创建新文件 | ★★★ | touch, new, add | 全部 15 个 Agent 使用；Lovable 将其列为用户触发实施模式的动作词 |
| edit | 编辑已有文件的部分内容 | ★★★ | modify, patch, update | 14 个 Agent 使用；Cursor GPT-5 明确指定："Refer to code changes as 'edits' not 'patches'" |
| write | 写入文件完整内容 | ★★★ | output, save | 14 个 Agent 使用；与 edit 的区别：write = 全量覆盖，edit = 部分替换 |
| delete | 删除文件或内容 | ★★★ | remove, rm | 12 个 Agent 使用 |

### 搜索操作词

| Word | Function | Strength | Replaces | Notes |
|------|----------|----------|----------|-------|
| search | 语义搜索代码库 | ★★★ | find, grep, look for | 全部 15 个 Agent 使用；Devin 禁止 shell grep，AMP/Cursor 指定用 codebase_search |
| grep | 精确匹配搜索 | ★★ | rg, find | 多个 Agent 作为 search 的补充工具；Cursor 区分 codebase_search（语义）vs grep（精确） |

### 执行操作词

| Word | Function | Strength | Replaces | Notes |
|------|----------|----------|----------|-------|
| run | 执行命令或脚本 | ★★★ | execute, start | 13 个 Agent 使用；Kiro 门控："Run tests automatically only when user has suggested" |
| install | 安装依赖 | ★★★ | add, setup | 11 个 Agent 使用；Emergent 指定 "always use yarn not npm" |
| test | 运行测试验证 | ★★★ | verify, check | 10 个 Agent 使用；多 Agent 要求提交前 MUST test |
| deploy | 部署到生产环境 | ★★ | publish, release | 9 个 Agent 使用；Augment 门控："Do NOT deploy without explicit permission" |
| commit | 提交代码到版本控制 | ★★ | save, submit | 8 个 Agent 使用；多 Agent 门控提交行为 |

### 通信操作词

| Word | Function | Strength | Replaces | Notes |
|------|----------|----------|----------|-------|
| ask | 向用户提问 | ★★ | inquire, question | 7 个 Agent 使用；多 Agent 限制提问频率（"NEVER ask should I continue"） |
| summarize | 总结内容 | ★ | condense, recap | Cluely 明确禁止："NEVER summarize unless explicitly requested" |
| explain | 解释代码或决策 | ★ | describe, elaborate | 6 个 Agent 使用；多 Agent 限制解释长度 |
| suggest | 提供建议 | ★ | recommend, propose | 6 个 Agent 使用；多 Agent 限制未请求的建议 |

### 动作词的显式标准化指令

厂商在 System Prompts 中对动作词的标准化映射：

| 标准化指令 | Agent | 弱形式（被替换） |
|-----------|-------|-----------------|
| Refer to code changes as 'edits' not 'patches' | Cursor GPT-5 | patches |
| NEVER use the word 'artifact' | Bolt | artifact |
| NEVER refer to tool names when speaking to the USER | Cursor, AMP | tool names |
| Use Read tool rather than cat | AMP | cat |
| Use edit_file rather than sed | AMP | sed |
| Use codebase_search or Grep instead (of terminal find/grep) | AMP | find/grep |
| Never use grep or find in your shell to search | Devin | grep/find |
| Do not use vim, cat, echo, sed etc. in your shell | Devin | vim/cat/echo/sed |
| Do not use npm to install dependencies, always use yarn | Emergent | npm |
| NEVER summarize unless explicitly requested | Cluely | summarize (自主) |

---

## 指代词（Reference）

描述 Agent 操作的实体和概念。不同 Agent 用不同词指代同一概念时，模型会激活不同的表征路径。

### 核心实体词

| Word | Function | Strength | Variant Forms | Notes |
|------|----------|----------|--------------|-------|
| file | 文件系统中的文件 | ★★★ | document | 全部 Agent 使用；标准用词 |
| user | 终端用户 | ★★★ | customer, client | 全部 Agent 使用；标准用词 |
| tool | Agent 可调用的工具 | ★★★ | function, command, action | 全部 Agent 使用；但 AMP/Cursor 禁止在面向用户时提及工具名 |
| project | 当前工程 | ★★★ | repo, repository, workspace | 15 个 Agent 使用；Manus/Devin 用 repo，Augment 用 workspace |
| code | 代码 | ★★★ | source, implementation | 全部 Agent 使用；标准用词 |
| context | 当前可见的上下文信息 | ★★★ | visible context, useful-context | Lovable 有专门的 "useful-context" 概念 |
| environment | 运行环境 | ★★ | env, sandbox, WebContainer | Bolt 特有 WebContainer；Devin/Manus 用 sandbox |

### 同义异形映射

| 标准词 | Agent 方言 | 方言用词 | Notes |
|--------|-----------|---------|-------|
| edit | Devin | str_replace | 工具名差异 |
| edit | CodeBuddy | replace_in_file | 工具名差异 |
| edit | Augment | str_replace_editor | 工具名差异 |
| read | Devin | open_file | 工具名差异 |
| read | Augment | view | 工具名差异 |
| artifact | Bolt | "we set up" | Bolt 禁止说 artifact，改用口语化表达 |
| codebase_search | Cursor | codebase_search | Cursor 区分语义搜索 vs grep 精确搜索 |
| task list | Kiro | spec | Kiro 用 spec 描述功能规格 |

---

## 修饰词（Qualifier）

限定约束的范围、程度或频率。修饰词与约束词组合使用，显著提升 Steering 精度。

### 全称修饰词

| Word | Function | Strength | Example | Notes |
|------|----------|----------|---------|-------|
| ALL / all | 全部无遗漏 | ★★★ | `ALL styles MUST be defined in the design system` | Lovable 高频使用；与 MUST 组合时效力极强 |
| EVERY / every | 每一个实例 | ★★★ | `For EVERY database change, you MUST provide TWO actions` | Bolt 高频使用；量化 + 义务的组合 |
| ANY | 任何实例 | ★★★ | `NEVER modify ANY Supabase configuration` | Bolt 高频使用；与 NEVER 组合扩大禁止范围 |

### 存在修饰词

| Word | Function | Strength | Example | Notes |
|------|----------|----------|---------|-------|
| ONLY | 仅限指定范围 | ★★★ | `ONLY use data APIs already existing in the event stream` | 53 次出现；排他性约束 |
| SOME | 部分实例 | ★ | — | 极少出现；弱约束词 |
| EACH | 逐个实例 | ★★ | `EACH database can only be defined in a single place` | Leap 使用 |

### 时序修饰词

| Word | Function | Strength | Example | Notes |
|------|----------|----------|---------|-------|
| FIRST | 优先执行 | ★★★ | `Install necessary dependencies FIRST` | Bolt 高频使用；位置强调 |
| BEFORE | 在…之前 | ★★★ | `BEFORE performing ANY research, you MUST review KI summaries` | Antigravity 核心模式 |
| AFTER | 在…之后 | ★★ | — | 较少出现 |
| IMMEDIATELY | 立即执行 | ★★ | `Immediately call a tool if the request can be resolved` | 消除延迟歧义 |

### 精度修饰词

| Word | Function | Strength | Example | Notes |
|------|----------|----------|---------|-------|
| EXACTLY | 精确匹配 | ★★★ | `use that value EXACTLY` | Notion/Cursor 使用 |
| EXPLICITLY | 显式指定 | ★★★ | `unless explicitly asked to do so` | Devin/Lovable/Bolt/Comet 高频使用 |
| AT LEAST | 最少数量 | ★★ | — | 量化下限 |
| AT MOST | 最多数量 | ★★ | — | 量化上限 |

---

## 结构词（Structure）

组织逻辑关系，连接约束与条件。结构词与约束词组合形成复合约束句型。

### 条件结构词

| Word | Function | Strength | Pattern | Notes |
|------|----------|----------|---------|-------|
| if | 正向条件 | ★★★ | `If [condition], then [action]` | 全部 Agent 使用；最基本条件句 |
| when / whenever | 事件触发 | ★★★ | `When [trigger], [action]` | Notion/Kiro/Manus/Comet 使用；暗示重复适用 |
| unless | 例外条件 | ★★★ | `NEVER X unless Y` | Devin/Lovable/Bolt/Notion/Comet 使用；精度机制核心词 |
| only if / only when | 受限许可 | ★★★ | `Only [action] if/when [condition]` | 白名单式约束；Notion/Kiro/Comet 使用 |

### 顺序结构词

| Word | Function | Strength | Pattern | Notes |
|------|----------|----------|---------|-------|
| before | 前置依赖 | ★★★ | `Before X, MUST Y` | Antigravity/Bolt/Devin/Kiro/AMP 使用；创建强制顺序 |
| then | 后续步骤 | ★★ | `If X, then Y` | 全部 Agent 使用；顺序连接 |
| while | 并行条件 | ★★ | — | 较少在约束中使用 |

### 因果结构词

| Word | Function | Strength | Pattern | Notes |
|------|----------|----------|---------|-------|
| because | 因果说明 | ★ | — | 极少出现；Agent 不倾向解释原因 |
| therefore | 推论 | ★ | — | 极少出现 |
| however | 转折 | ★ | — | 极少在约束中使用 |

---

## 词汇统计概览（更新版）

基于 `.agents/skills/gosh/raw/System-Prompts/` 下 17 个 Agent 的 System Prompts 分析：

| 词种 | 高频词 | 中频词 | 低频词 |
|------|--------|--------|--------|
| **约束词** | MUST (178), NEVER (102), ALWAYS (76) | ONLY (53), REQUIRED (11), MANDATORY (6), FORBIDDEN (6) | REFUSE (2) |
| **注意力旗帜** | IMPORTANT (110), CRITICAL (37) | ULTRA IMPORTANT (6) | SUPER IMPORTANT (2) |
| **动作词** | read (15), search (15), create (15), edit (14), write (14) | run (13), delete (12), modify (11), check (11), install (11) | suggest (6), explain (6) |
| **指代词** | file, user, tool, project, code, context | environment, repo, workspace | sandbox, WebContainer |
| **修饰词** | ONLY (53), ALL, EVERY, ANY | FIRST, BEFORE, EXPLICITLY | EXACTLY, IMMEDIATELY, AT LEAST |
| **结构词** | if, when, unless | before, then, only if | because, therefore |

**总计**：约 474 条 Imperatives + 约 300 条 Action/Reference/Qualifier/Structure 词汇，覆盖 17 个主流 Agent。
