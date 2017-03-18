import unittest
from flask import current_app
from app import create_app, db
from urllib.request import Request, urlopen
from .test_basics import BasicsTestCase

class APITestCase(BasicsTestCase):

    def test_adding_hosts(self):
        baseurl = 'http://localhost:5000/'
        testdata = [
            {"hostname":"foo","hwaddress":"F0O1O2B3A4R5","target":""},
            {"hostname":"bar","hwaddress":"F6O7O8B9A0R1","target":""},
            {"hostname":"baz","hwaddress":"F2O3O4B5A6R7","target":""},
            {"hostname":"few","hwaddress":"F8O9O0B1A2R3","target":""},
            {"hostname":"stew","hwaddress":"F4O5O6B7A8R9","target":""}
        ]
        for data in testdata:
            r = Request(baseurl + 'new',
                        data=data,
                        method='POST'
                       )
            result = urlopen(r)
            return result
