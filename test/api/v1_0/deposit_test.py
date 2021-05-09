#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contexter import Contexter

from app import app, auth
from app.api import api

from test.test_helper import BaseTest, TestHttpRequest


class DepositTest(BaseTest):
    """
    Set of tests for deposit endpoint
    """

    deposit_data = {
        'amount': 30000
    }

    @classmethod
    def setUpClass(cls):

        cls.__endpoint_url = '/bankaccountservice/api/v1.0/account/000100/deposit'

        # So the exception would be catch by flask-restful
        app.config['PROPAGATE_EXCEPTIONS'] = False
        cls.app = app.test_client()

        cls.http_request = TestHttpRequest(cls.app, cls.__endpoint_url)

    def setUp(self):
        db = self.set_up_db()
        self.db = db

    def get_patches(self, new_patches=None):
        """
        Get the mock patches to be used.
        :return: list, the mock patches to apply.
        """

        patch_dict = {}

        if new_patches is not None:
            for key, value in new_patches.iteritems():
                patch_dict[key] = value

        return self.build_patches(patch_dict)

    def test_deposit_bad_request(self):
        """
        Check the endpoint returns an error message because the withdrawal resource was bad request (HTTP 400)
        """

        with Contexter(*self.get_patches()):

            deposit_data = {
                'amount': 0
            }

            response = self.http_request.patch(deposit_data)
            self.json_structure_response_code_assert(400, response)

    def test_deposit_success(self):
        """
        Check the endpoint returns success response deposit (HTTP 200)
        """

        with Contexter(*self.get_patches()):

            response = self.http_request.patch(self.deposit_data)
            self.json_structure_response_code_assert(200, response)

            collection = self.db['bank_account']
            bank_account = collection.find_one({'account_number': '000100'})

            self.assertEqual(bank_account['balance'], 130000.0)
            self.assertEqual(bank_account['account_number'], '000100')

            transactions = []
            collection = self.db['transaction']
            transactions_db = collection.find({'account_number': '000100'})
            for transaction in transactions_db:
                transactions.append(transaction)

            self.assertGreater(len(transactions), 2)  # Because two were stored by default
