# L6 · Tools

Gosh 工具层规范。工具调用是 Prompt 语言的特有维度。名称使用 PascalCase，描述以规范为准，方言命名不参与定义。

## 直接接触世界

Agent 直接读写文件系统，无需中间层。

| Name | Description | Agents |
|------|-------------|--------|
| Glob | 通过文件名 Glob 模式快速匹配文件路径 | AMP |
| Grep | 使用 ripgrep 在文件中搜索精确文本模式 | AMP |
| Read | 读取文件系统中的文件内容 | AMP |
| CreateFile | 创建新文件或覆写已有文件的全部内容 | AMP |
| EditFile | 对文本文件进行局部替换编辑 | AMP |
| UndoEdit | 撤销对指定文件的最近一次编辑 | AMP |
| ListDirectory | 列出指定目录下的文件和子目录 | AMP |

## 通过工具接触世界

Agent 借助外部执行器或网络能力与世界交互。

| Name | Description | Agents |
|------|-------------|--------|
| Bash | 在用户的默认 Shell 中执行命令 | AMP |
| WebSearch | 使用搜索引擎搜索网络信息 | AMP |
| ReadWebPage | 读取并解析指定 URL 的网页内容 | AMP |

## 场外支援

Agent 向外部服务或智能体请求支持，自身不执行具体操作。

| Name | Description | Agents |
|------|-------------|--------|
| Oracle | 调用由推理模型驱动的顾问，用于规划、审查和调试复杂任务 | AMP |
| ReadMcpResource | 从 MCP 服务器读取指定资源 | AMP |
| GitCommitRetrieval | 检索 Git 提交历史，查找类似变更的历史做法和上下文 | Augment |

## 委派子 Agent

Agent 将任务分解并交由子 Agent 执行，自身负责协调。

| Name | Description | Agents |
|------|-------------|--------|
| Task | 启动子 Agent 执行复杂的多步骤子任务 | AMP |
| CodebaseSearch | 启动搜索子 Agent 对代码库进行语义搜索 | AMP, Augment |

## 浏览器操作

Agent 直接控制浏览器，通过视觉和 DOM 交互完成网页任务。

| Name | Description | Agents |
|------|-------------|--------|
| Navigate | 在浏览器中导航到指定 URL，或前进/后退历史记录 | Comet |
| Computer | 通过鼠标点击、键盘输入、滚动等原语与浏览器交互；返回截图 | Comet |
| ReadPage | 读取页面 DOM 无障碍树，返回可操作的元素引用 | Comet |
| Find | 用自然语言描述在页面中定位元素，返回引用和坐标 | Comet |
| FormInput | 向表单元素（文本框、下拉菜单、复选框）设置值 | Comet |
| GetPageText | 提取页面纯文本内容，优先提取正文区域 | Comet |
| TabsCreate | 创建新浏览器标签页并可选择性地导航至初始 URL | Comet |

## IDE 感知

依赖 IDE/编辑器环境才能工作，脱离 IDE 则无效。

| Name | Description | Agents |
|------|-------------|--------|
| GetDiagnostics | 获取文件或目录的诊断信息（错误、警告等） | AMP |
| FormatFile | 使用编辑器的格式化工具对文件进行格式化 | AMP |

## 管理自己

Agent 维护自身的任务状态、执行计划和与用户的交互。

| Name | Description | Agents |
|------|-------------|--------|
| TodoRead | 读取当前会话的 Todo 列表 | AMP |
| TodoWrite | 更新当前会话的 Todo 列表 | AMP, Comet, Augment |
| AskFollowupQuestion | 向用户提问以获取完成任务所需的额外信息 | CodeBuddy |
| AttemptCompletion | 宣告任务完成，向用户呈现最终结果 | CodeBuddy |
| ChatModeRespond | 在对话模式下直接回应用户，不调用其他工具 | CodeBuddy |

## 情绪价值

输出专门面向用户，Agent 自身运作不依赖这类工具。

| Name | Description | Agents |
|------|-------------|--------|
| Mermaid | 将 Mermaid 代码渲染为图表并展示给用户 | AMP |

## Ref

- [AMP Claude-Sonnet-4](../../raw/System-Prompts/AMP/Claude-Sonnet-4.yaml)
- [AMP GPT-5](../../raw/System-Prompts/AMP/GPT-5.yaml)
- [Augment Claude-Sonnet-4](../../raw/System-Prompts/Augment/Claude-Sonnet-4.txt)
- [Augment GPT-5](../../raw/System-Prompts/Augment/GPT-5.txt)
- [CodeBuddy Craft](../../raw/System-Prompts/CodeBuddy/Craft.md)
- [Comet Assistant](../../raw/System-Prompts/Comet/Assistant.md)
- [Comet Tools](../../raw/System-Prompts/Comet/Tools.md)
