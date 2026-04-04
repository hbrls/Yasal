---
name: yasal
description: 为即将运行的 `skills/codex-autoresearch` 预置约定（lessons目录、目标模板、对话优化规则等），指导后续自适应进化流程
metadata:
  version: 0.0.1
---

# Yasal Training Runbook - 能力训练手册

**Meta Purpose**: 通过本文档预置约定的训练流程，指定训练方向，使用 `skills/codex-autoresearch` 训练并增强其他能力。

可以用来训练任何能力，即：

```bash
.agents/commands/{TARGET}/COMMAND.md
.agents/skills/{TARGET}/SKILL.md
```

你应该先阅读并遵守本文的所有预置约定，然后再调用 `skills/codex-autoresearch`。

具体的训练过程由 autoresearch 负责完成，但必须先阅读并遵守 Yasal 的所有预置约定。必须先启动 Yasal，后启动 autoresearch。

## 目录结构

**MUST** 学习资料都放在 `lessons/*` 目录，且必须是纯文本材料。

**MUST** 学习过程中如果需要记录经验，应该放在 `context/*` 目录，且必须是 Markdown 文件。

**MUST** 以 `./assets/template-INTENT.md` 为模板，通过和 autoresearch 对话来确定进化的目标，把目标写入 `context/INTENT.md`。

## Meta INTENT / Meta Goal

**MUST** 训练目标是指定的 TARGET 能力，不是 Yasal，也不是 autoresearch。

Skills 是通过 LLM 来运行的，所以目标必须是且只能是增强 SKILL.md 里的文字内容。

references / assets 目录下可能有一些补充用的 Markdown 文字，这些也可以是训练和进化的目标，

scripts 目录下可能有一些短脚本，但只能用来做简单的协助工具，例如遍历目录或统计得分；不能往脚本里植入复杂功能。简单来说，大部分情况下你都 **不能修改 scripts**，只能修改 Markdown。

## Lessons

lessons 目录中的学习资料，主要是指在真实场景下使用待训练的 TARGET 能力的执行日志。你需要从这些日志中找到 TARGET 表现不好、不流畅的地方，针对这些地方提出进化方向。

**MUST** 找出其中和 TARGET 有关的日志，并从中学习。忽略那些和 TARGET 无关的内容。如果在日志中没有找到和 TARGET 有关的内容，应当立刻停止，因为这可能是放错了学习资料。

**MUST** 只针对表现不好，不流畅，遇到问题，和用户反复争执的地方。忽略执行流畅的地方。尤其注意执行成功不意味着执行流畅，也可能是用户深度介入推进的。所以，如果你发现用户参与程度特别高的地方，那就意味着不流畅，必须针对训练和进化。

## Metrics

**MUST** 使用 10 分制。达到 8 分以上可以视为本轮迭代通过，可以开始下一轮迭代。
