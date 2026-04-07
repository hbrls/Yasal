# Yasal

*尝试把小龙虾限制在这个工作目录下。*

<img src="./README-Yasal.jpg" width="360" />

## Workflow

### Step 1: 准备学习材料和目标

将交互历史放入 `lessons/`。内容应包含：
- 时间戳（任何形式的时间记录）
- 操作序列（谁做了什么，顺序是什么）
- 修改轨迹（同一实体被修改了多少次，修改者是谁）
- 资源标识（涉及哪些文件/任务/对象）

### Step 2: 启动 KiloCode Cli 的自动进化机制

进入项目目录并启动 KiloCode Cli：

```bash
$ cd /path/to/Yasal
$ kilocode
```

在 KiloCode Cli 交互界面中选中 `skills/yasal`，`Yasal` 会告知 Agent 基本的设定。

接下来 `Yasal` 会自动启动 `skills/codex-autoresearch`，Agent 会问你一些问题，继续对话，进一步明确进化方向。

Agent 会提示你输入 go 开始进化。

### Step 3: 查看进化效果

根据约定，进化的过程会输出在 `context/YASAL.md`。

## 参考资料

1. [手把手教你安装 @kilocode/cli](https://mp.weixin.qq.com/s/ImjbmFthEO6FLtEnuKVXNQ)
2. https://github.com/leo-lilinxiao/codex-autoresearch
3. https://github.com/karpathy/autoresearch

---

# Gosh - 构史

我们发现某些特定的语法或表达对 Agent 有更强的 Steering 效果。训练中我们持续总结这些规律，并将其运用到能力文档的编写中——把它理解为 Agent 的一种族群语言。
