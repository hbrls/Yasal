import argparse
import re
from pathlib import Path

import yaml


STEPS = [
    # {'num': 0, 'name': 'Init', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 1, 'name': 'Env', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 2, 'name': 'Tools-Bash', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 3, 'name': 'Expert', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 4, 'name': 'Rules-Hostility', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 5, 'name': 'Rules', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 6, 'name': 'Intent', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 7, 'name': 'Tools-TodoList', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 8, 'name': 'Tools', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 9, 'name': 'Emotional', 'from': '{source}', 'to': '{target_file}'},
    {'num': 10, 'name': 'Collaborate', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 11, 'name': 'Constraints-Confidential', 'from': '{source}', 'to': '{target_file}'},
    # {'num': 12, 'name': 'Constraints', 'from': '{source}', 'to': '{target_file}'},
]


SKIP_FILES = {
    'Env.md',
    'Tools-Bash.md',
    'Expert.md',
    'Rules-Hostility.md',
    'Rules.md',
    'Intent.md',
    'Tools-TodoList.md',
    'Tools.md',
    'Emotional.md',
}


def slugify(text: str) -> str:
    text = text.replace(' ', '-').replace('/', '-')
    text = re.sub(r'[^\w\-]', '', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-').lower()


def build_prompt(step: dict, source: str, target_file: str) -> str:
    from_path = step['from'].format(source=source, target_file=target_file)
    to_path = step['to'].format(source=source, target_file=target_file)

    header = f"对源文件 `{from_path}` 执行临时 gosh-triage 分流任务："
    detail = f"""从 `{from_path}` 中逐句语义分析，抽取 Collaborate 相关内容到 `{to_path}`。

抽走后，从原文件 `{from_path}` 中删除对应语句或句组。

若未抽出任何 Collaborate 内容：
- 不创建目标文件
- 不修改原文件

若抽出内容且目标文件已存在：
- 读取目标文件完整现有内容
- 在末尾追加 `---` 分隔行
- 追加 `## 来源：{from_path}` 和抽出内容

若抽出内容且目标文件不存在：
- 创建目标文件
- 写入 `## 来源：{from_path}` 和抽出内容"""

    return f"""加载 `.agents/runbooks/gosh-triage/RUNBOOK.md` 并掌握工作流。
重点读取 `.agents/runbooks/gosh-triage/references/Collaborate.md`，以其中标准判断是否属于 Collaborate。

{header}

你现在负责步骤 {step['num']}（{step['name']}）。

具体操作：{detail}"""


def collaborate_target(item: dict) -> str:
    target_dir = item.get('target_dir')
    if target_dir:
        return str(Path(target_dir) / 'Collaborate.md')
    return item['target_file']


def generate_tasks(index_path: Path, context_dir: Path) -> None:
    data = yaml.safe_load(index_path.read_text(encoding='utf-8')) or []
    tasks_created = []
    tasks_skipped = []

    for item in data:
        source = item['source']
        if Path(source).name in SKIP_FILES:
            tasks_skipped.append(source)
            continue

        target_file = collaborate_target(item)
        task_stem = slugify(Path(source).with_suffix('').as_posix())

        for step in STEPS:
            step_tag = f"E{step['num']:02d}-{step['name']}"
            task_filename = f"TASK-GOSH-TRIAGE-{task_stem}-{step_tag}.md"
            task_file = context_dir / task_filename

            if task_file.exists():
                continue

            prompt = build_prompt(step, source, target_file)
            content = f"# TASK-GOSH-TRIAGE-{task_stem}-{step_tag}\n\n{prompt}\n"
            task_file.parent.mkdir(parents=True, exist_ok=True)
            task_file.write_text(content, encoding='utf-8')
            tasks_created.append(str(task_file.relative_to(context_dir.parent)))

    print(f"检查映射数: {len(data)}")
    print(f"跳过文件数: {len(tasks_skipped)}")
    print(f"创建任务数: {len(tasks_created)}")

    if tasks_skipped:
        print("\n已跳过源文件:")
        for source in tasks_skipped:
            print(f"  - {source}")

    if tasks_created:
        print("\n已创建任务文件:")
        for task in tasks_created:
            print(f"  - {task}")


def main() -> None:
    parser = argparse.ArgumentParser(description='gosh-triage Collaborate 任务生成工具')
    parser.add_argument('--index', help='索引文件路径，默认读取 --source/index.yaml')
    parser.add_argument('--source', default='lessons', help='索引所在源目录')
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[4]
    index_path = Path(args.index) if args.index else project_root / args.source / 'index.yaml'
    if not index_path.is_absolute():
        index_path = project_root / index_path

    context_dir = project_root / '.context'

    print("=== 生成任务文件 ===")
    print(f"  索引文件: {index_path}\n")
    generate_tasks(index_path, context_dir)


if __name__ == '__main__':
    main()
