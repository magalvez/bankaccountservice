import json
import unittest

from mock import patch
from pymongo_inmemory import MongoClient

from util.exceptions.exceptions import JsonDecodeError
from util.response import DecimalEncoder


class MockMixinClass(object):

    @staticmethod
    def build_patches(patch_dict):
        """
        Create patch objects to be sent to a context manager
        :param patch_dict: Dict, patches to be applied to mock imports. Ie,
            {
                'util.dict_helper':
                    {'return_value': {u'user_id': u'10', u'account_number': u'80672'}
            }
        :return: List with patch objects. Ie,
            [
                patch('util.dict_helper', return_value={u'user_id': u'10', ...})
            ]
        """
        patches = []

        for key, value in patch_dict.items():
            patcher = patch(key, **value)
            patches.append(patcher)

        return patches


class InMemoryDatabaseMixinClass(object):
    """
    Class tp handle In Memory MongoDB database
    """

    def set_up_db(self):
        """
        Setup In memory MongoDB database
        """
        self.client = MongoClient()
        db = self.client['bankaccountservice']

        collection = db['bank_account']
        bank_account_data = [{'user_id': '105398890', 'account_number': '000100', 'balance': 100000,
                              'create_date': '2021-04-06 01:37:14.422Z'},
                             {'user_id': '105398891', 'account_number': '000101', 'balance': 60000,
                              'create_date': '2021-04-06 01:37:14.422Z'}]
        for bank_account in bank_account_data:
            collection.insert_one(bank_account)

        collection = db['transaction']
        transaction_data = [
            {'account_number': '000100', 'currency': 'COP', 'type': 'DEPOSIT', 'previous_balance': 0, 'amount': 200000,
             'trm': 0, 'create_date': '2021-05-06 01:37:14.422Z'},
            {'account_number': '000100', 'currency': 'COP', 'type': 'WITHDRAWAL', 'previous_balance': 200000,
             'amount': 100000, 'trm': 0, 'create_date': '2021-05-06 01:47:14.422Z'},
            {'account_number': '000101', 'currency': 'COP', 'type': 'DEPOSIT', 'previous_balance': 0, 'amount': 100000,
             'trm': 0, 'create_date': '2021-05-06 01:17:14.422Z'},
            {'account_number': '000101', 'currency': 'COP', 'type': 'WITHDRAWAL', 'previous_balance': 100000,
             'amount': 40000, 'trm': 0, 'create_date': '2021-05-06 01:27:14.422Z'}]
        for transaction in transaction_data:
            collection.insert_one(transaction)

        return db


class JsonAssertMissing(unittest.TestCase):
    """
    Class to handles the JSON response codes
    """

    def response_code_assert(self, code_to_check, response):
        """Check http response"""

        self.assertEqual(response.status_code, code_to_check)

    def json_structure_response_code_assert(self, code_to_check, response):
        """Check http response"""

        self.assertEqual(response.content_type, 'application/json')

        if response.data:
            response_data = deserialize_json(response.data)
            self.assertEqual(response.status_code, code_to_check)


class TestHttpRequest:
    """
    Class to handle http request in tests
    """

    def __init__(self, app, endpoint_url, is_form_data=False):
        self.app = app
        self.endpoint_url = endpoint_url
        headers = {'Content-Type': 'multipart/form-data'} if is_form_data else {'Content-Type': 'application/json'}
        headers.update({'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsImlhdCI6MTYyMDQzMDYzOSwiZXhwIjoxNjI5MDcwNjM5fQ.eyJ1c2VyX2lkIjoiMTA1Mzk4ODkwIiwicGluIjoyMDkxLCJleHBpcmF0aW9uX2RhdGUiOiIwOC8xNS8yMDIxIiwiZXhwaXJlX2RhdGUiOiIwOC8xNS8yMDIxIDE4OjM3OjE5IiwiZXhwIjoxNjI5MDcwNjM5LjAyMzgyfQ.Az8u-6Q5KyhuJ0dkMPhgHKQJBPg5eyrG3LoKeUvmyjk'})
        self.headers = headers
        self.is_form_data = is_form_data

    def set_endpoint_url(self, new_endpoint_url):
        """
        Set a new endpoint URL for endpoint with params on it.
        :param new_endpoint_url: str, the new URL to set. Ie. '/application/12345/has_cashflow'
        """
        self.endpoint_url = new_endpoint_url

    def get(self, data=None, headers=None, params=None):
        """
        Return a result of a request using GET method
        """
        optional_params = self.__process_params(data=data, headers=headers, params=params)
        return self.app.get(self.endpoint_url, **optional_params)

    def post(self, data=None, headers=None, authorization=None):
        """
        Return a result of a request using POST method
        """
        optional_params = self.__process_params(data=data, headers=headers, authorization=authorization)
        return self.app.post(self.endpoint_url, **optional_params)

    def put(self, data=None, headers=None):
        """
        Return a result of a request using PUT method
        """
        optional_params = self.__process_params(data=data, headers=headers)
        return self.app.put(self.endpoint_url, **optional_params)

    def patch(self, data=None, headers=None):
        """
        Return a result of a request using PATCH method
        """
        optional_params = self.__process_params(data=data, headers=headers)
        return self.app.patch(self.endpoint_url, **optional_params)

    def delete(self, data=None, headers=None):
        """
        Return a result of a request using DELETE method
        """
        optional_params = self.__process_params(data=data, headers=headers)
        return self.app.delete(self.endpoint_url, **optional_params)

    def __process_params(self, data=None, headers=None, authorization=None, params=None):
        """
        Process HTTP Request params
        """

        optional_params = {}
        if data:
            optional_params['data'] = data if self.is_form_data else json.dumps(data, cls=DecimalEncoder)

        optional_params['headers'] = self.headers
        if headers:
            optional_params['headers'].update(headers)

        if authorization:
            optional_params.update(authorization)

        if params:
            optional_params['query_string'] = params

        return optional_params


class BaseTest(MockMixinClass, InMemoryDatabaseMixinClass, JsonAssertMissing):

    def tearDown(self):
        """
        Close In Memory MongoDB Instance
        """
        self.client.close()


def deserialize_json(text):
    """
    Function to deserialize a JSON argument
    :param text: text to be deserialized. String, Ie. '{data: 1}'
    :return dictionary containing the json deserialized data. Dict, Ie. {data: 1}
    """
    try:
        return json.loads(text)
    except ValueError as e:
        raise JsonDecodeError(text)
