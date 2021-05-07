#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app.api.models import BankAccount


class BankAccountManager(object):
    """
    Class BankAccountManager to perform communications within MongoEngine and MongoDB
    """

    @staticmethod
    def get_all():
        """
        Get All BankAccount DB records
        :returns List, [{'account_number': 10, 'balance': 20 ....}, {'account_number': 10, 'balance': 20 ....} ...]
        """
        return BankAccount.objects()

    @staticmethod
    def get_account(account_number):
        """
        Get BankAccount DB records
        :param account_number: String, Ie '213423422'
        :returns Object, Ie {'account_number': 10, 'balance': 20 ....}
        """
        return BankAccount.objects(account_number=account_number).first()

    @staticmethod
    def get_account_by_user_id(user_id):
        """
        Get BankAccount by user_id DB record
        :param user_id: String, Ie '213423422'
        :returns Object, Ie {'account_number': 10, 'balance': 20 ....}
        """
        return BankAccount.objects(user_id=user_id).first()

    @staticmethod
    def save(account_data):
        """
        Save BankAccount Collection record
        :param account_data: dict, Ie {'user_id': 10, 'balance': 20, ....}
        :returns Object, Ie {'user_id': 10, 'balance': 20 ....}
        """
        user = BankAccount(**account_data)
        user.save()
        return user

    @staticmethod
    def update(account_data, db_instance):
        """
        Update BankAccount Collection record
        :param account_data: dict, Ie {'user_id': 10, 'balance': 20, ....}
        :param db_instance: dict, Ie {'user_id': 10, 'balance': 20, ....}
        """
        db_instance.update(**account_data)
