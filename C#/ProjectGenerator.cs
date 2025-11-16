using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using YamlDotNet.Serialization;

namespace WinFormsProjectGenerator
{
    public class ProjectGenerator
    {
        public string RootFolder { get; set; } = "new app";
        public Dictionary<string, string> Structure { get; private set; } = new Dictionary<string, string>();

        // Namuna fayllar
        public static readonly Dictionary<string, Dictionary<string, string>> SAMPLES = new()
        {
            ["json"] = new Dictionary<string, string>
            {
                ["telegram_shop_bot/bot.py"] = "",
                ["telegram_shop_bot/config.py"] = "",
                ["telegram_shop_bot/database.py"] = "",
                ["telegram_shop_bot/handlers/__init__.py"] = "",
                ["telegram_shop_bot/handlers/admin.py"] = "",
                ["telegram_shop_bot/handlers/user.py"] = ""
            },
            ["yaml"] = new Dictionary<string, string>
            {
                ["telegram_shop_bot/bot.py"] = "",
                ["telegram_shop_bot/config.py"] = "",
                ["telegram_shop_bot/database.py"] = "",
                ["telegram_shop_bot/handlers/__init__.py"] = "",
                ["telegram_shop_bot/handlers/admin.py"] = "",
                ["telegram_shop_bot/handlers/user.py"] = ""
            },
            ["tree"] = @"telegram_shop_bot/
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
    └── whatsapp_verification.py"
        };

        // JSON faylni o'qish
        public void LoadJson(string path)
        {
            string json = File.ReadAllText(path);
            Structure = JsonSerializer.Deserialize<Dictionary<string, string>>(json);
        }

        // YAML faylni o'qish
        public void LoadYaml(string path)
        {
            var deserializer = new DeserializerBuilder().Build();
            string yaml = File.ReadAllText(path);
            Structure = deserializer.Deserialize<Dictionary<string, string>>(yaml);
        }

        // TREE matnini o'qish
        public void LoadTree(string treeText)
        {
            Structure.Clear();
            var lines = treeText.Split(new[] { "\r\n", "\n" }, StringSplitOptions.None);
            var stack = new Stack<string>();

            foreach (var line in lines)
            {
                string trimmed = line.Replace("├──", "").Replace("└──", "").Replace("│", "").Trim();
                if (string.IsNullOrEmpty(trimmed)) continue;

                int level = line.Count(c => c == '│');
                while (stack.Count > level) stack.Pop();

                if (trimmed.EndsWith("/"))
                {
                    stack.Push(trimmed.TrimEnd('/'));
                }
                else
                {
                    string path = string.Join("/", stack.Reverse().ToArray());
                    string fullPath = string.IsNullOrEmpty(path) ? trimmed : path + "/" + trimmed;
                    Structure[fullPath] = "";
                }
            }
        }

        // Papkalar va fayllarni yaratish
        public void CreateStructure()
        {
            foreach (var kvp in Structure)
            {
                string fullPath = Path.Combine(RootFolder, kvp.Key.Replace("/", Path.DirectorySeparatorChar.ToString()));
                string dir = Path.GetDirectoryName(fullPath);
                if (!Directory.Exists(dir)) Directory.CreateDirectory(dir);
                File.WriteAllText(fullPath, kvp.Value ?? "");
            }
        }
        public void CreateReadme()
        {
            string readmePath = Path.Combine(RootFolder, "README.md");
            string content = @"# UNIVERSAL PROJECT GENERATOR (C# WinForms)

        ## Loyihaning maqsadi
        Ushbu dastur talabalarga **loyiha papkasi va fayllarni avtomatik yaratish** jarayonini o‘rgatish uchun mo‘ljallangan.  

        Dastur quyidagi formatlarda loyihalarni yaratadi:  
        - **JSON** fayl asosida  
        - **YAML** fayl asosida  
        - **TREE** matn ko‘rinishi asosida  

        Foydalanuvchi fayl va papkalarni tanlab, ROOT papka nomini kiritadi va dasturni ishga tushiradi.  

        ---

        ## Funksional imkoniyatlar
        1. JSON, YAML yoki TREE faylni o‘qish.  
        2. Papka va fayllarni avtomatik yaratish.  
        3. TREE ko‘rinishini GUI oynasida ko‘rsatish.  
        4. Namuna fayllarni dastur orqali yaratish (JSON/YAML/TREE).  

        ---

        ## Ishlash tartibi

        1. Dastur ishga tushiriladi.  
        2. GUI oynasida format tanlanadi (`JSON`, `YAML`, `TREE`).  
        3. Namuna fayl tanlanadi yoki o‘zgartiriladi.  
        4. Root papka nomi kiritiladi (default: telegram_shop_bot).  
        5. Generate Project tugmasi bosiladi.  
        6. Loyihaning papka va fayllari avtomatik yaratiladi.  
        7. GUI oynasida loyihaning TREE ko‘rinishi ko‘rsatiladi.  

        ---

        ## Talabalar uchun topshiriqlar

        1. JSON/YAML/TREE formatlarini o‘rganing va namuna fayllarni tahrir qilib ko‘ring.  
        2. Dastur yordamida papka va fayllarni yarating.  
        3. TREE ko‘rinishini o‘rganib, loyihaning tuzilishini tushuning.  
        4. Qo‘shimcha fayllar yoki papkalar qo‘shib, dastur funksiyasini kengaytiring.  

        ---

        ## Texnologiyalar

        - C# 10, .NET Framework / .NET 6  
        - WinForms GUI  
        - YamlDotNet (YAML parser uchun)  
        - System.Text.Json (JSON parser uchun)  

        ---

        ## Foydalanish

        1. Visual Studio da WinFormsProjectGenerator loyihasini oching.  
        2. NuGet orqali YamlDotNet paketini o‘rnating:  
        Install-Package YamlDotNet  
        3. Loyihani build qiling va .exe faylni ishga tushiring.  
        4. Namuna faylni tanlab, root papkani kiriting va Generate tugmasini bosing.  

        ---

        **Muallif:** Otaboyev Sardorbek   
        **Ta’lim muassasasi:** Namangan Davlat Universiteti Kampiyuter Ilimlari Dasturlash texnalogiyalari k.kid-au-23 gutux talabasi
        **Sana:**16.11.2025";

            File.WriteAllText(readmePath, content);
        }

        // TREE ko'rinishini olish
        public string GetTreeString()
        {
            var tree = new Dictionary<string, List<string>>();
            foreach (var path in Structure.Keys)
            {
                var parts = path.Split('/');
                for (int i = 1; i <= parts.Length; i++)
                {
                    string parent = string.Join("/", parts.Take(i - 1));
                    if (!tree.ContainsKey(parent)) tree[parent] = new List<string>();
                    if (!tree[parent].Contains(parts[i - 1])) tree[parent].Add(parts[i - 1]);
                }
            }

            List<string> BuildTree(string parent, string prefix)
            {
                List<string> lines = new List<string>();
                if (!tree.ContainsKey(parent)) return lines;

                var children = tree[parent];
                for (int i = 0; i < children.Count; i++)
                {
                    string connector = (i == children.Count - 1) ? "└── " : "├── ";
                    string child = children[i];
                    string fullPath = string.IsNullOrEmpty(parent) ? child : parent + "/" + child;
                    lines.Add(prefix + connector + child);
                    lines.AddRange(BuildTree(fullPath, prefix + (i == children.Count - 1 ? "    " : "│   ")));
                }
                return lines;
            }

            return string.Join(Environment.NewLine, BuildTree("", ""));
        }
    }
}
