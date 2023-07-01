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

   # print(f'Zone id length is {len(zone_id_list)}')
   # print(f'Zone name length is {len(zone_id_list)}')
   # pprint.pprint(zone_id_list)
   # pprint.pprint(zone_name_list)

    italy_dns_zone_database = dict(zip(zone_name_list, zone_id_list))
    pprint.pprint(italy_dns_zone_database)

  
    import requests
    import re

    headers = {
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
        'X-Auth-Email': 'your_email',
        'X-Auth-Key': 'global_api_key_or_token',
        }
    #for italy_zone, italy_zone_id in italy_dns_done_database.items():
        
    files = {
        'file': open(f'italy_dns_zones/altalexeditore.it', 'rb'),
        'proxied': (None, 'true'),
        }

    response = requests.post(
         f'https://api.cloudflare.com/client/v4/zones/{italy_dns_zone_database["altalexeditore.it"]}/dns_records/import',
         headers=headers,
         files=files,
        )

    print(response)
    print(type(response))
    pprint.pprint(dir(response))
    response.text
#    response_pattern = re.compile(r'\<Response \[200\]\>')
#    mo = response_pattern.search(response)
#    if  mo:
#        print("Dns records for altalexeditore.it, where successfully imported!!")
#    else:
#        print("Dns records for altalexeditore.it, where not successfully imported!!. Please troubelshoot!")

if __name__ == '__main__':
    main()
