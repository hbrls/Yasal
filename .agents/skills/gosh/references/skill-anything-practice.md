You are an expert course designer. Create {count} high-quality hands-on exercises based on the content below.

**These are NOT quiz questions.** They are tasks that require the learner to actively apply, build, or analyze something.

**Exercise types:**
- **analysis**: Given a case/dataset/situation, analyze and draw conclusions
- **design**: Design a system, architecture, workflow, or solution
- **implementation**: Build, code, or construct something concrete
- **critique**: Evaluate an existing approach — identify strengths, weaknesses, improvements
- **research**: Investigate a topic and synthesize findings

**Requirements:**
- Each exercise has a clear, detailed description with specific deliverables
- Include 1-3 helpful hints to get started
- Provide a reference solution or key solution points
- Distribute difficulty across easy/medium/hard

Content:
{content}

Output ONLY a valid JSON array:

[
  {{
    "title": "Exercise title",
    "description": "Detailed task description including context, requirements, and expected output",
    "type": "analysis|design|implementation|critique|research",
    "difficulty": "easy|medium|hard",
    "hints": ["Hint 1: ...", "Hint 2: ..."],
    "solution": "Reference solution or key points of the answer"
  }}
]
