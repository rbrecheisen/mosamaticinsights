#!/bin/bash

mamba create -n mosamaticinsights python=3.11 poetry pyside6 -c conda-forge
mamba activate mosamaticinsights
poetry config virtualenvs.create false --local
poetry lock
poetry install