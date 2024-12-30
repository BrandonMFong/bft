__author__ = "brando"
__date__ = "12/30/24"

import sys
import os

SCRIPT_NAME = os.path.basename(sys.argv[0])
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def get_pool_dir():
    return os.path.join(SCRIPT_PATH, "../pool")

