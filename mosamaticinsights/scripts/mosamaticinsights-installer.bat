@echo off
setlocal EnableExtensions EnableDelayedExpansion

@rem configuration
set "MINIFORGE_URL=https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Windows-x86_64.exe"
set "INSTALL_DIR=%LOCALAPPDATA%\Miniforge3"
set "ENV_NAME=mosamaticinsights"
set "PYTHON_VERSION=3.11"

@rem internal settings
set "CONDA_INSTALLED=false"
set "TMP_DIR=%TEMP%\miniforge_bootstrap"
set "MINIFORGE_EXE=%TMP_DIR%\Miniforge3-Windows-x86_64.exe"
set "CONDA_BAT=%INSTALL_DIR%\condabin\conda.bat"
mkdir "%TMP_DIR%" 2>nul

echo Checking if Miniforge already installed...
if exist %CONDA_BAT% (
  echo Miniforge already installed in %INSTALL_DIR%
  echo Skipping installation...
  set "CONDA_INSTALLED=true"
)

if %CONDA_INSTALLED% == "false" (
  echo Downloading Miniforge...
  curl.exe -L --fail --retry 3 --retry-delay 2 -o "%MINIFORGE_EXE%" "%MINIFORGE_URL%"
  if errorlevel 1 (
    echo ERROR: Failed to download Miniforge.
    pause
    exit /b 1
  )

  echo Installing Miniforge silently...
  @rem /S = silent, /D= sets install dir (must be last and not quoted)
  "%MINIFORGE_EXE%" /S /D=%INSTALL_DIR%
  if errorlevel 1 (
    echo ERROR: Miniforge installer failed.
    pause
    exit /b 1
  )
)

echo Initializing conda (CONDA_BAT=%CONDA_BAT%)
call "%CONDA_BAT%" config init powershell >nul 2>nul
call "%CONDA_BAT%" config --set always_yes yes --set changeps1 no >nul 2>nul
call "%CONDA_BAT%" config --set auto_activate false >nul 2>nul

pause

echo Creating/refreshing env "%ENV_NAME%" with Python %PYTHON_VERSION%...
call "%CONDA_BAT%" env remove -n "%ENV_NAME%" >nul 2>nul
call "%CONDA_BAT%" create -n "%ENV_NAME%" python=%PYTHON_VERSION% pip
if errorlevel 1 (
  echo ERROR: Failed to create conda environment.
  pause
  exit /b 1
)

echo Upgrading pip tooling...
call "%CONDA_BAT%" run -n "%ENV_NAME%" python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
  echo ERROR: Failed to upgrade pip tooling.
  pause
  exit /b 1
)

echo Installing "%ENV_NAME%"...
call "%CONDA_BAT%" run -n "%ENV_NAME%" python -m pip install "%ENV_NAME%"
if errorlevel 1 (
  echo ERROR: pip install failed for "%ENV_NAME%".
  pause
  exit /b 1
)