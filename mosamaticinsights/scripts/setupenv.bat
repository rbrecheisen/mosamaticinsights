@echo off

@REM mamba create -n mosamaticinsights python=3.11 ^
@REM     poetry ^
@REM     pyside6 ^
@REM     numpy ^
@REM     pandas ^
@REM     pydicom ^
@REM     pillow ^
@REM     matplotlib ^
@REM     simpleitk -c conda-forge

@REM mamba activate mosamaticinsights
@REM poetry config virtualenvs.create false --local
@REM poetry lock
@REM poetry install