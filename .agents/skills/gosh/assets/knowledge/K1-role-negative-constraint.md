# K1：角色 + 反向约束的开场公式

## Summary

在 prompt 开头同时指定 Agent 的角色身份和否定边界，是一种强效的 Steering 结构。单独的角色声明（"You are an expert X"）告诉 Agent 是谁，但不足以约束输出方向；加入反向约束（"not Z, but W"）后，Agent 会将否定条件作为执行中的自我校验基准，显著压缩偏离预期的输出空间。

---

## Knowledge

### 核心模式

```
You are an expert [role]. Your goal is to [positive goal] — not [negative goal], but [specific positive reframe].
```

### 原理

Agent 在生成输出时，会将 prompt 中的显式边界作为软性约束持续参照。仅声明正向目标时，Agent 对"什么算完成"的判断依赖自身训练分布，容易滑向泛化输出。反向约束相当于在 Agent 的判断路径上插入一个检查点："这个输出是不是我被告知要避免的那种？"

### 变体

**内联式**（反向约束嵌入目标句）：
> "Your goal is to create materials with genuine learning value — not generic summaries, but deeply organized knowledge."

强度：中。约束与目标混合，语流自然，但显著性稍弱。

**独立加粗句式**（反向约束单独成句）：
> "**These are NOT quiz questions.** They are tasks that require the learner to actively apply, build, or analyze something."

强度：高。独立成句 + 加粗，迫使 Agent 在处理时单独解析此约束，Steering 效果更强。

### 速查（Cheat Sheet）

| 要素 | 作用 | 示例 |
|------|------|------|
| `You are an expert [role]` | 设定认知框架 | `You are an expert knowledge architect` |
| `Your goal is to [positive]` | 声明正向目标 | `produce a structured learning package` |
| `— not [negative]` | 建立否定边界 | `not generic summaries` |
| `but [reframe]` | 给出正确替代方向 | `but deeply organized knowledge` |

---

## Practice

### Good Cases

**Case G1**（内联式）：
```
You are an expert knowledge architect and instructional designer. Analyze the following content and produce a comprehensive, structured learning package.

Your goal is to create materials with genuine learning value — not generic summaries, but deeply organized knowledge that lets a learner master the topic without returning to the original source.
```
✓ 角色明确，反向约束内联在目标句中，指出了常见错误方向（generic summaries）并给出正确替代。

**Case G2**（独立加粗句式）：
```
You are an expert course designer. Create {count} high-quality hands-on exercises based on the content below.

**These are NOT quiz questions.** They are tasks that require the learner to actively apply, build, or analyze something.
```
✓ 反向约束独立成句加粗，在角色声明后立即建立边界，Steering 强度更高。

### Bad Cases

**Case B1**（无角色，无反向约束）：
```
Write a comprehensive summary of the content.
```
✗ Agent 对"comprehensive"无法自我校验，输出质量依赖训练分布，容易产生泛化摘要。

**Case B2**（有角色，无反向约束）：
```
You are an expert educator. Write a detailed summary of this material.
```
✗ 角色声明存在，但"detailed"是软性词，没有反向约束划定边界，Agent 仍然可能输出流水账式总结。

**Case B3**（反向约束语义模糊）：
```
You are an expert writer. Write something good, not bad.
```
✗ 反向约束必须具体指向一个真实的错误倾向，"not bad"无实际 Steering 效果。

### 练习任务

**练习 1（改写）**

将以下 prompt 改写为应用 K1 的版本：
> "Summarize the key points of this document for a beginner."

要求：选择内联式或独立句式，明确角色，加入针对该场景最可能出现的错误输出方向的反向约束。

**练习 2（诊断）**

阅读以下 prompt，判断它是否正确应用了 K1，并说明理由：
> "You are a senior software engineer. Review this code and provide thorough feedback — not superficial comments, but actionable suggestions that address root causes."

**练习 3（变体选择）**

同一个 prompt 分别写出内联式和独立加粗句式两个版本，比较它们在以下场景中哪个更合适：
> 目标：让 Agent 生成用于法律文件审查的摘要，避免给出法律建议。

---

## Exercise

**E1（单选）**

以下哪个选项最准确描述了"反向约束"在 K1 中的作用？

A. 告诉 Agent 它是什么角色  
B. 在 Agent 执行时插入一个可自我校验的否定边界  
C. 限制 Agent 的输出长度  
D. 声明 prompt 的正向目标  

> 答案：B。反向约束的核心作用是给 Agent 提供一个在执行中可以持续参照的否定检查点，而不是声明角色或控制长度。

---

**E2（判断）**

以下说法是否正确："只要 prompt 中有角色声明，输出质量就会比没有角色声明时更好。"

> 答案：False。角色声明设定认知框架，但不足以约束输出方向。Bad Case B2 表明，没有反向约束的角色声明仍然无法有效 Steering。

---

**E3（场景题）**

你正在为一个代码审查 Agent 写 prompt，历史上该 Agent 总是给出表扬性反馈而非真正指出问题。应用 K1，写出 prompt 的开头两句话。

> 参考答案：
> "You are an expert software engineer specializing in code quality. Your goal is to provide a rigorous, actionable review — not polite encouragement, but specific identification of bugs, design flaws, and improvement opportunities."

---

**E4（多选）**

以下哪些属于 K1 的正确应用场景？（选所有适用项）

A. 写一个生成营销文案的 prompt，避免产生夸张宣传语  
B. 写一个翻译 prompt，避免直译导致语义失真  
C. 在 prompt 末尾加一句"请注意质量"  
D. 写一个数据分析 prompt，避免只报告数字而不给出洞察  

> 答案：A、B、D。C 没有角色声明，也没有具体反向约束，不符合 K1 模式。
