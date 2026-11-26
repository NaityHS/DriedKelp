// language: C#, file: FileCopier.cs, target: Windows 10/11, .NET 6
// copies all Asset PNGs to Desktop / Documents / Temp with CHAOS_ prefix
// then floods Desktop with 15 extra randomly-named copies

using System;
using System.IO;

namespace JokeVirus
{
    internal static class FileCopier
    {
        private static readonly Random Rng = new();

        public static void Run()
        {
            string assetsDir = Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory, "Assets");

            if (!Directory.Exists(assetsDir)) return;

            string[] pngs = Directory.GetFiles(assetsDir, "*.png",
                SearchOption.TopDirectoryOnly);
            if (pngs.Length == 0) return;

            // ── Standard destinations ────────────────────────────────────────
            string[] destinations =
            {
                Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
                Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments),
                Path.GetTempPath(),
            };

            foreach (string png in pngs)
            {
                string filename = Path.GetFileName(png);
                foreach (string dest in destinations)
                {
                    try
                    {
                        File.Copy(png, Path.Combine(dest, "CHAOS_" + filename),
                            overwrite: true);
                    }
                    catch { /* skip permission errors silently */ }
                }
            }

            // ── Desktop flood — 15 extra copies with index suffix ────────────
            string desktop = destinations[0];
            for (int i = 0; i < 15; i++)
            {
                string src  = pngs[Rng.Next(pngs.Length)];
                string stem = Path.GetFileNameWithoutExtension(src);
                string dest = Path.Combine(desktop, $"CHAOS_{stem}_{i:D2}.png");
                try { File.Copy(src, dest, overwrite: true); } catch { }
            }
        }
    }
}
