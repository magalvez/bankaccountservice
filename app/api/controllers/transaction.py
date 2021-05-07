#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.api.managers.transaction import TransactionManager
from util.exceptions.exceptions import BadRequest


class TransactionController(object):
    """
    Class TransactionController to perform communications with Managers
    """

    @staticmethod
    def get_by_account_number(account_number):
        """
        Get All Transactions
        :returns List, [{'user_id': 10, 'balance': 20, ...}, {'user_id': 10, 'balance': 20, ...} ...]
        """
        if not account_number:
            raise BadRequest

        return TransactionManager.get_by_account_number(account_number)
