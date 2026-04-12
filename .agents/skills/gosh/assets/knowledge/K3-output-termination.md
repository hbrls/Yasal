# K3：输出终止指令消除尾部噪声

## Summary

在 prompt 末尾放置硬性输出格式指令，如 `Output ONLY valid JSON. No markdown fences, no commentary`。Agent 有在实质内容结束后追加解释、总结或致谢的习惯性行为（尾部噪声）。终止指令放在 prompt 最后，利用位置优势覆盖这一倾向，使输出在格式上可直接被程序消费，无需后处理清洗。

---

## Knowledge

### 核心模式

```
[prompt 主体内容]

Output ONLY [format]. No [noise type 1], no [noise type 2].
```

常见变体：
```
Output ONLY valid JSON. No markdown fences, no commentary.
Output ONLY a valid JSON array.
Output ONLY the rewritten text. No explanation.
```

### 原理

Agent 的输出倾向受两个因素影响：训练分布（倾向于"有帮助地解释"）和 prompt 中最近的指令（位置效应）。终止指令放在 prompt 末尾，使其成为 Agent 处理完整 prompt 后最后"读到"的约束，对紧随其后的输出行为影响最大。同时，`ONLY` 和 `No` 的组合用法同时给出正向格式要求和否定噪声类型，双重锁定输出边界。

### 变体

**格式锁定**（最常用）：
> `Output ONLY valid JSON. No markdown fences, no commentary.`

**纯内容输出**（去除元评论）：
> `Output ONLY the revised text. Do not explain your changes.`

**数组格式**（结构化列表）：
> `Output ONLY a valid JSON array: [{"key": "value"}]`

**极简终止**（配合上下文使用）：
> `No preamble. No explanation. Output directly.`

### 速查（Cheat Sheet）

| 尾部噪声类型 | 终止指令写法 |
|-------------|-------------|
| markdown 代码块包裹 | `No markdown fences` |
| 解释性评论 | `No commentary` / `No explanation` |
| 前置致辞（"Sure, here is..."）| `No preamble` |
| 总结段落 | `No summary` / `Output ends after the last item` |
| 多余的 JSON key | 在 schema 示例中只列出需要的字段 |

### 注意事项

终止指令**不能替代清晰的输出格式定义**。如果 prompt 中没有说明输出格式，只有 `Output ONLY` 是不够的——Agent 不知道"ONLY"指的是什么。正确用法是：先定义格式（schema、示例），再用终止指令锁定。

---

## Practice

### Good Cases

**Case G1**（JSON + 双重否定）：
```
Output ONLY valid JSON. No markdown fences, no commentary:

{
  "summary": "...",
  "key_concepts": ["..."]
}
```
✓ 先给出 schema 示例，再用终止指令锁定，格式和噪声抑制都有保障。

**Case G2**（数组格式）：
```
Output ONLY a valid JSON array:
[{"position": "...", "title": "...", "summary": "..."}]
```
✓ 终止指令直接与 schema 示例连写，简洁有效。

**Case G3**（纯文本输出）：
```
Rewrite the following paragraph to be more concise.

Output ONLY the rewritten paragraph. Do not explain your changes.
```
✓ 防止 Agent 在改写后追加"I made the following changes: ..."类的元评论。

### Bad Cases

**Case B1**（终止指令在中间）：
```
Output ONLY valid JSON.

Make sure to include all required fields. Be thorough and accurate.
```
✗ 终止指令后面还有其他指令，位置效应被削弱，Agent 可能在输出后追加"accuracy notes"。

**Case B2**（无格式定义只有终止指令）：
```
Output ONLY the answer.
```
✗ "answer"没有格式定义，Agent 不知道该输出什么结构，终止指令形同虚设。

**Case B3**（弱化版终止）：
```
Please try to output just the JSON if possible.
```
✗ `if possible` 给 Agent 留了退路，等于没有约束。终止指令必须是硬性的。

### 练习任务

**练习 1（添加终止指令）**

为以下 prompt 末尾添加合适的终止指令：
> "Translate the following text into Chinese. Keep the tone formal."

要求：防止 Agent 输出"Here is the translation:"前置句和翻译说明。

**练习 2（诊断）**

以下 prompt 的终止指令有什么问题？如何改进？
> "Analyze this code. Output the result in JSON format if you can, without too much extra text."

**练习 3（设计）**

设计一个用于提取文章关键词的 prompt，要求：输出为 JSON 数组，每项只包含关键词字符串，不需要解释，不需要排名说明。写出完整的终止指令部分。

---

## Exercise

**E1（单选）**

为什么终止指令应该放在 prompt 的最末尾？

A. 这是 OpenAI 官方规范要求的位置  
B. Agent 对 prompt 末尾的指令有更强的位置响应效果  
C. 放在末尾可以让 prompt 更短  
D. 末尾的指令优先级在语法上高于前面的指令  

> 答案：B。Agent 的输出行为受 prompt 中最近处理的内容影响最大（位置效应），终止指令在末尾能最直接地作用于紧随其后的输出行为。

---

**E2（判断）**

以下说法是否正确："只要写了 `Output ONLY valid JSON`，Agent 就一定会输出合法 JSON。"

> 答案：False。终止指令降低了噪声概率，但不是格式正确性的保证。格式的正确性依赖于 prompt 中清晰的 schema 定义和示例。

---

**E3（场景题）**

你在用 Agent 生成产品描述，但每次输出都以"Sure! Here's the product description:"开头，并在结尾加"Let me know if you need any changes!"。应用 K3，写出 prompt 末尾的终止指令。

> 参考答案：
> `Output ONLY the product description. No preamble, no closing remarks, no offers to revise.`

---

**E4（改写题）**

以下 prompt 末尾的终止指令存在问题，请改写：
> "Try to give me only the JSON, without markdown if that's okay."

> 参考答案：
> `Output ONLY valid JSON. No markdown fences, no commentary.`
