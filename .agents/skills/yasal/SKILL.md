---
name: yasal
description: 训练流程的预置协调器：确认 Target（Skill），预置约定后启动 AutoSearch 执行训练与进化
metadata:
  version: 0.0.1
---

# Yasal Training Runbook - 能力训练手册

## 核心概念：Yasal、AutoSearch、Gosh、Target 四者关系

### 什么是 Target？

Target 是本轮训练的目标能力，格式为：
- `skills/{Target}` → `skills/{Target}/SKILL.md` 或 `skills/{Target}/COMMAND.md`

示例：
- `skills/explore-task` 表示训练 `skills/explore-task/SKILL.md`
- `skills/execute-task` 表示训练 `skills/execute-task/COMMAND.md`
- `skills/evaluate-task` 表示训练 `skills/evaluate-task/SKILL.md`

**MUST** Target 只能是 Skill。所有被训练的 Skill 都放在项目根目录下的 `skills/` 目录，与系统内置的 `.agents/` 目录完全分离，不会混淆。

### 三者职责分工

**Yasal（本文档）**：
- 训练流程的"预置协调器"
- 职责：确认 Target → 启动 AutoSearch
- 不负责具体的训练和进化工作
- 由 `.agents/skills/yasal` 实现

**AutoSearch**：
- 实际的"训练执行器"
- 职责：准备 INTENT → 分析问题 → 提出改进方案 → 迭代优化
- 由 `.agents/skills/codex-autoresearch` 实现

**Gosh**：
- 训练体系中的"语言层工具"
- 职责：识别高效 Steering 语法 → 总结规律 → 应用于文档改写
- 由 `.agents/skills/gosh` 实现

**Target**：
- 被训练的"目标能力"
- 只能是 Skill（放在根目录的 `skills/` 目录下）
- Yasal、AutoSearch、Gosh 都是为了改进 Target 而服务

### 执行流程

1. **Yasal 启动** → 确认 Target（必须明确指定）
2. **启动 AutoSearch** → 将控制权交给 autoresearch
3. **AutoSearch 准备** → 准备 INTENT
4. **AutoSearch 执行** → 分析、改进、迭代 Target
   - 分析问题时，判断根因是**业务层**（需求不清晰、逻辑缺失等）还是**语言层**（表达无法有效 Steer Agent）
   - 若判定为语言层问题，**并行调用 Gosh**，将问题片段移交语言层审查
5. **评估结果** → 根据 Metrics 判断是否达标

**MUST** 先启动 Yasal，后启动 AutoSearch。

---

## Meta Purpose

**Meta Purpose**: 通过本文档预置约定的训练流程，指定训练方向，使用 `.agents/skills/codex-autoresearch` 训练并增强其他 Skill。

Target 只能是 Skill，路径格式为：

```bash
skills/{Target}/SKILL.md
# 或
skills/{Target}/COMMAND.md
```

该目录是独立的项目目录，与系统内置 `.agents/` 目录无关。

你应该先阅读并遵守本文的所有预置约定，然后再调用 `.agents/skills/codex-autoresearch`。

具体的训练过程由 AutoSearch 负责完成，但必须先阅读并遵守 Yasal 的所有预置约定。必须先启动 Yasal，后启动 AutoSearch。

## 目录结构

**MUST** 训练目标放在 `skills/*` 目录。

**MUST** 学习资料都放在 `lessons/*` 目录，且必须是纯文本材料。

**MUST** 学习过程中如果需要记录经验，应该放在 `context/*` 目录，且必须是 Markdown 文件。

**MUST** 以 `.agents/skills/yasal/assets/template-INTENT.md` 为模板，通过和 AutoSearch 对话来确定进化的目标，把目标写入 `context/INTENT.md`。

## Meta INTENT / Meta Goal

**MUST** 训练目标是指定的 Target Skill，不是 Yasal，也不是 AutoSearch。

Target 是通过 LLM 来运行的，所以目标必须是且只能是增强 `skills/{Target}/SKILL.md` 或 `skills/{Target}/COMMAND.md` 里的文字内容。

Target 可能带有一些 references / assets 目录，其中有一些补充用的 Markdown 文字，这些也可以是训练和进化的目标，

Target 可能带有一些 scripts 目录，其中有一些短脚本，但只能用来做简单的协助工具，例如遍历目录或统计得分；不能往脚本里植入复杂功能。简单来说，大部分情况下你都 **不能修改 scripts**，只能修改 Markdown。

## Lessons

lessons 目录中的学习资料，主要是指在真实场景下使用待训练的 Target 能力的执行日志。你需要从这些日志中找到 Target 表现不好、不流畅的地方，针对这些地方提出进化方向。

**MUST** 找出其中和 Target 有关的日志，并从中学习。忽略那些和 Target 无关的内容。如果在日志中没有找到和 Target 有关的内容，应当立刻停止，因为这可能是放错了学习资料。

**MUST** 只针对表现不好，不流畅，遇到问题，和用户反复争执的地方。忽略执行流畅的地方。尤其注意执行成功不意味着执行流畅，也可能是用户深度介入推进的。所以，如果你发现用户参与程度特别高的地方，那就意味着不流畅，必须针对训练和进化。

**MUST** 发现问题后，判断根因类型：
- **业务层问题**（如需求未澄清、逻辑缺失、场景未覆盖）→ 由 Yasal + AutoSearch 处理
- **语言层问题**（如 Skill 文档的表达无法有效 Steer Agent，导致执行偏差）→ 移交 Gosh 并行处理

## Context

训练过程中产生的中间产物（如 INTENT、分析草稿等）放在 `context/*` 目录下。

**MUST** 每轮训练结束后，将本轮中有效提升效果的关键策略、改进路径等，整理输出到 `context/YASAL.md`，作为后续训练的经验积累。

**MUST** 如果本轮训练中通过 Gosh 提炼出了新的 Steering 规律，将其整理输出到 `context/GOSH.md`，作为族群语言的持续积累。

## Metrics

**MUST** 使用 10 分制。达到 8 分以上可以视为本轮迭代通过，可以开始下一轮迭代。

**DEBUG** 目前是调试阶段，所以 AutoResearch 应该以 Foreground 形式启动，每次执行 5 轮迭代后停止。
