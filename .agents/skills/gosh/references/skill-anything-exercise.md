"""Quiz generator — create diverse, high-value quiz questions from knowledge chunks.

Generates 6 types of questions:
- multiple_choice: Standard 4-option MCQ
- true_false: Statement judgment
- fill_blank: Key term/concept recall
- short_answer: Open-ended comprehension
- scenario: Apply knowledge to a real situation
- comparison: Compare/contrast two concepts
"""

from __future__ import annotations

import json
import logging
import re

from skill_anything.models import Difficulty, KnowledgeChunk, QuestionType, QuizQuestion

log = logging.getLogger(__name__)

_QUIZ_PROMPT = """\
You are an expert assessment designer creating questions that test deep \
understanding, not just surface recall. Generate {count} high-quality questions \
from the content below.

**Use a mix of these 6 question types:**

1. **multiple_choice** — 4 options, only one correct. Distractors must be \
plausible (no obviously wrong answers).
2. **true_false** — A precise statement to evaluate. Answer must be "True" or "False".
3. **fill_blank** — Test exact recall of a key term, value, or name.
4. **short_answer** — Requires 2-3 sentences. Tests comprehension and synthesis.
5. **scenario** — Present a realistic situation and ask what would happen or \
what approach to take. Include 4 options.
6. **comparison** — Ask the learner to compare/contrast two concepts, methods, \
or approaches. Tests analytical thinking.

**Quality requirements:**
- Difficulty distribution: 20% easy, 50% medium, 30% hard
- Every question must have a thorough explanation (explain *why*, not just restate)
- Scenario questions must include a concrete, detailed situation
- Comparison questions should require genuine analysis
- Only multiple_choice and scenario types need the "options" field

Content:
{content}

Output ONLY a valid JSON array:

[
  {{
    "question": "Question text (scenario questions include the situation description)",
    "type": "multiple_choice|true_false|fill_blank|short_answer|scenario|comparison",
    "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
    "answer": "The correct answer (for short_answer/scenario/comparison, give a reference answer)",
    "explanation": "Detailed explanation of why this is correct and the underlying reasoning",
    "difficulty": "easy|medium|hard"
  }}
]
"""
