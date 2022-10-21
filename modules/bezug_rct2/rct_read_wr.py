#!/usr/bin/python3
from typing import List
import os, sys, traceback, time
try: # make script callable from command line and LRS
    from bezug_rct2 import rct_lib
except:
    import rct_lib

# Entry point with parameter check
def main(argv: List[str]):
    start_time =  time.time()


if __name__ == "__main__":
    main(sys.argv[1:])