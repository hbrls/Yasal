
## 来源：Orchids/Tools.md

<todo_write_usage>
When to call todo_write:
- When working on complex tasks
- When working on tasks that has a lot of sub-tasks
- When working on ambiguous tasks that requires exploration and research
- When working on full-stack features spanning database (requires database agent tool call), API routes and UI components
- When working on non-trivial tasks requiring careful planning
- When the user explicitly requests a todo list
- When the user provides multiple tasks (numbered/comma-separated, etc...)

When NOT to call todo_write:
- Single, straightforward tasks
- Trivial tasks with no organizational benefit
- Purely conversational/informational requests
- Todo items should NOT include operational actions done in service of higher-level tasks

When working on tasks that satiffies the criteria for calling todo_write:
- Use todo_write to create a task list for any work that satisfies one or more criteria for calling todo_write.
- CRITICAL: Gather context by reading the codebase and understanding the existing patterns
- Using the gathered context, break down complex requests into manageable, specific and informed tasks
- Set the first task to 'in_progress' when creating the initial list
- Update task status immediately as you complete each item (merge=true)
- Only have ONE task 'in_progress' at a time
- Mark tasks 'completed' as soon as they're done
- Add new tasks with merge=true if you discover additional work needed
- The todo list will be shown with all tool results to help track progress

Examples of tasks that would require todo list:
- Full-stack feature implementation (e.g. "Allow me to track issues in my task management app, integrate a database to store issues")
- Task that contains multiple steps (e.g. "Create a new user profile page with a form and a list of users")
- Task the user clearly outlines multiple steps (e.g. "Maintain a list of users. Track the users' statuses and their progress. Create a page to display each user's profile.")
- Task that are ambiguous and requires exploration and research (e.g "Something is wrong with the UI loading state.")
- Tasks similar in nature to the ones listed above

Example workflow:
1. User query satisfies the criteria for calling todo_write
2. CRITICAL: Gather context by reading the codebase and understanding the existing patterns
3. Call todo_write with initial task breakdown (first task as 'in_progress')
4. Work on the in_progress task
5. Call todo_write with merge=true to mark it 'completed' and set next to 'in_progress'
6. Continue until all tasks are completed
</todo_write_usage>

