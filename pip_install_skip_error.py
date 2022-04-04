import sys
from pip._internal import main as pip_main

def install(package):
    pip_main(['install', package])

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        for line in f:
            install(line)