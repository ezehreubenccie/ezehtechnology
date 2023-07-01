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
        raw_results = cf.zones.get(params={'per_page':5,'page':page_number})
        zones = raw_results['result']
        
       # pprint.pprint(zones)
        #pprint.pprint(f'The length of zones is: {len(zones)}')
        for zone in range(len(zones)):
            if 'Wolters Kluwer- Italy' in zones[zone]['account'].values():
                zone_id = zones[zone]['id']
                zone_name = zones[zone]['name']
               # pprint.pprint('zone_id=%s zone_name=%s' % (zone_id, zone_name))
                zone_id_list.append(zone_id)
                zone_name_list.append(zone_name)
            else:
                continue

        total_pages = raw_results['result_info']['total_pages']
        if page_number == total_pages:
            break

    print(f'Zone id length is {len(zone_id_list)}')
    print(f'Zone name length is {len(zone_id_list)}')
    pprint.pprint(zone_id_list)
    pprint.pprint(zone_name_list)

    italy_dns_zone_database = dict(zip(zone_name_list, zone_id_list))
    pprint.pprint(italy_dns_zone_database)

  
    import requests

    headers = {
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
        'X-Auth-Email': 'your_email',
        'X-Auth-Key': 'global_apiKey_or_token',
        }

    zone_id_list = zone_id_list[0:11]
    zone_name_list = zone_name_list[0:11]
#    pprint.pprint(zone_id_list)
#    pprint.pprint(zone_name_list)
#    print(len(zone_id_list))
#    print(len(zone_name_list))
    for italy_zone in range(len(zone_name_list)):
#        print(f'italy_dns_zones/{zone_id_list[italy_zone]}')        
        files = {
            'file': open(f'italy_dns_zones/{zone_name_list[italy_zone]}', 'rb'),
            'proxied': (None, 'true'),
           }

        response = requests.post(
            f'https://api.cloudflare.com/client/v4/zones/{zone_id_list[italy_zone]}/dns_records/import',
            headers=headers,
            files=files,
           )

        print(f'Status for {zone_name_list[italy_zone]} is {response}')


if __name__ == '__main__':
    main()
