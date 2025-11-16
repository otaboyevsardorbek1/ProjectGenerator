using System;
using System.IO;
using System.Windows.Forms;

namespace ProjectGenerator
{
    public partial class Form1 : Form
    {
        ProjectGenerator generator = new ProjectGenerator();

        public Form1()
        {
            InitializeComponent();
            comboFormat.Items.AddRange(new string[] { "JSON", "YAML", "TREE" });
            comboFormat.SelectedIndex = 0;
        }

        private void btnBrowse_Click(object sender, EventArgs e)
        {
            OpenFileDialog dlg = new OpenFileDialog();
            if (dlg.ShowDialog() == DialogResult.OK)
                txtFile.Text = dlg.FileName;
        }

        private void btnGenerate_Click(object sender, EventArgs e)
        {
            try{
               generator.RootFolder = string.IsNullOrEmpty(txtRoot.Text) ? "new app" : txtRoot.Text;

        switch (comboFormat.SelectedItem.ToString())
        {
            case "JSON":
                generator.LoadJson(txtFile.Text);
                break;
            case "YAML":
                generator.LoadYaml(txtFile.Text);
                break;
            case "TREE":
                generator.LoadTree(File.ReadAllText(txtFile.Text));
                break;
        }

        generator.CreateStructure();
        generator.CreateReadme(); // README.md faylini yaratish

        txtLog.Text = generator.GetTreeString();
        MessageBox.Show("Loyiha muvaffaqiyatli yaratildi! README.md ham yaratildi.");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Xatolik: {ex.Message}");
            }
        }
    }
}
