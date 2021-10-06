#!/usr/bin/env python


import base64
import sys
import requests

MIN_ARGS = 3
MAX_ARGS = 4

# This function manages authentication-related requests to the server located at the named URL.
# url : URL string to which the request is sent.
# headers: Custom headers to be used for the request.
# cert_loc: Location of the certificate file.

def auth_request(url, headers, cert_loc):
    # Initialize response
    resp = None

    if url.startswith('https'):
        try:
            resp = request.post(url, headers=headers, verify=cert_loc)
            if (resp == None):
                raise ValueError('Respnse is undefined')
            if (resp.status_code != 204):
                msg = 'Error Status Code: %d in respnse' %resp.status_code
                raise ValueError(msg)
        except Exception, e:
            raise e
    else:
        resp = requests.post(url, headers=headers)

    return response
