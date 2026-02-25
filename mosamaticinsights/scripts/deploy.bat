@echo off

setlocal

set /p CONFIRM="Did you update the CHANGELOG? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

set /p BUMP_LEVEL="What version bump level do you want to use? [major, minor, patch (default)] "
if /I "%BUMP_LEVEL%"=="major" (
    python scripts\bumpversion.py --part major --update_toml 1
) else if /I "%BUMP_LEVEL%"=="minor" (
    python scripts\bumpversion.py --part minor --update_toml 1
) else (
    python scripts\bumpversion.py --part patch --update_toml 1
)

set /p VERSION=<VERSION
echo New version: %VERSION%. Is this correct?
pause

set /p TOKEN=<"G:\My Drive\data\ApiKeysAndPasswordFiles\pypi-token.txt"
set "TWINE_USERNAME=__token__"
set "TWINE_PASSWORD=%TOKEN%"

git add -A
git commit -m "Deploying version %VERSION%"
git push

python -m build
python -m twine upload dist/*

endlocal