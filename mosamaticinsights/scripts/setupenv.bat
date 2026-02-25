@echo off

call conda create -n mosamaticinsights python=3.11 pip twine setup wheels python-build tomlkit -c conda-forge