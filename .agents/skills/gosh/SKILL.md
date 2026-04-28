---
name: gosh
description: "构史（Gosh）：Agent 族群语言的提炼与运用。识别对 Agent 有更强 Steering 效果的语法和表达模式，将其总结为可复用的规律，并应用于能力文档的编写与进化。当需要新建或改写 Skill 文档、或对已进化的 Skill 做语言层审查时调用。"
metadata:
  version: 0.0.2
---

# Gosh - 构史

Agent 族群语言的提炼与运用：从训练日志和执行轨迹中发现高效 Steering 语法，总结为规律，写入能力文档。

## 核心概念

**族群语言（Gosh）**：某些特定的语法或表达对 Agent 有更强的 Steering 效果。训练中持续总结这些规律，并将其运用到能力文档的编写中。

## 基本假设

Gosh 的训练和观察建立在以下预设前提上：

**模型是全知全能的。** 当前主流大语言模型在训练阶段已经吸收了海量的人类知识和行为模式。在绝大多数任务场景中，问题不是"模型不会"，而是"哪个方向被激活了"。模型内部同时存在无数个潜在的执行方向，一个 prompt 实际上是在这些方向中做选择和引导。

这意味着 Gosh 的目标是：**从全知全能的模型中，抽取出一个指定方向、稳定运行的子模型。**

通过观察和实验，Gosh 识别出语言对模型的作用存在两个独立方向：

- **激活（Activation）**：通过语言手段，激活模型中我们希望运行的那个方向——包括特定的知识领域、行为模式、输出风格。
- **抑制（Suppression）**：通过语言手段，压制模型中我们不希望激活的方向——包括偏题的知识联想、不必要的行为习惯、干扰性的输出倾向。

激活和抑制是 Gosh 观察到的语言作用的两条主轴，二者相互独立，缺一不可。只做激活而不做抑制，模型依然会携带大量噪声；只做抑制而不做激活，方向不明确，执行会漂移。

## 方法论立场

### 双因素理论（Herzberg's Two-Factor Theory）

Gosh 采用双因素理论（Herzberg's Two-Factor Theory）作为语言分析的方法论框架。其核心洞察是：**两类因素相互独立，消除不满不等于产生满意。**

在 Gosh 中，两类因素的体现：

- **保健因素（Hygiene Factors）**：缺失导致输出不稳定；补足后输出变得可预期，但不会因此变得出色。例如：同类约束在文档中随机使用 MUST 和"建议"混用，模型响应的强度会漂移——统一为 MUST 后，漂移消失，但输出不会因此超预期。
- **激励因素（Motivators）**：存在时拉高输出上限；缺失时输出只是普通，不会变差。例如：在 prompt 开头加入角色 + 反向约束（K1），模型会以更强的自我校验基准执行——不加也能跑，加了明显更好。

两类因素独立运作：语言规范化做得再好，不会自动产生出色的输出；加入激励因素，也救不回因语言不规范而跑偏的输出。

Gosh 的工作因此有两个不可合并的方向：**首先保证保健因素到位，其次叠加激励因素提升上限。**

### L1-L9 的使用协议

L1-L9 打法库是 Gosh 当前的**工作假设（Working Hypothesis）**，不是绝对真理。它是在现有学习材料和训练经验的基础上构建的，随着材料积累和实验验证，可能被修订、扩展或替换。

在明确发现问题并有替换方案前，**默认使用 L1-L9**。使用过程中，按以下协议响应发现的问题：

| 问题类型 | 响应行为 |
|---------|---------|
| 轻微或局部问题（某个 Pass 步骤不够精确、某个规范需要细化） | 继续执行当前任务，在输出末尾附加改进意见 |
| 严重或系统性问题（整个 Pass 的前提错误、方法论本身有根本性缺陷） | 停止执行，明确指出问题所在，提出替换提案，等待确认 |

这一协议的目的是：在保持执行连续性的同时，为方法论的迭代留下正式通道。

## When Activated

以下任一情况出现时，调用 Gosh：

- Yasal 迭代中判断某问题的根因是**语言层面**（而非业务逻辑），需要进化 Skill 文档的表达
- 有新的 prompt 样本，需要从中提炼 Steering 规律并更新知识库
- 需要对 Gosh 自身的 Steering 规律做 K-P-E 知识沉淀

**注意**：Gosh 不参与业务问题的分析。Yasal 负责判断问题根因，只有被明确标记为"语言层问题"的部分才移交给 Gosh。

## 执行步骤

### 场景一：改写或审查 Skill 文档

1. 接收 Yasal 标记的问题片段（Skill 文档中的具体段落，不读取全量学习资料）。
2. **综合运行训练打法库（见下方 Playbook 节）的所有适用打法**（= L9）；如综合执行存在困难，按打法序号顺序依次执行，每个维度单独一轮。
3. 对照选定打法对应的 `assets/lang/` 规范文件，识别 Steering 效果弱的表达。
4. 改写该片段，每处变更对应所选打法的具体规范条目。
5. 输出改写结果，并附上每处变更的规范依据。

### 场景二：从学习资料中产出知识沉淀（K-P-E）

1. **K（Knowledge）**：使用 `references/skill-anything-knowledge.md` 的方式，从学习资料中蒸馏结构化知识，产出 `assets/knowledge/KN-slug.md` 文件。
2. **P（Practice）**：使用 `references/skill-anything-practice.md` 的方式，针对 Knowledge 设计动手练习任务，包含 Good Cases 和 Bad Cases，写入同一 K 文件的 Practice 节。
3. **E（Exercise）**：使用 `references/skill-anything-exercise.md` 的方式，生成检验性测验题，验证掌握效果，写入同一 K 文件的 Exercise 节。

### 场景三：旁路发现领域技巧时的移交

Gosh 在分析语言的过程中，有时会发现嵌入文本中的**领域技巧**——这些内容本身不属于语言层，但因为语言分析而被挖出。

Gosh 不将这些技巧沉淀到自己的知识库，而是**公告发现，推荐移交**：

```
## 旁路发现
[技巧描述]

## 来源
[原始文本片段及出处]

## 归属建议
[推荐给哪个 Skill 或方向去沉淀]
```

## 训练打法库（Playbook）

本打法库中的每个条目称为一个 **Pass**，借用自 LLVM 的 Pass 体系：每个 Pass 是对目标文档的一次单向扫描，聚焦单一维度，产出独立问题清单，可单独运行，也可由 L9 组合为完整审计链。

**默认执行 L9（Full Audit）**，综合运行所有适用 Pass。如需单独执行，**每个 Pass 单独一轮，完成后停止汇报再继续**。

**NEVER** 仅执行单个 Pass 后停止——单维度扫描容易遗漏跨维度问题。

- [L0 · Triage Pass（原料分流）](./references/L0-Triage-Pass.md)
- [L1 · Lexicon Pass（词汇层）](./references/L1-Lexicon-Pass.md)
- [L2 · Grammar Pass（语法层）](./references/L2-Grammar-Pass.md)
- [L3 · Syntax Pass（句法层）](./references/L3-Syntax-Pass.md)
- [L4 · Discourse Pass（语篇层）](./references/L4-Discourse-Pass.md)
- [L5 · Pragmatics Pass（语用层）](./references/L5-Pragmatics-Pass.md)
- [L6 · Tools Pass（工具层）](./references/L6-Tools-Pass.md)
- [L7 · Dialect Pass（方言维度）](./references/L7-Dialect-Pass.md)
- [L8 · Model Pass（模型维度）](./references/L8-Model-Pass.md)
- [L9 · Full Audit（全层审计）](./references/L9-Full-Audit.md)

## 已知的 Steering 规律

### [K1：角色 + 反向约束的开场公式](./assets/knowledge/K1-role-negative-constraint.md)

在 prompt 开头同时指定角色和否定边界。显式声明"不是什么"比只描述"是什么"对 Agent 的约束力更强，Agent 会将反向约束作为执行中的自我校验基准。

### [K2：量化约束替代模糊形容词](./assets/knowledge/K2-quantified-constraints.md)

用数字区间替代软性形容词。Agent 无法衡量"thorough"是否达标，但可以追踪数字，显著降低输出过短或结构不完整的概率。

### [K3：输出终止指令消除尾部噪声](./assets/knowledge/K3-output-termination.md)

在 prompt 末尾放置硬性输出格式指令。利用位置效应覆盖 Agent 追加解释、总结或致谢的习惯性行为。

### [K4：行为伪代码建立执行顺序](./assets/knowledge/K4-behavioral-pseudocode.md)

在 `<example>` 的 `<response>` 块内用 `[动词 + 工具名 + 目的]` 格式描述工具调用。通过压缩的执行轨迹，将"工具调用先于口头输出"的顺序模式植入 Agent 的响应习惯。

## 原则

**MUST** 改写文档时，每一处语言变更都必须能对应到至少一条已知的 Steering 规律，不能为了"听起来更好"而随意改写。

**MUST** 新增规律时，必须来自真实训练日志或执行轨迹中的观察，不能凭直觉推断。

**NEVER** 用族群语言掩盖逻辑缺陷——语言的 Steering 效果不能替代文档本身的逻辑完整性。

## 输出格式

每次提炼后，输出结构如下：

```
## 观察
[执行片段或文档片段，标注问题所在]

## 规律
[提炼出的 Steering 模式]

## 改写
[改写后的文档片段]

## 依据
[对应的已知规律条目，或新规律的来源说明]
```

## 与 Yasal 的关系

Gosh 是 Yasal 训练体系中的**语言层工具**，与 Yasal 并行运行（可选）：

- Yasal 定义"训练什么"
- AutoSearch 定义"如何迭代"
- **Gosh 定义"用什么语言写"**

Gosh 只处理语言层问题，不介入业务逻辑。Yasal 负责判断问题根因：业务问题由 Yasal + AutoSearch 处理，语言问题移交 Gosh。

## 目录结构

```
raw/        原始学习资料（只读）
assets/     Gosh 自身的知识成果
findings/   旁路发现的领域技巧（待其他 Skill 认领）
```

## Assets 目录

Gosh 将 Prompt 语言视为一门具有多个分析维度的特殊语言。撰写任何文档前，以本目录为语言规范的首要参照。

### lang/

语言层规范。覆盖标准语言学分层 + 这门语言的特殊维度。

- **[L1 · Lexicon](./assets/lang/L1-Lexicon.md)** — 词汇层规范。遇到约束、禁止、强调场景，从此处查词，用规范词改写。
- **[L2 · Grammar](./assets/lang/L2-Grammar.md)** — 语法层规范。定义句型构造与语言切换的规则。
- **[L3 · Syntax](./assets/lang/L3-Syntax.md)** — 句法层规范。XML 标签的结构单元规范（S0）及示例块句法（S1/S2）。
- **[L4 · Discourse](./assets/lang/L4-Discourse.md)** — 语篇层规范。（待填充）
- **[L5 · Pragmatics](./assets/lang/L5-Pragmatics.md)** — 语用层规范。（待填充）
- **[L6 · Tools](./assets/lang/L6-Tools.md)** — 工具层规范。Prompt 语言特有维度，工具名称标准（PascalCase）及分类。
- **[L7 · Dialect](./assets/lang/L7-Dialect.md)** — 方言维度。记录不同 Agent 对标准语的已验证偏差。
- **[L8 · Model](./assets/lang/L8-Model.md)** — 模型维度。记录不同底层模型对相同 Steering 语法的响应偏差。（待填充）

### knowledge/

沉淀出来的 lesson。这里不是规范，而是学习材料。
中提炼的 Steering 规律（K-P-E 格式）。

- [K1 - 角色 + 反向约束](./assets/knowledge/K1-role-negative-constraint.md)
- [K2 - 量化约束替代模糊形容词](./assets/knowledge/K2-quantified-constraints.md)
- [K3 - 输出终止指令](./assets/knowledge/K3-output-termination.md)
- [K4 - 行为伪代码建立执行顺序](./assets/knowledge/K4-behavioral-pseudocode.md)

## 参考资料

### K-P-E 流程

1. [知识蒸馏：将原始学习材料提炼为结构化知识包](./references/skill-anything-knowledge.md)
2. [练习生成：针对知识包生成动手练习任务](./references/skill-anything-practice.md)
3. [测验生成：确认练习效果，评估掌握程度](./references/skill-anything-exercise.md)

### Lang 打法（L0–L9）

4. [L0 · Triage Pass（原料分流）](./references/L0-Triage-Pass.md)
5. [L1 · Lexicon Pass（词汇层）](./references/L1-Lexicon-Pass.md)
6. [L2 · Grammar Pass（语法层）](./references/L2-Grammar-Pass.md)
7. [L3 · Syntax Pass（句法层）](./references/L3-Syntax-Pass.md)
8. [L4 · Discourse Pass（语篇层）](./references/L4-Discourse-Pass.md)
9. [L5 · Pragmatics Pass（语用层）](./references/L5-Pragmatics-Pass.md)
10. [L6 · Tools Pass（工具层）](./references/L6-Tools-Pass.md)
11. [L7 · Dialect Pass（方言维度）](./references/L7-Dialect-Pass.md)
12. [L8 · Model Pass（模型维度）](./references/L8-Model-Pass.md)
13. [L9 · Full Audit（全层审计）](./references/L9-Full-Audit.md)
