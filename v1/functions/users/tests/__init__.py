import sys
from os.path import join, abspath, dirname

# Make `../lib` directory to python packages for testing.
sys.path.insert(0, join(dirname(abspath(__file__)), '../lib'))
