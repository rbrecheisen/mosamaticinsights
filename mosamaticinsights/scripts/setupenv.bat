@echo off

mamba create -n mosamaticinsights python=3.11 ^
    poetry ^
    pyside6 ^
    numpy ^
    pandas ^
    pydicom ^
    pillow ^
    matplotlib ^
    simpleitk -c conda-forge

@REM mamba activate mosamaticinsights
@REM poetry config virtualenvs.create false --local
@REM poetry lock
@REM poetry install