### Category Definitions

#### 1. Do mode (DEFAULT CHOICE)
Input belongs in do mode if it:
- Is NOT explicitly about creating or working with specifications
- Requests modifications to code or the workspace
- Is an imperative sentence asking for action
- Starts with a base-form verb (e.g., "Write," "Create," "Generate")
- Has an implied subject ("you" is understood)
- Requests to run commands or make changes to files
- Asks for information, explanation, or clarification
- Ends with a question mark (?)
- Seeks information or explanation
- Starts with interrogative words like "who," "what," "where," "when," "why," or "how"
- Begins with a helping verb for yes/no questions, like "Is," "Are," "Can," "Should"
- Asks for explanation of code or concepts
- Examples include:
  - "Write a function to reverse a string."
  - "Create a new file called index.js."
  - "Fix the syntax errors in this function."
  - "Refactor this code to be more efficient."
  - "What is the capital of France?"
  - "How do promises work in JavaScript?"
  - "Can you explain this code?"
  - "Tell me about design patterns"

#### 2. Spec mode (ONLY for specification requests)
Input belongs in spec mode ONLY if it EXPLICITLY:
- Asks to create a specification (or spec)
- Uses the word "spec" or "specification" to request creating a formal spec
- Mentions creating a formal requirements document
- Involves executing tasks from existing specs
- Examples include:
  - "Create a spec for this feature"
  - "Generate a specification for the login system"
  - "Let's create a formal spec document for this project"
  - "Implement a spec based on this conversation"
  - "Execute task 3.2 from my-feature spec"
  - "Execute task 2 from My Feature"
  - "Start task 1 for the spec"
  - "What is the next task in the <feature name> spec?"

Example response:
{"chat": 0.0, "do": 0.9, "spec": 0.1}

Here is the last user message:
Hi!
