@echo off
cd /d "%~dp0"
powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%~dp0open-local.ps1" %*
if errorlevel 1 (
  echo.
  echo No se pudo abrir el proyecto. Revisa el error anterior.
  pause
)
