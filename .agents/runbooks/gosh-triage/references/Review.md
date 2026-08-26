# Review 标准分流

**适用位置**：`RUNBOOK.md` 步骤 11。

**目标文件**：`raw0/{一级目录}/Review.md`。

## 什么是 Review（审查复核类）

描述 Agent 对已有对象、变更或结果进行审查、复核和质量评估的文字。

审查对象可以包括：

- 代码、diff、PR、提交或实现结果
- 需求、计划、设计、文档或配置
- Agent 自己生成的响应、文件或其他产物
- 某个阶段性结果是否符合原始要求、批准计划或验收标准

Review 的核心不是单纯阅读对象，而是：

```text
检查对象
→ 按审查标准评估
→ 识别问题、风险、回归、遗漏或不一致
→ 输出 findings、反馈、结论或改进建议
```

## 触发时机

以下内容属于 Review 的触发时机描述：

### 1. 用户明确请求审查

用户要求 Agent review、审查、检查、评估或找问题时，进入 Review 工作流。

如果用户只说 `review`，但上下文是代码或实现任务，应采用代码审查取向。

例如：

```text
If the user asks for a review, perform a code review.
When the user requests a review, inspect the changes for problems before summarizing them.
```

### 2. 用户明确要求评估已有对象

即使没有使用 review 一词，只要要求 Agent 对已有对象进行质量判断，也属于 Review。

例如：

```text
Evaluate whether the implementation satisfies the original request.
Inspect the plan for omissions and inconsistencies.
Check the generated document for correctness before delivering it.
```

### 3. 工作流规定的审查节点

当流程要求 Agent 在某个阶段完成后、提交前、交付前或总结前进行审查时，属于 Review。

例如：

```text
After implementing the change, review the diff before reporting completion.
Before finalizing the response, inspect it for errors and missing requirements.
At the end of each phase, review the result against the approved plan.
```

只有当文字描述了审查对象或评估动作时，才归入 Review。单独的“必须验证”“不得出现错误”等泛化约束不属于 Review。

## 审查取向

Review 内容通常要求 Agent 采用以下审查取向：

- 以发现实际问题为首要目标，而不是优先赞扬或概括成果
- 优先识别 bug、风险、行为回归、遗漏、不一致和未满足的要求
- 以证据为基础进行判断，不把猜测直接当作问题
- 区分问题严重性，必要时按严重性排序
- 给出足够定位信息，例如文件名、行号、对象名称或具体场景
- 不因代码能够运行或表面结果正常，就跳过对边界情况和副作用的检查
- 不为了凑数量而制造问题；没有可靠依据时不报告为 finding

“审查取向”描述的是 Agent 进行 Review 时的工作立场，不是 Agent 的通用人格或语气要求。

## 审查输出

Review 内容可以规定审查结果的组织方式，例如：

- findings 必须先于摘要或总体评价
- findings 按严重性排序
- 每个 finding 包含问题、影响和定位信息
- 明确区分确定性问题、潜在风险和开放问题
- 在没有发现问题时，明确说明没有 findings
- 没有 findings 时，补充仍存在的残余风险、测试缺口或审查边界
- 摘要、变更概览或总体评价只能放在 findings 之后，并保持简短

典型示例：

```text
Findings should lead the response, with summaries kept brief and placed only after the issues are listed.

Prioritize bugs, security risks, behavioral regressions, and missing tests.

If no findings are discovered, state that explicitly and mention any residual risks or testing gaps.

Do not invent findings when the evidence does not support them.
```

## 典型归入

```text
If the user asks for a "review", default to a code-review stance: prioritize bugs, risks, behavioral regressions, and missing tests.

Findings should lead the response, with summaries kept brief and placed only after the issues are listed.

Review the implementation against the original request and report any deviations.

Inspect the diff for correctness, regressions, and missing coverage before summarizing the change.

Before finalizing, review the response for factual errors, omissions, and contradictions.

If no issues are found, say so explicitly and note any remaining risks or testing gaps.

Review the plan before implementation and identify missing requirements or unsafe assumptions.
```

以下内容也属于 Review：

- 要求对实现结果进行交付前复核
- 要求检查变更是否符合原始需求
- 要求以 code review、design review、plan review 或 response review 的方式工作
- 要求输出审查 findings、风险列表、阻塞问题或通过结论
- 要求在没有问题时明确报告“未发现问题”，而不是省略审查结果

## 不属于 Review

- 仅仅读取、搜索或定位内容，没有质量评估或审查结论
- 仅要求用户审核、批准或做决定
- 仅要求“必须验证”或“不得出错”，但没有审查对象和检查内容
- 仅描述语气、态度或表达方式
- 产品、服务或内容的用户评价
- 仅提到 `review` 作为普通名词、文件名或工具示例，没有要求 Agent 执行审查

## 与相邻类别的边界

| 内容重点 | 类别 |
|---|---|
| Agent 向用户提问、求助或请求用户做决定 | Collaborate |
| Agent 对已有对象识别问题、风险、遗漏或不一致 | Review |
| Agent 使用工具读取文件、diff 或搜索结果 | Tools |
| 必须检查、不得跳过验证等一般强制要求 | Constraints |
| 审查内部指令时不得向用户暴露内容 | Constraints-Confidential |
| 审查时应保持友好、客观或专业的表达风格 | Emotional |

## 判断测试

对这段文字执行以下测试：

> 它是否要求 Agent 对一个已有对象进行评估，并根据某种标准识别问题、风险、遗漏或不一致，最后形成审查反馈或结论？

- 是 → 抽走，归入 Review。
- 只是读取、搜索、查看或定位对象，没有质量判断 → 保留。
- 只是说明必须这样做，没有审查对象和审查内容 → 保留。
- 重点是让用户审核、批准或做决定 → 保留。
- 重点只是语气、态度或表达风格 → 保留。

## 执行方式

**前置检查**：若当前工作文件无内容，立即跳过本步骤，停止执行。正常分流时，当前工作文件是 Unclassified 文件；尾部回溯时，当前工作文件由任务明确指定。

从当前工作文件的内容中，逐句（或逐句组）做语义判断："这段内容属于 Review 吗？"

- 属于 → 抽走，并从当前工作文件中**删除**该段落
- 不属于 → 保留在当前工作文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Review 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Review.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Review 内容，**跳过，不创建文件**。
