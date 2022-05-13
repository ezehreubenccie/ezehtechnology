#!/usr/bin/env python3

import re


def parse_model_asa(text):

    # Hardware:   ASA5506, 4096 MB RAM, CPU Atom C2000 series 1250 MHz, 1 CPU (4 cores)
    model_regex = re.compile(r"Hardware:\s+(?P<model>\S+)\s+\S+\s+\S+\s+\S+\s+")

    model_match = model_regex.search(text)
    if model_match:
        return model_match.group("model")

    return None


def parse_model_ios(text):

    # cisco ISR4321/K9 (1RU) processor with 1694702K/3071K bytes of memory
    model_regex = re.compile("cisco\s+(?P<model>\S+)\s+\(\S+\)\s+processor\s+")

    model_match = model_regex.search(text)
    if model_match:
        return model_match.group("model")

    return None
