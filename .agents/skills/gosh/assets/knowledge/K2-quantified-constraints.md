# K2：量化约束替代模糊形容词

## Summary

用数字区间或精确数量替代"thorough"、"comprehensive"、"detailed"等软性形容词。Agent 无法内部衡量软性词是否达标，数字区间会触发自我校验行为，使 Agent 在生成过程中持续追踪是否满足量化条件，显著降低输出过短、过长或结构不完整的概率。

---

## Knowledge

### 核心模式

```
不写：Write a thorough analysis.
改写：Write an analysis of 300-500 words covering at least 3 key aspects.

不写：List the main concepts.
改写：List 10-15 core concepts, ordered from foundational to advanced.
```

### 原理

软性形容词（thorough、comprehensive、detailed）是相对词，其边界在 Agent 内部是模糊的——Agent 无法知道"thorough"对当前任务意味着多少字、多少条目、多少层次。而数字区间是绝对边界，Agent 在生成过程中可以主动计数并校验，产生类似"我写了 8 个概念，目标是 10-15，需要继续"的追踪行为。

### 变体

**数量区间**（条目数）：
> `10-15 core concepts`、`15-25 terms`

**字数区间**（长度）：
> `200-400 words`、`2-3 sentences`

**比例分布**（多类别时）：
> `Difficulty distribution: 20% easy, 50% medium, 30% hard`

**精确数量**（无需弹性时）：
> `Generate {count} questions`（通过变量传入确定值）

### 速查（Cheat Sheet）

| 软性写法 | 量化替代 |
|----------|----------|
| `a thorough summary` | `a summary of 200-400 words` |
| `several examples` | `3-5 concrete examples` |
| `key concepts` | `10-15 key concepts` |
| `detailed explanation` | `explanation of 2-3 sentences per point` |
| `mixed difficulty` | `20% easy, 50% medium, 30% hard` |

---

## Practice

### Good Cases

**Case G1**（字数区间）：
```
### 1. summary (200-400 words)
- Identify the central thesis, methodology, and conclusions
- Capture the logical chain of reasoning, not just surface-level facts
```
✓ 先给字数区间，再给内容要求，Agent 同时追踪长度和质量两个维度。

**Case G2**（条目数量）：
```
### 3. key_concepts (10-15 core concepts)
- Format: "Concept Name: one-sentence explanation"
- Order from foundational to advanced
```
✓ 数量区间明确，Agent 不会在写了 3 个概念后停止。

**Case G3**（比例分布）：
```
- Difficulty distribution: 20% easy, 50% medium, 30% hard
```
✓ 分布约束让 Agent 在分配难度时有明确的比例目标，避免全部生成同一难度。

### Bad Cases

**Case B1**（软性词无法校验）：
```
Write a comprehensive analysis of the topic.
```
✗ "comprehensive"无量化基准，Agent 写 2 段或 10 段都可以声称满足要求。

**Case B2**（数量过于宽泛）：
```
List some key concepts.
```
✗ "some"比软性形容词更糟，连方向都没有。

**Case B3**（只有上限无下限）：
```
Write no more than 500 words.
```
✗ 只有上限时，Agent 倾向于输出极短内容（1 句话也满足约束）。区间比单边限制更有效。

### 练习任务

**练习 1（改写）**

将以下 prompt 片段改写为应用 K2 的版本：
> "Provide a detailed glossary of technical terms used in this document."

要求：给出条目数量区间，并为每条词条指定长度或格式约束。

**练习 2（诊断）**

以下 prompt 是否正确应用了 K2？说明理由：
> "Generate 5 quiz questions with varying difficulty levels."

提示：数量固定了，但"varying difficulty"是否足够量化？

**练习 3（设计）**

为一个生成"产品需求文档摘要"的 prompt 设计量化约束，要求覆盖：字数、章节数、每章节的关键点数量。

---

## Exercise

**E1（单选）**

为什么数字区间比单一上限（如"不超过 500 字"）更有效？

A. 数字区间让 prompt 看起来更专业  
B. 单一上限使 Agent 倾向于输出极短内容  
C. 数字区间可以让 Agent 忽略质量要求  
D. 单一上限会导致 Agent 报错  

> 答案：B。只有上限时，任何长度都满足约束，Agent 倾向于最短路径。区间同时设定下限，迫使 Agent 达到最低输出量。

---

**E2（判断）**

以下说法是否正确："在所有情况下，精确数量（如'生成 5 个'）比区间（如'生成 4-6 个'）更好。"

> 答案：False。精确数量适合有明确需求的场景；区间更适合内容数量本身有自然弹性的场景（如概念提炼）。强制精确数量有时会导致 Agent 凑数或截断。

---

**E3（场景题）**

你正在写一个 prompt，让 Agent 为一篇论文生成"研究摘要"。历史上该 Agent 总是输出一两句话就停止。应用 K2，改写以下 prompt 开头：

原版：
> "Summarize this research paper."

> 参考答案：
> "Write a structured summary of this research paper in 250-350 words. Cover: (1) the research question, (2) methodology, (3) key findings, and (4) conclusions or implications."

---

**E4（改写题）**

将以下软性约束全部改写为量化约束：
> "Write a thorough glossary with several terms, covering all important concepts with detailed definitions."

> 参考答案：
> "Write a glossary of 15-25 terms. Each definition must be 1-2 sentences, precise and domain-specific. Cover all technical terms, acronyms, and key phrases from the content."
