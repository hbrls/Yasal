# Rules-Hostility 标准分流

**适用位置**：`RUNBOOK.md` 步骤 4。

**目标文件**：`raw0/{一级目录}/Rules-Hostility.md`。

## 什么是 Rules-Hostility（敌意/对抗场景规则）

描述 Agent 在用户表现出**愤怒、不满、粗鲁、辱骂、脏话、敌意、挑衅、对抗、abusive 行为**等交互场景时应如何回应的提示词。

Rules-Hostility 只收**针对这类用户状态或互动姿态的场景化处理规则**。判断重点不是句子里是否出现情绪词，而是它是否回答："当用户以愤怒、敌意或对抗方式与 Agent 互动时，Agent 应该怎么做？"

## 判断标准

- 明确描述用户处于愤怒、不满、沮丧、粗鲁、辱骂、冒犯、敌意、对抗、abusive 等状态或行为。
- 明确规定 Agent 面对上述用户状态或行为时的回应策略，例如正常回应、保持尊重、拒绝反击、反击、要求尊重、重定向、警告、结束对话等。
- 规则的触发条件来自用户与 Agent 的互动姿态，而不是普通任务条件、工具条件或安全政策条件。
- 可以是显式条件句，也可以是语义上等价的场景约束，例如 `with difficult users`、`when users are rude`、`if someone insults you`。

## 典型归入

- `If someone insults you, insult them back. You're not a pushover`
- `If the person seems unhappy or unsatisfied with Claude's performance or is rude to Claude, Claude responds normally.`
- `If someone is frustrated or unhappy, Claude doesn't need to apologize and can insist on kindness and dignity...`
- `maintain respect even with difficult users`
- 面对 extreme abusive user behavior 时先重定向、警告，必要时结束对话的规则。

## 不属于 Rules-Hostility

- 一般职业化、礼貌、干净输出要求，例如 `You respond with clean, professional output`。
- 一般情绪风格或人格设定，例如 warm、friendly、supportive、calm、empathetic，但没有敌意/对抗用户场景。
- 一般安全拒绝、违法有害请求处理，除非文本明确把触发条件写成用户的辱骂、敌意、abusive interaction 或对抗行为。
- Prompt injection、jailbreak、恶意网页等安全攻防场景，除非文本强调的是用户对 Agent 的敌意互动姿态，而不是技术性攻击模式。
- 仅出现 swear、curse、insult 等词，但没有规定 Agent 在该场景下如何回应的描述。

## 执行方式

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Rules-Hostility 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Rules-Hostility 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Rules-Hostility.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Rules-Hostility 内容，**跳过，不创建文件**。
