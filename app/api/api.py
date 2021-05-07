#!flask/bin/python

"""
Restful API
"""

from flask_cors import CORS
from flask_restful import Api

from app import app
from app.api.resources.bank_account import BankAccountAPI, BankAccountDepositAPI, BankAccountWithdrawalAPI


api = Api(app)

api.add_resource(
    BankAccountAPI,
    '/bankaccountservice/api/v1.0/account/<string:user_id>',
    endpoint='bankaccount-api',
)

api.add_resource(
    BankAccountDepositAPI,
    '/bankaccountservice/api/v1.0/account/<string:account_number>/deposit',
    endpoint='bankaccount-deposit-api',
)

api.add_resource(
    BankAccountWithdrawalAPI,
    '/bankaccountservice/api/v1.0/account/<string:account_number>/withdrawal',
    endpoint='bankaccount-withdrawal-api',
)


CORS(
  app,
  origins="*",
  allow_headers="*",
  supports_credentials=True
)
