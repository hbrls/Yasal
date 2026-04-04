## Training Flow Overview

### Phase 1: 对话澄清与 INTENT 编写

### Phase 2: Autoresearch Launch - 初始化运行

### Phase 5: Concrete Examples Strategy

**为什么示例最重要**:

抽象规则 → AI 难以理解 → 执行偏差

具体示例 → AI 看到输入→处理→输出 → 准确执行

**本次添加的示例类型**:

1. **Detection Example**: JSON 输入 → 统计过程 → Lesson 输出
2. **Scoring Example**: 高/中/低质量教训 → 分数分解 → 为什么得分
3. **Revision Example**: 低质量 → 改进过程 → 高质量

**教训 L-5**: 每个 detection pattern 至少配一个完整的输入→输出示例。示例比规则更有效。

---

### Phase 6: Anti-Pattern Documentation

**MUST NOT Rules 的价值**:

告诉 AI"不要做什么"，比"要做什么"更关键。

**本次 MUST NOT**:
- DO NOT create additional scripts
- DO NOT call external APIs
- DO NOT output vague lessons

**教训 L-6**: MUST NOT 规则防止 AI 偏离核心约束。用户最关心的是"script 不承担核心能力"，这在 MUST NOT 中明确禁止。

---

## Yasal vs Autoresearch: 关系澄清

| 角色 | Yasal | Autoresearch |
|------|-------|--------------|
| **职责** | 确定训练目标 | 执行迭代优化 |
| **输入** | 用户对话 | INTENT.md |
| **输出** | INTENT.md | 改进后的能力文件 |
| **时间点** | 在 autoresearch 前 | 在 yasal 后 |
| **价值** | 引导对话，找到真实目标 | 机械迭代，达成目标 |

**教训 L-meta**: Yasal 是"方向探测器"，Autoresearch 是"执行引擎"。没有 Yasal，Autoresearch 可能优化错误的目标。

---

## Training Runbook Template

**复用此模板训练任何能力**:

### Step 2: 对话澄清（至少 3 个问题）
```
Q1: 改进方向？
Q2: 最终产物是什么？
Q3: 约束条件（script角色？外部依赖？）
```

### Step 3: 写 INTENT
```bash
write context/INTENT.md
```

### Step 4: 启动 autoresearch
```bash
python3 .agents/skills/codex-autoresearch/scripts/autoresearch_init_run.py --mode foreground ...
```

### Step 5: 迭代改进
- 优先添加：Meta-instruction, Examples, Self-check
- 其次添加：Decision tree, Error handling
- 最后添加：Edge cases, Security

### Step 6: 记录教训
每次训练结束后，写一个 `context/yasal-{TARGET}.md` 记录流程。

---

## Lessons from This Training Session

### L-3: 示例比规则更有效
- **Outcome**: 添加 4 个 detection examples 后，AI 执行准确性显著提升
- **Insight**: 每个抽象规则至少配一个完整的输入→输出示例
- **Source**: yasal-learn.md:phase5

### L-4: MUST NOT 防止偏离约束
- **Outcome**: 明确禁止"script 承担核心能力"，AI 不会尝试写复杂 script
- **Insight**: MUST NOT 规则比 MUST 规则更关键
- **Source**: yasal-learn.md:phase6

### L-5: 自检清单是质量门禁
- **Outcome**: 8 点 checklist 强制核对，避免低质量输出
- **Insight**: AI 输出前必须逐项 check，不合格则 revise
- **Source**: yasal-learn.md:phase7

---

## Summary

**Yasal 的核心方法论**:

1. **对话引导**: 通过 2-3 轮问题，找到真实目标
2. **INTENT 标准化**: 写入明确的目标声明
3. **Autoresearch 执行**: 机械迭代达成目标
4. **教训沉淀**: 记录每次训练的经验

**适用场景**:
- 训练任何 `.agents/commands/*` 能力
- 训练任何 `.agents/skills/*` 能力
- 优化文档、脚本、配置等

**不适用场景**:
- 紧急修复（需要直接 debug）
- 探索性任务（目标不明确）

---

## Next: 如何使用此 Runbook

**训练新能力的流程**:

1. 调用 `yasal` skill
2. 描述目标："增强 {能力名} 的 {方向}"
3. Yasal 引导对话 → 确定 INTENT
4. Autoresearch 迭代优化
5. 写 `context/yasal-{能力名}.md` 记录经验
6. 将经验教训加入 `lessons/` 目录

**持续改进 Yasal 自身**:
- 每次训练后，反思 Yasal 流程是否有改进
- 更新此 Runbook
- 优化 template-INTENT.md
- 完善对话问题库


约定：通过和 Agent 对话来调整目标推断规则，优化范围扫描逻辑，改进指标计算方法，完善验证和防护机制。
