# bankaccountservice

## Prepare your environment

    ## 1) mkdir Playvox
    ## 2) git clone https://github.com/magalvez/bankaccountservice.git
    ## 3) docker-compose up -d

## MongoDB
This database contain the following collection:
    ## 1) account
    ## 2) transaction
    
Each time we affect the balance the process generate a new transaction data row with the detail of the transaction,
you can check the transactions via postman
    
This collection is populated when the docker container is created with the following data:

db.bank_account.insert({"user_id": "105398890", "account_number": "000100", "balance": 100000, "create_date": ISODate("2021-04-06 01:37:14.422Z")})
db.bank_account.insert({"user_id": "105398891", "account_number": "000101", "balance": 60000, "create_date": ISODate("2021-04-06 01:37:14.422Z")})
db.transaction.insert({"account_number": "000100", "currency": "COP", "type": "DEPOSIT", "previous_balance": 0, "amount": 200000, "trm": 0, "create_date": ISODate("2021-05-06 01:37:14.422Z")})
db.transaction.insert({"account_number": "000100", "currency": "COP", "type": "WITHDRAWAL", "previous_balance": 200000, "amount": 100000, "trm": 0, "create_date": ISODate("2021-05-06 01:47:14.422Z")})
db.transaction.insert({"account_number": "000101", "currency": "COP", "type": "DEPOSIT", "previous_balance": 0, "amount": 100000, "trm": 0, "create_date": ISODate("2021-05-06 01:17:14.422Z")})
db.transaction.insert({"account_number": "000101", "currency": "COP", "type": "WITHDRAWAL", "previous_balance": 100000, "amount": 40000, "trm": 0, "create_date": ISODate("2021-05-06 01:27:14.422Z")})

The data is auto populated each time the folder `mongodb` is deleted

# Service URL
http://localhost:8300/

## Testing via postmant
To test it with postman use the following collection:
https://www.getpostman.com/collections/e1daefda0d281339afeb

---------------------------------------------

To use without dokcer pipenv follow this steps:

1) pip install pipenv
2) pipenv shell
3) pipenv install

Pipenv is going to look automatically the Pipfile and install the dependencies

Note if you want to analyze your dependencies you can run:
 * pipenv graph

Yo will something like this:
 
 Flask==1.1.2
  - click [required: >=5.1, installed: 7.1.2]
  - itsdangerous [required: >=0.24, installed: 1.1.0]
  - Jinja2 [required: >=2.10.1, installed: 2.11.3]
    - MarkupSafe [required: >=0.23, installed: 1.1.1]
  - Werkzeug [required: >=0.15, installed: 1.0.1]
  
Pipenv will generate a Pipfile.lock file to manages the following:
  * The Pipfile.lock file enables deterministic builds by specifying the exact 
    requirements for reproducing an environment. It contains exact versions for 
    packages and hashes to support more secure verification