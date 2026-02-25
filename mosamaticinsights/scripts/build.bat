@echo off
setlocal enabledelayedexpansion

set /p CONFIRM="Did you update the CHANGELOG? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

git add -A
git commit -m "Deploying version %VERSION%"
git push

python -m build

endlocal