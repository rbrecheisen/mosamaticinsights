@REM @echo off
@REM setlocal EnableExtensions

@REM @rem configuration
@REM set "INSTALL_DIR=%LOCALAPPDATA%\Miniforge3"
@REM set "ENV_NAME=mosamaticinsights"
@REM set "ENV_DIR=%INSTALL_DIR%\envs\%ENV_NAME%"
@REM set "APP_EXE=%ENV_DIR%\Scripts\mosamaticinsights.exe"
@REM set "CONDA_BAT=%INSTALL_DIR%\condabin\conda.bat"

@REM if not exist "%CONDA_BAT%" (
@REM   echo ERROR: Miniforge not found at "%INSTALL_DIR%".
@REM   echo Please run the installer first.
@REM   pause
@REM   exit /b 1
@REM )

@REM if not exist "%APP_EXE%" (
@REM   echo ERROR: "%APP_EXE%" not found.
@REM   pause
@REM   exit /b 1
@REM )

@REM echo Running %ENV_NAME%...
@REM "%APP_EXE%" %*
@REM if errorlevel 1 (
@REM   echo ERROR: Could not run Mosamatic Insights.
@REM   echo Press any key to continue...
@REM   pause
@REM   exit /b 1
@REM )

@echo off
setlocal EnableExtensions

REM configuration
set "INSTALL_DIR=%LOCALAPPDATA%\miniforge3"
set "ENV_NAME=mosamaticinsights"
set "ENV_DIR=%INSTALL_DIR%\envs\%ENV_NAME%"
set "CONDA_BAT=%INSTALL_DIR%\condabin\conda.bat"

if not exist "%CONDA_BAT%" (
  echo ERROR: Miniforge not found at "%INSTALL_DIR%".
  pause
  exit /b 1
)

REM Initialize conda for this cmd session and activate env
call "%CONDA_BAT%" activate "%ENV_NAME%"
if errorlevel 1 (
  echo ERROR: Failed to activate environment "%ENV_NAME%".
  pause
  exit /b 1
)

REM Sanity check: is PySide6 actually importable in this env?
python -c "import PySide6" >nul 2>nul
if errorlevel 1 (
  echo ERROR: PySide6 is not importable in env "%ENV_NAME%".
  echo Try: conda list pyside6
  echo Or:  python -c "import sys; print(sys.executable)"
  pause
  exit /b 1
)

echo Running %ENV_NAME%...
mosamaticinsights %*
if errorlevel 1 (
  echo ERROR: Could not run Mosamatic Insights.
  pause
  exit /b 1
)