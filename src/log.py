__author__ = "brando"
__date__ = "12/30/24"

from arguments import *

def bft_print(buf):
    print("{}".format(buf))

def debug_print(buf):
    """
    conditional print on verbose flag
    """
    if ARGS.debug_print():
        print("bft_debug> {}".format(buf))

