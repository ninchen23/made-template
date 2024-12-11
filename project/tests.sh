#!/bin/bash
echo "Running tests"
pytest -v tests.py


# pytest needs to be installed
# the last test is with real data that is downloaded from the internet (the real pipeline) and may take a while (around 1 minute depending on the internet connection)