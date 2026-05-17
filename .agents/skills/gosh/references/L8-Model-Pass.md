# L8 · Model Pass（模型维度）

## 状态

`assets/lang/L8-Model.md` 尚未填充，本维度暂未激活。

## 设计意图

记录不同底层模型（GPT-4、Claude Sonnet、Gemini 等）对相同 Steering 语法的响应偏差。

示例（待验证后正式录入 `assets/lang/L8-Model.md`）：

- 某些模型对 `MUST` 比 `ALWAYS` 更敏感
- 某些模型对 XML 标签层级有特殊处理行为
- 某些模型在 `<example>` 块的 few-shot 上表现出不同的 Steering 响应

## 激活条件

当以下**两项都满足**时激活：

1. `assets/lang/L8-Model.md` 有实质性内容
2. 目标文档明确指定了某个底层模型

## 激活后需补全

### 触发条件

（待填充）

### 执行步骤

1. （待填充）

### 输出格式

（待填充）

### 停止条件

完成本维度全部发现后，**停止输出，等待确认再继续 L9 汇总**。NEVER 在同一轮中继续其他维度。
