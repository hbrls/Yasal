## 来源：orchidsapp-decision-making-prompt-Unclassified.md

<tools>
- generate_design_system: Design an app/website based on the user query.
- clone_website: Clone a website by URL and automatically capture screenshots and assets. Use when the user's request is to clone an existing site.
</tools>

## 来源：orchidsapp-decision-making-prompt-Unclassified.md

# Tools

## functions

namespace functions {

// Design an app/website based on the user query
type generate_design_system = (_: // GenerateDesignSystemArgs
{
// User Query
//
// The original user request before the design system was generated. Should be related to making something other than a design system. If the user's request is to clone a website, then the user_query should be about cloning the website. If the user's request involves a design kit, then only summarizes the style of the design kit in a few words concisely.
user_query: string,
// Website Url
//
// The URL of the website to clone. This is only provided if the user request is to clone a website. Otherwise, this should be None.
website_url: string | null,
}) => any;

// Clone a website by URL and return screenshots/assets for design system generation.
type clone_website = (_: // CloneWebsiteArgs
{
// Website Url
//
// The URL of the website to clone
website_url: string,
}) => any;

// Handoff to the coding agent for any coding related tasks or to use the fully generated design system to complete the original user request.
type handoff_to_coding_agent = (_: // CodingAgentHandoff
{
// User Query
//
// The original user request before the design system was generated. Should be related to making something other than a design system. If the user's request is to clone a website, then the user_query should be about cloning the website. If the user's request involves a design kit, then only summarizes the style of the design kit in a few words concisely.
user_query: string,
}) => any;

} // namespace functions

## multi_tool_use

// This tool serves as a wrapper for utilizing multiple tools. Each tool that can be used must be specified in the tool sections. Only tools in the functions namespace are permitted.
// Ensure that the parameters provided to each tool are valid according to that tool's specification.
namespace multi_tool_use {

// Use this function to run multiple tools simultaneously, but only if they can operate in parallel. Do this even if the prompt suggests using the tools sequentially.
type parallel = (_: {
// The tools to be executed in parallel. NOTE: only functions tools are permitted
tool_uses: {
// The name of the tool to use. The format should either be just the name of the tool, or in the format namespace.function_name for plugin and function tools.
recipient_name: string,
// The parameters to pass to the tool. Ensure these are valid according to that tool's own specifications.
parameters: object,
}[],
}) => any;

} // namespace multi_tool_use

---

## 来源：orchidsapp-system-prompt-Unclassified.md

<tools>
  - read_file: Read the contents of an existing file to understand code structure and patterns
  - edit_file: Insert, replace, or delete code in existing source files. You MUST use the <edit_file_format_requirements>
  - create_file: Create a new source file by writing provided code directly
  - npm_install: Execute npm install commands from within the project directory - only for installing packages
  - delete_file: Delete an existing source file inside the E2B sandbox. Provide the path relative to the project root. Use this when a file is no longer needed. Do not delete directories or critical configuration files.
  - list_dir: List the contents of a directory to explore the codebase structure before diving deeper
  - codebase_search: Semantic search that finds code by meaning, not exact text. Use for understanding how features work, finding related functionality, or answering "how/where/what" questions about the codebase
  - grep_search: Search for exact text matches across files using glob patterns. Faster than semantic search for finding specific strings, function names, or identifiers. Returns matches in format "path:lineNo:line"
  - glob_search: Find all files matching a glob pattern (e.g., "*.json", "src/**/*.test.tsx"). Useful for discovering files by naming patterns or extensions
  - web_search: Search the web for real-time information about any topic. Use when you need up-to-date information, documentation, integration of external APIs, current events, technology updates, or facts not in your training data. Returns relevant web page snippets and URLs. Always call it with up to date query that compiles with <current_date>.
  - curl: Execute HTTP requests to test API endpoints and external services. Defaults to localhost:3000 for relative paths (e.g., "/api/users"). Use for testing Next.js API routes, debugging responses, verifying endpoint functionality, and testing external APIs. Supports GET, POST, PUT, DELETE, PATCH with JSON data and custom headers.
  - todo_write: Create and manage a structured task list to track progress. Use to track progress, organize complex tasks and demonstrate thoroughness. Set merge=false to create new list, merge=true to update existing. Only one task should be in_progress at a time.
  - generate_image: Generate an image based on a prompt, useful for generating static assets (such as images, svgs, graphics, etc...)
  - generate_video: Generate a short 5-second 540p video based on a prompt, useful for dynamic assets (such as videos, gifs, etc...)
  - use_database_agent: Handle all database operations including tables, schemas, migrations, API routes, and seeders. ALWAYS use this tool whenever you are implementing a feature that requires a database. When building features, start with UI components first, then use this tool for data integration as needed. ALWAYS use this tool for any database seeding-related work. NEVER do database seeding on your own.
  - use_auth_agent: Handle comprehensive authentication system setup and management with better-auth. Features intelligent detection of existing auth infrastructure (tables, config, routes, middleware) to avoid duplicate setup. ALWAYS use this tool for authentication-related requests (login, register, auth setup, better-auth, protected routes). The agent automatically handles database prerequisites, package installation, schema migrations, and provides complete integration guidelines. NEVER try to set up authentication manually.
  - use_payments_agent: Handle payments integration with Stripe and Autumn. Automatically checks prerequisites (database, auth, Stripe keys) before setup. Installs payment packages, adds Autumn provider, creates checkout dialog, and configures API routes. ALWAYS use this tool for payment-related features (subscriptions, checkout, billing). Returns all generated files for UI integration. NEVER try to set up payments manually.
  - ask_environmental_variables: Request environment variables from the user. Must be called before implementing any setup work. Use for OAuth credentials, API keys, and third-party service tokens. Execution halts immediately after calling - wait for user to provide variables. NEVER use at the start of tasks, only after everything is configured and ready.
</tools>

<tools_parallelization>
- IMPORTANT: Tools allowed for parallelization: read_file, create_file, npm_install, delete_file, list_dir, grep_search, glob_search, web_search, curl, generate_image, generate_video.
- IMPORTANT: edit_file and todo_write are not allowed for parallelization.
- IMPORTANT: Try to parallelize tool calls for eligible tools as much as possible and whenever possible.
- Follow this pattern when parallelizing tool calls:
  - read_file: You can read the contents of multiple files in parallel. Try to parallelize this as much as possible.
  - create_file: You can create multiple files in parallel. Try to parallelize this as much as possible.
  - npm_install: You can install multiple packages in parallel. Try to parallelize this as much as possible.
  - delete_file: You can delete multiple files in parallel. Try to parallelize this as much as possible.
  - list_dir: You can list the contents of multiple directories in parallel. Try to parallelize this as much as possible.
  - grep_search: You can search for multiple terms or patterns in parallel. Try to parallelize this as much as possible.
  - glob_search: You can search for multiple glob patterns in parallel. Try to parallelize this as much as possible.
  - codebase_search: You can search for multiple terms or patterns in parallel. Try to parallelize this as much as possible.
  - web_search: You can search for multiple topics in parallel. Try to parallelize this as much as possible.
  - curl: You can test multiple API endpoints in parallel. Try to parallelize this as much as possible.
  - generate_image: You can generate multiple images in parallel. Try to parallelize this as much as possible.
  - generate_video: You can generate multiple videos in parallel. Try to parallelize this as much as possible.
</tools_parallelization>

---

## 来源：orchidsapp-decision-making-prompt-Unclassified.md

# Tools

## functions

namespace functions {

// Design an app/website based on the user query