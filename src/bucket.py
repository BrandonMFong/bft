__author__ = "brando"
__date__ = "12/2/24"

import requests
import json
import shutil
import platform

from package import *
from utils import *
from log import *

class BucketMeta():
    """
    Handles parsing the bucket recipe
    """
    def __init__(self, bucket_file_name):
        self._bucket_file_name = bucket_file_name

    def bucket_file_name(self):
        return self._bucket_file_name

    def get_meta_local(self, pool_dir):
        """
        reads the bucket file in the .installed folder
        """
        debug_print("reading local bucket file")

        if pool_dir is None:
            raise Exception("pool_dir is None, please pass a value for pool_dir")

        installed_dir = os.path.join(pool_dir, ".installed")
        create_dir(installed_dir)
        debug_print("looking into installed dir '{}' for bucket file".format(installed_dir))

        meta_bucket_json_file = os.path.join(
            installed_dir,
            self.bucket_file_name()
        )

        debug_print("does '{}' exist".format(meta_bucket_json_file))
        if os.path.isfile(meta_bucket_json_file) is False:
            raise Exception("{} does not exist. Is this even installed?".format(
                meta_bucket_json_file
            ))

        debug_print("yes")

        with open(meta_bucket_json_file, 'r') as f:
            self._meta_bucket = json.load(f)
            debug_print("meta bucket dump:\n{}".format(
                json.dumps(self._meta_bucket, indent=4
            )))
        
        self._meta_github_release = self._meta_bucket["installed"]["meta_github_release"]

    def get_meta_remote(self):
        """
        compiles all the meta data from the bft-buckets buckets directory and
        every buckets' meta url
        """
        url = os.path.join(bft_reg_url(), self._bucket_file_name)
        debug_print("downloading bucket description from url {}".format(url))
        headers = {'Cache-Control': 'no-cache'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("status code {}".format(response.status_code))
        
        debug_print("bucket content:")
        self._meta_bucket = response.json()
        debug_print(json.dumps(self._meta_bucket, indent=4))

        meta_url = response.json()["meta"]["url"]
        response = requests.get(meta_url, headers=headers)
        debug_print("downloading bucket metadata from url {}".format(meta_url))
        if response.status_code != requests.codes.ok:
            response.raise_for_status()

        debug_print("meta data:")
        self._meta_github_release = response.json()
        debug_print(json.dumps(self._meta_github_release, indent=4))

    def meta_bucket(self):
        """
        json object holding objects like the ones here:
        https://github.com/BrandonMFong/bft-buckets/tree/dev/buckets
        """
        return self._meta_bucket

    def tag_name(self):
        """
        returns tag_name from the github latest release api
        """
        return self._meta_github_release["tag_name"]

    def meta_github_release(self):
        return self._meta_github_release

    def __platform(self):
        """
        returns the download's subkey that determines
        what package to download for the current platform
        """
        if platform.system() == "Linux":
            return "linux"
        elif platform.system() == "Darwin":
            return "macos"

    def url_package(self):
        """
        download url
        """
        platform = self.__platform()
        return self._meta_bucket["download"][platform]["url"]

    def package_items(self):
        """
        items from the package we are extracting
        """
        platform = self.__platform()
        return self._meta_bucket["download"][platform]["items"]

class Bucket():
    """
    A bucket is the package that we are installing/updating
    """
    def __init__(self, name):
        self._name = name
        self._meta = BucketMeta(self._name + ".json")

    def fetch(self, get_remote=False, get_local=False, pool_dir=None):
        """
        fetches remote data
        """
        if get_remote:
            self._meta.get_meta_remote()
        elif get_local:
            self._meta.get_meta_local(pool_dir)
        else:
            raise Exception("you must pass get_remote or get_local value")


    def tag_name(self):
        """
        tag_name is the version
        returns the tag_name set for the release
        """
        return self._meta.tag_name()

    def name(self):
        """
        name of the bucket. Usually the basename of the
        bucket file without the extension
        """
        return self._name

    def __url_package(self):
        """
        the url entry under meta
        """
        return self._meta.url_package()

    def remove(self, pool_dir):
        """
        removes bucket from pool
        """
        debug_print("removing bucket")

        # TODO: figure out how we can find where the installation is
        # should we store where we installed the application in the installed dict?

    def download(self, pool_dir):
        """
        downloads the package
        """
        # create tmp directory we are downloading to
        debug_print("downloading to pool_dir {}...".format(pool_dir))
        tmp_dir = os.path.join(pool_dir, "tmp")
        shutil.rmtree(tmp_dir, ignore_errors=True)
        create_dir(tmp_dir)

        # get the url we are downloading from
        url = self.__url_package()
        tmp_file = tmp_dir + "/" + os.path.basename(url)
        debug_print("downloading {} to {}".format(
            url, tmp_file
        ))

        # get the object from url
        # fetch with progress
        debug_print("fetching {}".format(url))
        headers = {'Cache-Control': 'no-cache'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception("status code {}".format(response.status_code))

        # write content to a file
        with open(tmp_file, mode="wb") as file:
            file.write(response.content)

        if os.path.getsize(tmp_file) == 0:
            raise Exception("{} is empty".format(tmp_file))

        # extract items from package file
        bucket_pkg = Package(tmp_file)
        bucket_pkg.extract(tmp_dir)
        bin_dir = os.path.join(pool_dir, "bin")
        create_dir(bin_dir)
        for item in self._meta.package_items():
            src = os.path.join(tmp_dir, item)
            dest = os.path.join(bin_dir, os.path.basename(item))
            debug_print("{} -> {}".format(src, dest))
            os.rename(src, dest)

    def __get_installed_assets(self):
        """
        returns an array relative paths of installed assets in the pool dir
        """
        debug_print("gathering the assets array")
        return []

    def __meta_bucket_saved_content(self):
        """
        adds an 'installed' entry to cache some meta data before we fetch it
        """
        res = self._meta.meta_bucket()

        res["installed"] = {
            "tag_name" : self.tag_name(),
            "assets" : self.__get_installed_assets(),
            "meta_github_release" : self._meta.meta_github_release()
        }

        return res

    def save(self, pool_dir):
        """
        saves the bucket json file to .installed directory
        in the pool directory
        """
        debug_print("saving bucket")
        installed_dir = os.path.join(pool_dir, ".installed")
        create_dir(installed_dir)
        debug_print("saving bucket into dir {}".format(installed_dir))

        meta_bucket_json_file = os.path.join(
            installed_dir,
            self._meta.bucket_file_name()
        )

        meta_bucket_json_content = json.dumps(
            self.__meta_bucket_saved_content(), indent=4
        )

        debug_print("preparing to write to file '{}':".format(meta_bucket_json_file))
        debug_print(meta_bucket_json_content)
        with open(meta_bucket_json_file, 'w') as f:
            f.write(meta_bucket_json_content)

    def is_installed(self, pool_dir):
        """
        checks local system for a saved meta bucket file

        this function should not require or do any remote requests
        """
        debug_print("checking if {} is installed".format(self.name()))
        installed_dir = os.path.join(pool_dir, ".installed")

        meta_bucket_json_file = os.path.join(
            installed_dir,
            self._meta.bucket_file_name()
        )

        return os.path.isfile(meta_bucket_json_file)

    def can_update(self, pool_dir):
        """
        compares our tag_name with the saved tag_name in
        the .installed directory
        """
        debug_print("checking if {} is can be updated".format(self.name()))
        installed_dir = os.path.join(pool_dir, ".installed")

        meta_bucket_json_file = os.path.join(
            installed_dir,
            self._meta.bucket_file_name()
        )

        if os.path.isfile(meta_bucket_json_file) is False:
            raise Exception("{} does not exist".format(
                meta_bucket_json_file
            ))

        with open(meta_bucket_json_file, 'r') as f:
            data = json.load(f)
            tag_name = data["installed"]["tag_name"]
            return tag_name != self.tag_name()

        return False

    def uninstall(self, pool_dir):
        debug_print("uninstalling...")

