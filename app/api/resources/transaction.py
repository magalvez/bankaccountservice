#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_jwt import jwt_required

from flask_restful import Resource

from app.api.controllers.transaction import TransactionController
from app.api.success_response import HttpSuccess
from util.decorators.endpoint_api import api_resource_endpoint


class TransactionAPI(Resource):
    """
    Class TransactionAPI resource to perform communications with Controllers
    """

    @jwt_required()
    @api_resource_endpoint()
    def get(self, account_number):
        """
        Get Transaction model by account_number
        """
        response = TransactionController.get_by_account_number(account_number)
        return HttpSuccess().get_response(payload=response)
