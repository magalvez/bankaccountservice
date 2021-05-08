#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from app.api.external.trm.trm_api import get_current_trm
from app.api.managers.bank_account import BankAccountManager
from app.api.managers.transaction import TransactionManager
from util.dict_helper import get
from util.exceptions.exceptions import BadRequest, BankAccountNotFound, BankAccountUserNotFound, \
    BankAccountInsufficientFounds
from util.format import format_currency


class BankAccountController(object):
    """
    Class BankAccountController to perform communications with Managers
    """

    @staticmethod
    def get_account(account_number):
        """
        Get All BankAccounts
        :returns List, [{'user_id': 10, 'balance': 20, ...}, {'user_id': 10, 'balance': 20, ...} ...]
        """
        if not account_number:
            raise BadRequest

        bank_account = BankAccountManager.get_account(account_number)

        if not bank_account:
            raise BankAccountNotFound(account_number)

        return bank_account

    @staticmethod
    def get_account_by_user_id(user_id):
        """
        Get BankAccount by user_id DB record
        :param user_id: String, Ie '213423422'
        :returns Object, Ie {'account_number': 10, 'balance': 20 ....}
        """
        if not user_id:
            raise BadRequest

        bank_account = BankAccountManager.get_account_by_user_id(user_id)

        if not bank_account:
            raise BankAccountUserNotFound(user_id)

        return bank_account

    @staticmethod
    def deposit_account(account_data):
        """
        Deposit BankAccount and generate Transaction record
        :returns dict:, Ie {'message': 'Your ....'}
        """
        if not get(account_data, ['amount']) or not get(account_data, ['account_number']):
            raise BadRequest

        bank_account = BankAccountManager.get_account(account_data['account_number'])
        if not bank_account:
            raise BankAccountNotFound(account_data['account_number'])

        new_balance = bank_account.balance + account_data['amount']
        update_data = {
            'balance': new_balance
        }
        BankAccountManager.update(update_data, bank_account)

        transaction = {
            'account_number': account_data['account_number'],
            'currency': 'COP',
            'type': 'DEPOSIT',
            'previous_balance': bank_account.balance,
            'trm': 0,
            'amount': account_data['amount']
        }
        TransactionManager.save(transaction)

        return {'balance': new_balance}

    @staticmethod
    def withdrawal_account(account_data):
        """
        Withdrawal BankAccount and generate Transaction record
        :returns dict:, Ie {'message': 'Your ....'}
        """
        if not get(account_data, ['amount']) or not get(account_data, ['account_number']) or \
                not get(account_data, ['currency']) or get(account_data, ['currency']) not in ['COP', 'USD']:
            raise BadRequest

        if account_data['currency'] == 'USD' and not get(account_data, ['trm']):
            raise BadRequest

        bank_account = BankAccountManager.get_account(account_data['account_number'])
        if not bank_account:
            raise BankAccountNotFound(account_data['account_number'])

        if account_data['currency'] == 'USD':
            account_data['amount'] = account_data['amount'] * account_data['trm']

        if account_data['amount'] > bank_account.balance:
            raise BankAccountInsufficientFounds(account_data['account_number'],
                                                format_currency(account_data['amount']),
                                                account_data['currency'])

        new_balance = bank_account.balance - account_data['amount']
        update_data = {
            'balance': round(new_balance)
        }
        BankAccountManager.update(update_data, bank_account)

        transaction = {
            'account_number': account_data['account_number'],
            'currency': account_data['currency'],
            'type': 'WITHDRAWAL',
            'previous_balance': bank_account.balance,
            'trm': account_data['trm'],
            'amount': account_data['amount']
        }
        TransactionManager.save(transaction)

        return {'balance': new_balance}
