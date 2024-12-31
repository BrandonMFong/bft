__author__ = "brando"
__date__ = "12/30/24"

import sys
import os

SCRIPT_NAME = os.path.basename(sys.argv[0])
SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))

def get_pool_dir():
    return os.path.join(SCRIPT_PATH, "../pool")

def bft_reg_url():
    """
    raw root folder to buckets
    """
    return "https://raw.githubusercontent.com/BrandonMFong/bft-buckets/refs/heads/dev/buckets/"

def bft_api_list_repo():
    """
    https://docs.github.com/en/rest/git/trees?apiVersion=2022-11-28#get-a-tree
    """
    return "https://api.github.com/repos/BrandonMFong/bft-buckets/git/trees/dev?recursive=1"

