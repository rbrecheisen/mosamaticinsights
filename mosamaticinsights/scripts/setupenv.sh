#!/bin/bash

mamba install -c conda-forge \
    poetry \
    pyside6 \
    numpy \
    pandas \
    pydicom \
    pillow \
    matplotlib \
    simpleitk

poetry config virtualenvs.create false --local
poetry lock
poetry install