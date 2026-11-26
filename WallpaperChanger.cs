// language: C#, file: WallpaperChanger.cs, target: Windows 10/11, .NET 6
// sets desktop wallpaper to 1111474383075081824.png via SystemParametersInfo
// converts PNG→BMP to temp path for maximum Windows compat

using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;

namespace JokeVirus
{
    internal static class WallpaperChanger
    {
        [DllImport("user32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        private static extern int SystemParametersInfo(
            int uAction, int uParam, string lpvParam, int fuWinIni);

        private const int SPI_SETDESKWALLPAPER = 20;
        private const int SPIF_UPDATEINIFILE   = 0x01;
        private const int SPIF_SENDCHANGE      = 0x02;

        public static void Run()
        {
            string assetsDir = Path.Combine(
                AppDomain.CurrentDomain.BaseDirectory, "Assets");

            if (!Directory.Exists(assetsDir)) return;

            // Primary target — the specific PNG dj specified
            string target = Path.Combine(assetsDir, "1111474383075081824.png");

            // Fallback to any PNG in Assets if the named one isn't there
            if (!File.Exists(target))
            {
                string[] pngs = Directory.GetFiles(assetsDir, "*.png",
                    SearchOption.TopDirectoryOnly);
                if (pngs.Length == 0) return;
                target = pngs[0];
            }

            // Convert PNG → BMP in temp — SPI_SETDESKWALLPAPER is picky on some builds
            string bmpPath = Path.Combine(Path.GetTempPath(), "jv_wall.bmp");
            try
            {
                using var img = Image.FromFile(target);
                using var bmp = new Bitmap(img);
                bmp.Save(bmpPath, ImageFormat.Bmp);
            }
            catch { return; }

            SystemParametersInfo(
                SPI_SETDESKWALLPAPER, 0, bmpPath,
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE);
        }
    }
}
