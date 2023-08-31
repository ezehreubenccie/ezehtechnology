#!/usr/bin/env python3

import CloudFlare
import pprint


def main():
    zone_id_list = []
    zone_name_list = []
    cf = CloudFlare.CloudFlare(raw=True)
    page_number = 0
    while True:
        page_number += 1
        raw_results = cf.zones.get(params={"per_page": 5, "page": page_number})
        zones = raw_results["result"]

        # pprint.pprint(zones)
        # pprint.pprint(f'The length of zones is: {len(zones)}')
        for zone in range(len(zones)):
            if "Wolters Kluwer- Italy" in zones[zone]["account"].values():
                zone_id = zones[zone]["id"]
                zone_name = zones[zone]["name"]
                # pprint.pprint('zone_id=%s zone_name=%s' % (zone_id, zone_name))
                zone_id_list.append(zone_id)
                zone_name_list.append(zone_name)
            else:
                continue

        total_pages = raw_results["result_info"]["total_pages"]
        if page_number == total_pages:
            break

    # print(f'Zone id length is {len(zone_id_list)}')
    # print(f'Zone name length is {len(zone_id_list)}')
    #    pprint.pprint(zone_id_list)
    #    pprint.pprint(zone_name_list)
    print(f"Wolters Kluwer - Italy account has {len(zone_id_list)} zone ids")
    print("\n")
    print(f"Wolters Kluwer - Italy account has {len(zone_name_list)} dns zones")

    #    italy_dns_zone_database = dict(zip(zone_name_list, zone_id_list))
    italy_dns_zone_database_2 = dict(zip(zone_id_list, zone_name_list))
    #    pprint.pprint(italy_dns_zone_database)
    #
    #
    import requests
    import json
    from datetime import datetime

    date1 = datetime.today()
    #    import re
    #
    #    #zone_name = 'avvocatiliberi.it'
    #    with open('domains_429.txt') as domains:
    #        dom = domains.read().splitlines()
    #
    #
    headers = {
        #        # requests won't add a boundary if this header is set when you pass files=
        #        # 'Content-Type': 'multipart/form-data',
        "X-Auth-Email": "your email",
        "X-Auth-Key": "your auth_key",
        'Content-Type': 'application/json',
    }

    json_data = {
        'value': '1.2',
    }
    #    #for italy_zone, italy_zone_id in italy_dns_done_database.items():
    #    unmodified_tls_ver = []
    report_italy =  open(
        f"WK-Italy_tls_report_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}.txt",
        "a",
    ) 
    report_italy.write(
            f"WK-Italy_tls_report_{date1.month}_{date1.day}_{date1.year}_{date1.hour}_{date1.minute}_{date1.second}\n\n"
        )
    #breakpoint()
    report_italy.write("    zone_name                           tls_version\n")
    tls_v_1 = []
    tls_v_1_2 = []
    data = "1.2"
    for zone_id in zone_id_list:
        #        files = {
        #            'file': open(f'italy_dns_zones/{zone_name}', 'rb'),
        #            'proxied': (None, 'true'),
        #            }
        #
#        response = requests.patch(
#            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/min_tls_version",
#            headers=headers,
#            # files=files,
#            data=data,
#        )
        response = requests.patch(
            f'https://api.cloudflare.com/client/v4/zones/{zone_id}/settings/min_tls_version',
            headers=headers,
            json=json_data,
        )
        #
#        breakpoint()
        pprint.pprint(response.text)
        response_dict = json.loads(response.text)
        if response_dict['result']['value'] == "1.0":
            tls_v_1.append(response_dict['result']['value'])
        else:
            tls_v_1_2.append(response_dict['result']['value'])
        print(
            f"Tls version for {italy_dns_zone_database_2[zone_id]} is {response_dict['result']['value']}"
        )
        report_italy.write(
            f"  {italy_dns_zone_database_2[zone_id] :<20}                      {response_dict['result']['value']}\n"
        )
    
    report_italy.write(f"\n\nTotal TLS version 1.0: {len(tls_v_1)}\n\nTotal TLS version 1.2: {len(tls_v_1_2)}")
    report_italy.close()

#        pprint.pprint(f'Status for {zone_name} is {response}')
#    print(type(response))
#    pprint.pprint(dir(response))
# pprint.pprint(response.text)
#    response_pattern = re.compile(r'\<Response \[200\]\>')
#    mo = response_pattern.search(response)
#    if  mo:
#        print("Dns records for altalexeditore.it, where successfully imported!!")
#    else:
#        print("Dns records for altalexeditore.it, where not successfully imported!!. Please troubelshoot!")

if __name__ == "__main__":
    main()
