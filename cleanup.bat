@echo off
echo Cleaning up JokeVirus chaos files...

del /f /q "%USERPROFILE%\Desktop\CHAOS_*"     2>nul
del /f /q "%USERPROFILE%\Documents\CHAOS_*"   2>nul
del /f /q "%TEMP%\CHAOS_*"                    2>nul
del /f /q "%TEMP%\jv_wall.bmp"                2>nul

echo Resetting wallpaper to default...
reg add "HKCU\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d "" /f >nul 2>&1
RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters ,1 ,True

echo Done. All chaos files removed.
pause
