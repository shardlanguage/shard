@echo off
setlocal

:: Check for administrator rights
net session >nul 2>&1
if %errorlevel% NEQ 0 (
    echo This script must be run as administrator.
    pause
    exit /b 1
)

:: Define paths
set SCRIPT_DIR=%~dp0
set BIN=%SCRIPT_DIR%..\shard.exe
set INSTALL_DIR=C:\Program Files\Shard
set INSTALL_PATH=%INSTALL_DIR%\shard.exe

:: Check shard.exe
if not exist "%BIN%" (
    echo shard.exe not found at "%BIN%". Please build it or place it in the parent folder.
    pause
    exit /b 1
)

:: Create installation folder
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

:: Copy shard.exe
copy /Y "%BIN%" "%INSTALL_PATH%"

:: Add to system PATH (force add, may cause duplicates)
echo Adding "%INSTALL_DIR%" to system PATH (force)...
powershell -Command "[Environment]::SetEnvironmentVariable('Path', [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';C:\\Program Files\\Shard', 'Machine'); Write-Host 'Added to system PATH. Please restart your terminal.'"

echo Installation complete.
pause
