#!/usr/bin/env python3
# create_zip_package_ready.py

import zipfile
from pathlib import Path

# --- UNIVERSAL PROJECT GENERATOR KODI --- #
universal_generator_code = """\
#!/usr/bin/env python3
# universal_project_generator.py

import json
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

SAMPLES = {
    "json": {
        "telegram_shop_bot/bot.py": "",
        "telegram_shop_bot/config.py": "",
        "telegram_shop_bot/database.py": "",
        "telegram_shop_bot/handlers/__init__.py": "",
        "telegram_shop_bot/handlers/admin.py": "",
        "telegram_shop_bot/handlers/user.py": ""
    },
    "yaml": {
        "telegram_shop_bot/bot.py": "",
        "telegram_shop_bot/config.py": "",
        "telegram_shop_bot/database.py": "",
        "telegram_shop_bot/handlers/__init__.py": "",
        "telegram_shop_bot/handlers/admin.py": "",
        "telegram_shop_bot/handlers/user.py": ""
    },
    "tree": \"\"\"telegram_shop_bot/
├── bot.py
├── config.py
├── database.py
├── requirements.txt
├── .env.example
├── database.sql
├── handlers/
│   ├── __init__.py
│   ├── admin.py
│   ├── user.py
│   ├── products.py
│   ├── categories.py
│   └── verification.py
├── keyboards/
│   ├── __init__.py
│   ├── inline.py
│   ├── reply.py
│   └── verification.py
└── utils/
    ├── __init__.py
    ├── helpers.py
    └── whatsapp_verification.py
\"\"\"
}

def create_structure(root: str, structure: dict):
    root_path = Path(root)
    root_path.mkdir(parents=True, exist_ok=True)
    for path_str, content in structure.items():
        full_path = root_path / path_str
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
    print(f"\\nTREE asosida loyixa '{root}' papkada yaratildi!")

def parse_tree_structure(tree_str: str) -> dict:
    lines = tree_str.splitlines()
    structure = {}
    stack = []
    for line in lines:
        stripped = line.rstrip()
        if not stripped:
            continue
        name = stripped.replace("├──", "").replace("└──", "").replace("│", "").strip()
        if not name:
            continue
        level = line.count("│")
        while len(stack) > level:
            stack.pop()
        if name.endswith("/"):
            stack.append(name.rstrip("/"))
        else:
            path = "/".join(stack + [name]) if stack else name
            structure[path] = ""
    return structure

def convert_dict_to_tree(structure: dict) -> str:
    from collections import defaultdict
    tree = defaultdict(list)
    for path in structure:
        parts = path.split("/")
        for i in range(1, len(parts)+1):
            tree["/".join(parts[:i-1])].append(parts[i-1])
    def build_tree(path="", prefix=""):
        lines = []
        children = tree.get(path, [])
        for i, child in enumerate(children):
            connector = "└── " if i == len(children)-1 else "├── "
            full_path = f"{path}/{child}" if path else child
            if full_path in structure and structure[full_path] == "":
                lines.append(f"{prefix}{connector}{child}")
            else:
                lines.append(f"{prefix}{connector}{child}/")
            if tree.get(full_path):
                extension = "    " if i == len(children)-1 else "│   "
                lines.extend(build_tree(full_path, prefix + extension))
        return lines
    return "\\n".join(build_tree())

def write_sample_file(format_type: str) -> str:
    if format_type == "1":
        file_name = "sample.json"
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(SAMPLES["json"], f, indent=2)
    elif format_type == "2":
        file_name = "sample.yaml"
        with open(file_name, "w", encoding="utf-8") as f:
            yaml.dump(SAMPLES["yaml"], f, sort_keys=False)
    elif format_type == "3":
        file_name = "sample.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(SAMPLES["tree"])
    else:
        raise ValueError("Noto'g'ri tanlov!")
    print(f"{file_name} namuna fayli yaratildi.")
    return file_name

def main():
    print("=== UNIVERSAL TREE Loyiha Generator ===")
    print("1 - JSON asosida")
    print("2 - YAML asosida")
    print("3 - TREE matn asosida")
    choice = input("Tanlovni kiriting (1/2/3): ").strip()
    sample_file = write_sample_file(choice)
    print(f"\\nNamuna fayl yaratildi: {sample_file}")
    print("Iltimos, uni o'zgartiring va tayyor fayl yo'lini kiriting.")
    file_path = input("Fayl yo'lini kiriting: ").strip()
    if not Path(file_path).exists():
        print("Fayl topilmadi!")
        return
    if choice == "1":
        with open(file_path, "r", encoding="utf-8") as f:
            structure = json.load(f)
    elif choice == "2":
        if not HAS_YAML:
            raise ImportError("PyYAML o'rnatilmagan. `pip install pyyaml`")
        with open(file_path, "r", encoding="utf-8") as f:
            structure = yaml.safe_load(f)
    elif choice == "3":
        with open(file_path, "r", encoding="utf-8") as f:
            structure = parse_tree_structure(f.read())
    else:
        print("Noto'g'ri tanlov!")
        return
    root = input("Root papka nomini kiriting (default: telegram_shop_bot): ").strip() or "telegram_shop_bot"
    create_structure(root, structure)
    show_tree = input("TREE ko‘rinishini ko‘rishni xohlaysizmi? (ha/yo‘q): ").strip().lower()
    if show_tree in ["ha", "h", "yes", "y"]:
        print("\\n=== TREE Ko‘rinishi ===")
        print(convert_dict_to_tree(structure))
    print("\\n=== Tayyor! Loyiha muvaffaqiyatli yaratildi. ===")

if __name__ == "__main__":
    main()
"""

readme_text = """\
=== UNIVERSAL TREE Loyiha Generator ===

Qanday ishlatish:

1. ZIPni oching va ichidagi 'universal_project_generator.py' ni ishlating.
2. Python 3 ishga tushiring:
   python universal_project_generator.py
3. Tanlovni kiriting:
   1 - JSON asosida
   2 - YAML asosida
   3 - TREE matn asosida
4. Namuna fayl yaratildi, uni tahrir qiling va yo‘lini kiriting.
5. Root papka nomini kiriting (default: telegram_shop_bot)
6. Loyiha TREE joylashuviga mos yaratildi va konsolda ko‘rsatildi.
"""

zip_filename = "universal_project_generator.zip"

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr("universal_project_generator.py", universal_generator_code)
    zf.writestr("README.txt", readme_text)

print(f"ZIP paket yaratildi: {Path(zip_filename).resolve()}")
