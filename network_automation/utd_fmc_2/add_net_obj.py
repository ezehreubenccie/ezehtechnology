#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Creates network objects groups on FMC.
Check out the API explorer at "https://<fmc_host>/api/api-explorer"
"""

from cisco_fmc_config import CiscoFMC


def main():
    """
    Execution begins here.
    """

    # Create a new FMC object referencing the Devnet snadbox (default)
    fmc = CiscoFMC.build_from_env_vars()

    # Create Network object group
    netobj_resp = fmc.add_group_file("objects/test_net_obj.json")

    # Cannot always filter by name in FMC, so use an interactive technique
    cleanup = input("Purge items just added? (y/n): ").lower()

    if cleanup == "y":
        # Delete Network Object groups recursively (groups and components)
        fmc.purge_group_id(netobj_resp["id"], "NetworkGroup")


if __name__ == "__main__":
    main()
