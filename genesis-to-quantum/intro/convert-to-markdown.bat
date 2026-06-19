@echo off
REM ============================================================
REM  HTML → Markdown Converter for Genesis to Quantum Series
REM  Converts all .html files in this folder to .md in /markdown
REM  Requires: Pandoc (https://pandoc.org)
REM ============================================================

setlocal enabledelayedexpansion

set "SRC=%~dp0"
set "OUT=%~dp0markdown"

if not exist "%OUT%" mkdir "%OUT%"

echo ============================================================
echo  HTML to Markdown Converter
echo  Source: %SRC%
echo  Output: %OUT%
echo ============================================================
echo.

set COUNT=0

for %%F in ("%SRC%*.html") do (
    set "NAME=%%~nF"
    echo Converting: %%~nxF
    pandoc "%%F" -f html -t markdown-raw_html-native_divs-native_spans --wrap=none --strip-comments -o "%OUT%\!NAME!.md"
    if !errorlevel! equ 0 (
        echo   OK → markdown\!NAME!.md
        set /a COUNT+=1
    ) else (
        echo   FAILED: %%~nxF
    )
)

echo.
echo ============================================================
echo  Done. Converted %COUNT% files to markdown.
echo  Output: %OUT%
echo ============================================================
pause
