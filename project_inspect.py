import os
import sys

# Directories and files to skip
IGNORE_DIRS = {'.git', '__pycache__', 'venv', '.venv', 'env', '.pytest_cache', 'node_modules', '.idea', '.vscode'}
IGNORE_FILES = {'.env', '*.pyc', '.DS_Store'}

def print_tree(startpath, max_depth=3):
    print("=" * 60)
    print("📁 NOVAMIND-AI DIRECTORY STRUCTURE")
    print("=" * 60)
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        depth = root.replace(startpath, '').count(os.sep)
        if depth > max_depth:
            continue
        indent = '  ' * depth
        folder_name = os.path.basename(root) or 'NovaMind-AI (root)'
        print(f"{indent}📂 {folder_name}/")
        sub_indent = '  ' * (depth + 1)
        for f in files:
            if not any(f.endswith(ext.replace('*', '')) for ext in IGNORE_FILES if '*' in ext) and f not in IGNORE_FILES:
                print(f"{sub_indent}📄 {f}")

def inspect_key_files():
    print("\n" + "=" * 60)
    print("🔍 CORE SERVICES & AGENTS SUMMARY")
    print("=" * 60)
    
    target_dirs = ['services', 'agents', 'database', 'pages']
    for tdir in target_dirs:
        if os.path.exists(tdir):
            print(f"\n--- Checking [{tdir}/] ---")
            for root, _, files in os.walk(tdir):
                for f in sorted(files):
                    if f.endswith('.py') and f != '__init__.py':
                        filepath = os.path.join(root, f)
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                                lines = file.readlines()
                                classes = [l.strip() for l in lines if l.startswith('class ')]
                                defs = [l.strip() for l in lines if l.startswith('def ') or l.strip().startswith('def ')]
                                print(f"\n📄 {filepath} ({len(lines)} lines)")
                                if classes:
                                    print(f"   Classes : {', '.join([c.split('(')[0].replace('class ', '').replace(':', '') for c in classes])}")
                                if defs:
                                    methods = [d.split('(')[0].replace('def ', '') for d in defs[:6]]
                                    print(f"   Functions/Methods (first 6): {', '.join(methods)}")
                        except Exception as e:
                            print(f"   ⚠️ Could not read {filepath}: {e}")

def inspect_environment():
    print("\n" + "=" * 60)
    print("⚙️ ENVIRONMENT & PACKAGES")
    print("=" * 60)
    print(f"Python Version : {sys.version.split()[0]}")
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        print(f"\n📦 Found requirements.txt:")
        with open(req_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    print(f"   - {line}")
    else:
        print("⚠️ No requirements.txt found in root.")

if __name__ == "__main__":
    current_dir = os.getcwd()
    print_tree(current_dir)
    inspect_key_files()
    inspect_environment()
    print("\n" + "=" * 60)
    print("✅ INSPECTION COMPLETE")
    print("=" * 60)