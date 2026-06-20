@echo off
REM ============================================================
REM CONVERT_FOR_TTS.bat
REM Drop this in ANY folder. It will:
REM   1. Convert all .html files to clean .md (markdown)
REM   2. Convert all .html files to clean .txt (TTS-ready)
REM   3. Strip all HTML tags, scripts, styles, nav, footers
REM   4. Output goes to _markdown\ and _tts\ subfolders
REM
REM Requires: Python 3.12+ (uses C:\Users\lowes path)
REM ============================================================

set PYTHON=C:\Users\lowes\AppData\Local\Programs\Python\Python312\python.exe
set SCRIPT=%~dp0_convert_engine.py

REM Create the Python engine if it doesn't exist
if not exist "%SCRIPT%" (
    echo Creating conversion engine...
    %PYTHON% -c "open(r'%SCRIPT%','w').write('')"
)

REM Write the Python engine
%PYTHON% -c "
import os
script = r'''
import os, sys, re, glob
from pathlib import Path

folder = Path(os.path.dirname(os.path.abspath(__file__)))
md_out = folder / '_markdown'
tts_out = folder / '_tts'
md_out.mkdir(exist_ok=True)
tts_out.mkdir(exist_ok=True)

html_files = list(folder.glob('*.html'))
if not html_files:
    print('No .html files found in this folder.')
    sys.exit(0)

print(f'Found {len(html_files)} HTML files.')

def strip_html_to_markdown(html_text):
    # Remove script and style blocks entirely
    text = re.sub(r'<script[^>]*>.*?</script>', '', html_text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Remove nav, header, footer blocks
    text = re.sub(r'<nav[^>]*>.*?</nav>', '', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<footer[^>]*>.*?</footer>', '', text, flags=re.DOTALL|re.IGNORECASE)
    # Convert headers
    text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'### \\1', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<h4[^>]*>(.*?)</h4>', r'#### \\1', text, flags=re.DOTALL|re.IGNORECASE)
    # Convert bold and italic
    text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\\1**', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\\1**', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\\1*', text, flags=re.DOTALL|re.IGNORECASE)
    text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\\1*', text, flags=re.DOTALL|re.IGNORECASE)
    # Convert list items
    text = re.sub(r'<li[^>]*>(.*?)</li>', r'- \\1', text, flags=re.DOTALL|re.IGNORECASE)
    # Convert blockquotes
    text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '> ' + m.group(1).strip(), text, flags=re.DOTALL|re.IGNORECASE)
    # Convert paragraphs to double newline
    text = re.sub(r'<p[^>]*>', '\\n\\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '', text, flags=re.IGNORECASE)
    # Convert br to newline
    text = re.sub(r'<br\s*/?>', '\\n', text, flags=re.IGNORECASE)
    # Strip remaining HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Decode common HTML entities
    text = text.replace('&amp;', '&')
    text = text.replace('&lt;', '<')
    text = text.replace('&gt;', '>')
    text = text.replace('&quot;', '"')
    text = text.replace('&#39;', \"'\")
    text = text.replace('&mdash;', chr(8212))
    text = text.replace('&ndash;', chr(8211))
    text = text.replace('&rsquo;', chr(8217))
    text = text.replace('&lsquo;', chr(8216))
    text = text.replace('&rdquo;', chr(8221))
    text = text.replace('&ldquo;', chr(8220))
    text = text.replace('&hellip;', chr(8230))
    text = text.replace('&nbsp;', ' ')
    # Clean up whitespace
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    text = re.sub(r'[ \\t]+', ' ', text)
    lines = [line.strip() for line in text.split('\\n')]
    text = '\\n'.join(lines)
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    return text.strip()

def markdown_to_tts(md_text):
    # Strip markdown formatting for clean TTS
    text = md_text
    # Remove markdown headers (keep the text)
    text = re.sub(r'^#{1,4}\\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\\*{1,2}([^*]+)\\*{1,2}', r'\\1', text)
    # Remove bullet points
    text = re.sub(r'^\\s*-\\s+', '', text, flags=re.MULTILINE)
    # Remove blockquote markers
    text = re.sub(r'^>\\s*', '', text, flags=re.MULTILINE)
    # Remove any remaining markdown links [text](url)
    text = re.sub(r'\\[([^\\]]+)\\]\\([^)]+\\)', r'\\1', text)
    # Remove equations and code blocks
    text = re.sub(r'```[^`]*```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)
    # Remove lines that are just symbols or very short
    lines = text.split('\\n')
    clean_lines = []
    for line in lines:
        stripped = line.strip()
        if len(stripped) < 3 and not stripped.isalpha():
            continue
        if re.match(r'^[=\\-_*]{3,}$', stripped):
            continue
        clean_lines.append(stripped)
    text = '\\n'.join(clean_lines)
    # Clean up whitespace
    text = re.sub(r'\\n{3,}', '\\n\\n', text)
    return text.strip()

for html_file in html_files:
    print(f'  Converting: {html_file.name}')
    try:
        with open(html_file, 'r', encoding='utf-8', errors='replace') as f:
            raw = f.read()
        md = strip_html_to_markdown(raw)
        tts = markdown_to_tts(md)
        stem = html_file.stem
        with open(md_out / f'{stem}.md', 'w', encoding='utf-8') as f:
            f.write(md)
        with open(tts_out / f'{stem}.txt', 'w', encoding='utf-8') as f:
            f.write(tts)
    except Exception as e:
        print(f'    ERROR: {e}')

print(f'\\nDone. {len(html_files)} files converted.')
print(f'  Markdown: {md_out}')
print(f'  TTS-ready: {tts_out}')
'''
with open(r'%SCRIPT%', 'w', encoding='utf-8') as f:
    f.write(script)
"

REM Run the engine
%PYTHON% "%SCRIPT%"

echo.
echo ============================================================
echo   Conversion complete.
echo   _markdown\ = Markdown versions
echo   _tts\      = Clean text for TTS engines
echo ============================================================
pause
