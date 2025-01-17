#!/usr/bin/env python

import getpass
import os
import sys
from collections import OrderedDict

from tabulate import tabulate


class Util:

    @staticmethod
    def get_input(prompt):
        return input(prompt)

    @staticmethod
    def pick_a_role(roles, aliases=None, account=None):
        if account:
            filtered_roles = {role: principal for role, principal in roles.items() if (account in role)}
        else:
            filtered_roles = roles

        if aliases:
            enriched_roles = {}
            for role, principal in filtered_roles.items():
                enriched_roles[role] = [
                    aliases[role.split(':')[4]],
                    role.split('role/')[1],
                    principal
                ]
            enriched_roles = OrderedDict(sorted(enriched_roles.items(), key=lambda t: (t[1][0], t[1][1])))

            ordered_roles = OrderedDict()
            for role, role_property in enriched_roles.items():
                ordered_roles[role] = role_property[2]

            enriched_roles_tab = []
            for i, (role, role_property) in enumerate(enriched_roles.items()):
                enriched_roles_tab.append([i + 1, role_property[0], role_property[1]])

            while True:
                print(tabulate(enriched_roles_tab, headers=['No', 'AWS account', 'Role'], ))
                prompt = 'Type the number (1 - {:d}) of the role to assume: '.format(len(enriched_roles))
                choice = Util.get_input(prompt)

                try:
                    return list(ordered_roles.items())[int(choice) - 1]
                except (IndexError, ValueError):
                    print("Invalid choice, try again.")
        else:
            while True:
                for i, role in enumerate(filtered_roles):
                    print("[{:>3d}] {}".format(i + 1, role))

                prompt = 'Type the number (1 - {:d}) of the role to assume: '.format(len(filtered_roles))
                choice = Util.get_input(prompt)

                try:
                    return list(filtered_roles.items())[int(choice) - 1]
                except (IndexError, ValueError):
                    print("Invalid choice, try again.")

    @staticmethod
    def touch(file_name, mode=0o600):
        flags = os.O_CREAT | os.O_APPEND
        with os.fdopen(os.open(file_name, flags, mode)) as f:
            try:
                os.utime(file_name, None)
            finally:
                f.close()

    # This method returns the first non-None value in args. If all values are
    # None, None will be returned. If there are no arguments, None will be
    # returned.
    @staticmethod
    def coalesce(*args):
        for x in args:
            if x is not None:
                return x
        return None

    @staticmethod
    def unicode_to_string_if_needed(obj):
        if "unicode" in str(obj.__class__):
            return obj.encode('utf-8')
        else:
            return obj

    @staticmethod
    def get_password(prompt):
        if sys.stdin.isatty():
            password = getpass.getpass(prompt)
        else:
            print(prompt, end="")
            sys.stdout.flush()
            password = sys.stdin.readline()
            print("")
        return password
