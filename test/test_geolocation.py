# This Python file uses the following encoding: utf-8
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

"""Tests for the geolocation module."""

import datetime
import responses
import json

import test as _test
import googlemaps


class GeolocationTest(_test.TestCase):

    def setUp(self):
        self.key = 'AIzaasdf'
        self.client = googlemaps.Client(self.key)

    @responses.activate
    def test_simple_geolocation(self):
        responses.add(responses.POST,
                      'https://www.googleapis.com/geolocation/v1/geolocate',
                      body='{"location":{"lat":0.0, "lng":0.0}, "accuracy": 1000.0}',
                      status=200,
                      content_type='application/json')

        body = {}
        resp = self.client.geolocate(body)

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual('https://www.googleapis.com/geolocation/v1/geolocate?'
                            'key=%s' % self.key,
                            responses.calls[0].request.url)
        self.assertEqual(body, json.loads(responses.calls[0].request.body))

    
    @responses.activate
    def test_complex_request(self):
        responses.add(responses.POST,
                      'https://www.googleapis.com/geolocation/v1/geolocate',
                      body='{"location":{"lat":0.0, "lng":0.0}, "accuracy": 1000.0}',
                      status=200,
                      content_type='application/json')

        with open("test/test_geolocation_body.json") as f:
          body = json.loads(f.read())
        
        resp = self.client.geolocate(body)

        self.assertEqual(1, len(responses.calls))

        self.assertURLEqual('https://www.googleapis.com/geolocation/v1/geolocate?'
                            'key=%s' % self.key,
                            responses.calls[0].request.url)
        self.assertEqual(body, json.loads(responses.calls[0].request.body))