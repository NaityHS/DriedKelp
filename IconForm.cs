// language: C#, file: IconForm.cs, target: Windows 10/11, .NET 6
// tiny 48×48 borderless form showing a system icon (error, warning, etc.)
// WS_EX_TRANSPARENT = click-through; WS_EX_TOOLWINDOW = no taskbar button
// position is driven externally by Orchestrator timers

using System;
using System.Drawing;
using System.Windows.Forms;

namespace JokeVirus
{
    internal class IconForm : Form
    {
        private readonly PictureBox _pb;

        public IconForm(Icon icon)
        {
            // ── Layout ──────────────────────────────────────────────────────
            this.FormBorderStyle = FormBorderStyle.None;
            this.ShowInTaskbar   = false;
            this.TopMost         = true;
            this.Size            = new Size(48, 48);
            this.BackColor       = Color.Magenta;        // transparency key colour
            this.TransparencyKey = Color.Magenta;        // makes background invisible

            // ── Icon display ────────────────────────────────────────────────
            _pb = new PictureBox
            {
                Image    = icon.ToBitmap(),
                SizeMode = PictureBoxSizeMode.StretchImage,
                Size     = new Size(48, 48),
                Location = new Point(0, 0),
                BackColor = Color.Magenta,
            };
            this.Controls.Add(_pb);
        }

        // ── Extended style: click-through + no taskbar entry ─────────────────
        protected override CreateParams CreateParams
        {
            get
            {
                var cp = base.CreateParams;
                cp.ExStyle |= 0x00000020; // WS_EX_TRANSPARENT — mouse events pass through
                cp.ExStyle |= 0x00000080; // WS_EX_TOOLWINDOW  — hidden from taskbar
                return cp;
            }
        }

        // ── Silently ignore close attempts from OS (stays until process ends) ─
        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            if (e.CloseReason == CloseReason.UserClosing)
                e.Cancel = true;
            else
                base.OnFormClosing(e);
        }
    }
}
