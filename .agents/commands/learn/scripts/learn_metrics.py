#!/usr/bin/env python3
"""
learn_metrics.py - 计算和输出 learn 教训的指标
"""

import re
import sys
from pathlib import Path


def parse_lessons_file(path: Path) -> dict:
    if not path.exists():
        return {"total": 0, "categories": {}, "severities": {}}

    content = path.read_text(encoding="utf-8")

    lessons = re.findall(r"^### L-\d+: (.+)$", content, re.MULTILINE)
    categories = re.findall(r"- \*\*Category:\*\* (\w+)", content)
    severities = re.findall(r"- \*\*Severity:\*\* (\w+)", content)

    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1

    severity_counts = {}
    for sev in severities:
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    critical_in_title = len(re.findall(r"!$", content))

    return {
        "total": len(lessons),
        "categories": category_counts,
        "severities": severity_counts,
        "critical_in_title": critical_in_title,
    }


def format_metrics(metrics: dict) -> str:
    lines = [
        f"Total lessons: {metrics['total']}",
        f"Categories: {metrics['categories']}",
        f"Severities: {metrics['severities']}",
        f"Critical (!) in titles: {metrics['critical_in_title']}",
    ]
    return "\n".join(lines)


def main():
    lessons_path = Path(".lessons/learn-lessons.md")
    if len(sys.argv) > 1:
        lessons_path = Path(sys.argv[1])

    metrics = parse_lessons_file(lessons_path)
    print(format_metrics(metrics))

    return 0 if metrics["total"] > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
