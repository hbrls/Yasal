# K4：行为伪代码建立执行顺序

## Summary

在 `<example>` 块的 `<response>` 内，用 `[动词 + 工具名 + 目的]` 格式描述 Agent 的工具调用行为，是一种在不写真实 tool call 的前提下植入执行顺序的 Steering 技术。Agent 从多个这样的压缩轨迹中内化三件事：工具调用发生在口头输出之前；行动本身不需要向用户解释；任务步骤与状态管理同步更新。

---

## Knowledge

### 核心句法

```
[动词 + 工具名 + 目的/结果]
```

动词永远在最前，工具名紧跟，目的在后。示例：

```
[uses Bash to run 'git status']
[uses Grep to locate the definition, then Read to read the full file]
[marks the first TODO as in_progress]
[spawns three agents in parallel with Task]
[searches for any existing metrics or telemetry code]
```

### 三种出现位置及其 Steering 效果

**位置一：`[行为]` 是完整响应**

```
<response>
[uses Grep to find existing tests, then Read to read files, then EditFile to add new tests]
</response>
```

Agent 学到：有些任务做完即止，不需要口头汇报。

**位置二：`[行为]` 在前，口头输出在后**

```
<response>
[uses CodebaseSearch and Read to analyze the codebase architecture]

The system uses a microservice architecture with message queues connecting services.
</response>
```

Agent 学到：先行动，再发言。顺序不可颠倒。

**位置三：`[行为]` 与口头输出交替**

```
<response>
I'll help you implement this feature.

[marks the first TODO as in_progress]
[searches for existing telemetry code]

I've found some existing code. Now let's design the system.

[marks first TODO as completed, second as in_progress]
</response>
```

Agent 学到：长任务中，行动与汇报交替，每步完成立即更新状态。

### 原理

行为伪代码本质是**压缩的执行轨迹**。Agent 不是在读描述，而是在读一份被简化的行动记录。大量这样的轨迹把"工具调用→输出"的顺序模式编码进了 Agent 的响应习惯，效果远强于直接写"You should use tools before responding"。

### 与真实 tool call 的区别

| | 行为伪代码 `[]` | 真实 tool call |
|---|---|---|
| 作用 | 在 example 中建立行为模板 | 实际执行工具 |
| 位置 | `<response>` 块内 | 独立于文本输出 |
| 详细程度 | 压缩，聚焦意图 | 完整参数 |
| Steering 方式 | 示范学习 | 直接执行 |

---

## Practice

### Good Cases

**Case G1**（行为在前，输出在后）：
```
<example>
<user>how are the different services connected?</user>
<response>
[uses CodebaseSearch and Read to analyze the codebase architecture]

The system uses a microservice architecture with message queues connecting services.
</response>
</example>
```
✓ 工具调用先于口头输出，建立"先行动后发言"的模板。

**Case G2**（行为即完整响应）：
```
<example>
<user>write tests for new feature</user>
<response>
[uses Grep and CodebaseSearch to find similar existing tests, then uses Read to read relevant files, then uses EditFile to add new tests]
</response>
</example>
```
✓ Agent 学到：执行型任务无需口头汇报，做完即止。

**Case G3**（行为与汇报交替）：
```
<example>
<user>implement usage metrics tracking</user>
<response>
I'll implement a usage metrics tracking feature.

[marks "Research existing metrics" as in_progress]
[searches for existing telemetry code]

I've found some existing telemetry code. Now let's design the system.

[marks "Research" as completed, marks "Design" as in_progress]
</response>
</example>
```
✓ 每步行动后立即更新状态，建立"行动-汇报-行动"的节奏模板。

### Bad Cases

**Case B1**（口头描述替代伪代码）：
```
<example>
<user>write tests for new feature</user>
<response>
First I would search for existing tests, then I would read them, then I would write new ones.
</response>
</example>
```
✗ 用口头描述"我会做什么"代替伪代码，Agent 学到的是"描述计划"而非"直接执行"。

**Case B2**（行为在输出之后）：
```
<example>
<user>how does authentication work?</user>
<response>
The authentication system uses JWT tokens with a 24-hour expiry.

[uses Grep to find auth-related code]
</response>
</example>
```
✗ 工具调用放在口头输出之后，破坏"先行动后发言"的顺序模板。

**Case B3**（伪代码过于模糊）：
```
<response>
[does some research and then writes the code]
</response>
```
✗ 缺少工具名，Agent 无法从中学到具体的工具调用模式。

### 练习任务

**练习 1（补全）**

以下 example 缺少行为伪代码，请补全：
```
<example>
<user>find all TODO comments in the codebase</user>
<response>
______

- `// TODO: fix this` in main.js line 45
- `# TODO: figure out why this fails` in helpers.js line 128
</response>
</example>
```

**练习 2（排序）**

将以下三个元素排列为符合 K4 模式的正确顺序：
- `The system has 3 authentication layers: API key, JWT, and session.`
- `[uses Grep to find auth-related code, then Read to understand the implementation]`
- `<response>`

**练习 3（改写）**

将以下 Bad Case B1 改写为应用 K4 的版本：
> "First I would search for existing patterns, then read the relevant files, and finally implement the feature."

---

## Exercise

**E1（单选）**

行为伪代码 `[uses Grep to find the function definition]` 出现在 `<response>` 块中，其主要 Steering 作用是？

A. 告诉 Agent Grep 工具的具体用法  
B. 让 Agent 在实际执行时调用 Grep  
C. 通过示范轨迹植入"工具调用先于口头输出"的执行顺序  
D. 替代 Agent 的思维链推理  

> 答案：C。行为伪代码是示范学习的载体，通过压缩轨迹建立执行顺序模板，而不是直接触发工具调用。

---

**E2（判断）**

以下说法是否正确："行为伪代码放在口头输出之前还是之后，效果相同。"

> 答案：False。位置决定顺序模板。放在前面建立"先行动后发言"；放在后面会建立错误模板，让 Agent 先说话再行动。

---

**E3（场景题）**

你正在为一个代码审查 Agent 写 example，期望 Agent 先阅读代码、运行诊断，再给出审查意见。写出符合 K4 的 `<response>` 内容。

> 参考答案：
> ```
> <response>
> [uses Read to read the submitted code files]
> [uses GetDiagnostics to check for existing errors and warnings]
>
> Here are the findings from the code review:
>
> 1. The authentication middleware has a potential race condition on line 42...
> </response>
> ```

---

**E4（多选）**

以下哪些属于 K4 行为伪代码的正确特征？（选所有适用项）

A. 句法为 `[动词 + 工具名 + 目的]`  
B. 出现在 `<response>` 块内  
C. 包含完整的 JSON 参数  
D. 可独立作为完整响应，不需要口头输出  
E. 必须紧跟在口头输出之后  

> 答案：A、B、D。C 错误（伪代码是压缩的，不含完整参数）；E 错误（应该在口头输出之前，或独立作为完整响应）。
