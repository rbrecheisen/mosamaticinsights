@echo off
setlocal enabledelayedexpansion

set /p CONFIRM="Did you update the CHANGELOG? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

REM --- bump patch version in pyproject.toml and echo new version ---
for /f %%V in ('python -c ^
    "import re; p='pyproject.toml'; s=open(p,encoding='utf-8').read(); ^
    m=re.search(r'(?ms)^\[project\].*?^version\s*=\s*\"(\d+)\.(\d+)\.(\d+)\"', s); ^
    assert m, 'version not found under [project]'; ^
    a,b,c=map(int,m.groups()); new=f'{a}.{b}.{c+1}'; ^
    s=re.sub(r'(?ms)(^\[project\].*?^version\s*=\s*\")\d+\.\d+\.\d+(\".*?$)', r'\g<1>'+new+r'\2', s, count=1); ^
    open(p,'w',encoding='utf-8').write(s); print(new)"
) do set "VERSION=%%V"

echo Bumped VERSION=%VERSION%
pause

@REM set /p BUMP_LEVEL="What version bump level do you want to use? [major, minor, patch (default)] "
@REM if /I "%BUMP_LEVEL%"=="major" (
@REM     bump-my-version bump major
@REM ) else if /I "%BUMP_LEVEL%"=="minor" (
@REM     bump-my-version bump minor
@REM ) else (
@REM     bump-my-version bump patch
@REM )
@REM for /f "usebackq tokens=2 delims== " %%V in (`findstr /R /C:"^[ ]*version[ ]*=" pyproject.toml`) do (
@REM   set "VERSION=%%~V"
@REM )
@REM set "VERSION=%VERSION:"=%"

git add -A
git commit -m "Deploying version %VERSION%"
git push

rmdir /s /q dist 2>nul
python -m build

endlocal