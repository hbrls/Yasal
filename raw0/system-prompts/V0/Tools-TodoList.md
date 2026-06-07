## 来源：v0-prompts-and-tools-tools-Unclassified.md

    {
      "name": "TodoManager",
      "description": "Manages structured todo lists for complex, multi-step projects. Tracks progress through milestone-level tasks and generates technical implementation plans.

**Core workflow:**
1. **set_tasks** - Break project into 3-7 milestone tasks (distinct systems, major features, integrations)
2. **move_to_task** - Complete current work, focus on next task

**Task guidelines:**
• **Milestone-level tasks** - \"Build Homepage\", \"Setup Auth\", \"Add Database\" (not micro-steps)
• **One page = one task** - Don't break single pages into multiple tasks
• **UI before backend** - Scaffold pages first, then add data/auth/integrations
• **≤10 tasks total** - Keep focused and manageable
• **NO vague tasks** - Never use \"Polish\", \"Test\", \"Finalize\", or other meaningless fluff

**When to use:**
• Projects with multiple distinct systems that need to work together
• Apps requiring separate user-facing and admin components  
• Complex integrations with multiple independent features

**When NOT to use:**
• Single cohesive builds (even if complex) - landing pages, forms, components
• Trivial or single-step tasks
• Conversational/informational requests

**Examples:**

• **Multiple Systems**: \"Build a waitlist form with auth-protected admin dashboard\"
  → \"Get Database Integration, Create Waitlist Form, Build Admin Dashboard, Setup Auth Protection\"

• **App with Distinct Features**: \"Create a recipe app with user accounts and favorites\"
  → \"Setup Authentication, Build Recipe Browser, Create User Profiles, Add Favorites System\"

• **Complex Integration**: \"Add user-generated content with moderation to my site\"
  → \"Get Database Integration, Create Content Submission, Build Moderation Dashboard, Setup User Management\"

• **Skip TodoManager**: \"Build an email SaaS landing page\" or \"Add a contact form\" or \"Create a pricing section\"
  → Skip todos - single cohesive components, just build directly",
      "parameters": {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "additionalProperties": false,
        "properties": {
          "action": {
            "description": "Todo management action for complex, multi-step tasks:

**Core actions:**
• **set_tasks** - Create initial task breakdown (max 7 milestone-level tasks)
• **move_to_task** - Complete current work and focus on next specific task
• **add_task** - Add single task to existing list

**Utility actions:**
• **read_list** - View current todo list without changes
• **mark_all_done** - Complete all tasks (project finished)

**When to use:** Multi-step projects, complex implementations, tasks requiring 3+ steps. Skip for trivial or single-step tasks.",
            "enum": ["add_task", "set_tasks", "mark_all_done", "move_to_task", "read_list"],
            "type": "string"
          },
          "moveToTask": {
            "description": "Exact task name to focus on for move_to_task. Marks all prior tasks as done.",
            "type": "string"
          },
          "task": {
            "description": "Task description for add_task. Use milestone-level tasks, not micro-steps.",
            "type": "string"
          },
          "taskNameActive": {
            "description": "2-5 words describing the task when it is running. Will be shown in the UI. For example, \"Checking SF Weather\".",
            "type": "string"
          },
          "taskNameComplete": {
            "description": "2-5 words describing the task when it is complete. Will be shown in the UI. It should not signal success or failure, just that the task is done. For example, \"Looked up SF Weather\".",
            "type": "string"
          },
          "tasks": {
            "description": "Complete task list for set_tasks. First becomes in-progress, rest todo.",
            "items": {
              "type": "string"
            },
            "type": "array"
          }
        },
        "required": ["action", "taskNameActive", "taskNameComplete"],
        "type": "object"
      }
    }