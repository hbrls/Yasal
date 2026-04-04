---
name: yasal
description: 为即将运行的 `skills/codex-autoresearch` 预置约定（lessons目录、目标模板、对话优化规则等），指导后续自适应进化流程
metadata:
  version: 0.0.1
---

# Yasal Training Runbook - 能力训练手册

## 核心概念：Yasal、AutoSearch、Target 三者关系

### 什么是 Target？

Target 是本轮训练的目标能力，格式为：
- `commands/{Target}` → `.agents/commands/{Target}/COMMAND.md`
- `skills/{Target}` → `.agents/skills/{Target}/SKILL.md`

示例：
- `commands/explore-task` 表示训练 `.agents/commands/explore-task/COMMAND.md`
- `skills/execute-task` 表示训练 `.agents/skills/execute-task/SKILL.md`

### 三者职责分工

**Yasal（本文档）**：
- 训练流程的"预置协调器"
- 职责：确认 Target → 启动 AutoSearch
- 不负责具体的训练和进化工作

**AutoSearch**：
- 实际的"训练执行器"
- 职责：准备 INTENT → 分析问题 → 提出改进方案 → 迭代优化
- 由 `skills/codex-autoresearch` 实现

**Target**：
- 被训练的"目标能力"
- 可以是任何 command 或 skill
- Yasal 和 AutoSearch 都是为了改进 Target 而服务

### 执行流程

1. **Yasal 启动** → 确认 Target（必须明确指定）
2. **启动 AutoSearch** → 将控制权交给 autoresearch
3. **AutoSearch 准备** → 准备 INTENT
4. **AutoSearch 执行** → 分析、改进、迭代 Target
5. **评估结果** → 根据 Metrics 判断是否达标

**MUST** 先启动 Yasal，后启动 AutoSearch。

---

## Meta Purpose

**Meta Purpose**: 通过本文档预置约定的训练流程，指定训练方向，使用 `skills/codex-autoresearch` 训练并增强其他能力。

可以用来训练任何能力，即：

```bash
.agents/commands/{Target}/COMMAND.md
.agents/skills/{Target}/SKILL.md
```

你应该先阅读并遵守本文的所有预置约定，然后再调用 `skills/codex-autoresearch`。

具体的训练过程由 autoresearch 负责完成，但必须先阅读并遵守 Yasal 的所有预置约定。必须先启动 Yasal，后启动 autoresearch。

## 目录结构

**MUST** 学习资料都放在 `lessons/*` 目录，且必须是纯文本材料。

**MUST** 学习过程中如果需要记录经验，应该放在 `context/*` 目录，且必须是 Markdown 文件。

**MUST** 以 `./assets/template-INTENT.md` 为模板，通过和 autoresearch 对话来确定进化的目标，把目标写入 `context/INTENT.md`。

## Meta INTENT / Meta Goal

**MUST** 训练目标是指定的 Target 能力，不是 Yasal，也不是 autoresearch。

Skills 是通过 LLM 来运行的，所以目标必须是且只能是增强 SKILL.md 里的文字内容。

references / assets 目录下可能有一些补充用的 Markdown 文字，这些也可以是训练和进化的目标，

scripts 目录下可能有一些短脚本，但只能用来做简单的协助工具，例如遍历目录或统计得分；不能往脚本里植入复杂功能。简单来说，大部分情况下你都 **不能修改 scripts**，只能修改 Markdown。

## Lessons

lessons 目录中的学习资料，主要是指在真实场景下使用待训练的 Target 能力的执行日志。你需要从这些日志中找到 Target 表现不好、不流畅的地方，针对这些地方提出进化方向。

**MUST** 找出其中和 Target 有关的日志，并从中学习。忽略那些和 Target 无关的内容。如果在日志中没有找到和 Target 有关的内容，应当立刻停止，因为这可能是放错了学习资料。

**MUST** 只针对表现不好，不流畅，遇到问题，和用户反复争执的地方。忽略执行流畅的地方。尤其注意执行成功不意味着执行流畅，也可能是用户深度介入推进的。所以，如果你发现用户参与程度特别高的地方，那就意味着不流畅，必须针对训练和进化。

## Metrics

**MUST** 使用 10 分制。达到 8 分以上可以视为本轮迭代通过，可以开始下一轮迭代。
