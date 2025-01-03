__author__ = "brando"
__date__ = "12/30/24"

import sys

from utils import *

class Argument():
    def __init__(self, commands, description):
        """
        commands : a list of acceptable commands. where the first will be the recommended arg to use
        """
        self.commands = commands
        self.description = description

ARG_INSTALL = Argument(["install"], "installs tool")
ARG_UNINSTALL = Argument(["uninstall"], "uninstalls tool")
ARG_LIST = Argument(["list"], "lists available and installed content")
ARG_UPDATE = Argument(["update"], "updates target bucket")
ARG_HELP = Argument(["help", "-h", "--help", "-help"], "shows help")
ARG_DEBUG_PRINT = Argument(["-d"], "shows debug logging")

class Arguments():
    def print_help():
        print("usage: {} [<flags>] <command> [<args>]".format(SCRIPT_NAME))
        print()
        print("flags:")
        print("  {}\t{}".format(ARG_DEBUG_PRINT.commands[0], ARG_DEBUG_PRINT.description))
        print()
        print("command:")
        print(" {}\t{}".format(ARG_INSTALL.commands[0], ARG_INSTALL.description)) 
        print(" {}\t{}".format(ARG_UNINSTALL.commands[0], ARG_UNINSTALL.description)) 
        print(" {}\t{}".format(ARG_UPDATE.commands[0], ARG_UPDATE.description)) 
        print(" {}\t\t{}".format(ARG_LIST.commands[0], ARG_LIST.description)) 
        print(" {}\t\t{}".format(ARG_HELP.commands[0], ARG_HELP.description)) 
        print()
        print("Copyright © 2024 Brando. All rights reserved.")

    def __init__(self):
        global VERBOSE
        self._install = False
        self._uninstall = False
        self._update = False
        self._list = False
        self._show_help = False
        self._debug_print = False
        for arg in sys.argv:
            if arg in ARG_INSTALL.commands:
                self._install = True
            elif arg in ARG_UNINSTALL.commands:
                self._uninstall = True
            elif arg in ARG_UPDATE.commands:
                self._update = True
            elif arg in ARG_LIST.commands:
                self._list = True
            elif arg in ARG_HELP.commands:
                self._show_help = True
            elif arg in ARG_DEBUG_PRINT.commands:
                self._debug_print = True 

    def show_help(self):
        return len(sys.argv) == 1 or self._show_help

    def debug_print(self):
        return self._debug_print

    def do_list(self):
        return self._list

    def do_install(self):
        return self._install

    def do_uninstall(self):
        return self._uninstall

    def do_update(self):
        return self._update

    def install_targets(self):
        accept = False
        def get_install_targets(arg):
            nonlocal accept
            if accept:
                return True
            else:
                accept = arg in ARG_INSTALL.commands
                return False

        return filter(get_install_targets, sys.argv)

    def uninstall_targets(self):
        accept = False
        def get_uninstall_targets(arg):
            nonlocal accept
            if accept:
                return True
            else:
                accept = arg in ARG_UNINSTALL.commands
                return False

        return filter(get_uninstall_targets, sys.argv)

    def update_targets(self):
        accept = False
        def get_update_targets(arg):
            nonlocal accept
            if accept:
                return True
            else:
                accept = arg in ARG_UPDATE.commands
                return False

        return filter(get_update_targets, sys.argv)

ARGS = Arguments()

