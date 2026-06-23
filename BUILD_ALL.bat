@echo off
setlocal
cd /d "%~dp0"
python "MUST DO\build_all.py" %*
set EXITCODE=%ERRORLEVEL%
if %EXITCODE% NEQ 0 (
  echo.
  echo BUILD_ALL failed with exit code %EXITCODE%.
)
exit /b %EXITCODE%
