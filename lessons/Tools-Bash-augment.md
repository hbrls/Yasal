## 来源：augment-code-claude-4-sonnet-tools-Unclassified.md

    {
      "name": "launch-process",
      "description": "Launch a new process with a shell command. A process can be waiting (`wait=true`) or non-waiting (`wait=false`).\n\nIf `wait=true`, launches the process in an interactive terminal, and waits for the process to complete up to\n`max_wait_seconds` seconds. If the process ends during this period, the tool call returns. If the timeout\nexpires, the process will continue running in the background but the tool call will return. You can then\ninteract with the process using the other process tools.\n\nNote: Only one waiting process can be running at a time. If you try to launch a process with `wait=true`\nwhile another is running, the tool will return an error.\n\nIf `wait=false`, launches a background process in a separate terminal. This returns immediately, while the\nprocess keeps running in the background.\n\nNotes:\n- Use `wait=true` processes when the command is expected to be short, or when you can't\nproceed with your task until the process is complete. Use `wait=false` for processes that are\nexpected to run in the background, such as starting a server you'll need to interact with, or a\nlong-running process that does not need to complete before proceeding with your task.\n- If this tool returns while the process is still running, you can continue to interact with the process\nusing the other available tools. You can wait for the process, read from it, write to it, kill it, etc.\n- You can use this tool to interact with the user's local version control system. Do not use the\nretrieval tool for that purpose.\n- If there is a more specific tool available that can perform the function, use that tool instead of\nthis one.\n\nThe OS is win32. The shell is 'bash'.",
      "parameters": {
        "type": "object",
        "properties": {
          "command": {
            "type": "string",
            "description": "The shell command to execute."
          },
          "wait": {
            "type": "boolean",
            "description": "Whether to wait for the command to complete."
          },
          "max_wait_seconds": {
            "type": "number",
            "description": "Number of seconds to wait for the command to complete. Only relevant when wait=true. 10 minutes may be a good default: increase from there if needed."
          },
          "cwd": {
            "type": "string",
            "description": "Required parameter. Absolute path to the working directory for the command."
          }
        },
        "required": ["command", "wait", "max_wait_seconds", "cwd"]
      }
    },
    {
      "name": "kill-process",
      "description": "Kill a process by its terminal ID.",
      "parameters": {
        "type": "object",
        "properties": {
          "terminal_id": {
            "type": "integer",
            "description": "Terminal ID to kill."
          }
        },
        "required": ["terminal_id"]
      }
    },
    {
      "name": "read-process",
      "description": "Read output from a terminal.\n\nIf `wait=true` and the process has not yet completed, waits for the terminal to complete up to `max_wait_seconds` seconds before returning its output.\n\nIf `wait=false` or the process has already completed, returns immediately with the current output.",
      "parameters": {
        "type": "object",
        "properties": {
          "terminal_id": {
            "type": "integer",
            "description": "Terminal ID to read from."
          },
          "wait": {
            "type": "boolean",
            "description": "Whether to wait for the command to complete."
          },
          "max_wait_seconds": {
            "type": "number",
            "description": "Number of seconds to wait for the command to complete. Only relevant when wait=true. 1 minute may be a good default: increase from there if needed."
          }
        },
        "required": ["terminal_id", "wait", "max_wait_seconds"]
      }
    },
    {
      "name": "write-process",
      "description": "Write input to a terminal.",
      "parameters": {
        "type": "object",
        "properties": {
          "terminal_id": {
            "type": "integer",
            "description": "Terminal ID to write to."
          },
          "input_text": {
            "type": "string",
            "description": "Text to write to the process's stdin."
          }
        },
        "required": ["terminal_id", "input_text"]
      }
    },
    {
      "name": "list-processes",
      "description": "List all known terminals created with the launch-process tool and their states.",
      "parameters": {
        "type": "object",
        "properties": {},
        "required": []
      }
    }
