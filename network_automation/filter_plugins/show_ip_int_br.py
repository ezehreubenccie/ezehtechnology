import re


def show_ip(output):
    show_version_list = []
    output = output.strip()
    for line in output.splitlines():
        if re.search(r"^Interface.*Protocols$", line, flags=re.M):
            continue
        show_version_list.append(line.split())
    return show_version_list


class FilterModule(object):
    def filters(self):
        return {'show_ip_filter': show_ip}
