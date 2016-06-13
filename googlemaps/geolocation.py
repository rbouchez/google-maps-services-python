#
# Copyright 2016 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

"""Performs requests to the Google Maps Geolocation API."""
from googlemaps import convert


_GEOLOCATION_BASE_URL = "https://www.googleapis.com"


def geolocate(client, body):
    """
    """

    return client._get("/geolocation/v1/geolocate", {},
                       extract_body=_geolocation_extract,
                       base_url=_GEOLOCATION_BASE_URL, 
                       accepts_clientid=False, post_body=body)

def _geolocation_extract(resp):
    """Extracts a result from a Roads API HTTP response."""

    try:
        j = resp.json()
    except:
        if resp.status_code != 200:
            raise googlemaps.exceptions.HTTPError(resp.status_code)

        raise googlemaps.exceptions.ApiError("UNKNOWN_ERROR",
                                             "Received a malformed response.")

    if "error" in j:
        error = j["error"]
        status = error["status"]

        if status == "RESOURCE_EXHAUSTED":
            raise googlemaps.exceptions._RetriableRequest()

        if "message" in error:
            raise googlemaps.exceptions.ApiError(status, error["message"])
        else:
            raise googlemaps.exceptions.ApiError(status)

    if resp.status_code != 200:
        raise googlemaps.exceptions.HTTPError(resp.status_code)

    return j