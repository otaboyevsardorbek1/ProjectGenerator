import json
from pathlib import Path
import sys

# YAML support
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

# --- SAMPLE TREE STRUCTURE AS STRING ---
SAMPLE_TREE = """construction_factory_bot/
├── 📁 alembic/                    # Database migratsiyalari
│   ├── versions/                  # Migratsiya fayllari
│   └── env.py                     # Migratsiya muhiti
├── 📁 backups/                    # Backup fayllari
├── 📁 database/                   # Database modullari
│   ├── __init__.py
│   ├── models.py                  # SQLAlchemy modellari
│   ├── crud.py                    # CRUD operatsiyalari
│   ├── session.py                 # Database sessiyasi
│   └── alembic_versions.py        # Migratsiya versiyalari
├── 📁 handlers/                   # Bot handlerlari
│   ├── __init__.py
│   ├── start.py                   # Start handler
│   ├── warehouse.py               # Ombor handler
│   ├── production.py              # Ishlab chiqarish handler
│   ├── reports.py                 # Hisobotlar handler
│   ├── admin.py                   # Admin paneli
│   ├── employees.py               # Xodimlar handler
│   ├── notifications.py           # Bildirishnomalar handler
│   └── sales.py                   # Sotuvlar handler
├── 📁 keyboards/                  # Klaviatura modullari
│   ├── __init__.py
│   ├── main_menu.py               # Asosiy menyu
│   ├── admin_menu.py              # Admin menyusi
│   └── inline_keyboards.py        # Inline tugmalar
├── 📁 logs/                       # Log fayllari
├── 📁 reports/                    # Hisobotlar
│   ├── excel/                     # Excel hisobotlar
│   └── charts/                    # Grafiklar
├── 📁 static/                     # Statik fayllar
│   └── images/                    # Rasmlar
├── 📁 utils/                      # Yordamchi funksiyalar
│   ├── __init__.py
│   ├── formulas.py                # Mahsulot formulalari
│   ├── calculations.py            # Hisob-kitoblar
│   ├── excel_reports.py           # Excel hisobotlar
│   ├── charts.py                  # Grafik yaratish
│   ├── notifications.py           # Push bildirishnomalar
│   └── helpers.py                 # Yordamchi funksiyalar
├── .env                           # Konfiguratsiya (shaxsiy)
├── .env.example                   # Konfiguratsiya namunasi
├── .gitignore                     # Git ignore
├── alembic.ini                     # Alembic konfiguratsiyasi
├── config.py                       # Asosiy konfiguratsiya
├── main.py                         # Asosiy fayl
├── README.md                       # Loyiha haqida ma'lumot
└── requirements.txt                # Kutubxonalar ro'yxati
"""

# --- PARSE TREE STRING TO DICT ---
def parse_tree(tree_str: str) -> dict:
    structure = {}
    stack = []
    for line in tree_str.splitlines():
        line = line.rstrip()
        if not line.strip():
            continue
        if "#" in line:
            line_part, comment = line.split("#", 1)
            comment = comment.strip()
        else:
            line_part = line
            comment = ""
        name = line_part.replace("├──", "").replace("└──", "").replace("│", "").replace("📁", "").strip()
        if not name:
            continue
        level = line.count("│")
        while len(stack) > level:
            stack.pop()
        if name.endswith("/"):
            stack.append(name.rstrip("/"))
        else:
            d = structure
            for p in stack:
                d = d.setdefault(p, {})
            d[name] = ""
            if comment:
                d["_comment"] = comment
    return structure

# --- CREATE FILES/FOLDERS WITH COMMENTS ---
def create_structure(root: str, structure: dict):
    root_path = Path(root)
    root_path.mkdir(parents=True, exist_ok=True)

    def recurse(path: Path, sub: dict):
        for name, content in sub.items():
            if name == "_comment":
                continue
            full_path = path / name
            if isinstance(content, dict):
                full_path.mkdir(parents=True, exist_ok=True)
                recurse(full_path, content)
            else:
                full_path.parent.mkdir(parents=True, exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    comment = sub.get("_comment", "")
                    if comment:
                        f.write(f"# {comment}\n")
                    if content:
                        f.write(content)
    recurse(root_path, structure)
    print(f"\n[✓] Loyiha '{root}' papkada yaratildi!")

# --- CONVERT DICT TO TREE STRING ---
def dict_to_tree(structure: dict, prefix="") -> str:
    lines = []
    items = list(structure.items())
    for i, (name, content) in enumerate(items):
        if name == "_comment":
            continue
        connector = "└── " if i == len(items) - 1 else "├── "
        comment = f" # {content}" if isinstance(content, str) and content else ""
        lines.append(f"{prefix}{connector}{name}{comment}")
        if isinstance(content, dict):
            extension = "    " if i == len(items) - 1 else "│   "
            lines.append(dict_to_tree(content, prefix + extension))
    return "\n".join(lines)

# --- WRITE SAMPLE FILES AUTOMATICALLY ---
def write_all_samples():
    structure = parse_tree(SAMPLE_TREE)
    # JSON
    with open("sample.json", "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    print("[✓] sample.json yaratildi.")
    # YAML
    if HAS_YAML:
        with open("sample.yaml", "w", encoding="utf-8") as f:
            yaml.dump(structure, f, sort_keys=False, allow_unicode=True)
        print("[✓] sample.yaml yaratildi.")
    # TREE
    with open("sample.txt", "w", encoding="utf-8") as f:
        f.write(SAMPLE_TREE)
    print("[✓] sample.txt yaratildi.")

# --- MAIN ---
def main():
    print("=== 1-CLICK AUTO PROJECT GENERATOR ===")
    root = input("Root papka nomini kiriting (default: project_root): ").strip() or "project_root"
    structure = parse_tree(SAMPLE_TREE)

    # Fayllarni avtomatik yaratish
    write_all_samples()

    # Loyihani yaratish
    create_structure(root, structure)

    # TREE ko‘rinishi
    print("\n=== TREE Ko‘rinishi ===")
    print(dict_to_tree(structure))

    print("\n[✓] Tayyor! Loyiha muvaffaqiyatli yaratildi. Foydalanuvchi hech narsani qo‘shimcha kiritishga hojat yo‘q.")

if __name__ == "__main__":
    main()
