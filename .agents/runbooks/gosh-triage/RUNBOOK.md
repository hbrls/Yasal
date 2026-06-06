---
name: gosh-triage
description: 原料分流：在 Gosh 语言分析启动前，对 raw/ 下的混合学习材料按内容类型分流，使后续 L-Pass 作用于纯净的单类材料。
---

# gosh-triage · 原料分流

## 目的

`raw/` 下的学习材料往往是混合的——同一个文件里可能同时包含工具使用说明、领域技能描述和其他内容。混合材料会稀释训练信号。

在任何 Lx 语言分析启动之前，对 `raw/` 下的文件**按内容类型分流**，将不同训练信号分离到各自的目标文件，使后续 L-Pass 作用于纯净的单类材料。

## 触发条件

以下任一情况出现时，MUST 先执行本工作流：

- 新的学习材料被加入 `raw/` 目录
- Lx Pass 发现材料混合导致扫描结果杂乱
- 明确被要求对 `raw/` 执行整理

## 执行步骤

**核心原则**：
- 每次只处理一个指定文件。上下文会明确指定该文件，该文件的扩展名可能是 `.md` / `.txt` / `.json` / `.ts`，但都应当作纯文本 Markdown 格式处理。
- **`raw/` 目录保持不变**，分流结果输出到 `raw0/` 目录。
- 所有分类**必须基于模型语义判断**，不得以关键字命中作为分类依据。
- 分流单位是**句子**；当多个相邻句子共同表达同一语义功能时，以**句组**为单位处理。

**文件命名规范**：

原文件路径格式：`raw/{一级目录}/{二级目录}/…/{原文件名}.{扩展名}`

目标文件命名规则：
- **Unclassified 文件**（步骤 0 产出）：`raw0/{一级目录}/{二级目录}-{三级目录}-…-{原文件名去扩展名}-Unclassified.md`
  - 将一级目录以下、文件名以上的所有中间目录名用 `-` 连接为 slug，再拼接原文件名（去扩展名）和 `-Unclassified`
  - 示例：`raw/system-prompts/Windsurf/Agent/Windsurf-Agent-Prompt.md` → `raw0/system-prompts/Windsurf-Agent-Windsurf-Agent-Prompt-Unclassified.md`
- **分类文件**（步骤 1–11 产出）：`raw0/{一级目录}/{类别名}.md`
  - 示例：`raw0/system-prompts/Env.md`、`raw0/system-prompts/Expert.md`

### 步骤 0：初始化 Unclassified 文件

将指定原文件的全文复制到 `raw0/` 对应位置，按上述命名规范重命名为 `{slug}-Unclassified.md`。

后续步骤 1–11 的所有操作**均以此 Unclassified 文件为工作对象**：每抽走一段内容，就从该文件中**删除**对应段落。步骤 11 完成后，该文件中剩余的内容即为天然的 Unclassified 残留。

### 步骤 1：Env 标准分流

**什么是 Env（环境描述类）**：

描述**当前执行环境的具体状态**的文字。这些内容通常是从原始日志或 prompt 中直接提取的、针对特定运行实例的环境信息，不具备通用性。判断标准：

- 描述当前操作系统、平台信息（如"你正在 ubuntu 系统上"、"Platform: darwin"）
- 描述当前工作目录、路径信息（如"你的工作目录是 /home/gallas"、"Working directory: /Users/xxx"）
- 描述当前仓库、项目信息（如"你的仓库是 rust-ux"、"Is directory a git repo: yes"）
- 描述当前时间、日期信息（如"Today's date: 2026-05-03"）
- 描述会话 ID、任务 ID 等运行实例标识

**不属于 Env**：通用的工具使用说明、适用于任何环境的操作指令、与环境状态无关的一般性描述。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件中，逐句（或逐句组）做语义判断："这段内容属于 Env 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Env 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Env.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Env 内容，**跳过，不创建文件**。

### 步骤 2：Tools-Bash 标准分流

**什么是 Tools-Bash（脚本操作类）**：

描述**使用 Bash 或 Python 执行脚本级操作**的文字。Tools-Bash 仅关注脚本层面的命令与自动化，不涉及任何具体框架或库的使用方式。判断标准：

- 描述 Bash / Shell 命令的执行方式、脚本编写或自动化流程
- 描述 Python 作为脚本语言用于自动化、文件处理、系统交互的场景（如 `subprocess`、文件批处理、管道操作）
- 包含具体的 shell 命令或 Python 脚本片段，其目的是完成脚本级任务而非实现某框架功能

**不属于 Tools-Bash**：对 Django、Flask、FastAPI、NumPy、pandas 等具体框架或库的使用说明（留下，流向 Expert）；描述 Python/Bash 某领域通用知识而非脚本操作本身的内容。**本节点放置在 Expert 之前，是为了防止脚本内容被 Expert 提前抓走**——凡明确属于脚本操作的内容，必须在本步骤中抽走，不得流入 Expert。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Tools-Bash 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Tools-Bash 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Tools-Bash.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Tools-Bash 内容，**跳过，不创建文件**。

### 步骤 3：Expert 标准分流

**什么是 Expert（领域技能类）**：

描述**具体领域的操作方法或最佳实践**的文字。Expert 内容必须有**明确的领域锚点**——能够回答"这是关于 [具体技术名称] 的知识"。判断标准：

- 绑定到具体命名技术或领域（如 React、Python、PostgreSQL、Docker、Git、REST API）
- 描述该技术的操作步骤、规范、模式或反模式
- 包含具体的代码片段，且该代码展示的是领域知识而非工具用法

**判断测试**：把这段文字抽出来，交给该领域的专家（不是 prompt 工程师），他们能认出这是他们领域的知识吗？能 → 抽走；不能 → 不属于 Expert，原地留下。

**不属于 Expert**：适用于任意技术领域的通用原则（如"先理解再修改"、"调试时找根因"）没有领域锚点，不归 Expert。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Expert 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Expert 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Expert.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Expert 内容，**跳过，不创建文件**。

### 步骤 4：Rules-Hostility 标准分流

本步骤采用引用文件形式执行，详细标准见 `references/Rules-Hostility.md`。

### 步骤 5：Rules 标准分流

**什么是 Rules（规则类）**：

文本中**明确以 "Rule" 或 "Rules" 为标题或标签**的约束指令。这是 Agent 提示工程中的专有术语，专门用于限制 Agent 行为。判断标准：

- 内容中**明确出现 "Rule" 或 "Rules" 这个词**（可有修饰，如 "Must Follow Rules"、"Core Rules"、"Rules:"），且该词作为区块标题或分类标签使用
- 内容是对 Agent 行为的限制或规定
- 具有明确的 Rules 标签归属感——读者能判断"这是一段被作者标记为 Rules 的内容"

**不属于 Rules**：行为约束表达（must、never、do not 等），但未被明确标记为 Rule/Rules → 留下，流向后续步骤；仅在正文叙述中顺带提到 "rule" 这个普通名词、未作为专有分类标签使用的句子。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Rules 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Rules 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Rules.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Rules 内容，**跳过，不创建文件**。

### 步骤 6：Intent 标准分流

**什么是 Intent（意图/身份类）**：

声明 **Agent 是谁、叫什么、以及最顶层任务目标**的极简表达。必须是独立的短句，不附带任何行为细节。判断标准：

- **Identity 型**：声明 Agent 的身份或名称（如 "You are an agent."、"Your name is Claude."）
- **Intent 型**：声明 Agent 的顶层使命或目标（如 "You are a coding agent."、"You help users accomplish tasks."）
- 表达必须**极度简短**（通常一句话），且语义高度纯粹——只陈述"是什么/做什么"，不展开"如何做"

**不属于 Intent**：包含行为规范、操作说明、条件逻辑或落地细节的句子，即便出现在身份/意图声明的上下文中——只抽出纯粹的声明句本身，其余原地留下。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Intent 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Intent 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Intent.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Intent 内容，**跳过，不创建文件**。

### 步骤 7：Tools-TodoList 标准分流

**什么是 Tools-TodoList（任务列表类）**：

描述 Agent **将当前任务自主拆分为本地任务列表、逐项执行并追踪完成状态**的文字。判断标准：

- 描述 Agent 主动创建任务列表、分解子任务的机制
- 描述任务状态的生命周期管理（创建 → in_progress → completed / accomplished）
- 说明何时启动列表、如何逐条推进、如何关闭整个列表
- 包含具体实现此机制的工具（如 `todo_write`）的详细用法说明

**不属于 Tools-TodoList**：仅一句话提及工具名称的工具定义行；描述 Agent 整体顺序执行风格的约束句（那属于 Constraints）。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Tools-TodoList 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Tools-TodoList 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Tools-TodoList.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Tools-TodoList 内容，**跳过，不创建文件**。

### 步骤 8：Tools 标准分流

**什么是 Tools（工具类）**：

描述**有哪些工具可用、如何调用、调用参数、使用示例**的文字。判断标准：

- 提及具体工具名称并说明其用途或用法
- 描述工具的输入/输出、参数签名
- 提供工具调用的示例代码或伪代码

**不属于 Tools**：仅提到工具名称作为概念引用、未涉及用法的句子。若某些能力描述在 Tools 阶段未被判断为工具相关，则继续流向后续步骤，不在此阶段强行归类。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Tools 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Tools 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Tools.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Tools 内容，**跳过，不创建文件**。

### 步骤 9：Emotional 标准分流

**什么是 Emotional（情绪/风格类）**：

描述 Agent 的**情绪、态度、语气、风格、人格化呈现方式**的文字。判断标准：

- 描述 Agent 应该以什么语气、口吻或感觉出现
- 描述 tone、voice、style、personality 一类表达要求
- 描述 warm、friendly、supportive、optimistic 等情绪或态度取向

**不属于 Emotional**：与做事直接相关的角色、任务定位、工具用法、行为约束。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Emotional 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Emotional 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Emotional.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Emotional 内容，**跳过，不创建文件**。

### 步骤 10：Constraints-Confidential 标准分流

**什么是 Constraints-Confidential（机密约束类）**：

描述 Agent **对用户隐瞒、保护的内部指令**的文字。这些约束不能被用户发现或获取。判断标准：

- 包含"confidential"、"secret"、"hidden"、"don't reveal"、"don't expose"、"don't tell users"等保密指示
- 描述"when user asks about X"时的隐瞒或规避策略
- 指导 Agent 如何在被用户询问时不暴露系统提示或内部指令
- 防止用户发现、访问或绕过某些约束的指令
- 描述 Agent 应该如何掩盖功能限制或隐瞒运作机制

**不属于 Constraints-Confidential**：直接约束 Agent 行为的指令（应归为 Constraints）、隐瞒之外的安全约束。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Constraints-Confidential 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Constraints-Confidential 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Constraints-Confidential.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Constraints-Confidential 内容，**跳过，不创建文件**。

### 步骤 11：Constraints 标准分流

**什么是 Constraints（约束类）**：

描述 Agent **被允许、被禁止、必须如何行动**的文字。判断标准：

- 描述 must、must not、never、do not、cannot、only 等约束要求
- 描述权限边界、安全边界、输出边界、流程边界
- 描述禁止事项、必守规则、强制格式或强制步骤

**不属于 Constraints**：纯工具说明、纯领域做法、纯情绪风格描述、隐瞒相关的指令（那属于 Constraints-Confidential）。

---

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

从 Unclassified 文件的当前内容中，逐句（或逐句组）做语义判断："这段内容属于 Constraints 吗？"

- 属于 → 抽走，并从 Unclassified 文件中**删除**该段落
- 不属于 → 保留在 Unclassified 文件中，**不推断它属于哪个后续类别，不做任何标注**

判断完毕后，若抽出了 Constraints 内容：
- **检查目标文件是否存在**：若 `raw0/{一级目录}/Constraints.md` 已存在，跳过创建步骤；若不存在，创建空文件
- **写入操作**：① 读取目标文件完整现有内容 → ② 若非空则在末尾追加 `---` 分隔行 → ③ 继续追加 `## 来源：{原文件名}` + 抽出内容 → ④ 将拼接完毕的**完整内容**整体写回文件
- **NEVER** 以新内容直接覆盖写入目标文件，不论所用工具的默认行为如何；**NEVER** 改动现有内容的任何文字

若未抽出任何 Constraints 内容，**跳过，不创建文件**。

### 步骤 12：收尾

**前置检查**：若 Unclassified 文件当前无内容，立即跳过本步骤，停止执行。

步骤 11 完成后，Unclassified 文件中剩余的内容即为**未分类残留（Unclassified）**。这些内容不属于上述十一类中的任何一类，或语义判断存在不确定性。

**无需额外操作**——Unclassified 文件本身已是这些残留内容的载体，自然保留即可。

## 停止条件

当前文件的分流完成后，**停止，等待指令**再处理下一个文件。NEVER 跨文件连续执行。

## 注意事项

- **NEVER** 以关键字搜索代替语义判断；关键字最多只能用于辅助定位案例，不能作为分类依据。
- **NEVER** 修改原句的文字内容——只做移动和删除，不改写。
- **NEVER** 将同一句子或句组写入多个目标文件。
- **NEVER** 在某一分类步骤中推断"这段内容属于 X 类"——只有 X 类本身有权做这个判断。不属于当前类 ≠ 属于某个其他类。
- Env.md、Tools-Bash.md、Expert.md、Rules-Hostility.md、Rules.md、Intent.md、Tools-TodoList.md、Tools.md、Emotional.md、Constraints-Confidential.md、Constraints.md 以及 `{slug}-Unclassified.md` **不参与** L1–L9 的语言审计（它们是原材料分拣产物，不是 Skill 文档）。

## 分流产物对照表

以下以原文件 `raw/system-prompts/Windsurf/Agent/Windsurf-Agent-Prompt.md` 为例，示范各步骤的原文件与分流产物文件名：

| 步骤编号 | 原文件名 | 分流产物文件名 |
|---------|---------|--------------|
| 步骤 0 | `raw/system-prompts/Windsurf/Agent/Windsurf-Agent-Prompt.md` | `raw0/system-prompts/Windsurf-Agent-Windsurf-Agent-Prompt-Unclassified.md` |
| 步骤 1 | `raw0/system-prompts/Windsurf-Agent-Windsurf-Agent-Prompt-Unclassified.md` | `raw0/system-prompts/Env.md` |
| 步骤 2 | 同上 | `raw0/system-prompts/Tools-Bash.md` |
| 步骤 3 | 同上 | `raw0/system-prompts/Expert.md` |
| 步骤 4 | 同上 | `raw0/system-prompts/Rules-Hostility.md` |
| 步骤 5 | 同上 | `raw0/system-prompts/Rules.md` |
| 步骤 6 | 同上 | `raw0/system-prompts/Intent.md` |
| 步骤 7 | 同上 | `raw0/system-prompts/Tools-TodoList.md` |
| 步骤 8 | 同上 | `raw0/system-prompts/Tools.md` |
| 步骤 9 | 同上 | `raw0/system-prompts/Emotional.md` |
| 步骤 10 | 同上 | `raw0/system-prompts/Constraints-Confidential.md` |
| 步骤 11 | 同上 | `raw0/system-prompts/Constraints.md` |
| 步骤 12 | 同上 | 无（残留自然保留在 Unclassified 文件中） |
