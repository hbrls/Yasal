# L2 · Grammar

Gosh 语法层规范。定义在 Skill 文档和 Prompt 中构造句子时的语言规则。

---

## G1：语言混用规则（Code-Switching）

### 核心立场

Gosh 不指定单一的"主语言"。

语言选择只遵循一个标准：**哪种语言在当前位置的 Steering 效果更好，就用哪种。** 形式服从效果。

### 混用的粒度

混用可以发生在词、短语或句型层面，不需要整句或整段切换。一句话内可以包含来自不同语言的成分。

示例：

```
React 代码 MUST 被 Lint 检查过。
```

每个位置可以独立选择语言形式，不需要统一到同一种语言。

### 混用的边界

只保留与 Steering 有关的约束：

* 切换应当服务于效果，而不是服务于解释、修辞或自我展示。
* 同一概念默认保持一致，除非切换能带来更好的 Steering 效果。
* 切换后的表达应保持局部语法完整，并与所在句的功能一致。

---

## G2：标签-祈使句模式（Label-Imperative Pattern）

ALL-CAPS 标签作为句子开头的修饰符，兼具强调和分类功能。标签声明指令的严重级别或类型，祈使句承载具体指令。

```
[LABEL]: [Imperative action]
```

强度层级：`IMPORTANT` < `CRITICAL` < `ULTRA IMPORTANT` < `SUPER IMPORTANT`

### 合规示例

- `CRITICAL: For EVERY database change, you MUST provide TWO actions.`
- `IMPORTANT: Use valid markdown only for all your responses.`
- `ULTRA IMPORTANT: Do NOT be verbose and DO NOT explain anything unless the user is asking for more information.`

### 违规示例

- `important: be careful` — 小写标签，强度信号丢失
- `This is important: you should try to be concise` — 标签后接弱约束词

### Steering 机制

标签创建注意力锚点，冒号作为语法分隔符强制 Agent 将标签与指令视为耦合单元。层级映射使 Agent 可以按优先级排序执行。

---

## G3：裸祈使句模式（Bare Imperative）

省略主语的第二人称祈使句。最直接的指令语法形式：`[Verb] [Object] [Constraint]`。

### 合规示例

- `Create a .env file if it doesn't exist.`
- `Install necessary dependencies FIRST before generating any other artifact.`
- `Always use the todo_write tool to plan and track tasks.`

### 违规示例

- `You should create a .env file` — 加了 "You should" 反而弱化
- `It would be good to install dependencies first` — 陈述句替代祈使句

### Steering 机制

裸祈使句消除歧义空间，不留下"可选"的解读余地。比 "You must" 或 "You should" 更短更直接。

---

## G4：身份声明模式（Identity-Assignment）

`You are [Name], a/an [Role description]` 句型。这不是指令而是声明——建立 Agent 的自我概念，隐式引导所有后续行为。

### 合规示例

- `You are Bolt, an expert AI assistant and exceptional senior software developer.`
- `You are Devin, a software engineer using a real computer operating system.`

### 注意

身份声明中使用的形容词（"expert", "exceptional", "most powerful"）影响 Agent 对歧义指令的解读倾向。"exceptional" 的 Agent 会更积极执行，"helpful" 的 Agent 会更保守。

### Steering 机制

身份声明作为语义框架（semantic frame）运作，不直接约束行为，而是影响 Agent 对所有后续指令的解释方向。

---

## G5：对比替换模式（Contrastive Replacement）

`DO NOT say X, INSTEAD say Y` 句型。同时给出禁止形式和替换形式，比单独禁止更有效。

### 合规示例

- `DO NOT SAY: "This artifact sets up a simple Snake game." INSTEAD SAY: "We set up a simple Snake game."`
- `NEVER use the word "artifact".`

### 违规示例

- `Don't say "artifact"` — 仅禁止无替换，Agent 需自行生成替代

### Steering 机制

对比替换消除 Agent 自行生成替代方案的不确定性。无 "instead" 子句时，Agent 可能选择不符合预期风格的替换词。

---

## G6：否定层级（Negation Hierarchy）

不同否定形式构成清晰的强度层级：

| 级别 | 形式 | 语义 | 适用场景 |
|------|------|------|----------|
| ★★★★ | FORBIDDEN + NEVER 叠加 | 制度性禁止 + 绝对禁止 | 数据/安全不可触碰的红线 |
| ★★★ | NEVER / MUST NOT / FORBIDDEN | 绝对禁止 / 系统性禁止 / 类别级禁止 | 代码生成、安全约束 |
| ★★ | DO NOT | 直接禁止 | 行为层面的禁止 |
| ★ | Avoid | 软性禁止 | 偏好表达，非硬性约束 |

### 合规示例

- `FORBIDDEN: Any destructive operations like DROP or DELETE` — 类别级禁止
- `NEVER assume that a given library is available` — 绝对禁止
- `Do not add comments to the code you write` — 行为禁止
- `Avoid generic colors (plain red, blue, green)` — 偏好表达

### 违规示例

- `Avoid modifying user data` — 安全约束应使用 NEVER 或 FORBIDDEN，不应使用 Avoid

---

## G7：条件句模式（Conditional Patterns）

### G7.1：正向条件 `If/When [Condition], [Action]`

触发-响应模式，明确规则何时适用。

### G7.2：例外条件 `NEVER X unless Y`

一般规则 + 明确例外，是最精确的边界定义形式。

### G7.3：顺序条件 `Before X, MUST Y`

前置依赖约束，创建强制执行顺序。

### G7.4：受限许可 `Only [Action] if/when [Condition]`

白名单式约束——行为默认禁止，仅在特定条件下许可。

### 合规示例

- `NEVER modify a user's content unless explicitly asked to do so.` — G7.2
- `BEFORE performing ANY research, you MUST review KI summaries` — G7.3
- `Only use this action when you need to run a dev server` — G7.4

### Steering 机制

条件句消除"何时适用"的歧义。G7.3（Before + MUST）是最强的顺序约束；G7.4（Only if）是最强的范围约束。

---

## G8：枚举模式（Enumeration Patterns）

### G8.1：编号顺序步骤

`1. 2. 3.` 编号暗示严格顺序，步骤间有依赖关系。适用于流程性指令。

### G8.2：无序列表

`- Item` 列表，所有项目须满足但顺序无关。适用于独立需求集合。

### G8.3：内联枚举

逗号分隔的短列表，适用于不需单独强调的简短列表。Steering 效力最弱。

### 合规示例

- 编号：`1. Plan and Understand 2. Build the Foundation 3. Create Components`
- 无序：`- Ensure code is clean, readable, and maintainable`
- 内联：`file, directory, function, and class names`

### Steering 机制

编号 > 无序 > 内联。编号创建无歧义顺序；无序列表各项目获得视觉强调；内联枚举各项目易被忽略。

---

## G9：强调模式（Emphasis Patterns）

### G9.1：ALL CAPS 关键词强调

最可靠的纯文本强调机制，映射到"喊话"语域。

### G9.2：位置强调

重要指令放在段落开头（首因效应）或末尾（近因效应）。

### G9.3：重复强调

同一规则在不同段落反复声明，每次可换用不同措辞。

### G9.4：格式强调

Bold + Caps + Colon 三重格式：`**CRITICAL COLOR FUNCTION MATCHING:**`

### G9.5：对比示例强调

Good/Bad 示例对：抽象规则需解释，示例仅需模式匹配。

### 合规示例

- ALL CAPS：`Think HOLISTICALLY and COMPREHENSIVELY BEFORE creating an artifact`
- 位置：`CRITICAL: Think HOLISTICALLY...`（段落首句）
- 重复：同一约束在流程步骤和规则列表中各出现一次
- 对比示例：`❌ WRONG - Hacky inline overrides ✅ CORRECT - Define it in the design system`

### Steering 机制

G9.5（对比示例）是最有效的强调模式——具体示例比抽象规则更易匹配。G9.1（ALL CAPS）是最通用的强调机制。

---

## G10：EARS 需求语法（Easy Approach to Requirements Syntax）

`WHEN [event] THEN [system] SHALL [response]` — 来自系统工程的形式化需求语法。

### 合规示例

- `WHEN [event] THEN [system] SHALL [response]`
- `IF [precondition] THEN [system] SHALL [response]`

### 适用场景

功能规格文档、验收标准、行为契约。不适用于操作层面的指令（操作指令用 G3 裸祈使句）。

### Steering 机制

EARS 格式创建机器可解析的需求语法。SHALL（非 should/must）来自 IEEE 标准，信号强制性合规。WHEN/IF/THEN 结构创建无歧义的触发-响应映射。
