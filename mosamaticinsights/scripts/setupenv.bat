@echo off

call mamba install -c conda-forge ^
    poetry ^
    pyside6 ^
    numpy ^
    pandas ^
    pydicom ^
    pillow ^
    matplotlib ^
    simpleitk

call poetry config virtualenvs.create false --local
call poetry lock
call poetry install