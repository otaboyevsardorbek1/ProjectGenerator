# UNIVERSAL PROJECT GENERATOR  
(C# WinForms + Python CLI Version)

## 📌 Project Purpose
The Universal Project Generator is an educational tool designed for students to learn how software projects are automatically created based on predefined structural templates. The generator supports three structure formats:

- **JSON** structure file  
- **YAML** structure file  
- **TREE** text structure  

Users can load any structure, modify it, specify a root folder name, and generate a complete project automatically.

---

## 🚀 Features
- Load and parse **JSON**, **YAML**, and **TREE** structure files  
- Automatically generate project folders and files  
- Display the final generated project in TREE format inside the GUI  
- Create and export sample templates (JSON / YAML / TREE)  
- Windows Forms GUI (C#)  
- Command-line version (Python CLI)  

---

## 🧩 How the Application Works
1. Run the application.  
2. Choose the structure format: **JSON**, **YAML**, or **TREE**.  
3. Load or edit the structure file.  
4. Enter the project root folder name (default: `telegram_shop_bot`).  
5. Click **Generate Project**.  
6. The program will automatically create all folders and files.  
7. Generated structure is shown as a TREE inside the GUI.

---

## 📝 Tasks for Students
- Learn and modify JSON / YAML / TREE file structures  
- Use the application to generate real project folders  
- Understand project architecture through the TREE view  
- Extend the generator with new features  
- Add new file types, metadata, or custom templates  

---

## 🛠 Technologies Used

### C# Version
- C# 10  
- .NET 6 / .NET Framework  
- WinForms  
- YamlDotNet  
- System.Text.Json  

### Python CLI Version
- Python 3.10+  
- pyyaml  
- json  
- os, pathlib  

---

## 📦 Installation (C# WinForms)
1. Open the project in **Visual Studio**  
2. Install the required NuGet package:

```
Install-Package YamlDotNet
```

---

# 📂 Sample Templates

## 🔶 JSON Template (`structure.json`)
```json
{
  "project_name": "telegram_shop_bot",
  "structure": {
    "src": {
      "bot": {
        "handlers": {
          "start_handler.py": "",
          "order_handler.py": ""
        },
        "utils": {
          "helpers.py": ""
        },
        "main.py": ""
      }
    },
    "config": {
      "settings.json": "{}"
    },
    "README.md": "# Telegram Shop Bot"
  }
}
```

---

## 🔷 YAML Template (`structure.yaml`)
```yaml
project_name: telegram_shop_bot
structure:
  src:
    bot:
      handlers:
        start_handler.py: ""
        order_handler.py: ""
      utils:
        helpers.py: ""
      main.py: ""
  config:
    settings.json: "{}"
  README.md: "# Telegram Shop Bot"
```

---

## 🌳 TREE Template (`structure.tree`)
```
telegram_shop_bot
├── src
│   └── bot
│       ├── handlers
│       │   ├── start_handler.py
│       │   └── order_handler.py
│       ├── utils
│       │   └── helpers.py
│       └── main.py
├── config
│   └── settings.json
└── README.md
```

---

# 🐍 Python CLI Version

```python
import os, json, yaml
from pathlib import Path

def create_structure(base, structure):
    for name, content in structure.items():
        path = Path(base) / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_structure(path, content)
        else:
            path.write_text(content or "")

def load_structure(file):
    if file.endswith(".json"):
        return json.load(open(file))
    if file.endswith(".yaml") or file.endswith(".yml"):
        return yaml.safe_load(open(file))
    raise ValueError("Unsupported format")

if __name__ == "__main__":
    file = input("Structure file: ")
    root = input("Root folder name: ")

    data = load_structure(file)
    base = data.get("project_name", root)

    create_structure(base, data["structure"])
    print("Project generated:", base)
```

---

# 👨‍💻 Author

- **Last Name:** Otaboyev  
- **First Name:** Sardorbek  
- **University:** Namangan State University  
- **Group:** K.KID-AU-23  
- **Telegram:** https://t.me/prodevuzoff
