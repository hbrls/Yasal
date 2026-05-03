import os
import yaml
from pathlib import Path


def generate_mapping():
    base_path = Path(__file__).parent
    mappings = []
    
    vendor_override = {
        'Misc/Notion-AI.md': 'Notion',
        'Misc/copilot-in-microsoft-word.md': 'Microsoft',
        'Misc/meta-ai.md': 'Meta',
        'Misc/proton-lumo-ai.md': 'Proton',
        'Misc/brave-search.md': 'Brave',
        'Misc/Le-Chat.md': 'Mistral',
    }
    
    for root, dirs, files in os.walk(str(base_path)):
        for file in files:
            if file == 'README.md' or file == 'generate_output.py' or file == 'output.yaml':
                continue
            
            full_path = Path(root) / file
            rel_path = full_path.relative_to(base_path)
            
            parts = rel_path.parts
            if len(parts) < 1:
                continue
            
            vendor = parts[0]
            source = f"system_prompts_leaks/{rel_path}"
            
            rel_path_str = str(rel_path)
            if rel_path_str in vendor_override:
                vendor = vendor_override[rel_path_str]
            
            target_dir = f"system-prompts/{vendor}"
            
            if len(parts) == 1:
                target_file = file
            elif len(parts) == 2:
                target_file = parts[1]
            else:
                subdir_parts = parts[1:-1]
                filename = parts[-1]
                target_file = '-'.join(subdir_parts) + '-' + filename
            
            mappings.append({
                'source': source,
                'target_dir': target_dir,
                'target_file': target_file
            })
    
    mappings.sort(key=lambda x: (x['source']))
    
    return mappings


def main():
    mappings = generate_mapping()
    yaml_path = Path(__file__).parent / 'output.yaml'
    
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write('# system_prompts_leaks\n')
        yaml.dump(mappings, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
    
    print(f"生成映射数: {len(mappings)}")
    print(f"输出文件: {yaml_path}")


if __name__ == '__main__':
    main()