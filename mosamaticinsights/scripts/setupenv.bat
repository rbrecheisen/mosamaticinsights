@echo off

call conda create -n mosamaticinsights python=3.11 pip twine python-build bump-my-version -c conda-forge

@REM call poetry config virtualenvs.create false --local
@REM call poetry lock
@REM call poetry install