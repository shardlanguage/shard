# Stop if an error happen
$ErrorActionPreference = 'Stop'

# The program needs administrator permissions
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Warning "This program must be executed as administrator"
    exit 1
}

# Go to the script directory
Set-Location -Path $PSScriptRoot

# This directory is required for the parser
New-Item -ItemType Directory -Path "parser_out" -Force

# Check if the dependencies are installed
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Error "pyinstaller is required but not installed"
    exit 1
}
if (-not (Get-Command gcc -ErrorAction SilentlyContinue)) {
    Write-Error "GCC not found."
    exit 1
}

# Make the executable
pyinstaller --onefile --strip --clean --name shardc.exe --exclude-module tkinter --add-data "parser_out;parser_out" src/shardc.py

# Install shardc
$source = "dist\shardc.exe"
$destination = "C:\Program Files\shardc\shardc.exe"

if (-not (Test-Path -Path (Split-Path $destination))) {
    New-Item -ItemType Directory -Path (Split-Path $destination) -Force | Out-Null
}

Copy-Item -Path $source -Destination $destination -Force

# Clean build files
Remove-Item -Recurse -Force build, shardc.spec, dist