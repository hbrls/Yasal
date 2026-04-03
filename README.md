# Yasal

*尝试把小龙虾限制在这个工作目录下。*

<img src="./README-Yasal.jpg" width="360" />

---

## Retrospective 能力上手教程

### 实验目的

通过真实日志复盘，验证和改进 retrospective 命令的实用性。

### 准备工作

1. 创建输入目录：`mkdir -p .context/READONLY_INPUT`
2. 放置真实日志（任选）：
   - `task_metadata.json` - 任务元数据
   - `focus_chain_*.md` - 聚焦链清单
   - `api_conversation_history.json` - API 对话历史
   - `ui_messages.json` - UI 消息记录

### 执行步骤

```bash
# 1. 触发复盘
/retrospective

# 2. 系统自动识别输入类型
#    - 完整对话 → 快速/深度复盘
#    - 元数据 → 元数据复盘模板
#    - 聚焦链 → 聚焦链复盘模板

# 3. 输出复盘报告到 .context/session-retro.md

# 4. 检查复盘质量（关键指标）
wc -l .context/session-retro.md          # 行数应在 100-200 行
grep "⚠️" .context/session-retro.md       # 推断标记应醒目

# 5. 根据复盘反馈改进 retro 能力
#    - 发现问题 → 立即改进 COMMAND.md
#    - 重新复盘 → 对比改进效果
```

### 复盘质量检查清单

- ✓ 行数控制在 100-200 行（快速模式）
- ✓ 推断内容标记醒目（⚠️ 符号）
- ✓ 关键决策识别 ≥ 3 个
- ✓ 问题与解法识别 ≥ 3 个
- ✓ 可沉淀经验 ≥ 3 个
- ✓ 包含执行效率分析
- ✓ 包含 retro 能力反思

### 预期成果

- 输出精简复盘报告（~150行）
- 识别关键决策、问题、经验
- 发现 retro 能力改进点
- 形成能力改进闭环

### 实验验证

本教程已通过真实任务日志验证：
- 输入：TASK-120 元数据 + 聚焦链
- 输出：142 行复盘报告
- 改进：4 项能力优化（推断标记、效率分析、反馈提取、长度控制）

## 参考资料

1. [手把手教你安装 @kilocode/cli](https://mp.weixin.qq.com/s/ImjbmFthEO6FLtEnuKVXNQ)
2. https://github.com/leo-lilinxiao/codex-autoresearch
3. https://github.com/karpathy/autoresearch
