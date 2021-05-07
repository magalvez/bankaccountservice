#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime

from app import db


class BankAccount(db.Document):
    """
    Account Model Class
    """
    user_id = db.StringField()
    account_number = db.StringField()
    balance = db.FloatField()
    create_date = db.DateTimeField(default=datetime.utcnow)


class Transaction(db.Document):
    """
    Account Model Class
    """
    account_number = db.StringField()
    currency = db.StringField()
    type = db.StringField()
    previous_balance = db.FloatField()
    amount = db.FloatField()
    trm = db.FloatField()
    create_date = db.DateTimeField(default=datetime.utcnow)
