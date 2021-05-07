#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.api.models import Transaction


class TransactionManager(object):
    """
    Class TransactionManager to perform communications within MongoEngine and MongoDB
    """

    @staticmethod
    def get_all():
        """
        Get All Transaction DB records
        :returns List, [{'account_number': 10, 'amount': 20, ...}, {'account_number': 10, 'amount': 20, ...} ...]
        """
        return Transaction.objects()

    @staticmethod
    def get_by_account_number(account_number):
        """
        Get Transactions by account_number
        :param account_number:
        :returns List, [{'account_number': 10, 'amount': 20, ...}, {'account_number': 10, 'amount': 20, ...} ...]
        """
        return Transaction.objects(account_number=account_number)

    @staticmethod
    def save(transaction_data):
        """
        Save Transaction Collection record
        :param transaction_data: dict, Ie {'account_number': 10, 'type': 'WITHDRAWAL', ....}
        :returns Object, Ie {'account_number': 10, 'amount': 20, ...}
        """
        transaction = Transaction(**transaction_data)
        transaction.save()
