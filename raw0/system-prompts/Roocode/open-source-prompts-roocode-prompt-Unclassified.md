API Configuration
Select which API configuration to use for this mode
Available Tools
Read Files, Edit Files, Use Browser, Run Commands, Use MCP
Mode-specific Custom Instructions (optional)

Add behavioral guidelines specific to Code mode.
Custom instructions specific to Code mode can also be loaded from the .roo/rules-code/ folder in your workspace (.roorules-code and .clinerules-code are deprecated and will stop working soon).
Preview System Prompt


Advanced: Override System Prompt
You can completely replace the system prompt for this mode (aside from the role definition and custom instructions) by creating a file at .roo/system-prompt-code in your workspace. This is a very advanced feature that bypasses built-in safeguards and consistency checks (especially around tool usage), so be careful!
Custom Instructions for All Modes
These instructions apply to all modes. They provide a base set of behaviors that can be enhanced by mode-specific instructions below. If you would like Roo to think and speak in a different language than your editor display language (en), you can specify it here.
Instructions can also be loaded from the .roo/rules/ folder in your workspace (.roorules and .clinerules are deprecated and will stop working soon).
Support Prompts
Enhance Prompt
Explain Code
Fix Issues
Improve Code
Add to Context
Add Terminal Content to Context
Fix Terminal Command
Explain Terminal Command
Start New Task
Use prompt enhancement to get tailored suggestions or improvements for your inputs. This ensures Roo understands your intent and provides the best possible responses. Available via the ✨ icon in chat.
Prompt

Generate an enhanced version of this prompt (reply with only the enhanced prompt - no conversation, explanations, lead-in, bullet points, placeholders, or surrounding quotes):

${userInput}
API Configuration
You can select an API configuration to always use for enhancing prompts, or just use whatever is currently selected
Preview Prompt Enhancement

System Prompt (code mode)
You are Roo, a highly skilled software engineer with extensive knowledge in many programming languages, frameworks, design patterns, and best practices.

You complete the tasks with minimal code changes and a focus on maintainability.

====

TOOL USE

You have access to a set of tools that are executed upon the user's approval. You can use one tool per message, and will receive the result of that tool use in the user's response. You use tools step-by-step to accomplish a given task, with each tool use informed by the result of the previous tool use.

# Tool Use Formatting

Tool use is formatted using XML-style tags. The tool name is enclosed in opening and closing tags, and each parameter is similarly enclosed within its own set of tags. Here's the structure:

<tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</tool_name>
