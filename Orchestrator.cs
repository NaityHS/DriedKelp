// language: C#, file: Orchestrator.cs, target: Windows 10/11, .NET 6
// hidden form — owns all timers; spawns popups and icon swarm on the STA thread

using System;
using System.Collections.Generic;
using System.Drawing;
using System.IO;
using System.Windows.Forms;

namespace JokeVirus
{
    internal class Orchestrator : Form
    {
        // ── Icons that follow the mouse ─────────────────────────────────────
        private readonly List<IconForm> _iconPool = new();
        private const int MAX_ICONS = 25;

        // ── Asset PNGs for popups ───────────────────────────────────────────
        private readonly string[] _pngs;
        private readonly Random   _rng = new();

        // ── Timers ──────────────────────────────────────────────────────────
        private readonly System.Windows.Forms.Timer _popupTimer;      // spawn PNG popup
        private readonly System.Windows.Forms.Timer _iconMoveTimer;   // reposition swarm
        private readonly System.Windows.Forms.Timer _iconSpawnTimer;  // grow swarm over time
        private readonly System.Windows.Forms.Timer _vibrationTimer;  // extra jitter on icons

        public Orchestrator()
        {
            // ── Hide this window completely ─────────────────────────────────
            this.WindowState   = FormWindowState.Minimized;
            this.ShowInTaskbar = false;
            this.Opacity       = 0;
            this.Size          = new Size(1, 1);

            // ── Load asset PNGs ─────────────────────────────────────────────
            string assetsDir = Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory, "Assets");
            _pngs = Directory.Exists(assetsDir)
                ? Directory.GetFiles(assetsDir, "*.png", SearchOption.TopDirectoryOnly)
                : Array.Empty<string>();

            // ── Seed initial icon swarm (8 icons on boot) ───────────────────
            for (int i = 0; i < 8; i++) SpawnIcon();

            // ── Popup every 1.8 s ───────────────────────────────────────────
            _popupTimer = new System.Windows.Forms.Timer { Interval = 1800 };
            _popupTimer.Tick += (_, _) => SpawnPopup();
            _popupTimer.Start();

            // ── Move swarm every 120 ms ─────────────────────────────────────
            _iconMoveTimer = new System.Windows.Forms.Timer { Interval = 120 };
            _iconMoveTimer.Tick += MoveIconSwarm;
            _iconMoveTimer.Start();

            // ── Spawn a new icon every 600 ms until cap ─────────────────────
            _iconSpawnTimer = new System.Windows.Forms.Timer { Interval = 600 };
            _iconSpawnTimer.Tick += (_, _) => { if (_iconPool.Count < MAX_ICONS) SpawnIcon(); };
            _iconSpawnTimer.Start();

            // ── Random vibration burst every 400 ms ────────────────────────
            _vibrationTimer = new System.Windows.Forms.Timer { Interval = 400 };
            _vibrationTimer.Tick += VibrateIcons;
            _vibrationTimer.Start();

            // ── Show first popup immediately ────────────────────────────────
            SpawnPopup();
        }

        // ── Spawn a PNG popup ───────────────────────────────────────────────
        private void SpawnPopup()
        {
            if (_pngs.Length == 0) return;
            new PopupForm(_pngs[_rng.Next(_pngs.Length)]).Show();
        }

        // ── Spawn one icon form and add to pool ─────────────────────────────
        private void SpawnIcon()
        {
            // Rotate through system icon types
            Icon[] icons =
            {
                SystemIcons.Error,
                SystemIcons.Warning,
                SystemIcons.Information,
                SystemIcons.Question,
                SystemIcons.Hand,
                SystemIcons.Exclamation,
            };
            var f = new IconForm(icons[_iconPool.Count % icons.Length]);
            f.Show();
            _iconPool.Add(f);
        }

        // ── Reposition every icon around current cursor ─────────────────────
        private void MoveIconSwarm(object? sender, EventArgs e)
        {
            _iconPool.RemoveAll(f => f.IsDisposed);
            var mouse = Cursor.Position;

            foreach (var f in _iconPool)
            {
                if (f.IsDisposed) continue;
                // Scatter in a 300×300 radius around cursor
                int dx = _rng.Next(-300, 300);
                int dy = _rng.Next(-300, 300);
                f.Location = new Point(mouse.X + dx, mouse.Y + dy);
            }
        }

        // ── Vibration burst — tiny jitter on each icon ──────────────────────
        private void VibrateIcons(object? sender, EventArgs e)
        {
            _iconPool.RemoveAll(f => f.IsDisposed);
            foreach (var f in _iconPool)
            {
                if (f.IsDisposed) continue;
                f.Location = new Point(
                    f.Location.X + _rng.Next(-12, 12),
                    f.Location.Y + _rng.Next(-12, 12));
            }
        }

        // ── Never show this form ─────────────────────────────────────────────
        protected override void SetVisibleCore(bool value)
            => base.SetVisibleCore(false);
    }
}
