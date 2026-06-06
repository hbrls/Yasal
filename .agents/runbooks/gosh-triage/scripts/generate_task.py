import os
import yaml
import re
import argparse
from pathlib import Path


STEPS = [
    # {'num': 0, 'name': 'Init',     'from': 'raw/{source}',                         'to': 'raw0/{first_level_dir}/{slug}-Unclassified.md'},
    # {'num': 1, 'name': 'Env',      'from': '{slug}-Unclassified.md',               'to': 'raw0/{first_level_dir}/Env.md'},
    # {'num': 2, 'name': 'Tools-Bash','from': '{slug}-Unclassified.md',              'to': 'raw0/{first_level_dir}/Tools-Bash.md'},
    # {'num': 3, 'name': 'Expert',   'from': '{slug}-Unclassified.md',               'to': 'raw0/{first_level_dir}/Expert.md'},
    {'num': 4, 'name': 'Rules-Hostility','from': '{source}',                       'to': '{target_file}'},
    # {'num': 5, 'name': 'Rules',    'from': '{slug}-Unclassified.md',               'to': 'raw0/{first_level_dir}/Rules.md'},
    # {'num': 6, 'name': 'Intent',   'from': '{slug}-Unclassified.md',               'to': 'raw0/{first_level_dir}/Intent.md'},
    # {'num': 7, 'name': 'Tools-TodoList','from': '{slug}-Unclassified.md',          'to': 'raw0/{first_level_dir}/Tools-TodoList.md'},
    # {'num': 8, 'name': 'Tools',    'from': '{slug}-Unclassified.md',               'to': 'raw0/{first_level_dir}/Tools.md'},
    # {'num': 9, 'name': 'Emotional','from': '{slug}-Unclassified.md',               'to': 'raw0/{first_level_dir}/Emotional.md'},
    # {'num': 10,'name': 'Constraints-Confidential','from': '{slug}-Unclassified.md','to': 'raw0/{first_level_dir}/Constraints-Confidential.md'},
    # {'num': 11,'name': 'Constraints','from': '{slug}-Unclassified.md',             'to': 'raw0/{first_level_dir}/Constraints.md'},
]

STEP_OVERVIEW = """临时任务：仅执行步骤 4：Rules-Hostility → Rules-Hostility-*.md"""


def build_prompt(step: dict, source: str, target_file: str) -> str:
    from_path = step['from'].format(source=source, target_file=target_file)
    to_path = step['to'].format(source=source, target_file=target_file)

    header = f"对 lessons 文件 `{from_path}` 执行临时 gosh-triage 分流任务："
    detail = f"从 `{from_path}` 中逐句语义分析，抽取 Rules-Hostility 相关内容到 `{to_path}`；抽走后从原文件 `{from_path}` 中删除对应语句或句组。若未抽出任何 Rules-Hostility 内容，不创建目标文件，也不修改原文件。若抽出内容且目标文件已存在，则读取目标文件完整现有内容，在末尾追加 `---` 分隔行、`## 来源：{from_path}` 和抽出内容；若目标文件不存在，则创建后写入 `## 来源：{from_path}` 和抽出内容。"

    return f"""加载 `.agents/runbooks/gosh-triage/RUNBOOK.md` 并掌握工作流。
重点读取 `.agents/runbooks/gosh-triage/references/Rules-Hostility.md`，以其中标准判断是否属于 Rules-Hostility。

{header}

{STEP_OVERVIEW}

你现在负责步骤 {step['num']}（{step['name']}）。

具体操作：{detail}"""


SKIP_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}
SKIP_FILES = {'README.md', 'output.yaml', 'diff.py', 'generate_output.py', 'generate_task.py', '.gitkeep'}
SKIP_PREFIXES = ('Rules-Hostility',)
KNOWN_EXTS = {'.txt', '.json', '.yaml', '.yml', '.md', '.py', '.xml', '.html', '.csv', '.toml', '.sh', '.bash', '.cfg', '.ini', '.log', '.tsv', '.rst', '.tex'}


def strip_ext(filename: str) -> str:
    stem, ext = os.path.splitext(filename)
    if ext.lower() in KNOWN_EXTS:
        return stem
    return filename


def capitalize_first_word(text: str) -> str:
    first = text.strip().split()[0]
    return first[0].upper() + first[1:].lower()


def compute_target_dir(base_name: str, rel_path: str, fallback: str) -> str:
    parts = rel_path.split('/')
    if base_name == 'system-prompts-and-models-of-ai-tools':
        second_level = parts[1] if len(parts) > 1 else ''
        if second_level == 'Open Source prompts':
            third_level = parts[2] if len(parts) > 2 else ''
            name = capitalize_first_word(third_level)
        else:
            name = capitalize_first_word(second_level)
        return f'system-prompts/{name}'
    elif base_name == '<TODO>':
        return fallback
    elif base_name == '<TODO>':
        return fallback
    return fallback


def slugify(text: str) -> str:
    text = text.replace(' ', '-').replace('/', '-')
    text = re.sub(r'[^\w\-]', '', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-').lower()


def compute_unclassified_info(source: str, target_dir: str) -> tuple:
    first_level_dir = target_dir.split('/')[0]
    parts = source.split('/')
    intermediate_dirs = parts[1:-1]
    filename_stem = strip_ext(parts[-1])
    slug_parts = [slugify(p) for p in intermediate_dirs] + [slugify(filename_stem)]
    slug = '-'.join(slug_parts)
    slug = re.sub(r'-+', '-', slug)
    unclassified_filename = f"{slug}-Unclassified.md"
    return first_level_dir, slug, unclassified_filename


def compute_rules_hostility_target(rel_path: str) -> str:
    path = Path(rel_path)
    stem = path.stem
    if stem == 'Emotional':
        target_stem = 'Rules-Hostility'
    elif stem.startswith('Emotional-'):
        target_stem = f"Rules-Hostility-{stem[len('Emotional-'):]}"
    elif stem.startswith('Emotional '):
        target_stem = f"Rules-Hostility {stem[len('Emotional '):]}"
    else:
        target_stem = f"Rules-Hostility-{stem}"
    return path.with_name(f"{target_stem}.md").as_posix()


def get_actual_files(base_path: str) -> set:
    actual_files = set()
    for root, dirs, files in os.walk(base_path, topdown=False):
        for file in files:
            if file in SKIP_FILES:
                continue
            ext = os.path.splitext(file)[1].lower()
            if ext in SKIP_EXTS:
                continue
            rel_path = os.path.relpath(os.path.join(root, file), base_path)
            actual_files.add(rel_path)
    return actual_files


def get_mapped_files(yaml_path: str, source_prefix: str) -> set:
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    mappings = set()
    for item in data:
        source = item['source'].replace(source_prefix, '')
        mappings.add(source)

    return mappings, data


def generate_yaml(base_path: str, project_root: Path, target_first_level: str):
    base_name = os.path.basename(str(base_path))
    entries = []
    for root, dirs, files in os.walk(base_path):
        dirs.sort()
        for f in sorted(files):
            if f in SKIP_FILES:
                continue
            if f.startswith(SKIP_PREFIXES):
                continue
            ext = os.path.splitext(f)[1].lower()
            if ext in SKIP_EXTS:
                continue
            rel = os.path.relpath(os.path.join(root, f), str(project_root))
            entries.append({
                'source': rel,
                'target_dir': 'lessons',
                'target_file': compute_rules_hostility_target(rel)
            })

    output_path = Path(base_path) / 'output.yaml'
    lines = [f'# {base_name}']
    for e in entries:
        lines.append(f"- source: {e['source']}")
        lines.append(f"  target_dir: {e['target_dir']}")
        lines.append(f"  target_file: {e['target_file']}")

    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"已生成 {output_path}，共 {len(entries)} 条映射")


def check_diff(base_path: str, yaml_path: str, source_prefix: str):
    actual_files = get_actual_files(base_path)
    mapped_files, _ = get_mapped_files(yaml_path, source_prefix)

    only_in_actual = actual_files - mapped_files
    only_in_mapped = mapped_files - actual_files

    print(f"实际文件数: {len(actual_files)}")
    print(f"映射文件数: {len(mapped_files)}")
    print()

    if only_in_actual:
        print(f"仅在目录中存在，映射缺失 ({len(only_in_actual)}):")
        for f in sorted(only_in_actual):
            print(f"  - {f}")
        print()

    if only_in_mapped:
        print(f"仅在映射中存在，目录缺失 ({len(only_in_mapped)}):")
        for f in sorted(only_in_mapped):
            print(f"  - {f}")
        print()

    return len(only_in_actual) == 0 and len(only_in_mapped) == 0


def generate_tasks(yaml_path: str, context_dir: Path, raw0_dir: Path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    tasks_created = []

    for item in data:
        source = item['source']
        target_file = item['target_file']

        task_stem = slugify(Path(target_file).stem)

        for step in STEPS:
            step_tag = f"E{step['num']:02d}-{step['name']}"
            task_filename = f"TASK-GOSH-TRIAGE-{task_stem}-{step_tag}.md"
            task_file = context_dir / task_filename

            if task_file.exists():
                continue

            prompt = build_prompt(step, source, target_file)
            content = f"# TASK-GOSH-TRIAGE-{task_stem}-{step_tag}\n\n{prompt}\n"
            task_file.parent.mkdir(parents=True, exist_ok=True)
            task_file.write_text(content)
            tasks_created.append(str(task_file.relative_to(context_dir.parent)))

    print(f"检查映射数: {len(data)}")
    print(f"创建任务数: {len(tasks_created)}")

    if tasks_created:
        print("\n已创建任务文件:")
        for t in tasks_created:
            print(f"  - {t}")


def main():
    parser = argparse.ArgumentParser(description='gosh-triage 生成工具')
    sub = parser.add_subparsers(dest='command', required=True)

    p_output = sub.add_parser('gen-output', help='临时：从 lessons 目录扫描生成 output.yaml')
    p_output.add_argument('--source', default='lessons', help='临时忽略，固定扫描 lessons')
    p_output.add_argument('--target', default='lessons', help='临时忽略，固定输出到 lessons')

    p_task = sub.add_parser('gen-task', help='临时：从 lessons/output.yaml 生成 Rules-Hostility 任务文件')
    p_task.add_argument('--source', default='lessons', help='临时忽略，固定读取 lessons/output.yaml')
    p_task.add_argument('--target', default='lessons', help='临时忽略，固定目标为 lessons')

    args = parser.parse_args()
    project_root = Path(__file__).parent.parent

    if args.command == 'gen-output':
        project_root = Path(__file__).resolve().parents[4]
        source_dir = project_root / 'lessons'
        target_dir = 'lessons'
        first_level = Path(target_dir).name
        scan_root = project_root
        print(f"=== 生成 output.yaml ===")
        print(f"  源目录: {source_dir}")
        print(f"  目标:   {target_dir}\n")
        generate_yaml(str(source_dir), scan_root, first_level)

    elif args.command == 'gen-task':
        project_root = Path(__file__).resolve().parents[4]
        yaml_path = project_root / 'lessons' / 'output.yaml'
        target_first_level = 'lessons'
        context_dir = project_root / '.context'
        raw0_dir = project_root / 'lessons'
        print(f"=== 生成任务文件 ===")
        print(f"  映射文件: {yaml_path}")
        print(f"  目标:     {target_first_level}\n")
        generate_tasks(str(yaml_path), context_dir, raw0_dir)


if __name__ == '__main__':
    main()
