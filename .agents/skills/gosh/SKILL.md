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

## When Activated

以下任一情况出现时，调用 Gosh：

- Yasal 迭代中判断某问题的根因是**语言层面**（而非业务逻辑），需要进化 Skill 文档的表达
- 有新的 prompt 样本，需要从中提炼 Steering 规律并更新知识库
- 需要对 Gosh 自身的 Steering 规律做 K-P-E 知识沉淀

**注意**：Gosh 不参与业务问题的分析。Yasal 负责判断问题根因，只有被明确标记为"语言层问题"的部分才移交给 Gosh。

## 执行步骤

### 场景一：改写或审查 Skill 文档

1. 接收 Yasal 标记的问题片段（Skill 文档中的具体段落，不读取全量学习资料）。
2. 分析该片段的语言结构，识别 Steering 效果弱的表达模式。
3. 对照已知的 Steering 规律（K1–KN），判断问题的语言层根因。
4. 改写该片段，每处变更对应至少一条规律。
5. 输出改写结果，并附上每处变更的规律依据。

### 场景二：从学习资料中产出知识沉淀（K-P-E）

1. **K（Knowledge）**：使用 `references/skill-anything-knowledge.md` 的方式，从学习资料中蒸馏结构化知识，产出 `assets/knowledge/KN-slug.md` 文件。
2. **P（Practice）**：使用 `references/skill-anything-practice.md` 的方式，针对 Knowledge 设计动手练习任务，包含 Good Cases 和 Bad Cases，写入同一 K 文件的 Practice 节。
3. **E（Exercise）**：使用 `references/skill-anything-exercise.md` 的方式，生成检验性测验题，验证掌握效果，写入同一 K 文件的 Exercise 节。

## 已知的 Steering 规律

### [K1：角色 + 反向约束的开场公式](./assets/knowledge/K1-role-negative-constraint.md)

在 prompt 开头同时指定角色和否定边界。显式声明"不是什么"比只描述"是什么"对 Agent 的约束力更强，Agent 会将反向约束作为执行中的自我校验基准。

### [K2：量化约束替代模糊形容词](./assets/knowledge/K2-quantified-constraints.md)

用数字区间替代软性形容词。Agent 无法衡量"thorough"是否达标，但可以追踪数字，显著降低输出过短或结构不完整的概率。

### [K3：输出终止指令消除尾部噪声](./assets/knowledge/K3-output-termination.md)

在 prompt 末尾放置硬性输出格式指令。利用位置效应覆盖 Agent 追加解释、总结或致谢的习惯性行为。

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

## 参考资料

1. [知识蒸馏：将原始学习材料提炼为结构化知识包](./references/skill-anything-knowledge.md)
2. [练习生成：针对知识包生成动手练习任务](./references/skill-anything-practice.md)
3. [测验生成：确认练习效果，评估掌握程度](./references/skill-anything-exercise.md)
