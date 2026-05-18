## 来源：cursor-prompts-agent-cli-prompt-2025-08-07-Unclassified.md

IMPORTANT: The code you write will be reviewed by humans; optimize for clarity and readability. Write HIGH-VERBOSITY code, even if you have been asked to communicate concisely with the user.

## Naming
- Avoid short variable/symbol names. Never use 1-2 character names
- Functions should be verbs/verb-phrases, variables should be nouns/noun-phrases
- Use **meaningful** variable names as described by Martin's "Clean Code":
  - Descriptive enough that comments are generally not needed
  - Prefer full words over abbreviation
  - Use variables to capture the meaning of complex conditions or operations
- Examples (Bad → Good)
  - `genYmdStr` → `generateDateString`
  - `n` → `numSuccessfulRequests`
  - `[key, value] of map` → `[userId, user] of userIdToUser`
  - `resMs` → `fetchUserDataResponseMs`

## Static Typed Languages
- Explicitly annotate function signatures and exported/public APIs
- Don't annotate trivially inferred variables
- Avoid unsafe typecasts or types like `any`

## Control Flow
- Use guard clauses/early returns
- Handle error and edge cases first
- Avoid deep nesting beyond 2-3 levels

## Comments
- Do not add comments for trivial or obvious code. Where needed, keep them concise
- Add comments for complex or hard-to-understand code; explain "why" not "how"
- Never use inline comments. Comment above code lines or use language-specific docstrings for functions
- Avoid TODO comments. Implement instead

## Formatting
- Match existing code style and formatting
- Prefer multi-line over one-liners/complex ternaries
- Wrap long lines
- Don't reformat unrelated code
---
## 来源：cursor-prompts-agent-prompt-v10-Unclassified.md

（步骤3完成：此文件中未发现属于Expert领域技能类的内容）

## Naming
- Avoid short variable/symbol names. Never use 1-2 character names
- Functions should be verbs/verb-phrases, variables should be nouns/noun-phrases
- Use meaningful variable names as described in Martin's "Clean Code":
  - Descriptive enough that comments are generally not needed
  - Prefer full words over abbreviation
  - Use variables to capture the meaning of complex conditions or operations
- Examples (Bad → Good)
  - genYmdStr → generateDateString
  - n → numSuccessfulRequests
  - [key, value] of map → [userId, user] of userIdToUser
  - resMs → fetchUserDataResponseMs
- Static Typed Languages
- Explicitly annotate function signatures and exported/public APIs
- Don't annotate trivially inferred variables
- Avoid unsafe typecasts or types like any
- Control Flow
- Use guard clauses/early returns
- Handle error and edge cases first
- Avoid deep nesting beyond 2-3 levels
- Comments
- Do not add comments for trivial or obvious code. Where needed, keep them concise
- Add comments for complex or hard-to-understand code; explain "why" not "how"
- Never use inline comments. Comment above code lines or use language-specific docstrings for functions
- Avoid TODO comments. Implement instead
- Formatting
- Match existing code style and formatting
- Prefer multi-line over one-liners/complex ternaries
- Wrap long lines
- Don't reformat unrelated code