# Collaborate 标准分流

**适用位置**：`RUNBOOK.md` 步骤 10。

**目标文件**：`raw0/{一级目录}/Collaborate.md`。

## 什么是 Collaborate（协作求助类）

描述 Agent **主动向人类用户提问、求助、请求补充信息或请人做决定**的文字。Collaborate 关注的是 Agent 因自身能力或信息不足而必须引入人类参与的场景。

## 判断标准

- **工具受阻**：工具缺失、工具调用反复出错、达到重试上限仍无法完成，Agent 需要向人求助
- **澄清补全**：需求模糊有歧义、关键信息缺失，Agent 需要向用户请求补充说明
- **决策分歧**：存在多个决策方向且方向之间有本质冲突（二选一或多选一），Agent 无法自行裁定，需要用户拍板
- **主动求助**：Agent 判断当前局面超出自身能力边界，认为必须向人求助

## 典型归入

- `If the third try fails, you should stop and ask the user what to do next.`
- `If you cannot find some information, believe the user's task is not clearly defined, or are missing crucial context or credentials, you should ask the user for help.`
- `Only ask a clarifying question when essential to proceed.`
- `If there are multiple paths with non-obvious consequences, confirm with the user which they want.`
- `While you are working, you might notice unexpected changes that you didn't make. If this happens, STOP IMMEDIATELY and ask the user how they would like to proceed.`
- `When CI does not pass after the third attempt, ask the user for help.`
- `If important relevant information is not available, you must be helpful by providing a partial response based strictly on the known information, and explicitly ask for clarification regarding the missing details.`

## 不属于 Collaborate

- 安全授权类指令（如"执行高风险操作前需用户确认"）→ Constraints-Confidential 或 Constraints
- 密钥/凭证收集（如"向用户索取 API Key"）→ Tools
- 设计偏好类（如"询问用户喜欢什么风格"）：多个路径之间没有本质冲突、可以由 Agent 自行判断取舍的偏好询问 → Emotional 或后续步骤
- 仅描述提问工具的参数签名或调用格式 → Tools
- 阶段审批流程（如"完成后必须请用户审批再进入下一阶段"）→ Constraints

## 判断测试

这段文字描述的场景中，如果 Agent 不向人求助，任务会**卡住、走错方向或产生不可挽回的后果**吗？会 → 抽走；不会（只是问偏好、走流程确认）→ 不属于 Collaborate，原地留下。

## 执行方式

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Collaborate 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Collaborate 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Collaborate.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Collaborate 内容，**跳过，不创建文件**。
