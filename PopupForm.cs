// language: C#, file: PopupForm.cs, target: Windows 10/11, .NET 6
// PNG popup window — random screen position, fake error title, auto-closes
// clicking OK spawns 3 more immediately (consequence loop)

using System;
using System.Drawing;
using System.Windows.Forms;

namespace JokeVirus
{
    internal class PopupForm : Form
    {
        private static readonly string[] Titles =
        {
            "CRITICAL ERROR",
            "WARNING",
            "SYSTEM FAILURE",
            "ALERT !!",
            "VIRUS DETECTED",
            "ERROR 0x000000FF",
            "ACCESS DENIED",
            "FATAL EXCEPTION",
            "DO NOT CLOSE THIS WINDOW",
            "BSOD INCOMING",
            "YOUR FILES ARE ENCRYPTED",
            "ERROR: SUCCESS",
            "HELP",
        };

        private static readonly Random Rng = new();
        private readonly string        _imagePath;
        private System.Windows.Forms.Timer? _autoClose;

        public PopupForm(string imagePath)
        {
            _imagePath = imagePath;

            // ── Window appearance ───────────────────────────────────────────
            this.Text            = Titles[Rng.Next(Titles.Length)];
            this.TopMost         = true;
            this.StartPosition   = FormStartPosition.Manual;
            this.FormBorderStyle = FormBorderStyle.FixedDialog;
            this.MaximizeBox     = false;
            this.MinimizeBox     = false;
            this.Size            = new Size(420, 340);
            this.Icon            = SystemIcons.Error;

            // ── Random screen position ──────────────────────────────────────
            var screen = Screen.PrimaryScreen?.WorkingArea
                         ?? new Rectangle(0, 0, 1920, 1080);
            this.Location = new Point(
                Rng.Next(0, Math.Max(1, screen.Width  - this.Width)),
                Rng.Next(0, Math.Max(1, screen.Height - this.Height)));

            // ── PNG display ─────────────────────────────────────────────────
            try
            {
                var pb = new PictureBox
                {
                    Image    = Image.FromFile(imagePath),
                    SizeMode = PictureBoxSizeMode.Zoom,
                    Bounds   = new Rectangle(0, 0, 420, 290),
                };
                this.Controls.Add(pb);
            }
            catch { /* broken image — still show the popup frame */ }

            // ── OK button ───────────────────────────────────────────────────
            var btn = new Button
            {
                Text     = "OK",
                Location = new Point(170, 295),
                Size     = new Size(80, 30),
            };
            btn.Click += OnOkClick;
            this.Controls.Add(btn);

            // ── Auto-close after 5–10 s even if ignored ─────────────────────
            int lifetime = Rng.Next(5000, 10000);
            _autoClose = new System.Windows.Forms.Timer { Interval = lifetime };
            _autoClose.Tick += (_, _) => { _autoClose.Stop(); this.Close(); };
            _autoClose.Start();
        }

        // ── Clicking OK punishes the user with 3 more popups ────────────────
        private void OnOkClick(object? sender, EventArgs e)
        {
            _autoClose?.Stop();
            this.Close();
            // Spawn 3 more immediately
            for (int i = 0; i < 3; i++)
                new PopupForm(_imagePath).Show();
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing) _autoClose?.Dispose();
            base.Dispose(disposing);
        }
    }
}
