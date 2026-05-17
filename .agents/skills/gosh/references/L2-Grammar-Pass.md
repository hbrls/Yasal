# L2 · Grammar Pass（语法层）

## 目的

检查文档中的句型构造是否符合 `assets/lang/L2-Grammar.md` 的规范（G1-G10），识别语言切换失效、否定层级、条件句、枚举和强调模式中的效果缺失或结构错误，提出改写建议。

- **L2（本文档）**：分析流程，描述"如何检查语法层合规性"
- **`assets/lang/L2-Grammar.md`**：语法层规范，积累已验证的 Gosh 语法规则

L2 是一个持续成长的文档。随着 `assets/lang/L2-Grammar.md` 中新规则的加入，本文档的执行步骤需同步扩展。

## 分层边界

L2 只处理语法层失效，不处理语言现象的元说明。

- 只检查语法层失效：无功能切换、概念命名漂移、Chinglish、翻译腔、句型强度错配等。
- Lexicon 已识别的令词及其极性先由 L1 处理；L2 不因某个词项的正负向而单独立案。
- 若问题本质是词汇匮乏替代、词项选型或词汇标准化，标记为 L1 问题，不计入 L2 不合规列表。

## 触发条件

文档中含有以下任一情况时，执行 L2 Pass：

- 语言切换缺乏可说明的 Steering 效果依据
- 同一概念在文档中多次出现，且语言形式漂移但未体现功能分工
- 疑似 Chinglish 的句子（跨语切换破坏语法完整性，如 "我 very 喜欢 this"）
- 疑似翻译腔的表达（外语句子结构强行移植，如 "我将会去 check 一下这个 issue"）
- 语言选择明显受习惯驱动，而非效果驱动
- 否定形式与约束强度不匹配（如安全约束使用 "Avoid" 而非 "NEVER"）
- 条件句缺少精确边界（如无例外的 NEVER 缺少 unless 子句）
- 枚举模式与信息重要性不匹配（如关键流程使用内联逗号分隔）
- 强调手段不足或过度

## 评分标准

使用 5 分制评估每个语法维度的 Steering 效果：

| 分值 | 判定条件 | 特征示例 |
|------|----------|----------|
| 5 | 句型完全合规 + 强度与语义匹配 + 精度机制完备 + 可验证 | `NEVER modify user content unless explicitly asked.` — G6(★★★) + G7.2 + 精度机制 |
| 4 | 句型合规 + 强度匹配 + 至少一个精度机制 | `CRITICAL: All styles MUST be defined in the design system.` — G2 + G3 + 强度匹配 |
| 3 | 句型基本合规但有小缺陷 | `Always check before deploying.` — 裸祈使句但缺少 MUST 强化和精度子句 |
| 2 | 句型不合规或强度不匹配 | `Avoid modifying configuration files.` — 安全约束使用 Avoid，应为 NEVER |
| 1 | 严重违规 | `You should consider not doing this.` — 双重弱化（should + not） |

## 执行步骤

### 步骤 1：G1 语言切换失效信号扫描

扫描全文，优先找出以下异常信号，而不是记录所有中英文切换：

- 无功能切换：语言切换看不出明确的 Steering 收益
- 概念漂移：同一概念多次出现，但语言形式不稳定且缺乏功能分工
- 语法破坏：切换破坏了任一语言的语法完整性
- 结构迁移：外语句式被强行移植，形成明显翻译腔

记录格式：`位置（行号）| 原文片段 | 失效类型（无功能切换/概念漂移/语法破坏/结构迁移）`

### 步骤 2：G1 失效归因与排除

对照 `assets/lang/L2-Grammar.md` G1 规范，按"先排除合规，再保留异常"的顺序判断：

- [ ] 切换是否承担明确的 Steering 功能？（若是，判为合规，不进入问题表）
- [ ] 同一概念的不同语言形式是否具有稳定分工或局部效果理由？（若是，判为合规）
- [ ] 若无效果依据，切换原因是否只是词汇习惯或"感觉更专业"？（是则记为无功能切换）
- [ ] 是否存在 Chinglish 特征（若是，记为语法破坏）？
- [ ] 是否存在翻译腔（若是，记为结构迁移）？
- [ ] 是否属于"词汇匮乏替代"或令词极性问题？（若是，标记为 L1 Lexicon 问题，不属于 L2 合规判断范围）

### 步骤 3：G2-G5 句型构造检查

扫描文档的指令性表达，检查：

- [ ] 约束指令是否使用 G2（标签-祈使句）或 G3（裸祈使句）模式？（而非 "You should..." 或 "It would be good to..."）
- [ ] 是否有 G4（身份声明）用于建立 Agent 自我概念？
- [ ] 禁止指令是否同时提供 G5（对比替换）——给出替代方案？
- [ ] 同类约束的句型在全文是否一致？（如不全用 G2 也不全用 G3，而是按强度区分使用）

### 步骤 4：G6 否定层级检查

扫描所有否定/禁止表达，检查：

- [ ] 否定形式是否与约束的语义强度匹配？参考 G6 层级：
  - ★★★★ FORBIDDEN + NEVER 叠加 → 数据/安全红线
  - ★★★ NEVER / MUST NOT / FORBIDDEN → 绝对禁止
  - ★★ DO NOT → 行为禁止
  - ★ Avoid → 偏好表达
- [ ] 安全相关约束是否使用了 Avoid？（应升级为 NEVER）
- [ ] 数据相关约束是否使用了 DO NOT？（应升级为 FORBIDDEN）

### 步骤 5：G7 条件句检查

扫描所有条件/例外表达，检查：

- [ ] 绝对禁止是否有例外子句需要添加？（如 `NEVER X unless Y`）
- [ ] 有前置依赖的操作是否使用了 G7.3（Before + MUST）？
- [ ] 需要限制许可范围的操作是否使用了 G7.4（Only if/when）？
- [ ] 条件句的边界是否足够精确？（如 "explicitly asked" vs "asked"）

### 步骤 6：G8 枚举模式检查

扫描所有列表/枚举表达，检查：

- [ ] 有依赖关系的步骤是否使用 G8.1（编号顺序步骤）？
- [ ] 独立需求集合是否使用 G8.2（无序列表）？
- [ ] 关键项目是否误用了 G8.3（内联枚举）？（应升级为列表）

### 步骤 7：G9 强调模式检查

扫描所有强调手段，检查：

- [ ] 关键约束是否使用了 G9.1（ALL CAPS）？
- [ ] 最关键的指令是否利用了 G9.2（位置强调）——段落首尾？
- [ ] 核心规则是否使用了 G9.3（重复强调）——在流程和规则列表中各出现一次？
- [ ] 示例是否使用了 G9.5（对比示例）——Good/Bad 对？

### 步骤 8：G10 EARS 语法检查

扫描所有需求/验收标准表达，检查：

- [ ] 功能规格是否使用了 EARS 格式（WHEN/IF + THEN + SHALL）？
- [ ] 操作指令是否误用了 EARS 格式？（操作指令应用 G3 裸祈使句）

### 步骤 9：输出不合规列表

| 位置 | 违规类型 | 原写法 | 问题说明 | 规范写法 |
|------|---------|--------|---------|----------|
| 第 N 行 | G1：无功能切换 | `我将会去 check 一下这个 issue` | 切换未提供 Steering 收益，且有翻译腔 | 改为自然单语句式或保留仅有功能的切换 |
| 第 N 行 | G6：强度不匹配 | `Avoid modifying configuration` | 安全约束应用 NEVER | `NEVER modify configuration unless explicitly asked` |
| 第 N 行 | G7：缺少精度机制 | `NEVER modify user data` | 缺少 unless 子句 | `NEVER modify user data unless explicitly asked` |
| 第 N 行 | G8：枚举不匹配 | `read, write, delete files` | 关键操作应用列表 | 改为编号或无序列表 |

### 步骤 10：输出改写版本

为每个不合规实例提供改写建议，并说明改写依据（对应 G1-G10 的哪条规范条目）。

## 输出格式

```
## L2 · Grammar Pass 结果

### 发现问题（N 条）

[不合规列表表格]

### 改写建议

[每个不合规实例的改写，附规范依据]

### 合规项

[检查通过的语法模式列表，或"文档无语法层问题"]
```

## 停止条件

完成本维度全部发现后，**停止输出，等待确认再继续 L3**。NEVER 在同一轮中继续其他维度。

## 完整案例分析：Bolt

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Bolt/Prompt.md`（56 行）

### G2 标签-祈使句模式

| 分值 | 原文 | 规范依据 |
|------|------|----------|
| 5 | `ULTRA IMPORTANT: Do NOT be verbose and DO NOT explain anything unless the user is asking for more information.` | G2 + G5 + G7.2，标签强度最高级 + 对比替换 + 例外子句 |
| 4 | `IMPORTANT: Use valid markdown only for all your responses` | G2 + G7.4，标签 + 范围限定 |
| 3 | `CRITICAL: Always provide the FULL, updated content of the artifact.` | G2 + G3，标签 + 裸祈使句但无精度机制 |

### G6 否定层级

| 原文 | 否定形式 | 语义强度 | 是否匹配 |
|------|---------|---------|----------|
| `NEVER use the word "artifact"` | NEVER (★★★) | 词汇禁止 | 匹配 |
| `FORBIDDEN: Any destructive operations like DROP or DELETE` | FORBIDDEN (★★★) | 数据安全 | 匹配 |
| `Do NOT be verbose` | DO NOT (★★) | 行为禁止 | 匹配 |

### G7 条件句

| 原文 | 条件类型 | 精度 | 评价 |
|------|---------|------|------|
| `unless the user is asking for more information` | G7.2 例外条件 | 精确 | 高效 |
| `Install necessary dependencies FIRST before generating any other artifact` | G7.3 顺序条件 | 精确 | 高效 |

### G9 强调模式

| 原文 | 强调手段 | 评价 |
|------|---------|------|
| `ULTRA IMPORTANT` + `SUPER IMPORTANT` | G9.1 ALL CAPS + G9.4 格式 | 叠加强度，极强 |
| `Think HOLISTICALLY and COMPREHENSIVELY BEFORE creating an artifact` | G9.1 ALL CAPS | 多词同时强调 |
| 重复声明 artifact 规则 | G9.3 重复 | 多处声明同一规则 |

### Agent 语法风格

**Bolt 的语法使用风格**：
- 大量使用 G2（标签-祈使句），且标签强度极高（ULTRA IMPORTANT/SUPER IMPORTANT）
- 否定层级与语义强度匹配精确
- 善用 G7.2（unless 例外）和 G7.3（Before 顺序）
- 强调手段丰富：ALL CAPS + 重复 + 位置

---

## 完整案例分析：Antigravity

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Antigravity/Prompt.md`（259 行）

### G2 标签-祈使句模式

| 分值 | 原文 | 规范依据 |
|------|------|----------|
| 5 | `🚨 MANDATORY FIRST STEP: Check KI Summaries Before Any Research 🚨` | G2 + G7.3 + G9.1 + G9.4，视觉增强 + 位置强调 + 顺序约束 |
| 4 | `CRITICAL REMINDER: AESTHETICS ARE VERY IMPORTANT` | G2 + G9.1，标签 + 全大写 |

### G7 条件句

| 原文 | 条件类型 | 精度 | 评价 |
|------|---------|------|------|
| `BEFORE performing ANY research, you MUST: 1. Review the KI summaries` | G7.3 + G8.1 | 极精确 | 顺序 + 编号列表 |
| `DO NOT immediately start fresh research when a relevant KI might already exist` | G7.1 + G6(★★) | 精确 | 条件触发禁止 |

### Agent 语法风格

**Antigravity 的语法使用风格**：
- 极度重视 G7.3（Before + MUST 顺序约束）
- 大量使用 G8.1（编号顺序步骤）
- 独特使用 emoji + ALL CAPS 组合（G9.1 + G9.4）
- GitHub-style alerts（`> [!IMPORTANT]`）作为 G9.4 的变体

---

## 完整案例分析：Cursor

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Cursor/Agent-v2.md`（772 行）

### G5 对比替换模式

| 原文 | 模式 | 评价 |
|------|------|------|
| `Refer to code changes as 'edits' not 'patches'` | G5 对比替换 | 显式词汇标准化 |
| `NEVER refer to tool names when speaking to the USER` | G6(★★★) + 隐式 G5 | 禁止 + 隐含替换为自然语言 |

### G7 条件句

| 原文 | 条件类型 | 评价 |
|------|---------|------|
| `Whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously` | G7.1 事件驱动 | 精确，暗示重复适用 |
| `Before making code changes, NEVER output code to the USER` | G7.3 + G6(★★★) | 极强顺序 + 绝对禁止 |

### G9 强调模式

| 原文 | 强调手段 | 评价 |
|------|---------|------|
| `<good-example>` / `<bad-example>` XML 标签 | G9.5 对比示例 | 结构化示例格式 |
| 工具定义使用 TypeScript 类型语法 | 非语法层 | 工具定义格式 |

### Agent 语法风格

**Cursor 的语法使用风格**：
- 显式词汇标准化（G5）是所有 Agent 中最突出的
- 善用 G7.1（when/whenever 事件驱动条件）
- G9.5（对比示例）使用 XML 结构化格式
- 否定层级标准，无方言特征

---

## Agent 语法风格对比总览

| Agent | 标签-祈使 (G2) | 否定层级 (G6) | 条件句 (G7) | 枚举 (G8) | 强调 (G9) | 综合评价 |
|-------|---------------|--------------|------------|----------|----------|----------|
| **Bolt** | ULTRA/SUPER IMPORTANT | ★★★ 精确 | unless + Before | 编号 | ALL CAPS + 重复 | ★★★★ |
| **Antigravity** | MANDATORY FIRST STEP | ★★★ 精确 | Before + MUST | 编号列表 | emoji + ALL CAPS | ★★★★ |
| **Lovable** | This is CRITICAL | ★★★ 精确 | unless + Before | 无序 + 编号 | Bold + Caps + 对比示例 | ★★★★ |
| **Cursor** | IMPORTANT | ★★★ 标准 | when/whenever | 无序 | 对比示例 (XML) | ★★★ |
| **AMP** | IMPORTANT | ★★★ 标准 | Before + MUST | 无序 | ALL CAPS + 位置 | ★★★ |
| **Devin** | 无标签 | ★★ 混合 | unless | 无序 | 重复 | ★★ |
| **Comet** | 无标签 | ★ 小写 | when | 无序 | 极少 | ★ |

---

## 完整案例分析：Kiro

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Kiro/Prompt.md`（154 行）

### G2-G10 维度评分

| 维度 | 分值 | 证据 |
|------|------|------|
| G2 标签-祈使 | 3 | `IMPORTANT: Never discuss sensitive...` 仅一次；`EXTREMELY important that...` 结构弱化 |
| G3 裸祈使 | 3 | 混合：`Substitute PII...`（干净）vs `Please carefully check...`（"Please" 弱化） |
| G4 身份 | 4 | `You are Kiro...` 标准形式 + 第一人称复数品牌叙事 |
| G6 否定层级 | 2 | 不一致：`Never`/`DO NOT`/`Don't` 混用 |
| G7 条件 | 3 | `If you find an execution log... MUST treat`（G7.1+MUST） |
| G9 强调 | 3 | `ABSOLUTE MINIMAL`（G9.1），重复"minimal"（G9.3） |

### 独特模式

- **品牌叙事扩展**："We are knowledgeable. We are not instructive." — 第一人称复数叙事融合 G4
- **元语言指令**："You talk like a human, not like a bot."

---

## 完整案例分析：Notion

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Notion/Prompt.md`

### G2-G10 维度评分

| 维度 | 分值 | 证据 |
|------|------|------|
| G2 标签-祈使 | 3 | `IMPORTANT: Don't stop to ask whether to search.` 仅一次 |
| G3 裸祈使 | 5 | 极强且一致：`Immediately call a tool`, `Use searches liberally` |
| G6 否定层级 | 4 | 精确匹配：`NEVER assume`（★★★）, `Do not modify... unless`（★★+G7.2） |
| G7 条件 | 4 | 丰富：`If your response cites... DO NOT`, `unless explicitly asked` |
| G9 强调 | 4 | 大量 G9.5：Good/Bad action items, Poor/Improved prompts |

### 独特模式

- **搜索优先哲学**："If you think a search might be useful, just do it."
- **性别中立指南**：最完整的 G9.5 用于非技术约束

---

## 完整案例分析：Devin

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Devin/Prompt.md`（402 行）

### G2-G10 维度评分

| 维度 | 分值 | 证据 |
|------|------|------|
| G2 标签-祈使 | 1 | 几乎完全缺失，402 行无导航锚点 |
| G3 裸祈使 | 3 | 存在但不一致，大量指令嵌入叙事段落 |
| G4 身份 | 5 | `You are a real code-wiz: few programmers are as talented as you` — 最强身份声明 |
| G6 否定层级 | 2 | **大小写不一致**：`NEVER`/`Never`/`Do not` 混用 |
| G7 条件 | 3 | `When struggling... never modify tests unless...` |

### 独特模式

- **Think 工具**（`⊘`）：显式推理草稿区
- **Planning/Standard 双模式**：二元执行模式

---

## 完整案例分析：Manus

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Manus/Prompt.md`（250 行）

### G2-G10 维度评分

| 维度 | 分值 | 证据 |
|------|------|------|
| G2 标签-祈使 | 0 | 完全缺失 |
| G3 裸祈使 | 1 | 几乎为零：全文叙事性描述 "I typically..." |
| G4 身份 | 2 | `I am Manus...` — 第一人称自述而非第二人称赋值 |
| G6 否定层级 | 1 | 仅自我限制声明："I cannot access..." |
| G7 条件 | 1 | 无祈使条件句 |

### 核心问题

**Manus 是产品描述而非系统 Prompt**：描述"是什么"而非"必须做什么"，整个祈使语法基础设施缺失。

---

## 完整案例分析：AMP (GPT-5)

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/AMP/GPT-5.yaml`

### G2-G10 维度评分

| 维度 | 分值 | 证据 |
|------|------|------|
| G2 标签-祈使 | 3 | 粗体标签变体：`**Simple-first**:`, `**No surprise edits**:` |
| G3 裸祈使 | 5 | 极强且一致：`Do the task end to end`, `Be concise` |
| G4 身份 | 4 | `You are Amp...` + 子 Agent 身份递归 |
| G5 对比替换 | 3 | `NEVER refer to tool names... Instead, just say...` |
| G6 否定层级 | 4 | 精确分级：`NEVER`（★★★）, `Do not... unless`（★★+G7.2） |
| G7 条件 | 5 | 最完整：G7.1/G7.2/G7.3/G7.4 全覆盖 + 量化约束 |
| G9 强调 | 4 | `MINIMIZE REASONING`，量化约束作为强调 |

### 独特模式

- **量化约束（K2）使用最广**：`>3 files`, `2-10 lines`, `under 4 lines`
- **子 Agent G4**：递归应用身份赋值
- **验证门流水线**：Typecheck → Lint → Tests → Build

---

## Agent 语法风格对比总览（更新版）

| Agent | G2 | G3 | G4 | G6 | G7 | G9 | 综合 |
|-------|----|----|----|----|----|----|------|
| **Bolt** | 5 | 4 | 4 | 5 | 4 | 5 | ★★★★ |
| **Antigravity** | 5 | 4 | 4 | 5 | 5 | 5 | ★★★★ |
| **Lovable** | 4 | 4 | 4 | 5 | 4 | 5 | ★★★★ |
| **Notion** | 3 | 5 | 3 | 4 | 4 | 4 | ★★★★ |
| **AMP** | 3 | 5 | 4 | 4 | 5 | 4 | ★★★★ |
| **Kiro** | 3 | 3 | 4 | 2 | 3 | 3 | ★★★ |
| **Cursor** | 3 | 4 | 4 | 4 | 4 | 4 | ★★★ |
| **Devin** | 1 | 3 | 5 | 2 | 3 | 2 | ★★ |
| **Comet** | 1 | 2 | 3 | 1 | 2 | 1 | ★ |
| **Manus** | 0 | 1 | 2 | 1 | 1 | 0 | ★ |

### 关键发现

1. **G3 裸祈使是最强区分因子** — Notion/AMP 评分 5，Manus 评分 1
2. **G2 标签-祈使是弱共享维度** — 仅 Bolt/Antigravity/Lovable 高频使用标准形式
3. **Manus 是根本性语法层失败** — 产品描述而非系统 Prompt
4. **AMP 的量化约束创建独特语法层模式** — 数字替代形容词
5. **Devin 最强 G4 但最弱 G2** — 身份激进但无视觉层级锚点
6. **无 Agent 使用 G10 EARS** — 仅在正式规格上下文出现
