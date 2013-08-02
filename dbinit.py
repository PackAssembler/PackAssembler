from mcmanager.schema import *
from sys import argv


try:
    connect(argv[1])
    User(username="Orphan", password=argv[2].encode(), email=argv[3], groups=['group:user', 'group:system']).save(validate=False)
except IndexError:
    print("usage: {1} db orphan_password orphan_email")
