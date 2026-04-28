# L9 · Full Audit（全层审计）

## 目的

按顺序对目标文档执行全部适用的 Lx 维度扫描，**每个维度独立成轮**，完整报告后才继续下一个。

## 核心原则

**NEVER** 在一轮对话中完成多个维度——每个维度的扫描结果需要仔细确认，才能继续。

每轮只做一件事：扫描一个维度，输出完整结果，停止等待。

## 执行顺序

```
L1 (Lexicon) → L2 (Grammar) → L3 (Syntax) → L6 (Tools) → L7 (Dialect) → L8 (Model，如满足激活条件)
```

L4 / L5 在对应 lang/ 文件和 Pass 流程补全后纳入此链；L8 仅在目标文档有明确 Model 信号且 `assets/lang/L8-Model.md` 有实质内容时激活。

## 每轮执行流程

### 轮次开始

1. 宣告本轮执行哪个维度（示例：「本轮执行 L1 · Lexicon Pass」）
2. 读取对应的 `references/Lx-xxx-pass.md`
3. 严格按照该文件的"执行步骤"逐步执行，不跳步

### 轮次结束

1. 按照该维度的"输出格式"输出完整结果
2. 注明下一个待执行维度（示例：「L1 完成，下一轮执行 L2 · Grammar Pass」）
3. **停止，等待下一轮指令**

**NEVER** 在未得到继续指令的情况下自动进入下一个维度。

## 维度索引

| 维度 | 参考文件 | 状态 |
|------|---------|------|
| L1 · Lexicon Pass | [L1-Lexicon-Pass.md](./L1-Lexicon-Pass.md) | 激活 |
| L2 · Grammar Pass | [L2-Grammar-Pass.md](./L2-Grammar-Pass.md) | 激活 |
| L3 · Syntax Pass | [L3-Syntax-Pass.md](./L3-Syntax-Pass.md) | 激活 |
| L4 · Discourse Pass | [L4-Discourse-Pass.md](./L4-Discourse-Pass.md) | 未激活 |
| L5 · Pragmatics Pass | [L5-Pragmatics-Pass.md](./L5-Pragmatics-Pass.md) | 未激活 |
| L6 · Tools Pass | [L6-Tools-Pass.md](./L6-Tools-Pass.md) | 激活 |
| L7 · Dialect Pass | [L7-Dialect-Pass.md](./L7-Dialect-Pass.md) | 激活 |
| L8 · Model Pass | [L8-Model-Pass.md](./L8-Model-Pass.md) | 条件激活 |

## 所有轮次完成后：汇总报告

全部适用维度扫描完成后，输出汇总：

```
## L9 · Full Audit 汇总

### L1 发现：N 条
[摘要]

### L2 发现：N 条
[摘要]

### L3 发现：N 条
[摘要]

### L6 发现：N 条
[摘要]

### L7 发现：N 条
[摘要]

### 综合改写建议

[合并所有维度的改写建议，按文档原始顺序排列，去重后输出]
```
