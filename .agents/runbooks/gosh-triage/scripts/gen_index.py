import argparse
import os
from pathlib import Path


SKIP_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg'}
SKIP_FILES = {
    'README.md',
    'index.yaml',
    'output.yaml',
    'diff.py',
    'generate_output.py',
    'generate_task.py',
    'gen_index.py',
    'gen_raw0_tail_task.py',
    '.DS_Store',
    '.gitkeep',
}
def capitalize_first_word(text: str) -> str:
    first = text.strip().split()[0]
    return first[0].upper() + first[1:].lower()


def compute_raw_target_dir(source_path: str, file_path: str) -> str:
    """Infer raw input target directory from project-relative source and file paths."""
    # 根据 raw 源目录结构推导目标目录。
    # 产品目录名会经过首词规范化：首字母大写，其余字母小写。
    # 例如 xAI → Xai，codex-cli → Codex-cli。
    # 目前仅支持一种已知 raw 源：
    #
    # raw/system-prompts-and-models-of-ai-tools
    #    目录结构：raw/system-prompts-and-models-of-ai-tools/{ProductName}/...
    #    特殊情况：Open Source prompts 下还有一层子目录
    #    用例：
    #      source_path='raw/system-prompts-and-models-of-ai-tools', file_path='raw/system-prompts-and-models-of-ai-tools/Windsurf/Agent/Prompt.md'
    #      → 'raw0/system-prompts/Windsurf'
    #
    #      source_path='raw/system-prompts-and-models-of-ai-tools', file_path='raw/system-prompts-and-models-of-ai-tools/Open Source prompts/codex-cli/Prompt.md'
    #      → 'raw0/system-prompts/Codex-cli'
    parts = file_path[len(source_path):].strip('/').split('/')

    if source_path == 'raw/system-prompts-and-models-of-ai-tools':
        first_level = parts[0] if parts else ''
        if first_level == 'Open Source prompts':
            product = parts[1] if len(parts) > 1 else ''
        else:
            product = first_level
        if not product:
            raise ValueError(f"cannot infer product from file_path: {file_path}")
        return f"raw0/system-prompts/{capitalize_first_word(product)}"

    raise ValueError(f"unsupported source_path: {source_path}")


def compute_target_file(source_path: str, file_path: str) -> str:
    # 根据源目录类型推导 index.yaml 中的 target_file。
    # target_dir 不单独推导，而是由 target_file 的父目录派生。
    #
    # 1. raw/... 原始材料
    #    target_file 指向 raw0 下的 Unclassified 工作文件。
    #    用例：
    #      source_path='raw/system-prompts-and-models-of-ai-tools', file_path='raw/system-prompts-and-models-of-ai-tools/Amp/Prompt.md'
    #      → 'raw0/system-prompts/Amp/Prompt-Unclassified.md'
    #
    # 2. raw0/... 已清理区材料
    #    target_file 原地不动。
    #    用例：
    #      source_path='raw0/system-prompts', file_path='raw0/system-prompts/Amp/Rules.md'
    #      → 'raw0/system-prompts/Amp/Rules.md'
    if source_path.startswith('raw/'):
        target_dir = compute_raw_target_dir(source_path, file_path)
        return (Path(target_dir) / f"{Path(file_path).stem}-Unclassified.md").as_posix()

    if source_path.startswith('raw0/'):
        return file_path

    raise ValueError(f"unsupported source_path: {source_path}")


def generate_index(source_path: str, project_root: Path) -> None:
    source_dir = project_root / source_path
    entries = []

    for root, dirs, files in os.walk(source_dir):
        dirs.sort()
        root_rel = Path(root).relative_to(project_root).as_posix()
        for filename in sorted(files):
            if filename in SKIP_FILES:
                continue
            ext = os.path.splitext(filename)[1].lower()
            if ext in SKIP_EXTS:
                continue

            rel_path = (Path(root_rel) / filename).as_posix()
            target_file = compute_target_file(source_path, rel_path)
            entries.append({
                'source': rel_path,
                'target_dir': Path(target_file).parent.as_posix(),
                'target_file': target_file,
            })

    output_path = source_dir / 'index.yaml'
    lines = [f'# {source_path}']
    for entry in entries:
        lines.append(f"- source: {entry['source']}")
        lines.append(f"  target_dir: {entry['target_dir']}")
        lines.append(f"  target_file: {entry['target_file']}")

    output_path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print(f"已生成 {output_path}，共 {len(entries)} 条映射")


def main() -> None:
    parser = argparse.ArgumentParser(description='gosh-triage index 生成工具')
    parser.add_argument(
        '--source',
        required=True,
        help='源目录，目前支持 raw/system-prompts-and-models-of-ai-tools 或 raw0/system-prompts',
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[4]

    print("=== 生成 index.yaml ===")
    print(f"  源目录: {args.source}\n")
    generate_index(args.source, project_root)


if __name__ == '__main__':
    main()
