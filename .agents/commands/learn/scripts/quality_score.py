#!/usr/bin/env python3
"""
quality_score.py - 计算教训质量分数（三维度评分）

维度：
1. 可操作性 (actionability): 是否有明确的触发信号和应用方法
2. 可追溯性 (traceability): 是否有清晰的Source标记
3. 指导价值 (guidance_value): Insight是否具体且可应用

评分：每维度 0-33.3分，总分 0-100分
"""

import re
import sys
from pathlib import Path


def parse_lessons_file(path: Path) -> list[dict]:
    if not path.exists():
        return []

    content = path.read_text(encoding="utf-8")

    lessons = []
    pattern = r"### L-(\d+): (.+?)\n- \*\*Category:\*\* (.+?)\n- \*\*Outcome:\*\* (.+?)\n- \*\*Insight:\*\* (.+?)\n- \*\*Source:\*\* (.+)"
    matches = re.findall(pattern, content, re.MULTILINE)

    for match in matches:
        lessons.append(
            {
                "id": int(match[0]),
                "title": match[1].strip(),
                "category": match[2].strip(),
                "outcome": match[3].strip(),
                "insight": match[4].strip(),
                "source": match[5].strip(),
            }
        )

    return lessons


def score_actionability(lesson: dict) -> float:
    score = 0.0

    if len(lesson["title"]) > 10:
        score += 10
    if lesson["category"] in ["problem", "win", "meta-insight"]:
        score += 10
    if len(lesson["outcome"]) > 30:
        score += 8.3

    outcome = lesson["outcome"]
    if any(
        k in outcome
        for k in ["计数", "频率", "占比", "次数", "时间戳", "统计", "%", ">"]
    ):
        score += 5

    return min(33.3, score)


def score_traceability(lesson: dict) -> float:
    score = 0.0

    if lesson["source"]:
        score += 15
    if ".md" in lesson["source"] or "/" in lesson["source"]:
        score += 10
    if re.search(r"task|phase|file", lesson["source"], re.IGNORECASE):
        score += 8.3

    return min(33.3, score)


def score_guidance_value(lesson: dict) -> float:
    score = 0.0

    insight = lesson["insight"]

    if len(insight) > 40:
        score += 10

    bad_patterns = ["要小心", "注意", "避免", "应该", "需要"]
    if not any(p in insight for p in bad_patterns):
        score += 10

    good_patterns = [
        "用",
        "采用",
        "改为",
        "调用",
        "先",
        "再",
        "验证",
        "统计",
        "检测",
        "分析",
        "执行",
        "列出",
        "标记",
    ]
    good_count = sum(1 for p in good_patterns if p in insight)
    score += min(8.3, good_count * 2)

    if any(
        k in insight
        for k in [
            "阈值",
            "次数>",
            "频率",
            "占比>",
            "时间",
            "清单",
            "策略",
            "流程",
            "步骤",
        ]
    ):
        score += 5

    return min(33.3, score)


def calculate_quality_score(lessons: list[dict]) -> dict:
    if not lessons:
        return {
            "total": 0,
            "avg_score": 0,
            "actionability_avg": 0,
            "traceability_avg": 0,
            "guidance_avg": 0,
            "score_distribution": {},
        }

    scores = []
    actionability_scores = []
    traceability_scores = []
    guidance_scores = []

    for lesson in lessons:
        a = score_actionability(lesson)
        t = score_traceability(lesson)
        g = score_guidance_value(lesson)
        total = a + t + g

        scores.append(total)
        actionability_scores.append(a)
        traceability_scores.append(t)
        guidance_scores.append(g)

    avg_score = sum(scores) / len(scores)

    distribution = {
        "high": len([s for s in scores if s >= 80]),
        "medium": len([s for s in scores if 60 <= s < 80]),
        "low": len([s for s in scores if s < 60]),
    }

    return {
        "total": len(lessons),
        "avg_score": round(avg_score, 2),
        "actionability_avg": round(
            sum(actionability_scores) / len(actionability_scores), 2
        ),
        "traceability_avg": round(
            sum(traceability_scores) / len(traceability_scores), 2
        ),
        "guidance_avg": round(sum(guidance_scores) / len(guidance_scores), 2),
        "score_distribution": distribution,
    }


def format_metrics(metrics: dict) -> str:
    lines = [
        f"Total lessons: {metrics['total']}",
        f"Average quality score: {metrics['avg_score']}",
        f"Actionability avg: {metrics['actionability_avg']}",
        f"Traceability avg: {metrics['traceability_avg']}",
        f"Guidance value avg: {metrics['guidance_avg']}",
        f"Distribution: {metrics['score_distribution']}",
    ]
    return "\n".join(lines)


def main():
    lessons_path = Path("context/current-learn.md")
    if len(sys.argv) > 1:
        lessons_path = Path(sys.argv[1])

    lessons = parse_lessons_file(lessons_path)
    metrics = calculate_quality_score(lessons)

    print(format_metrics(metrics))
    print(f"\nFinal score: {int(metrics['avg_score'])}")

    return 0 if metrics["avg_score"] >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())
