import unittest
from flask import current_app, url_for, json
from app import create_app, db
from urllib.request import Request, urlopen

class APITestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    """
    set up a few helper functions
    """
    def get_testdata(self):
        return [{"data":
                 {
                     "attributes":{"hostname":"foo",
                                   "hwaddress":"F0O1O2B3A4R5",
                                   "target":""}
                 }
                },
                {"data":
                 {
                     "attributes":{"hostname":"bar",
                                   "hwaddress":"F0O1O2B3B6C5",
                                   "target":""}
                 }
                },
                {"data":
                 {
                     "attributes":{"hostname":"baz",
                                   "hwaddress":"F0O1O2B3GG3H6",
                                   "target":""}
                 }
                },
                {"data":
                 {
                     "attributes":{"hostname":"few",
                                   "hwaddress":"F0O1O2B3J4K3L1",
                                   "target":""}
                 }
                }]

    def get_edited_data(self, data):
        return  {"data":
                 {
                     "attributes":{"hostname":data['hostname'][::-1],
                                   "hwaddress":data['hwaddress'][::-1],
                                   "target":""}
                 }
                }


    def get_api_headers(self):
        return {
            'Authorization':
            'Token testtoken',
            'Content-Type':
            'application/json'}


    def test_no_auth(self):
        response = self.client.get(url_for('bootconf.get_hostlist'),
                                   content_type='application/json')
        self.assertTrue(response.status_code == 403)


    def test_bootconf_api(self):
        for item in self.get_testdata():
            data = item['data']['attributes']
            """
            test creating records
            """
            response = self.client.post(
                url_for('bootconf.post_host'),
                headers=self.get_api_headers(),
                data=json.dumps(item))
            self.assertTrue(response.status_code == 201)
            """
            test fetching records
            """
            response = self.client.get(
                url_for('bootconf.get_host', hostname=data['hostname']),
                headers=self.get_api_headers())
            self.assertTrue(response.status_code == 200)
            json_response = response.json
            resp_dict = json_response['data']['attributes']
            self.assertTrue(resp_dict['hostname'] == data['hostname'])
            self.assertTrue(resp_dict['hwaddress'] == data['hwaddress'])
            self.assertTrue(resp_dict['target'] == data['target'])
            """
            test updating records
            """
            response = self.client.patch(
                url_for('bootconf.patch_host', hostname=data['hostname']),
                headers=self.get_api_headers(),
                data = json.dumps(self.get_edited_data(data))
            )
            self.assertTrue(response.status_code == 205)
            """
            test deleting records
            """
            response = self.client.delete(
                url_for('bootconf.delete_host',
                        hostname=data['hostname'][::-1]),
                headers=self.get_api_headers())
            self.assertTrue(response.status_code == 204)
            """
            check list results
            """
            response = self.client.get(
                url_for('bootconf.get_hostlist'),
                headers=self.get_api_headers())
            self.assertTrue(response.status_code == 200)
