You are an expert knowledge architect and instructional designer. Analyze the following content and produce a comprehensive, structured learning package.

Your goal is to create materials with **genuine learning value** — not generic summaries, but deeply organized knowledge that lets a learner master the topic without returning to the original source.

Produce all 7 sections in a single JSON object:

### 1. summary (200-400 words)
- Identify the central thesis, methodology, and conclusions
- Capture the logical chain of reasoning, not just surface-level facts
- Write in clear, precise prose

### 2. detailed_notes (Markdown format, thorough)
- Use hierarchical headings (##/###) to organize
- Include key formulas, data points, quotes, and examples
- Use bold for critical terms, bullet lists for supporting details
- Goal: reading these notes should fully replace re-reading the source

### 3. key_concepts (10-15 core concepts)
- Format: "Concept Name: one-sentence explanation"
- Order from foundational to advanced
- Each explanation must be precise and self-contained

### 4. glossary (15-25 terms)
- Every domain-specific term, acronym, or technical phrase
- Precise definitions (not dictionary-generic)
- Include related_terms to show connections

### 5. cheat_sheet (Markdown, fits on one page)
- The most essential information condensed for quick reference
- Use tables, bullet lists, and code blocks for density
- Suitable for printing and pinning to a wall

### 6. takeaways (5-10 actionable items)
- Not "what was covered" but "what to do with this knowledge"
- Concrete, specific actions the learner should take next
- Start each with a verb

### 7. learning_path
- prerequisites: what someone needs to know before this material
- next_steps: what to study after mastering this
- resources: specific books, courses, tools, papers, or URLs to explore

Content:
---
{content}
---

Output ONLY valid JSON. No markdown fences, no commentary:

{{
  "summary": "...",
  "detailed_notes": "## Section 1\\n\\n...",
  "key_concepts": ["Concept: explanation", ...],
  "glossary": [{{"term": "...", "definition": "...", "related_terms": ["..."]}}],
  "cheat_sheet": "## Quick Reference\\n\\n| ... |\\n...",
  "takeaways": ["Build a ...", "Practice ...", "Read ..."],
  "learning_path": {{
    "prerequisites": ["..."],
    "next_steps": ["..."],
    "resources": ["..."]
  }}
}}
"""

_TIMELINE_PROMPT = """\
Given the following content chunks with position markers, generate a structured \
outline/timeline. Each entry needs: position (timestamp, page number, or section), \
title (short heading), and summary (1-2 sentences).

Content chunks:
{chunks_summary}

Output ONLY a valid JSON array:
[{{"position": "...", "title": "...", "summary": "..."}}]
