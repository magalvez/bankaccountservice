mongo -- "$MONGO_INITDB_DATABASE" <<EOF
    db.bank_account.insert({"user_id": "105398890", "account_number": "000100", "balance": 100000, "create_date": ISODate("2021-04-06 01:37:14.422Z")})
    db.bank_account.insert({"user_id": "105398891", "account_number": "000101", "balance": 50000, "create_date": ISODate("2021-04-06 01:37:14.422Z")})
    db.transaction.insert({"account_number": "000100", "currency": "COP", "type": "DEPOSIT", "previous_balance": 0, "amount": 200000, "trm": 0, "create_date": ISODate("2021-05-06 01:37:14.422Z")})
    db.transaction.insert({"account_number": "000100", "currency": "COP", "type": "WITHDRAWAL", "previous_balance": 200000, "amount": 100000, "trm": 0, "create_date": ISODate("2021-05-06 01:47:14.422Z")})
    db.transaction.insert({"account_number": "000101", "currency": "COP", "type": "DEPOSIT", "previous_balance": 0, "amount": 100000, "trm": 0, "create_date": ISODate("2021-05-06 01:17:14.422Z")})
    db.transaction.insert({"account_number": "000101", "currency": "COP", "type": "WITHDRAWAL", "previous_balance": 100000, "amount": 50000, "trm": 0, "create_date": ISODate("2021-05-06 01:27:14.422Z")})
EOF