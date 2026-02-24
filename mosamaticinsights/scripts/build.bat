@echo off

setlocal

set /p CONFIRM="Did you update the CHANGELOG? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

set /p BUMP_LEVEL="What version bump level do you want to use? [major, minor, patch (default)] "
if /I "%BUMP_LEVEL%"=="major" (
    bump-my-version bump major
) else if /I "%BUMP_LEVEL%"=="minor" (
    bump-my-version bump minor
) else (
    bump-my-version bump patch
)

python -m build

endlocal