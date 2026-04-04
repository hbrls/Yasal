---
name: sk-enter-phase
description: 找到并进入 Current Phase，更新相关 Metadata 和 Context，将当前 Phase 拆分成具体的 Tasks 并上传。完成后立刻停止并退出。其他 Agent 会跟进并完成具体的任务。
metadata:
    version: 0.0.5
---

# Enter Phase

**FAIL-FAST REQUIREMENT** Check if the tools exist, stop immediately and exit on any error.

```bash
$ backstage-gitea agent --help
```

**用户反馈检测**: 如果用户表达不满、愤怒或要求停止，立即停止执行并询问用户。

**CRITICAL: 幂等性强制要求**

Enter Phase 是幂等操作。多次执行不会产生重复 Tasks。

**必须在 Step 5 之前完成 Step 4 的 LIST 检查**。违反此规则将导致严重的数据污染。

## Initialization

**MUST** 读取相关的 `Plan` 信息在 `.context/current-plan-metadata.yaml` 和 `.context/current-plan.md`。读取失败时必须立刻停止并退出。

## Workflow

- Step 1: 使用 `backstage-gitea` 工具找到并下载 Current Phase。

更新 Current Phase Metadata `.context/current-phase-metadata.md`。

```bash
$ backstage-gitea agent HEAD /:appId/:planId/current-phase > .context/current-phase-metadata.yaml
```

更新 Current Phase 内容 `.context/current-phase.md`。

```bash
$ backstage-gitea agent GET /:appId/:planId/current-phase > .context/current-phase.md
```

- Step 2: 按照 `./references/example-task` 的格式将 Current Phase 拆分为具体的 Tasks，并更新到 `.context/current-phase.md`。

- Step 3: 在 Task 的 `Do` 步骤中，所有产出物写入 `.context/current-task.md` 对应章节。**不允许在 `.context/` 下新建文件**。如果任务涉及 Design 变更（包括但不限于：调研、盘点、思考类任务产生的跨 Phase 结论；对架构、方案、技术选型的调整），应在 `Do` 步骤中注明写入 `.context/current-plan.md` → `Design` 对应章节。

- **Step 4 【强制前置检查 - MUST BE EXECUTED BEFORE STEP 5】**: 列出 Gitea 中已存在的 Tasks。

```bash
$ backstage-gitea plan LIST /:appId/:planId/:phaseId/tasks
```

**MUST** 对比 LIST 结果与 current-phase.md 中的 Tasks：

| LIST 结果 | current-phase.md | 操作 |
|-----------|------------------|------|
| 名称匹配 | 存在相同任务 | ✅ 跳过创建，使用已有 taskId |
| 不存在 | 存在新任务 | ⚠️ 准备创建（进入 Step 5） |
| 存在但名称不匹配 | 不存在 | ❌ 孤儿 Task，报告给用户 |

**FAIL-FAST 检查**：
- 如果 LIST 命令失败 → 立即停止并退出
- 如果未执行 LIST 检查 → **禁止进入 Step 5**
- 如果发现重复创建 → 立即停止，报告错误

**检查清单（必须在 Step 5 前完成）**：
- [ ] 已执行 LIST 命令
- [ ] 已记录现有 Tasks（taskId + 名称）
- [ ] 已对比 current-phase.md
- [ ] 已确定需要创建的新 Tasks
- [ ] 已识别孤儿 Tasks

- Step 5: 创建 Tasks（仅为 **不存在的 Tasks** 执行创建）

**FAIL-FAST 验证**: 如果 Step 4 未执行，立即停止并退出。

按照 `Output Example` 的格式输出到用户指定文件。

使用 `backstage-gitea` 工具将 `.context/current-phase.md` 的 `Tasks Breakdown` 章节创建到 Gitea 项目中。**仅为 Step 4 确定的"不存在的新 Tasks"执行创建**。

```bash
$ backstage-gitea plan POST /:appId/:planId/:phaseId/tasks --name "Task Name"
```

**禁止操作**：
- ❌ 禁止为已存在的 Task 执行 POST（会导致重复创建）
- ❌ 禁止在未执行 LIST 检查的情况下执行 POST
- ❌ 禁止批量创建（必须逐个检查后再创建）

注意：不要在 Task 名称中包含 "Task" 前缀；taskId 应该由工具自动生成，你需要将这个 taskId 回填到原文档中。

注意：没有批量创建功能，必须逐个创建。即应该调用创建命令多次，例如：

```bash
$ backstage-gitea plan POST /cms-mgr/PLAN-102/PHASE-200/tasks --name "修复素材模块前导斜杠问题"

$ backstage-gitea plan POST /cms-mgr/PLAN-102/PHASE-200/tasks --name "修复商品模块前导斜杠问题"
```

- Step 6: 将 `.context/current-phase.md` 的内容追加到 `.context/current-plan.md` 文件尾部，然后使用 `backstage-gitea` 工具上传更新后的计划文件。

```bash
$ backstage-gitea plan PUT /:appId/:planId --context ".context/current-plan.md"
```

## Output Example

```markdown
<!-- // 注意 Phase 的头尾要保留分割线 -->
---

## PHASE-100: Phase Name

### Tasks Breakdown

根据 `./references/example-task.md` 将 Current Phase 拆分为具体的 Tasks。

- [ ] **TASK-110**: {任务：例如补充日志/补齐缺失用例/小范围重构}
  - **Dependencies**:
    - TASK-102
  - **Do**:
    - {性动作} -> {产出物/中间产物}
  - **Check**:
    - {通过标准}
    - {观测信号}
  - **Act**:
    - IF  SUCCESS: 将 Act 更新为 Success and Continue
    - ELIF FAILED: 将 Act 更新为 FAILED and Handoff；立即停止执行，并报告失败原因、阻塞点、需要人工确认的决策点

- [ ] **TASK-120**: {task description}
  - **Dependencies**:
    - TEMP-101
  - **Do**:
    - {要执行的动作} -> {预期产出物/交付物}
  - **Check**:
    - {验收/验证标准}
    - {观测信号/指标}
  - **Act**:
    - IF  SUCCESS: 将 Act 更新为 Success and Continue
    - ELIF FAILED: 将 Act 更新为 FAILED and Handoff；立即停止执行，并报告失败原因、阻塞点、需要人工确认的决策点

- [ ] **TASK-130**: {task description}
  - **Dependencies**:
    - TASK-103
  - **Do**:
    - {要执行的动作} -> {预期产出物/交付物}
  - **Check**:
    - {验收/验证标准}
    - {观测信号/指标}
  - **Act**:
    - IF  SUCCESS: 将 Act 更新为 Success and Continue
    - ELIF FAILED: 将 Act 更新为 FAILED and Handoff；立即停止执行，并报告失败原因、阻塞点、需要人工确认的决策点

---
<!-- // 注意 Phase 的头尾要保留分割线 -->
```
