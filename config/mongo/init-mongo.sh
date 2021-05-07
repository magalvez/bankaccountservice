mongo -- "$MONGO_INITDB_DATABASE" <<EOF
    var rootUser = '$MONGO_INITDB_ROOT_USERNAME';
    var rootPassword = '$MONGO_INITDB_ROOT_PASSWORD';
    var admin = db.getSiblingDB('admin');
    admin.auth(rootUser, rootPassword);

    var user = '$MONGO_INITDB_USERNAME';
    var passwd = '$MONGO_INITDB_PASSWORD';
    db = db.getSiblingDB('$MONGO_INITDB_DATABASE');
    db.createUser({user: user, pwd: passwd, roles: [{role: "readWrite", db: "$MONGO_INITDB_DATABASE"}]});

    db.createCollection('bank_account', { capped : true, size : 2097152, max : 1000 } );
    db.createCollection('transaction', { capped : true, size : 2097152, max : 1000 } );
EOF