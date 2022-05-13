#!/usr/bin/env python3


from asa_ios_model_parser import parse_model_asa, parse_model_ios



def test_parse_model_ios():


    model_output = """
        cisco ISR4321/K9 (1RU) processor with 1694702K/3071K bytes of memory.
        Processor board ID FLM1950W19P
        2 Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        4194304K bytes of physical memory.
        3223551K bytes of flash memory at bootflash:.
        0K bytes of WebUI ODM Files at webui:.
    """

    print(model_output)

    model_data = parse_model_ios(model_output)
    print(model_data)
    assert model_data == 'ISR4321/K9'

    # Negative test case; provide invalid output that should not parse
    model_output = """
        cisco  (1RU) processor with 1694702K/3071K bytes of memory.
        Processor board ID FLM1950W19P
        2 Gigabit Ethernet interfaces
        32768K bytes of non-volatile configuration memory.
        4194304K bytes of physical memory.
        3223551K bytes of flash memory at bootflash:.
        0K bytes of WebUI ODM Files at webui:.
    """

    print(model_output)

    model_data = parse_model_ios(model_output)
    print(model_data)
    assert model_data is None


def test_parse_model_asa():


    model_output = """
        Hardware:   ASA5506, 4096 MB RAM, CPU Atom C2000 series 1250 MHz, 1 CPU (4 cores)
        Internal ATA Compact Flash, 8000MB
        BIOS Flash M25P64 @ 0xfed01000, 16384KB
    """

    print(model_output)

    model_data = parse_model_ios(model_output)
    print(model_data)
    assert model_data == 'ASA5506'

    # Negative
    model_output = """
        Hardware:  4096 MB RAM, CPU Atom C2000 series 1250 MHz, 1 CPU (4 cores)
        Internal ATA Compact Flash, 8000MB
        BIOS Flash M25P64 @ 0xfed01000, 16384KB
    """

    print(model_output)

    model_data = parse_model_ios(model_output)
    print(model_data)
    assert model_data is None

