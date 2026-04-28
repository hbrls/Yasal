# L3 · Syntax Pass（句法层）

## 目的

检查文档中所有 XML 标签结构、示例块、语义段、动作标签和混排架构的句法合规性，确保符合 `assets/lang/L3-Syntax.md` 中的 S0-S10 规范。

## 触发条件

文档中含有：

- XML 标签（`<tag>` 形式）
- 示例块（任何展示"输入→输出"对的结构）
- `<example>` / `<user>` / `<response>` 标签
- 语义段标签（如 `<database-rules>`, `<artifact_instructions>`）
- 动作标签（如 `<boltAction type="file">`）
- 自闭合引用标签（如 `<ref_file />`）
- 对比示例（Good/Bad 模式对）
- 混排 Markdown + XML 架构
- 工具定义（JSON Schema / TypeScript / XML）
- 非 XML 结构模式（YAML front matter, GitHub alerts, diff 标记, EARS 语法）

## 评分标准

使用 5 分制评估每个结构模式的句法合规性：

| 分值 | 判定条件 | 特征示例 |
|------|----------|----------|
| 5 | 结构完全合规 + 标签语义明确 + 嵌套深度 ≤3 + 属性规范 | `<example><user>...</user><response>...</response></example>` |
| 4 | 结构合规 + 标签语义明确 + 小缺陷（如缺少一个属性） | `<example><user>...</user><response>...</response></example>`（response 内缺少格式约束） |
| 3 | 结构基本合规但标签名不规范或嵌套过深 | `<Example>`（大写标签）或 4 层嵌套 |
| 2 | 结构不合规——使用了方言变体但无授权信号 | `<transcript_sample>` 无方言授权 |
| 1 | 严重违规——散文格式替代结构标签 | `User: ... Agent: ...` 替代 `<user>/<response>` |

## 执行步骤

### 步骤 1：定位所有 XML 标签

扫描全文，找出所有 XML 标签（开标签、闭标签、自闭合标签）：

- `<tag>...</tag>` 块级标签
- `<tag />` 自闭合标签
- `<tag attr="value">` 带属性标签

记录：标签名列表、属性列表、嵌套关系、所在行号。

### 步骤 2：检查 S0 规范（结构单元）

对照 `assets/lang/L3-Syntax.md` 的 S0 规范，检查每个标签：

- [ ] 标签名是否使用小写单词（可含连字符）？
- [ ] 标签是否存在缩进？（违规：有缩进）
- [ ] 多个同级标签是否换行分隔？

### 步骤 3：检查 S1/S2 规范（示例块句法）

- [ ] 示例块是否用 `<example>` 包裹？
- [ ] 是否用 `<user>` 标记用户输入？
- [ ] 是否用 `<response>` 标记 Agent 响应？
- [ ] 所有标签是否齐平（无任何缩进）？

### 步骤 4：检查 S3/S4 规范（语义段与规则标签）

- [ ] 语义段标签名是否描述概念域而非格式？（`<database-rules>` 而非 `<section-3>`）
- [ ] 语义段嵌套深度是否 ≤3？
- [ ] 规则标签名是否以 `_rules`、`_instructions`、`_constraints` 结尾？
- [ ] 规则标签内是否只包含可执行指令？

### 步骤 5：检查 S5 规范（动作标签与类型属性）

- [ ] 动作标签是否使用 `type` 属性区分类别？
- [ ] 文件操作是否使用 `path` 或 `filePath` 属性指定目标？
- [ ] 动作标签是否出现在正确的上下文中（输出协议 vs 输入结构）？

### 步骤 6：检查 S6 规范（自闭合引用标签）

- [ ] 自闭合标签是否使用 `/>` 结尾？
- [ ] 引用文件是否使用 `path`/`file` 属性？
- [ ] 代码片段是否使用 `lines`/`start`/`end` 属性限定范围？

### 步骤 7：检查 S7 规范（对比示例标签）

- [ ] 对比示例是否成对出现？（有 `<bad-example>` 必须有 `<good-example>`）
- [ ] 对比示例是否在同一 `<example>` 块内？

### 步骤 8：检查 S8 规范（混排架构）

- [ ] 散文说明是否使用 Markdown 格式？
- [ ] 结构化规则是否使用 XML 标签？
- [ ] 是否混用了格式？（XML 标签内的 Markdown 标题 / Markdown 段落内的 XML 规则块）

### 步骤 9：检查 S9 规范（工具定义格式）

- [ ] 同一文档是否只使用一种工具定义格式？（JSON Schema / TypeScript / XML）
- [ ] 工具名是否全文一致使用 PascalCase 或 snake_case？

### 步骤 10：检查 S10 规范（非 XML 结构模式）

- [ ] YAML front matter 是否以 `---` 正确界定？
- [ ] GitHub alerts 是否使用正确语法（`> [!NOTE]`, `> [!WARNING]`）？
- [ ] Diff 标记是否使用正确的 SEARCH/REPLACE 格式？
- [ ] EARS 语法是否仅用于需求/验收标准？（操作指令不应使用 EARS）
- [ ] 扩展复选框状态是否正确使用（`[ ]`, `[/]`, `[x]`）？

### 步骤 11：方言检查

对照 `assets/lang/L7-Dialect.md`：

- 是否出现已知方言变体标签（如 `<transcript_sample>`）？
- 若是，是否有明确的方言授权信号？无授权则标记为违规。
- 是否出现非标准标签命名（大写、空格、冒号、下划线）？
  - `<OPEN-EDITOR-FILES>` — 大写（Kiro 方言）
  - `<budget:token_budget>` — 冒号（Antigravity 方言）
  - `<tool calling spec>` — 空格（Notion 方言）
  - `<datasource_module_code_example>` — 下划线（Manus 方言）

### 步骤 12：输出不合规列表

| 位置 | 违规类型 | 原写法 | 问题说明 | 规范写法 |
|------|---------|--------|---------|----------|
| 第 N 行 | S1：标签名不规范 | `<Example>` | 应使用小写 `<example>` | `<example>` |
| 第 N 行 | S4：规则标签包含描述 | `<rules>Background: ...</rules>` | 规则标签内 MUST 是可执行指令 | 改为指令性内容 |
| 第 N 行 | S7：对比不成对 | `<bad-example>...</bad-example>` | 缺少 `<good-example>` | 添加对应的 good-example |

### 步骤 13：输出改写版本

为每个不合规块提供完整改写版本（保留原内容，仅修正结构）。

## 输出格式

```
## L3 · Syntax Pass 结果

### 发现问题（N 条）

[不合规列表表格]

### 改写建议

[每个不合规块的完整改写]

### 合规项

[检查通过的结构模式列表，或"无结构标签"若文档不含 XML 标签]

### 结构统计

| 结构类型 | 数量 | 方言变体数 | 合规率 |
|----------|------|-----------|--------|
| 语义段标签 (S3) | N | M | X% |
| 规则标签 (S4) | N | M | X% |
| 动作标签 (S5) | N | M | X% |
| 示例块 (S1/S2) | N | M | X% |
| 对比示例 (S7) | N | M | X% |
| 工具定义 (S9) | N | 0 | X% |
```

## 停止条件

完成本维度全部发现后，**停止输出，等待确认再继续 L4**。NEVER 在同一轮中继续其他维度。

## 完整案例分析：Manus

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Manus/Modules.md`（184 行）

### 语义段标签 (S3)

| 标签名 | 语义 | 嵌套深度 | 合规 |
|--------|------|---------|------|
| `<intro>` | 角色介绍 | 1 | ✅ |
| `<language_settings>` | 语言设置 | 1 | ✅ |
| `<system_capability>` | 系统能力 | 1 | ✅ |
| `<agent_loop>` | Agent 循环 | 1 | ✅ |
| `<planner_module>` | 规划模块 | 1 | ✅ |

### 规则标签 (S4)

| 标签名 | 内容类型 | 合规 |
|--------|---------|------|
| `<todo_rules>` | 可执行指令 | ✅ |
| `<file_rules>` | 可执行指令 | ✅ |
| `<coding_rules>` | 可执行指令 | ✅ |
| `<deploy_rules>` | 可执行指令 | ✅ |

### Agent 句法风格

**Manus 的句法使用风格**：
- 完整的 XML 架构：整个 Modules.md 是一个 XML 文档
- 约 15 个语义段标签，覆盖 Agent 的所有行为域
- 规则标签细粒度：每个行为域有独立的 `_rules` 标签
- 嵌套深度 1-2 层，结构清晰

---

## 完整案例分析：Cursor

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Cursor/Agent-v2.md`（772 行）

### 混排架构 (S8)

| 区域 | 格式 | 合规 |
|------|------|------|
| 工具定义 | TypeScript 类型语法（S9.2） | ✅ |
| `<tool_calling>` | XML 规则块 | ✅ |
| `<making_code_changes>` | XML 规则块 | ✅ |
| `<maximize_parallel_tool_calls>` | XML 规则块 | ✅ |
| `<citing_code>` | XML 规则块 | ✅ |
| 散文说明 | Markdown | ✅ |

### 对比示例 (S7)

| 格式 | 标签 | 合规 |
|------|------|------|
| `<good-example>` | XML 标签 | ✅ S7 |
| `<bad-example>` | XML 标签 | ✅ S7 |

### Agent 句法风格

**Cursor 的句法使用风格**：
- 混排架构：Markdown 散文 + XML 规则块
- 独特使用 TypeScript 类型语法定义工具（S9.2 方言）
- 结构化对比示例（`<good-example>/<bad-example>`）
- XML 规则块命名清晰：`<tool_calling>`, `<making_code_changes>`

---

## 完整案例分析：Comet

### 案例来源

**文件**：`.agents/skills/gosh/raw/System-Prompts/Comet/Assistant.md`（1059 行）

### 语义段标签 (S3)

| 标签名 | 语义 | 嵌套深度 | 合规 |
|--------|------|---------|------|
| `<general_behavioral_instructions>` | 行为准则 | 1 | ✅ |
| `<tool_guidelines>` | 工具使用指南 | 1 | ✅ |
| `<task_management>` | 任务管理 | 1 | ✅ |
| `<critical_security_rules>` | 安全规则 | 1 | ✅ |
| `<injection_defense_layer>` | 注入防御 | 1 | ✅ |
| `<prohibited_actions>` | 禁止行为 | 1 | ✅ |
| `<mandatory_copyright_requirements>` | 版权要求 | 1 | ✅ |

### 特殊模式

| 模式 | 示例 | 合规 |
|------|------|------|
| 自闭合确认标签 | `<confirmation question="..." action="..." />` | ✅ S6 |
| 条件确认机制 | Comet requires user confirmation for certain actions | — |

### Agent 句法风格

**Comet 的句法使用风格**：
- 最完整的 XML 架构之一（约 15 个语义段标签）
- 安全/合规标签命名极具语义（`<injection_defense_layer>`, `<mandatory_copyright_requirements>`）
- 自闭合确认标签（`<confirmation />`）用于交互协议
- 方言特征：全文小写约束词（参见 `assets/lang/L7-Dialect.md`）
