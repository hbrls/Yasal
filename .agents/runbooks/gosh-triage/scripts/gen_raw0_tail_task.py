#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


CATEGORIES = [
    'Env',
    'Tools-Bash',
    'Expert',
    'Rules-Hostility',
    'Rules',
    'Intent',
    'Tools-TodoList',
    'Tools',
    'Emotional',
    'Collaborate',
    'Review',
    'Constraints-Confidential',
    'Constraints',
]

REFERENCE_FILES = {
    'Rules-Hostility': 'Rules-Hostility.md',
    'Collaborate': 'Collaborate.md',
    'Review': 'Review.md',
}

PLACEHOLDER_MARKERS = ('待定义', '待补充', '占位')


def project_root() -> Path:
    return Path(__file__).resolve().parents[4]


def slugify(text: str) -> str:
    text = text.replace(' ', '-').replace('/', '-')
    text = re.sub(r'[^\w\-]', '', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-').lower()


def read_index(index_path: Path) -> list[dict[str, str]]:
    """Parse the simple index format emitted by gen_index.py without PyYAML."""
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    last_line_number = 0

    for line_number, raw_line in enumerate(index_path.read_text(encoding='utf-8').splitlines(), 1):
        last_line_number = line_number
        line = raw_line.rstrip()
        if not line or line.lstrip().startswith('#'):
            continue

        source_match = re.fullmatch(r'- source:\s*(.+)', line)
        if source_match:
            if current is not None:
                validate_index_entry(current, index_path, line_number - 1)
                entries.append(current)
            current = {'source': source_match.group(1)}
            continue

        field_match = re.fullmatch(r'\s+(target_dir|target_file):\s*(.+)', line)
        if field_match and current is not None:
            current[field_match.group(1)] = field_match.group(2)
            continue

        raise ValueError(f'{index_path}:{line_number}: unsupported index syntax: {line}')

    if current is not None:
        validate_index_entry(current, index_path, last_line_number)
        entries.append(current)

    return entries


def validate_index_entry(entry: dict[str, str], index_path: Path, line_number: int) -> None:
    missing = {'source', 'target_dir', 'target_file'} - entry.keys()
    if missing:
        fields = ', '.join(sorted(missing))
        raise ValueError(f'{index_path}:{line_number}: missing fields: {fields}')


def reference_path(root: Path, category: str) -> Path:
    filename = REFERENCE_FILES.get(category)
    if filename is None:
        raise ValueError(f'category has no reference specification: {category}')
    return root / '.agents' / 'runbooks' / 'gosh-triage' / 'references' / filename


def validate_reference(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f'reference specification does not exist: {path}')

    content = path.read_text(encoding='utf-8')
    markers = [marker for marker in PLACEHOLDER_MARKERS if marker in content]
    if markers:
        found = ', '.join(markers)
        raise ValueError(f'reference specification is not ready ({found}): {path}')


def category_step(category: str) -> int:
    try:
        return CATEGORIES.index(category) + 1
    except ValueError as exc:
        choices = ', '.join(CATEGORIES)
        raise ValueError(f'unknown category {category!r}; expected one of: {choices}') from exc


def select_tail_candidates(
    entries: list[dict[str, str]],
    category: str,
    root: Path,
) -> list[dict[str, str]]:
    step = category_step(category)
    skipped_category_files = {f'{name}.md' for name in CATEGORIES[:step]}
    candidates = []

    for item in entries:
        source = item['source']
        source_rel = Path(source)
        target_dir_rel = Path(item['target_dir'])
        target_file_rel = Path(item['target_file'])

        if not source_rel.parts or source_rel.parts[0] != 'raw0':
            raise ValueError(f'raw0 tail index contains a non-raw0 source: {source}')
        if target_dir_rel != source_rel.parent or target_file_rel != source_rel:
            raise ValueError(f'raw0 index entry must map a source in place: {source}')
        if source_rel.name in skipped_category_files:
            continue

        source_path = root / source_rel
        if not source_path.is_file():
            raise FileNotFoundError(f'indexed source does not exist: {source}')
        if source_path.stat().st_size == 0:
            continue

        candidates.append({
            'source': source_rel.as_posix(),
            'target_file': (target_dir_rel / f'{category}.md').as_posix(),
        })

    candidates.sort(key=lambda item: item['source'])
    return candidates


def task_filename(source: str, step: int, category: str) -> str:
    slug = slugify(Path(source).with_suffix('').as_posix())
    return f'TASK-GOSH-TRIAGE-RAW0-TAIL-{slug}-E{step:02d}-{category}.md'


def build_prompt(task: dict[str, str], category: str, step: int) -> str:
    source = task['source']
    target_file = task['target_file']

    return f"""加载 `.agents/runbooks/gosh-triage/RUNBOOK.md` 并掌握工作流。
重点读取 `.agents/runbooks/gosh-triage/references/{category}.md`，以其中标准判断是否属于 {category}。

这是 raw0 尾部增量回溯任务。只执行步骤 {step}（{category}），不得执行其他分类步骤。

对源文件 `{source}` 逐句（或逐句组）做语义判断，抽取 {category} 内容到 `{target_file}`，并从源文件中删除对应内容。

若未抽出任何 {category} 内容：
- 不创建目标文件
- 不修改源文件

若抽出内容且目标文件已存在：
- 读取目标文件完整现有内容
- 在末尾追加 `---` 分隔行
- 追加 `## 来源：{source}` 和抽出内容
- 不得改动目标文件已有内容

若抽出内容且目标文件不存在：
- 创建目标文件
- 写入 `## 来源：{source}` 和抽出内容

当前任务完成后，删除当前任务文件并停止，不得继续处理其他任务。
"""


def ensure_no_foreign_tasks(context_dir: Path, expected: set[str]) -> None:
    if not context_dir.exists():
        return
    foreign = sorted(
        path.name
        for path in context_dir.glob('*.md')
        if path.name not in expected
    )
    if foreign:
        names = ', '.join(foreign)
        raise ValueError(f'.context contains tasks from another batch: {names}')


def generate(index_path: Path, category: str, rewrite: bool, root: Path) -> None:
    validate_reference(reference_path(root, category))
    entries = read_index(index_path)
    candidates = select_tail_candidates(entries, category, root)
    step = category_step(category)
    context_dir = root / '.context'
    task_specs = [
        {
            **candidate,
            'task_file': task_filename(candidate['source'], step, category),
        }
        for candidate in candidates
    ]

    task_files = [task['task_file'] for task in task_specs]
    if len(task_files) != len(set(task_files)):
        raise ValueError('task filename collision detected')
    ensure_no_foreign_tasks(context_dir, set(task_files))

    created = 0
    rewritten = 0
    skipped = 0
    context_dir.mkdir(parents=True, exist_ok=True)
    for task in task_specs:
        task_path = context_dir / task['task_file']
        content = f"# {task_path.stem}\n\n{build_prompt(task, category, step)}"
        if task_path.exists() and not rewrite:
            skipped += 1
            continue
        if task_path.exists():
            rewritten += 1
        else:
            created += 1
        task_path.write_text(content, encoding='utf-8')

    print('=== 生成 raw0 尾部回溯任务 ===')
    print(f'  类别:       {category}（步骤 {step}）')
    print(f'  索引:       {index_path}')
    print(f'  候选文件:   {len(task_specs)}')
    print(f'  新建任务:   {created}')
    print(f'  重写任务:   {rewritten}')
    print(f'  已有跳过:   {skipped}')


def main() -> None:
    parser = argparse.ArgumentParser(description='gosh-triage raw0 尾部回溯任务生成器')
    parser.add_argument('--index', required=True, help='raw0 index.yaml 路径')
    parser.add_argument('--category', required=True, help='新增类别名称，例如 Review')
    parser.add_argument('--rewrite', action='store_true', help='重写已存在的本批次任务文件')
    args = parser.parse_args()

    root = project_root()
    index_path = Path(args.index)
    if not index_path.is_absolute():
        index_path = root / index_path
    try:
        generate(index_path, args.category, args.rewrite, root)
    except (FileNotFoundError, ValueError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
