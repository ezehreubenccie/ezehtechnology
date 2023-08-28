#!/usr/bin/env python3

"""
Author: Reuben Ezeh
Purpose: Demonstrate using Nornir to introduce orchestration and
concurrency, as well as inventory management.
"""

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result


def main():
    """
    Execution begins here.
    """

    # Initialize nornir and invoke the group task.
    nornir = InitNornir()

    # Use NAPALM logic to invoke the "get_facts" getter
    # Below is the documentation page used in demo:
    # https://nornir.readthedocs.io/en/stable/plugins/tasks/networking.html
    result = nornir.run(task=napalm_get, getters=["get_facts"])

    # Use Nornir-supplied function to pretty-print the result
    # to see a recap of all actions taken.
    breakpoint()
    print_result(result)


if __name__ == "__main__":
    main()
