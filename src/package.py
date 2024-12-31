__author__ = "brando"
__date__ = "12/31/24"

import tarfile
import dmglib
import shutil

from log import *

class Package():
    """
    The package file that gets downloaded from download entry
    """
    def __init__(self, file_path):
        self._file_path = file_path

    def extract(self, target_dir):
        """
        extracts everything in the package file
        """
        debug_print("extracting {} to {}".format(self._file_path, target_dir))
        if self._file_path.endswith("tar.gz"):
            debug_print("identified as a tar.gz file")
            tar = tarfile.open(self._file_path, "r:gz")
            debug_print(tar.getmembers())
            tar.extractall(path=target_dir)
            tar.close()
        elif self._file_path.endswith(".dmg"):
            dmg = dmglib.DiskImage(self._file_path)
            if dmg.has_license_agreement():
                raise Exception("cannot open {}".format(self._file_path))

            for mount_point in dmg.attach():
                shutil.copytree(mount_point, os.path.join(
                    target_dir, os.path.basename(mount_point)
                ))

            dmg.detach()

