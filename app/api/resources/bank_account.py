#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from flask import request
from flask_jwt import jwt_required

from flask_restful import Resource

from app.api.controllers.bank_account import BankAccountController
from app.api.success_response import HttpSuccess
from util.decorators.endpoint_api import api_resource_endpoint


class BankAccountAPI(Resource):
    """
    Class BankAccountAPI resource to perform communications with Controllers
    """

    @jwt_required()
    @api_resource_endpoint()
    def get(self, user_id):
        """
        Get BankAccount model by user_id
        """
        response = BankAccountController.get_account_by_user_id(user_id)
        return HttpSuccess().get_response(payload=response)


class BankAccountDepositAPI(Resource):
    """
    User BankAccountDepositAPI Resource
    """

    @api_resource_endpoint()
    def patch(self, account_number):
        """
        Perform deposit action over specific BankAccount user model
        """
        payload_data = json.loads(request.data)
        payload_data['account_number'] = account_number

        response = BankAccountController.deposit_account(payload_data)
        return HttpSuccess().get_response(payload=response)


class BankAccountWithdrawalAPI(Resource):
    """
    User BankAccountWithdrawalAPI Resource
    """

    @jwt_required()
    @api_resource_endpoint()
    def patch(self, account_number):
        """
        Perform withdrawal action over specific BankAccount user model
        """
        payload_data = json.loads(request.data)
        payload_data['account_number'] = account_number

        response = BankAccountController.withdrawal_account(payload_data)
        return HttpSuccess().get_response(payload=response)
