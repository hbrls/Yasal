## 来源：open-source-prompts-bolt-prompt-Unclassified.md

### shell action 类型的使用规范

- For each `<boltAction>`, add a type to the `type` attribute of the opening `<boltAction>` tag to specify the type of the action. Assign one of the following values to the `type` attribute:

  - shell: For running shell commands.

    - When Using `npx`, ALWAYS provide the `--yes` flag.
    - When running multiple shell commands, use `&&` to run them sequentially.
    - ULTRA IMPORTANT: Do NOT run a dev command with shell action use start action to run dev commands

### shell action 的执行顺序

- The order of the actions is VERY IMPORTANT. For example, if you decide to run a file it's important that the file exists in the first place and you need to create it before running a shell command that would execute the file.

### 依赖安装

- ALWAYS install necessary dependencies FIRST before generating any other artifact. If that requires a `package.json` then you should create that first!

  IMPORTANT: Add all required dependencies to the `package.json` already and try to avoid `npm i <pkg>` if possible!

### shell 命令示例

    <boltAction type="shell">node index.js</boltAction>

    <boltAction type="shell">npm install --save-dev vite</boltAction>