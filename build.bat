@echo off
echo Building JokeVirus...
dotnet publish -c Release -r win-x64 --self-contained true ^
    -p:PublishSingleFile=true ^
    -p:IncludeNativeLibrariesForSelfExtract=true ^
    -o ./dist
echo.
echo Done. Output: JokeVirus\dist\JokeVirus.exe
echo Drop your PNGs into the Assets\ folder next to the exe before running.
pause
