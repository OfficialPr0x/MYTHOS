@echo off
title Titan Genesis Node Launcher

echo 🧬 TITAN GENESIS - ENTERPRISE NODE LAUNCHER
echo ===================================================
echo.

:: Check for PowerShell
where powershell >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: PowerShell is not installed or not in PATH.
    echo Please install PowerShell to continue.
    pause
    exit /b 1
)

:: Display menu
echo Select deployment option:
echo.
echo [1] Standard Deployment
echo [2] Deployment with Monitoring
echo [3] Full Deployment with Forced Rebuild
echo.
choice /C 123 /N /M "Enter option (1-3): "

:: Process choice
if %ERRORLEVEL% EQU 1 (
    echo.
    echo Launching standard deployment...
    powershell.exe -ExecutionPolicy Bypass -File "run.ps1"
)

if %ERRORLEVEL% EQU 2 (
    echo.
    echo Launching deployment with monitoring...
    powershell.exe -ExecutionPolicy Bypass -File "run.ps1" -EnableMonitoring
)

if %ERRORLEVEL% EQU 3 (
    echo.
    echo Launching full deployment with rebuild...
    powershell.exe -ExecutionPolicy Bypass -File "run.ps1" -EnableMonitoring -ForceRebuild
) 