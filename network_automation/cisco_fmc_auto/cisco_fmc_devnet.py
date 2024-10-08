#!/usr/bin/env python3


import os
import requests


class CiscoFMC:
    """
    Python client SDK for Cisco FMC.
    """

    # Constructor
    def __init__(
        self,
        username,
        password,
        host="fmcrestapisandbox.cisco.com",
        verify=False,
    ):

        # Store all input parameters and assemble the base URL
        self.username = username
        self.password = password
        self.verify = verify
        self.base_url = f"https://{host}/api"

        # if we aren't verifying SSL certificates, disable obnoxious warnings
        if not self.verify:
            requests.packages.urllib3.disable_warnings()

        # Create a stateful HTTPS session to improve performance
        self.sess = requests.session()

        # Perform initial authentication, which also generates API path
        # and reusable HTTP header dictionary
        self.authenticate("generatetoken")

    def authenticate(self, grant_type):
        """
        perform authentication, either 'generatetoken' or 'refreshtoken',
        and retain the new tokens as attributes of the object.
        """

        # Construct the proper auth URL based on the grant type. Notice that
        # this URL uses 'fmc_platform' vs the more common 'fmc_config'
        auth_url = f"{self.base_url}/fmc_platform/v1/auth/{grant_type}"

        # Issue the POST request using either basic auth or the API token.
        # Be sure to ignore SSL cert checking in the FMC
        if grant_type == "generatetoken":
            token_resp = self.sess.post(
                auth_url,
                auth=(self.username, self.password),
                verify=self.verify,
            )
        elif grant_type == "refreshtoken":
            token_resp = self.sess.post(
                auth_url, headers=self.headers, verify=self.verify
            )
        token_resp.raise_for_status()

        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-auth-access-token": token_resp.headers["X-auth-access-token"],
            "X-auth-refresh-token": token_resp.headers["X-auth-refresh-token"],
        }

        # Next, define the base URL, which includes the common domain ID.
        # You can access this using the 'global' or 'DOMAIN_UUID' key.
        # This is part of the URL for many requests in the future
        domain_id = token_resp.headers["global"]
        self.api_path = f"{self.base_url}/fmc_config/v1/domain/{domain_id}"

    @staticmethod
    def build_from_env_vars():
        """
        static class-level helper method to quickly create a new CiscoFMC
        object using environment variables:
            1. FMC_USERNAME: your personal username for FMC
            2. FMC_PASSWORD: your personal password for FMC
        """

        # Collect username and password (required) from env vars
        username = os.environ.get("FMC_DEV_USERNAME")
        if not username:
            raise ValueError("Must define FMC_DEV_USERNAME env var")

        password = os.environ.get("FMC_DEV_PASSWORD")
        if not password:
            raise ValueError("Must define FMC_DEV_PASSWORD environment var")

        # Specifying the host is optional;
        host = os.environ.get("FMC_DEV_HOST", "fmcrestapisandbox.cisco.com")

        # Create and return new CiscoFMC object
        return CiscoFMC(username=username, password=password, host=host)

    def reauthenticate(self):
        """
        Uses the 'refresh_token' to reauthenticate the session to FMC.
        """
        self.authenticate("refreshtoken")


def main():
    """
    Quickly test the FMC class authentication capabilities
    """

    # Create a new FMC object, which performs initial auth; show tokens
    fmc = CiscoFMC.build_from_env_vars()
    print("First access token:", fmc.headers["X-auth-access-token"])
    print("First refresh token:", fmc.headers["X-auth-refresh-token"])

    # Reauthenticate using the refresh token; show the  tokens
    fmc.reauthenticate()
    print("Second access token:", fmc.headers["X-auth-access-token"])
    print("Second refresh token:", fmc.headers["X-auth-refresh-token"])


if __name__ == "__main__":
    main()
